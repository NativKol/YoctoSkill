# License of the manual text in this skill

Everything under `references/` in this skill is derived from the official Yocto
Project documentation and is **not** covered by the MIT license of this repository.

- **Yocto Project manuals** (Reference Manual, Development Tasks Manual, Overview and
  Concepts Manual, BSP Guide, Kernel Development Manual, Profiling and Tracing Manual,
  SDK Manual, Test Environment Manual, Contributor Guide, Security Reference, migration
  guides and release notes), release 5.0 "scarthgap", from
  https://docs.yoctoproject.org/scarthgap/.
  Copyright © The Linux Foundation and the Yocto Project contributors. Licensed under the
  Creative Commons Attribution-Share Alike 2.0 UK: England & Wales license
  (https://creativecommons.org/licenses/by-sa/2.0/uk/).
- **BitBake User Manual**, release 2.8, from https://docs.yoctoproject.org/bitbake/2.8/.
  Copyright © The BitBake contributors. Licensed under the Creative Commons Attribution
  License (https://creativecommons.org/licenses/by/2.5/).

## Changes made

The HTML pages were converted to Markdown, navigation and cross-reference markup was
removed, the text was split into one file per manual page and one file per keyword
(variable, class, task, feature, QA check), and personal email addresses and home
directory paths in examples were replaced with placeholders (`<email>`, `/home/user`).
The wording is otherwise unchanged.

## Share-alike

If you redistribute these files or adaptations of them, keep this notice, credit the
Yocto Project, and license your adaptations under the same terms (CC BY-SA 2.0 UK).
Skill-specific references elsewhere in this repository that paraphrase the manuals say
so at the bottom of the file.
