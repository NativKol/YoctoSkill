#!/usr/bin/env python3
# Generated copy of tools/ylookup.py by tools/build_manual_refs.py. Do not edit.
"""Offline lookup in the Yocto Project scarthgap (5.0) / BitBake 2.8 manuals.

Prints only the entry or section asked for, so an agent never has to load a whole
manual. Works with no network: it reads this skill's references/keywords.md and,
when it is installed next to this skill (as in the YoctoSkill repository or plugin),
the full offline manuals in the yocto-manuals skill.

Usage (run from anywhere; paths are resolved relative to this script):
  ylookup.py IMAGE_INSTALL do_rootfs core-image   keyword entries (var, task, class, ...)
  ylookup.py --kind feature distro:systemd        force the kind (var|class|task|qa|feature)
  ylookup.py --find RECOMMEND                     keywords whose name or summary matches
  ylookup.py --topic "read-only root"             manual sections whose heading matches
  ylookup.py --section dev-manual/layers.md "Appending Other Layers" [--shallow]
                                                  print one manual section (--shallow: only
                                                  its intro plus a list of subsections)
  ylookup.py --grep "BB_DANGLINGAPPENDS" [--in ref-manual]
                                                  matching lines across the manuals
Options: --max-lines N (default 80, 0 = no limit).

Set YOCTO_MANUALS=/path/to/yocto-manuals/references to point at another copy.
Standard library only. Source of truth: tools/ylookup.py in the YoctoSkill repository;
skills/*/scripts/ylookup.py are generated copies (tools/build_manual_refs.py).
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
KINDS = {"var": "Variable", "class": "Class", "task": "Task", "qa": "QA check", "feature": "Feature"}
SUBDIR = {"var": "variables", "class": "classes", "task": "tasks", "qa": "qa"}


def manuals_root() -> Path | None:
    env = os.environ.get("YOCTO_MANUALS")
    for cand in ([Path(env)] if env else []) + [
        SKILL / "references" if SKILL.name == "yocto-manuals" else None,
        SKILL.parent / "yocto-manuals" / "references",
    ]:
        if cand and (cand / "INDEX.md").exists():
            return cand
    return None


def safe(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.\-]", "_", name).strip("_")


def clip(text: str, max_lines: int, hint: str) -> str:
    lines = text.rstrip().splitlines()
    if max_lines and len(lines) > max_lines:
        rest = len(lines) - max_lines
        return "\n".join(lines[:max_lines]) + f"\n[... {rest} more lines; rerun with --max-lines 0 {hint}]"
    return "\n".join(lines)


def strip_generated(text: str) -> str:
    text = re.sub(r"^<!--.*?-->\n+", "", text, flags=re.S)
    return text.split("\n---\nRelease:", 1)[0]


def guess_kinds(name: str) -> list[str]:
    if name.startswith("do_"):
        return ["task"]
    if ":" in name and name.split(":", 1)[0] in ("distro", "machine", "image"):
        return ["feature"]
    if re.fullmatch(r"[A-Z0-9_\-\[\]]+", name) or "_" in name and name.upper() == name:
        return ["var"]
    if re.fullmatch(r"[a-z0-9\-]+", name):
        return ["qa", "class", "feature"] if "-" in name else ["class", "qa", "feature"]
    return ["var", "class", "task", "qa"]


def from_glossary(kind: str, name: str) -> str | None:
    glossary = SKILL / "references" / "keywords.md"
    if not glossary.exists():
        return None
    text = glossary.read_text(encoding="utf-8")
    head = f"## {KINDS[kind]} `{name}`"
    start = text.find("\n" + head + "\n")
    if start < 0:
        return None
    nxt = re.compile(r"\n## (?:%s) `" % "|".join(map(re.escape, KINDS.values())))
    m = nxt.search(text, start + len(head) + 2)
    return text[start + 1:m.start() if m else len(text)]


def from_manuals(root: Path, kind: str, name: str) -> str | None:
    if kind == "feature":
        fk, _, fn = name.partition(":")
        if not fn:  # bare feature name: try every feature kind
            for fk in ("distro", "machine", "image"):
                hit = from_manuals(root, "feature", f"{fk}:{name}")
                if hit:
                    return hit
            return None
        path = root / "features" / fk / f"{safe(fn)}.md"
    else:
        path = root / SUBDIR[kind] / f"{safe(name)}.md"
    if not path.exists() and kind == "var":
        for cand in (root / "variables").glob("*.md"):  # case-insensitive fallback
            if cand.stem.lower() == safe(name).lower():
                path = cand
                break
    return strip_generated(path.read_text(encoding="utf-8")) if path.exists() else None


def lookup(names: list[str], kind: str | None, max_lines: int) -> int:
    root = manuals_root()
    missing = 0
    for name in names:
        found = None
        for k in ([kind] if kind else guess_kinds(name)):
            found = from_glossary(k, name) or (from_manuals(root, k, name) if root else None)
            if not found and k == "feature" and ":" not in name:
                for fk in ("distro", "machine", "image"):
                    found = from_glossary(k, f"{fk}:{name}")
                    if found:
                        break
            if found:
                break
        if found:
            print(clip(found, max_lines, (f"--kind {kind} " if kind else "") + name))
        else:
            missing += 1
            where = "the offline manuals" if root else "this skill's keywords.md (full manuals not installed)"
            print(f"{name}: not found in {where}. Try --find {name} or --grep {name}.")
        print()
    return 1 if missing else 0


def need_root() -> Path:
    root = manuals_root()
    if not root:
        sys.exit("The full offline manuals are not installed next to this skill. Install the "
                 "yocto-manuals skill from the same repository, or set YOCTO_MANUALS. This "
                 "skill's own keywords are in references/keywords.md.")
    return root


def find(text: str, limit: int = 25) -> int:
    rx = re.compile(re.escape(text), re.I)
    hits = [l for l in (need_root() / "INDEX.md").read_text(encoding="utf-8").splitlines()
            if l.startswith("| ") and rx.search(l)]
    for line in hits[:limit]:
        cols = [c.strip() for c in line.strip("|").split(" | ")]
        if len(cols) >= 3:
            print(f"{cols[0]:7} {cols[1]:32} {cols[2][:110]}")
    if len(hits) > limit:
        print(f"[... {len(hits) - limit} more; narrow the search]")
    return 0 if hits else 1


def headings(path: Path):
    fence = False
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
        if line.startswith("```"):
            fence = not fence
        elif not fence and re.match(r"^#{1,6} ", line):
            yield i, len(line.split(" ", 1)[0]), line.split(" ", 1)[1].strip()


def plain(s: str) -> str:
    return s.replace("`", "").lower()


def topic(text: str, limit: int = 30) -> int:
    root = need_root()
    rx = re.compile(re.escape(plain(text)))
    n = 0
    for doc in sorted((root / "manuals").rglob("*.md")):
        for _, _, title in headings(doc):
            if rx.search(plain(title)):
                n += 1
                if n <= limit:
                    print(f'{doc.relative_to(root / "manuals").as_posix()}  "{title}"')
    if n > limit:
        print(f"[... {n - limit} more; narrow the search]")
    if n:
        print('\nRead one with: ylookup.py --section <file> "<heading text>"')
    return 0 if n else 1


def section(doc: str, title: str, max_lines: int, shallow: bool = False) -> int:
    root = need_root()
    path = root / "manuals" / doc
    if not path.exists():
        sys.exit(f"No manual page {doc}. Use --topic to find one.")
    lines = path.read_text(encoding="utf-8").splitlines()
    heads = list(headings(path))
    for idx, (line_no, level, head) in enumerate(heads):
        if plain(title) in plain(head):
            end = len(lines)
            subs = []
            for nxt_line, nxt_level, nxt_head in heads[idx + 1:]:
                if nxt_level <= level:
                    end = nxt_line
                    break
                if shallow and end == len(lines):
                    end = nxt_line
                if nxt_level == level + 1:
                    subs.append(nxt_head)
            print(clip("\n".join(lines[line_no:end]), max_lines, f'--section {doc} "{title}"'))
            if shallow and subs:
                print("\nSubsections (read one with --section):\n" + "\n".join(f"- {s}" for s in subs))
            return 0
    sys.exit(f'No heading containing "{title}" in {doc}.')


def grep(pattern: str, within: str | None, limit: int = 40) -> int:
    limit = limit or 10**9
    root = need_root()
    rx = re.compile(pattern, re.I)
    base = root / "manuals" / (within or "")
    n = 0
    for doc in sorted(base.rglob("*.md")):
        for i, line in enumerate(doc.read_text(encoding="utf-8").splitlines(), 1):
            if rx.search(line):
                n += 1
                if n <= limit:
                    print(f"{doc.relative_to(root / 'manuals').as_posix()}:{i}: {line.strip()[:200]}")
    if n > limit:
        print(f"[... {n - limit} more matches; narrow with --in <manual> or a stricter pattern]")
    return 0 if n else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("names", nargs="*")
    ap.add_argument("--kind", choices=sorted(KINDS))
    ap.add_argument("--find")
    ap.add_argument("--topic")
    ap.add_argument("--section", nargs=2, metavar=("FILE", "HEADING"))
    ap.add_argument("--shallow", action="store_true",
                    help="with --section: print only the text before the first subsection, then list subsections")
    ap.add_argument("--grep")
    ap.add_argument("--in", dest="within")
    ap.add_argument("--max-lines", type=int, default=80)
    a = ap.parse_args()
    if a.find:
        return find(a.find)
    if a.topic:
        return topic(a.topic)
    if a.section:
        return section(a.section[0], a.section[1], a.max_lines, a.shallow)
    if a.grep:
        return grep(a.grep, a.within, min(a.max_lines, 40) if a.max_lines else 0)
    if a.names:
        return lookup(a.names, a.kind, a.max_lines)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
