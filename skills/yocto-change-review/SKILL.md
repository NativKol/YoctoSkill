---
name: yocto-change-review
description: Automated code review of changes to Yocto Project / OpenEmbedded repositories - a diff, commit, branch, pull request, merge request, or git format-patch series touching recipes (.bb, .bbappend, .inc), classes (.bbclass), layer.conf, distro and machine conf, local.conf templates, image recipes, packagegroups, SRC_URI patches, kernel config fragments (.cfg, .scc) or wic kickstart (.wks) files. Explains what each change actually does downstream (operator and override semantics, DEPENDS vs RDEPENDS, DISTRO_FEATURES and PACKAGECONFIG impact, task signature and sstate rebuild blast radius, QA checks it will trigger, license, CVE, patch Upstream-Status, security, reproducibility, commit message conventions) and reports ranked findings with file:line, severity, manual citation and a suggested fix. Has a strictness setting - gentle, standard (default), strict - for how hard to be on the author. Use it whenever someone asks to review, check, look over, approve, or nitpick a Yocto/BitBake change, patch, PR or commit, even if they just paste a diff from a meta-* layer and ask "is this OK?".
---

# Yocto Change Review

Review a *change* to Yocto/OpenEmbedded metadata the way an experienced layer maintainer
would: understand what the change does to the build, prove it where possible, and report
only what matters at the requested strictness. Target release: **Yocto Project 5.0
"scarthgap" (BitBake 2.8)**, provisional until the user confirms; facts that differ by
release are marked *[release-specific]* in the references.

This skill is change-centric. It does not replace the object checklists of
`yocto-recipe-review` and `yocto-layer-review`; when a change *adds* a whole new recipe or
layer, also apply that skill's checklist to the new file (if installed), and keep this
skill's workflow, severity and output format.

## 1. Pick the strictness level

| Level | Reports | Tone |
|---|---|---|
| `gentle` | blockers and majors; at most three minors as "worth knowing"; no nits | welcoming, plain words, every finding has a paste-ready fix |
| `standard` (default) | blockers, majors, minors; nits only as a one-line count | direct and courteous |
| `strict` | everything, including nits and every upstream submission rule | concise maintainer voice, still courteous |

Choose in this order: the user's explicit words ("be gentle", "newcomer", "upstream
maintainer bar", "nitpick everything", `strictness: strict`) > a review policy stated in
the repository (README, CONTRIBUTING, MAINTAINERS) > `standard`. State the level in the
first line of the report. Strictness filters what is *reported*; it never changes a
finding's severity, and blockers and security findings are reported at every level.
Read [references/strictness-levels.md](references/strictness-levels.md) for the full
severity scale, tone rules, confidence labels and false-positive guards before writing
the report.

## 2. Workflow

1. **Collect the change.** Get the exact diff and its base: `git diff <base>...HEAD`,
   `git show <commit>`, `git format-patch` files, or a PR diff. Record the commit
   messages too; they are reviewed. Find the release from `LAYERSERIES_COMPAT_*` in
   `conf/layer.conf` or the branch name; if unknown, assume scarthgap and say so.
2. **Read context, not only hunks.** For every changed file open the whole file, plus
   what it interacts with: the recipe a `.bbappend` targets, `.inc` files it `require`s,
   classes it inherits, other bbappends for the same recipe, and the layer's
   `conf/layer.conf`. Most false positives come from judging a hunk without knowing that
   the "missing" variable is set in an include or class.
3. **Classify each changed file** and run the per-type checks in
   [references/file-type-checks.md](references/file-type-checks.md): recipe, bbappend,
   include, class, layer.conf, distro conf, machine conf, local.conf template, image
   recipe, packagegroup, patch file, kernel fragment or `.scc`, `.wks`, scripts/lib code.
4. **Work out the effects.** For each semantic change ask "what does BitBake do with this,
   for whom, and what rebuilds?" using
   [references/change-effects.md](references/change-effects.md): operator and override
   evaluation, dependency semantics, feature propagation, provider and priority changes,
   versioning and feed upgrades, QA checks the change will trigger, and the
   signature/sstate blast radius.
5. **Check conventions** with [references/conventions.md](references/conventions.md)
   (recipe style guide, naming, licensing, layer best practices, security) and the commit
   and patch rules in
   [references/commit-and-patch-rules.md](references/commit-and-patch-rules.md)
   (shortlog prefix, body, Signed-off-by, Upstream-Status, CVE tag, License-Update,
   series hygiene, AI-assisted contribution policy).
