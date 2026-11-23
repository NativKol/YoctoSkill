---
name: yocto-manuals
description: Offline copy of the official Yocto Project 5.0 (scarthgap) manuals and the BitBake 2.8 User Manual, split per keyword. Use it to look up the exact, official meaning of any Yocto or BitBake variable (DEPENDS, RDEPENDS, IMAGE_INSTALL, PACKAGECONFIG, SRC_URI, OVERRIDES...), class (image, core-image, kernel-yocto, insane, buildhistory...), task (do_rootfs, do_populate_sysroot...), machine/distro/image feature, or QA check message, and to read any section of the Reference Manual, Development Tasks Manual, Overview and Concepts, BSP Guide, Kernel Development, SDK, Test, Contributor Guide, migration notes or release notes. Use it whenever an answer depends on precise Yocto behavior, before giving advice from memory, and whenever another Yocto skill's keywords.md does not cover a keyword.
---

# Yocto Manuals (scarthgap 5.0 / BitBake 2.8)

The local text of the official manuals for **Yocto Project 5.0 "scarthgap"** and
**BitBake 2.8**, as published on docs.yoctoproject.org, converted to Markdown. Use it
to ground every Yocto statement in the manual instead of memory.

Release check first: this copy matches scarthgap. If the project is on another release
(look at `LAYERSERIES_COMPAT_*` in `conf/layer.conf`, the poky/openembedded-core
branch, or `DISTRO_VERSION`), say so, and use
`https://docs.yoctoproject.org/<release>/` for anything that may differ.

## How to look something up

1. **One keyword** (variable, class, task, feature, QA check): open the per-keyword file.
   - Variable: `references/variables/<NAME>.md`, for example
     [references/variables/IMAGE_INSTALL.md](references/variables/IMAGE_INSTALL.md).
     It holds the Yocto Reference Manual glossary entry and, when one exists, the
     BitBake User Manual entry.
   - Class: `references/classes/<name>.md`, for example
     [references/classes/image.md](references/classes/image.md).
   - Task: `references/tasks/<do_task>.md`, for example
     [references/tasks/do_rootfs.md](references/tasks/do_rootfs.md).
   - Feature: `references/features/<machine|distro|image>/<name>.md`.
   - QA check: `references/qa/<check>.md`, for example
     [references/qa/installed-vs-shipped.md](references/qa/installed-vs-shipped.md).
   - Not sure of the exact name? Grep [references/INDEX.md](references/INDEX.md), which
     has one line per keyword with a summary and its file. Flag-style names such as
     `TUNEVALID[feature]` are stored as `TUNEVALID_feature_.md`.
2. **A topic or workflow** (customizing images, writing a recipe, layers, shared state,
   the build process, licensing, SBOM, kernel fragments, devtool, wic, multiconfig...):
   grep [references/MANUALS.md](references/MANUALS.md), the table of contents of every
   page, then read the section from `references/manuals/<manual>/<page>.md`.
3. **Syntax and evaluation rules** (operators `=`, `?=`, `??=`, `:=`, `+=`, `.=`,
   `:append`, `:prepend`, `:remove`, overrides, `include`/`require`/`inherit`, flags,
   anonymous Python, task dependencies): read
   [references/manuals/bitbake-user-manual/bitbake-user-manual-metadata.md](references/manuals/bitbake-user-manual/bitbake-user-manual-metadata.md)
   and, for parse and execution order,
   [references/manuals/bitbake-user-manual/bitbake-user-manual-execution.md](references/manuals/bitbake-user-manual/bitbake-user-manual-execution.md).
4. **Release changes**: [references/manuals/migration-guides/migration-5.0.md](references/manuals/migration-guides/migration-5.0.md)
   (moving from 4.3 nanbield to 5.0), and `references/manuals/migration-guides/release-notes-5.0.*.md`
   for what each point release fixed.

Use grep, not full reads: `variables.md` alone is about 400 KB. For example:
`grep -n "^\*\*PACKAGE_EXCLUDE\*\*" -A30 references/manuals/ref-manual/variables.md`, or
`grep -ril "BAD_RECOMMENDATIONS" references/manuals`.

## Rules when answering

- Quote or paraphrase the manual entry, and cite it as the file plus the online URL
  printed under each entry (`Source:`), so the user can check it.
- The glossary describes defaults and intent. The real value in a build comes from the
  metadata: confirm it with `bitbake-getvar -r <recipe> <VAR>` (add `--value` for the
  value only) or `bitbake -e <recipe>`, which also show the history of every assignment.
- Cross-references from the HTML manuals are plain text here. A name in capitals is
  usually a variable; look it up in `references/variables/`.
- When the manual is silent or ambiguous, say so, and point to the class or recipe
  source in the user's layers (for example `meta/classes-recipe/image.bbclass`) as the
  final authority.

## What is included

- Yocto Project Reference Manual: variables glossary (880 entries with the BitBake
  glossary merged in), classes (166), tasks (50), features (99), QA checks (46), images,
  variable context, terms, the source directory structure, devtool and kickstart
  references, and the FAQ.
- Overview and Concepts Manual, Development Tasks Manual, BSP Developer's Guide, Linux
  Kernel Development Manual, Profiling and Tracing, SDK Manual, Test Environment Manual,
  Contributor Guide (including the recipe style guide and patch submission rules),
  Security Reference, Quick Build, "What I wish I'd known", migration guides and 5.0.x
  release notes.
- BitBake 2.8 User Manual: overview, execution, syntax and operators, fetching, the
  variables glossary and the "Hello World" example.
- Left out: the Toaster manual, and release notes and migration guides from before 5.0.

## Provenance and license

Converted from the `singleindex.html` pages of
https://docs.yoctoproject.org/scarthgap/ (5.0, docs tip at 5.0.x) and
https://docs.yoctoproject.org/bitbake/2.8/ by `tools/convert_manuals.py`. The
per-keyword files and indexes are generated by `tools/build_manual_refs.py`. Personal
email addresses and home paths in the manual examples were replaced with placeholders.
See [LICENSE-docs.md](LICENSE-docs.md): the text is CC BY-SA 2.0 UK (the BitBake manual
is CC BY 2.5), unlike the MIT-licensed code in this repository.
