---
name: yocto-change-review
description: Automated code review of changes to Yocto Project / OpenEmbedded repositories - a diff, commit, branch, pull request, merge request, or git format-patch series touching recipes (.bb, .bbappend, .inc), classes (.bbclass), layer.conf, distro and machine conf, local.conf templates, image recipes, packagegroups, SRC_URI patches, kernel config fragments (.cfg, .scc) or wic kickstart (.wks) files. Explains what each change actually does downstream (operator and override semantics, DEPENDS vs RDEPENDS, DISTRO_FEATURES and PACKAGECONFIG impact, task signature and sstate rebuild blast radius, QA checks it will trigger, license, CVE, patch Upstream-Status, security, reproducibility, commit message conventions) and reports ranked findings with file:line, severity, manual citation and a suggested fix. Has a strictness setting - gentle, standard (default), strict - for how hard to be on the author. Use it whenever someone asks to review, check, look over, approve, or nitpick a Yocto/BitBake change, patch, PR or commit, even if they just paste a diff from a meta-* layer and ask "is this OK?".
---

# Yocto Change Review

Review a *change* to Yocto/OpenEmbedded metadata the way an experienced layer maintainer
would: understand what the change does to the build, prove it where possible, and report
only what matters at the requested strictness. Target: **Yocto Project 5.0 "scarthgap"
(BitBake 2.8)**; check the project's release first. Release-dependent facts are marked
*[release-specific]* in the references.

This skill is change-centric. When a change *adds* a whole new recipe or layer, also apply
the checklist of `yocto-recipe-review` or `yocto-layer-review` (if installed) to the new
file, and keep this skill's workflow, severity and output format.

## 1. Pick the strictness level

| Level | Reports | Tone |
|---|---|---|
| `gentle` | blockers and majors; at most three minors as "worth knowing"; no nits | welcoming, plain words, every finding has a paste-ready fix |
| `standard` (default) | blockers, majors, minors; nits only as a one-line count | direct and courteous |
| `strict` | everything, including nits and every upstream submission rule | concise maintainer voice, still courteous |

Choose: the user's explicit words ("be gentle", "nitpick everything", `strictness: strict`)
> a review policy in the repository (README, CONTRIBUTING, MAINTAINERS) > `standard`.
State the level in the first line. Strictness filters what is *reported*, never a
finding's severity; blockers and security findings are reported at every level. Before
writing the report, read [references/strictness-levels.md](references/strictness-levels.md)
(severity scale, tone, confidence labels, false-positive guards).

## 2. Workflow

1. **Collect the change**: the exact diff and its base (`git diff <base>...HEAD`,
   `git show <commit>`, format-patch files, or a PR diff) and the commit messages, which are
   reviewed too. Release from `LAYERSERIES_COMPAT_*` or the branch; if unknown, assume
   scarthgap and say so.
2. **Read context, not only hunks**: the whole changed file, plus the recipe a `.bbappend`
   targets, `require`d `.inc` files, inherited classes, other bbappends for the recipe, and
   the layer's `conf/layer.conf`. Most false positives come from missing that a "missing"
   variable is set in an include or class.
3. **Classify each changed file** and run its checks in
   [references/file-type-checks.md](references/file-type-checks.md).
4. **Work out the effects** ("what does BitBake do with this, for whom, and what
   rebuilds?") with [references/change-effects.md](references/change-effects.md):
   operators and overrides, dependencies, features, providers and priority, versions and
   feed upgrades, QA checks triggered, signature/sstate blast radius.
5. **Check conventions** with [references/conventions.md](references/conventions.md) and
   the commit/patch rules in
   [references/commit-and-patch-rules.md](references/commit-and-patch-rules.md).
6. **Verify what you can** with [references/verification.md](references/verification.md)
   when a configured build directory exists. Parse-only and signature commands are cheap;
   never start a long build without the user's agreement. Label each finding `verified` or
   `reasoned`.
7. **Rank, filter by strictness, write the report.**

## 3. Report format

```text
Yocto change review - <change title or commit range> - strictness: <level>
Release assumed: scarthgap (5.0) [from LAYERSERIES_COMPAT | assumed]
Verdict: <request changes | approve with suggestions | approve>
Summary: <2-4 lines: what the change does, its blast radius, the main risk>

Findings
1. [blocker] [verified|reasoned] <path>:<line> - <one-line problem>
   Effect: <what happens in the build, image or device, and for whom>
   Manual: <offline manual page: section, e.g. dev-manual/layers.md: 3.6> - "<short quote>"
   Fix:
     <minimal replacement metadata or commit-message text>
2. [major] ...
Nits (<n>): <one line at standard; full list at strict; omitted at gentle>

Questions for the author
- <things that may be intentional; asked, not asserted>

Not checked
- <what needs a build, a target, or files you did not see>
Verification run
- <command> -> <result>   (or "none: no build directory available")
```

Order by severity, then file; cite the line in the new version. One finding per root
cause (list its several effects under it). If nothing is wrong, say so and name what you
checked; do not invent findings.

## 4. Ground rules

- Critique the change, never the person. Explain why, cite the manual, offer the fix.
- A finding you cannot support from the diff, surrounding files or a command output
  becomes a question or is dropped.
- No fixes by suppression: `INSANE_SKIP`, `BB_DANGLINGAPPENDS_WARNONLY`, lowering
  `ERROR_QA` or blanket `BBMASK` need a stated, narrow reason and are never the default.
- Do not recommend deleting `tmp/`, `sstate-cache/` or `downloads/` as a review action.
- Never add a `Signed-off-by:` line for the author or tell an agent to add one; the Yocto
  Project AI policy forbids it (commit-and-patch-rules.md). Review text posted to a Yocto
  Project mailing list must disclose that it is AI-generated and be read by a human first.
- Old override syntax (`FOO_append`) is an error in scarthgap, but `BBFILE_PATTERN_<layer>`,
  `LAYERDEPENDS_<layer>`, `SRCREV_<name>` and `PREFERRED_VERSION_<recipe>` legitimately use
  `_`; do not flag them.

## 5. Offline lookup

Everything this skill needs is in the repository; it works without internet. Pull only the text you need instead of reading whole files (pages run to thousands of lines). From this skill's folder:

- `python3 scripts/ylookup.py <NAME>...` prints the scarthgap manual entry for any variable, class, task, feature or QA check (`--kind var|class|task|feature|qa` to disambiguate, `--find TEXT` when unsure of the name).
- `--topic TEXT` lists manual sections, `--section <manual/page.md> "<heading>"` prints one, `--grep REGEX [--in ref-manual]` finds anything else.
- URLs in these files are citations for the user, not lookups. The manuals are scarthgap 5.0: if the project is on another release, tell the user rather than going online. Without Python: `` grep -n -A30 '^## Variable `NAME`' references/keywords.md ``.

Look a keyword up before asserting what it does; `references/keywords.md` is large, so never read it whole.
