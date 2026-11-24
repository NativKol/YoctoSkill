---
name: yocto-manuals
description: Offline copy of the official Yocto Project 5.0 (scarthgap) manuals and the BitBake 2.8 User Manual, split per keyword. Use it to look up the exact, official meaning of any Yocto or BitBake variable (DEPENDS, RDEPENDS, IMAGE_INSTALL, PACKAGECONFIG, SRC_URI, OVERRIDES...), class (image, core-image, kernel-yocto, insane, buildhistory...), task (do_rootfs, do_populate_sysroot...), machine/distro/image feature, or QA check message, and to read any section of the Reference Manual, Development Tasks Manual, Overview and Concepts, BSP Guide, Kernel Development, SDK, Test, Contributor Guide, migration notes or release notes. Use it whenever an answer depends on precise Yocto behavior, before giving advice from memory, and whenever another Yocto skill's keywords.md does not cover a keyword.
---

# Yocto Manuals (scarthgap 5.0 / BitBake 2.8)

The local text of the official manuals for **Yocto Project 5.0 "scarthgap"** and
**BitBake 2.8**, converted to Markdown. Use it to ground every Yocto statement in the
manual instead of memory. It is fully offline: nothing here needs the internet.

This copy covers scarthgap 5.0 only. If the project is on another release (look at
`LAYERSERIES_COMPAT_*` in `conf/layer.conf`, the poky/openembedded-core branch, or
`DISTRO_VERSION`), tell the user that the answer comes from the scarthgap manuals and may
differ for their release; do not go online to fill the gap.

## Offline lookup

Everything this skill needs is in the repository; it works without internet. Pull only the text you need instead of reading whole files (pages run to thousands of lines). From this skill's folder:

- `python3 scripts/ylookup.py <NAME>...` prints the scarthgap manual entry for any variable, class, task, feature or QA check (`--kind var|class|task|feature|qa` to disambiguate, `--find TEXT` when unsure of the name).
- `--topic TEXT` lists manual sections, `--section <manual/page.md> "<heading>"` prints one, `--grep REGEX [--in ref-manual]` finds anything else.
- URLs in these files are citations for the user, not lookups. The manuals are scarthgap 5.0: if the project is on another release, tell the user rather than going online. Without Python: `grep -n "<NAME>" references/INDEX.md`, then read the per-keyword file it names.

## What to use when

1. **One keyword** (variable, class, task, feature, QA check): `ylookup.py IMAGE_INSTALL do_rootfs core-image`.
   Output is clipped at 80 lines with a hint; `--max-lines 0` prints all. The per-keyword
   files behind it are `references/{variables,classes,tasks,features/<kind>,qa}/<name>.md`
   (flag-style names such as `TUNEVALID[feature]` are stored as `TUNEVALID_feature_.md`).
2. **A topic or workflow** (customizing images, writing a recipe, layers, shared state,
   licensing, SBOM, kernel fragments, devtool, wic, multiconfig...): `ylookup.py --topic
   "<words>"`, then `--section` on the narrowest heading it lists. Chapter-level headings
   print every subsection, so prefer a numbered subsection.
3. **Syntax and evaluation rules** (operators, `:append`/`:remove`, overrides,
   `include`/`require`/`inherit`, flags, anonymous Python, task dependencies):
   `--topic` on `bitbake-user-manual/bitbake-user-manual-metadata.md` headings
   ("Syntax and Operators", "Conditional Syntax"); parse and execution order is in
   `bitbake-user-manual/bitbake-user-manual-execution.md`.
4. **Release changes**: `manuals/migration-guides/migration-5.0.md` (4.3 nanbield to 5.0)
   and `manuals/migration-guides/release-notes-5.0.*.md`; search them with
   `--grep <REGEX> --in migration-guides`.

## Rules when answering

- Quote or paraphrase the manual entry and cite the offline file it came from (each entry
  ends with "Offline source: ..."; the online URL beside it is an optional citation for
  the user).
- The glossary describes defaults and intent. The real value in a build comes from the
  metadata: confirm it with `bitbake-getvar -r <recipe> <VAR>` (add `--value` for the
  value only) or `bitbake -e <recipe>`, which also show the history of every assignment.
- Cross-references from the HTML manuals are plain text here. A name in capitals is
  usually a variable; look it up with `ylookup.py`.
- When the manual is silent or ambiguous, say so, and point to the class or recipe
  source in the user's layers (for example `meta/classes-recipe/image.bbclass`) as the
  final authority.

## What is included

- Yocto Project Reference Manual: variables glossary (880 entries with the BitBake
  glossary merged in), classes (166), tasks (50), features (99), QA checks (46), images,
  variable context, terms, the source directory structure, devtool and kickstart
  references, and the FAQ.
- Overview and Concepts, Development Tasks, BSP Guide, Linux Kernel Development,
  Profiling and Tracing, SDK, Test Environment, Contributor Guide (recipe style guide,
  patch submission rules, AI policy), Security Reference, Quick Build, "What I wish I'd
  known", migration guides and 5.0.x release notes.
- BitBake 2.8 User Manual: overview, execution, syntax and operators, fetching, the
  variables glossary and the "Hello World" example.
- Left out: the Toaster manual, and release notes and migration guides from before 5.0.

## Provenance and license

Converted by `tools/convert_manuals.py` from the scarthgap 5.0 (docs tip at 5.0.x) and
BitBake 2.8 single-page HTML manuals (source: https://docs.yoctoproject.org/scarthgap/ and
https://docs.yoctoproject.org/bitbake/2.8/). The per-keyword files and indexes are
generated by `tools/build_manual_refs.py`. Personal email addresses and home paths in the
manual examples were replaced with placeholders. See [LICENSE-docs.md](LICENSE-docs.md):
the text is CC BY-SA 2.0 UK (the BitBake manual is CC BY 2.5), unlike the MIT-licensed
code in this repository.
