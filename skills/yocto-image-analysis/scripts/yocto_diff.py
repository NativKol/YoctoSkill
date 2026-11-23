#!/usr/bin/env python3
"""Compare Yocto build evidence before and after a change.

Standard library only. Three subcommands:

  manifest OLD NEW
      Diff two package lists: image manifests (``<image>.manifest``, one
      "name arch version" line per package), buildhistory
      ``installed-package-names.txt`` (one name per line), or any file whose
      first column is a package name.

  env OLD NEW [--only REGEX] [--ignore REGEX] [--history N]
      Diff two ``bitbake -e <target>`` dumps. For each variable whose final
      value changed, print the old and new value (as added/removed words for
      lists) and the last N history operations ("op file:line") recorded in the
      NEW dump, which point at the line that set the value.

  why DEPENDS_DOT PACKAGE [--max N]
      Read a buildhistory image ``depends.dot`` and print the chains of
      installed packages that pull PACKAGE into the image, from a top-level
      package (one nothing else depends on) down to PACKAGE. Edges are marked
      "->" for RDEPENDS, "~>" for RRECOMMENDS and "=>" for a dependency
      satisfied through RPROVIDES.

Add --json to any subcommand for machine-readable output.

Exit status: 0 when the inputs are identical, 1 when differences were found
(``why``: 1 when at least one chain was printed), 2 on usage or input errors.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import deque
from pathlib import Path

# ---------------------------------------------------------------------------
# manifest


def parse_package_list(text: str) -> dict[str, tuple[str, str]]:
    """Return {name: (arch, version)}; arch/version are "" when absent."""
    pkgs: dict[str, tuple[str, str]] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split()
        name = fields[0]
        arch = fields[1] if len(fields) > 1 else ""
        version = " ".join(fields[2:]) if len(fields) > 2 else ""
        pkgs[name] = (arch, version)
    return pkgs


def diff_manifests(old: dict, new: dict) -> dict:
    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    changed = []
    for name in sorted(set(old) & set(new)):
        (oarch, over), (narch, nver) = old[name], new[name]
        if (oarch, over) != (narch, nver):
            changed.append({"package": name, "old_arch": oarch, "new_arch": narch,
                            "old_version": over, "new_version": nver})
    return {
        "added": [{"package": p, "arch": new[p][0], "version": new[p][1]} for p in added],
        "removed": [{"package": p, "arch": old[p][0], "version": old[p][1]} for p in removed],
        "changed": changed,
        "old_count": len(old),
        "new_count": len(new),
    }


def print_manifest_diff(result: dict) -> None:
    print(f"packages: {result['old_count']} -> {result['new_count']}")
    for title, key in (("added", "added"), ("removed", "removed")):
        print(f"\n{title} ({len(result[key])}):")
        for item in result[key]:
            extra = " ".join(x for x in (item["arch"], item["version"]) if x)
            print(f"  {'+' if key == 'added' else '-'} {item['package']}" + (f"  [{extra}]" if extra else ""))
    print(f"\nchanged ({len(result['changed'])}):")
    for item in result["changed"]:
        parts = []
        if item["old_version"] != item["new_version"]:
            parts.append(f"version {item['old_version'] or '?'} -> {item['new_version'] or '?'}")
        if item["old_arch"] != item["new_arch"]:
            parts.append(f"arch {item['old_arch'] or '?'} -> {item['new_arch'] or '?'}")
        print(f"  ~ {item['package']}: " + ", ".join(parts))


# ---------------------------------------------------------------------------
# env (bitbake -e)

ASSIGN = re.compile(r'^(?:export )?(?P<name>[^\s="#][^\s=]*)="(?P<rest>.*)$')
UNSET = re.compile(r"^unset (?P<name>\S+)$")
HIST_HEAD = re.compile(r"^# \$(?P<name>\S+)(?: \[\d+ operations\])?$")
HIST_EVENT = re.compile(r"^#   (?P<op>\S.*?) (?P<file>\S+):(?P<line>\S+?)(?: \[(?P<func>[^\]]+)\])?$")
SHELL_FUNC = re.compile(r"^\S+\(\) \{$")
PY_FUNC = re.compile(r"^python \S+ \(\) \{$")

# Values that differ between any two runs and say nothing about the metadata.
DEFAULT_IGNORE = r"^(DATE|TIME|DATETIME|BB_CONSOLELOG|BB_DEFAULT_EVENTLOG|BUILDNAME|PID|BB_TASKHASH|BB_UNIHASH)$"


def _closed(rest: str) -> bool:
    """True when rest ends with a closing quote that is not escaped."""
    if not rest.endswith('"'):
        return False
    backslashes = len(rest) - 1 - len(rest[:-1].rstrip("\\"))
    return backslashes % 2 == 0


def _unescape(value: str) -> str:
    # bitbake's emit_var: '"' -> '\"', newline -> ' \' + newline, '$' -> '\$'
    return value.replace(" \\\n", "\n").replace('\\"', '"').replace("\\$", "$")


def parse_env(text: str) -> tuple[dict[str, str], dict[str, list[dict]]]:
    """Parse ``bitbake -e`` output into (values, history)."""
    values: dict[str, str] = {}
    history: dict[str, list[dict]] = {}
    current_hist: str | None = None
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if SHELL_FUNC.match(line) or PY_FUNC.match(line):
            i += 1
            while i < len(lines) and lines[i] != "}":
                i += 1
            i += 1
            current_hist = None
            continue
        if line.startswith("#"):
            head = HIST_HEAD.match(line)
            if head:
                current_hist = head.group("name")
                history.setdefault(current_hist, [])
            elif current_hist:
                event = HIST_EVENT.match(line)
                if event and not line.startswith(("#     ", '#   "')):
                    history[current_hist].append({
                        "op": event.group("op"),
                        "file": event.group("file"),
                        "line": event.group("line"),
                        "func": event.group("func") or "",
                    })
            i += 1
            continue
        unset = UNSET.match(line)
        if unset:
            values.pop(unset.group("name"), None)
            i += 1
            continue
        match = ASSIGN.match(line)
        if match:
            name, rest = match.group("name"), match.group("rest")
            chunks = [rest]
            while not _closed(chunks[-1]) and i + 1 < len(lines):
                i += 1
                chunks.append(lines[i])
            values[name] = _unescape("\n".join(chunks)[:-1])
            current_hist = None
        i += 1
    return values, history


def _words(value: str) -> list[str]:
    return value.split()


def diff_env(old_text: str, new_text: str, only: str | None, ignore: str | None,
             history_n: int) -> dict:
    old_vals, old_hist = parse_env(old_text)
    new_vals, new_hist = parse_env(new_text)
    only_re = re.compile(only) if only else None
    ignore_re = re.compile(DEFAULT_IGNORE + (f"|{ignore}" if ignore else ""))
    names = sorted(set(old_vals) | set(new_vals))
    changes = []
    for name in names:
        if only_re and not only_re.search(name):
            continue
        if ignore_re.search(name):
            continue
        old, new = old_vals.get(name), new_vals.get(name)
        if old == new:
            continue
        entry = {"variable": name, "old": old, "new": new}
        if old is not None and new is not None and _words(old) != _words(new):
            ow, nw = _words(old), _words(new)
            entry["words_added"] = [w for w in nw if w not in ow]
            entry["words_removed"] = [w for w in ow if w not in nw]
        elif old is not None and new is not None:
            entry["whitespace_only"] = True
        hist = new_hist.get(name) or old_hist.get(name) or []
        entry["history"] = hist[-history_n:] if history_n > 0 else []
        changes.append(entry)
    return {"changes": changes, "old_vars": len(old_vals), "new_vars": len(new_vals)}


def _short(value: str | None, limit: int = 300) -> str:
    if value is None:
        return "<unset>"
    value = value.replace("\n", "\\n")
    return value if len(value) <= limit else value[:limit] + " ..."


def print_env_diff(result: dict) -> None:
    print(f"variables: {result['old_vars']} -> {result['new_vars']}, changed: {len(result['changes'])}")
    for c in result["changes"]:
        print(f"\n{c['variable']}")
        if "words_added" in c:
            if c["words_added"]:
                print("  + " + " ".join(c["words_added"]))
            if c["words_removed"]:
                print("  - " + " ".join(c["words_removed"]))
            if not c["words_added"] and not c["words_removed"]:
                print("  (same words, different order or count)")
        elif c.get("whitespace_only"):
            print("  (whitespace only)")
        else:
            print(f"  old: {_short(c['old'])}")
            print(f"  new: {_short(c['new'])}")
        for h in c["history"]:
            func = f" [{h['func']}]" if h["func"] else ""
            print(f"  history: {h['op']} {h['file']}:{h['line']}{func}")


# ---------------------------------------------------------------------------
# why (buildhistory depends.dot)

EDGE = re.compile(r'^\s*"(?P<src>[^"]+)"\s*->\s*"(?P<dst>[^"]+)"\s*(?P<attrs>\[.*\])?\s*;?\s*$')


def parse_depends_dot(text: str) -> dict[str, list[tuple[str, str]]]:
    """Return reverse edges {dependency: [(dependent, kind)]}; kind is R, rec or rprov."""
    reverse: dict[str, list[tuple[str, str]]] = {}
    for line in text.splitlines():
        m = EDGE.match(line)
        if not m:
            continue
        attrs = m.group("attrs") or ""
        kind = "rec" if "dotted" in attrs else "rprov" if "dashed" in attrs else "R"
        reverse.setdefault(m.group("dst"), []).append((m.group("src"), kind))
        reverse.setdefault(m.group("src"), reverse.get(m.group("src"), []))
    return reverse


def why_chains(reverse: dict, target: str, max_chains: int) -> list[list[tuple[str, str]]]:
    """Breadth-first search upwards from target; shortest chains first."""
    if target not in reverse:
        return []
    chains = []
    queue = deque([[(target, "")]])
    while queue and len(chains) < max_chains:
        path = queue.popleft()
        node = path[-1][0]
        parents = [p for p in reverse.get(node, []) if p[0] not in {n for n, _ in path}]
        if not parents:
            chains.append(list(reversed(path)))
            continue
        for parent, kind in parents:
            queue.append(path + [(parent, kind)])
    return chains


ARROW = {"R": "->", "rec": "~>", "rprov": "=>"}


def format_chain(chain: list[tuple[str, str]]) -> str:
    out = chain[0][0]
    for (_, kind), (node, _) in zip(chain, chain[1:]):
        out += f" {ARROW[kind]} {node}"
    return out


# ---------------------------------------------------------------------------


def _read(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError as error:
        raise SystemExit(f"error: cannot read {path}: {error}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_man = sub.add_parser("manifest", help="diff two package lists / image manifests")
    p_man.add_argument("old")
    p_man.add_argument("new")
    p_man.add_argument("--json", action="store_true")

    p_env = sub.add_parser("env", help="diff two `bitbake -e` dumps")
    p_env.add_argument("old")
    p_env.add_argument("new")
    p_env.add_argument("--only", help="regex: only variables whose name matches")
    p_env.add_argument("--ignore", help="regex: extra variable names to ignore")
    p_env.add_argument("--history", type=int, default=3, help="history operations to show per variable (default 3)")
    p_env.add_argument("--json", action="store_true")

    p_why = sub.add_parser("why", help="explain why a package is in an image (buildhistory depends.dot)")
    p_why.add_argument("dotfile")
    p_why.add_argument("package")
    p_why.add_argument("--max", type=int, default=5, help="maximum chains to print (default 5)")
    p_why.add_argument("--json", action="store_true")

    args = parser.parse_args(argv)

    if args.cmd == "manifest":
        result = diff_manifests(parse_package_list(_read(args.old)), parse_package_list(_read(args.new)))
        print(json.dumps(result, indent=2)) if args.json else print_manifest_diff(result)
        return 1 if result["added"] or result["removed"] or result["changed"] else 0

    if args.cmd == "env":
        try:
            result = diff_env(_read(args.old), _read(args.new), args.only, args.ignore, args.history)
        except re.error as error:
            print(f"error: bad regex: {error}", file=sys.stderr)
            return 2
        print(json.dumps(result, indent=2)) if args.json else print_env_diff(result)
        return 1 if result["changes"] else 0

    reverse = parse_depends_dot(_read(args.dotfile))
    chains = why_chains(reverse, args.package, args.max)
    if args.json:
        print(json.dumps([[{"package": n, "edge_to_next": k} for n, k in c] for c in chains], indent=2))
    elif not chains:
        print(f"{args.package}: not found in {args.dotfile} (not installed, or the name is a recipe "
              f"name rather than a runtime package name)")
    else:
        print("legend: -> RDEPENDS, ~> RRECOMMENDS, => satisfied via RPROVIDES")
        for chain in chains:
            print(format_chain(chain))
    return 1 if chains else 0


if __name__ == "__main__":
    sys.exit(main())
