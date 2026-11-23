---
name: yocto-recipe-review
description: Write, fix, review and modernize Yocto/OpenEmbedded recipe metadata - .bb, .bbappend, .inc and .bbclass files - covering SRC_URI/SRCREV/S, LICENSE and LIC_FILES_CHKSUM fields, DEPENDS vs RDEPENDS, PACKAGES/FILES package splitting (leftmost package wins), PACKAGECONFIG, inherit choice (autotools, cmake, meson, cargo, go, python_pep517, systemd, useradd, update-alternatives...), do_install logic, fixing QA errors such as installed-vs-shipped, dev-so, dev-deps or file-rdeps in the recipe, patch Upstream-Status headers, devtool add/modify/finish, and converting old _append/FILES_${PN} override syntax to the ":" syntax. Use it whenever someone shares a recipe or bbappend, asks how to package or depend on something in Yocto, or asks what an operator or override in a recipe does, even if they never say "review". Targets Yocto 5.0 scarthgap / BitBake 2.8. For a full diff/PR/commit review use yocto-change-review; for layer.conf and bbappend matching use yocto-layer-review; for a build log with an unknown cause start with bitbake-debug.
---

# Yocto Recipe Review

Aim for metadata that builds reproducibly on scarthgap, packages every installed file in the right package, and expresses dependencies in the right namespace.

## Workflow

1. **Release.** Scarthgap uses `:` override syntax. The old `_append`, `_prepend`, `_remove`, `FILES_${PN}` forms are a parse error from 3.4 "honister" on; only layers for 3.3 "hardknott" or older use them. Convert with OE-Core's `scripts/contrib/convert-overrides.py` and review the result, because `PREFERRED_PROVIDER_<item>`, `PREFERRED_VERSION_<pn>`, `LAYERSERIES_COMPAT_<col>` and `SRCREV_<name>` keep their underscore.
2. **Read the real values** before judging: `bitbake-getvar -r <recipe> VAR` (history included), `bitbake-getvar -r <recipe> do_install`.
3. **Walk the checklist** in [references/yocto-field-guide.md](references/yocto-field-guide.md) section 5: required fields, source pinning, `S`, class choice, `DEPENDS` (recipe names, `-native` for tools) vs `RDEPENDS:<pkg>` (package names), installs under `${D}`, packaging, QA skips.
4. **Packaging.** Apply the leftmost-package-wins rule and the default `FILES` sets ([references/variables-core.md](references/variables-core.md) section 8). Adding a path to `FILES:${PN}` that `${PN}-dev` already matches does nothing. Unversioned shared libraries need `SOLIBS = ".so"` plus `FILES_SOLIBSDEV = ""`.
5. **Classes.** Check that every class variable has its class and the class is the right one ([references/classes-core.md](references/classes-core.md)). The systemd class packages listed units itself and does nothing without `systemd` in `DISTRO_FEATURES`.
6. **QA.** Map each QA tag to its real cause with [references/qa-errors.md](references/qa-errors.md); `INSANE_SKIP:<pkg>` only for the documented narrow cases, with a comment.
7. **Patches.** Each patch needs `Upstream-Status:` with one of `Pending`, `Submitted [where]`, `Backport [version]`, `Denied`, `Inactive-Upstream [lastcommit: when (and/or) lastrelease: when]`, `Inappropriate [reason]` (reasons today: `oe specific`, `upstream ticket <link>`), and CVE fixes a `CVE:` tag. Refresh fuzzy patches with `devtool modify` + `devtool finish --force-patch-refresh` ([references/debug-tools.md](references/debug-tools.md) section 4).

## Findings to Prioritize

- old override syntax, or underscore variables wrongly converted to `:`
- missing/vague `LICENSE`, missing `LIC_FILES_CHKSUM`, checksum changed without a `License-Update:` reason
- `${AUTOREV}` or a branch name instead of a commit in production
- runtime dependency put in `DEPENDS`, or a recipe name used in `RDEPENDS`
- `FILES` additions that cannot take effect (leftmost rule) or that pull `-dev` content into `${PN}`
- installs outside `${D}`, `cp -a` in `do_install`, host paths
- `+=` used where `:append` is needed (class defaults, `local.conf`), missing leading space in `:append`
- unexplained `INSANE_SKIP`, patches without `Upstream-Status`
- bbappend pinned to a version (`foo_1.2.bbappend`) when `foo_%.bbappend` was meant

## References

- [references/variables-core.md](references/variables-core.md): operators, overrides and their order, dependency and packaging variables.
- [references/classes-core.md](references/classes-core.md): scarthgap class behavior and variables.
- [references/qa-errors.md](references/qa-errors.md): QA tags, messages, fixes.
- [references/yocto-field-guide.md](references/yocto-field-guide.md): recipe checklist, per-task playbook, red flags.
- [references/debug-tools.md](references/debug-tools.md): devtool and inspection commands.
- [references/keywords.md](references/keywords.md): official scarthgap manual entry for every keyword named here; grep `` ## Variable `NAME` ``. Other keywords: `yocto-manuals` skill.

## Output

```text
Findings:
- [severity] file:line - issue and its Yocto effect (cite variable/class/QA tag)

Suggested metadata:
<minimal diff>

Validation:
- bitbake-getvar -r <recipe> <VAR>
- bitbake -c package_qa <recipe>
- bitbake <recipe>
```