6. **Verify what you can.** If a configured build directory is available, prove the
   claims that matter with the commands in
   [references/verification.md](references/verification.md) (`bitbake-getvar`,
   `bitbake -e`, `bitbake -S printdiff`, `bitbake-diffsigs`, `bitbake-layers`,
   `buildhistory-diff`, `yocto-check-layer`, `patchtest`, `oelint-adv` if installed).
   Never start a long build without the user's agreement; parse-only and signature
   commands are cheap. Label each finding `verified` or `reasoned`.
7. **Rank, filter by strictness, write the report** in the format below.

## 3. Report format

```text
Yocto change review - <change title or commit range> - strictness: <level>
Release assumed: scarthgap (5.0) [from LAYERSERIES_COMPAT | assumed]
Verdict: <request changes | approve with suggestions | approve>
Summary: <2-4 lines: what the change does, its blast radius, the main risk>

Findings
1. [blocker] [verified|reasoned] <path>:<line> - <one-line problem>
   Effect: <what happens in the build, image or device, and for whom>
   Manual: <doc path or docs.yoctoproject.org/scarthgap URL> - "<short quote>"
   Fix:
     <minimal replacement metadata or commit-message text>
2. [major] ...
...
Nits (<n>): <one line at standard; full list at strict; omitted at gentle>

Questions for the author
- <things that may be intentional; asked, not asserted>

Not checked
- <what needs a build, a target, or files you did not see>
Verification run
- <command> -> <result>   (or "none: no build directory available")
```

Order findings by severity, then by file. Cite the line in the new version of the file.
One finding per root cause: if a single wrong `:append` breaks three variables, report it
once and list the three effects. If nothing is wrong, say so plainly and name what you
checked; do not invent findings to fill the report.

## 4. Ground rules

- Critique the change, never the person. Explain why, cite the manual, offer the fix.
- Verify before reporting. A finding you cannot support from the diff, the surrounding
  files or a command output becomes a question or is dropped.
- Do not "fix" things by suppression: `INSANE_SKIP`, `BB_DANGLINGAPPENDS_WARNONLY`,
  lowering `ERROR_QA`, or blanket `BBMASK` are only acceptable with a stated, narrow
  reason, and suggesting them is never the default fix.
- Do not recommend deleting `tmp/`, `sstate-cache/` or `downloads/` as a review action.
- Never add a `Signed-off-by:` line for the author and never tell an agent to add one;
  the Yocto Project AI policy forbids it (see commit-and-patch-rules.md). If the review
  text will be posted to a Yocto Project mailing list, it must disclose that it is
  AI-generated, and a human must read it before it is sent.
- Old override syntax (`FOO_append`) is a real error in scarthgap, but
  `BBFILE_PATTERN_<layer>`, `LAYERDEPENDS_<layer>`, `SRCREV_<name>` and
  `PREFERRED_VERSION_<recipe>` legitimately use `_`; do not flag them.

## 5. References

- [references/strictness-levels.md](references/strictness-levels.md) - levels, severity
  scale, tone, confidence labels, false-positive guards, borrowed review practices.
- [references/change-effects.md](references/change-effects.md) - what a change does:
  operators, overrides, dependencies, features, providers, versions, signatures, QA.
- [references/file-type-checks.md](references/file-type-checks.md) - per-file-type
  checklists for changed files.
- [references/conventions.md](references/conventions.md) - recipe style guide, naming,
  licensing, layer best practices, security and reproducibility conventions.
- [references/commit-and-patch-rules.md](references/commit-and-patch-rules.md) - commit
  messages, patch headers, series hygiene, stable branches, AI contribution policy.
- [references/verification.md](references/verification.md) - build-backed verification
  commands and how to report their results.
- [references/keywords.md](references/keywords.md) - verbatim scarthgap glossary entries
  for every variable, class, task and QA check this skill relies on (generated from
  `keywords.txt`). It is large: search it for the heading (e.g. "Variable `IMAGE_INSTALL`",
  "QA check `dev-so`") instead of reading it whole. Look a keyword up there before
  asserting what it does. If the `yocto-manuals` skill is installed, it holds the full
  scarthgap manuals for anything not covered here.
