---
name: yocto-agent-skills
description: Official-doc-first Yocto Project 5.0 (scarthgap) and BitBake 2.8 help for when this whole repository is installed as a single skill - debugging BitBake build failures and QA errors, reviewing recipes, bbappends, classes and layers, image and rootfs content, machine/BSP/kernel/devicetree/U-Boot metadata, license/CVE/SBOM compliance, and release or migration questions. Use it for any .bb, .bbappend, .bbclass, layer.conf, local.conf, bblayers.conf, machine or distro conf, image recipe, kernel recipe, or BitBake/tmp/work log. Install either this root skill or the individual skills under skills/, not both, or the two will compete for the same requests.
---

# Yocto Agent Skills

Compatibility router for hosts that install the repository as one skill. When the host supports skill collections, install the focused skills in `skills/` instead (not both):

- `skills/bitbake-debug`: build failures, task logs, parse errors, QA during builds, sstate/signature questions.
- `skills/yocto-recipe-review`: `.bb`/`.bbappend`/`.bbclass` content, dependencies, packaging, override syntax, devtool, patches.
- `skills/yocto-layer-review`: `layer.conf`, compatibility, priority, bbappend matching, providers.
- `skills/yocto-image-rootfs`: image recipes, `IMAGE_INSTALL`/`IMAGE_FEATURES`, `do_rootfs`, postinsts, wic, SDK.
- `skills/yocto-bsp-kernel`: machine, kernel config, devicetree, U-Boot, FIT, deploy artifacts.
- `skills/yocto-security-sbom`: license, CVE, SPDX/SBOM, archiver.
- `skills/yocto-doc-router`: which manual/section/release applies.
- `skills/yocto-manuals`: offline scarthgap manuals, per keyword.
- `skills/yocto-change-review` and `skills/yocto-image-analysis`: diff/PR review, and analysis of what a built image contains.

## Ground Rules

1. **Release first.** Detect it from the build: `bitbake --version` (2.8.x = scarthgap), `bitbake-getvar --value DISTRO_VERSION`, `LAYERSERIES_COMPAT_*` in each `conf/layer.conf`, the poky/oe-core branch. If unknown, say you assume scarthgap.
2. **Docs and metadata over memory.** Route with [references/shared/official-doc-map.md](references/shared/official-doc-map.md); verify names in the manuals.
3. **Smallest useful evidence:** the failing task and its first error, `tmp/work/<arch>/<pn>/<pv>/temp/log.do_<task>`, the recipe or append, `bitbake-getvar -r <recipe> VAR`.
4. **Map every fix to BitBake terms** (variable, task, class, package, layer); a generic Linux fix is not a Yocto fix.
5. **Modern syntax.** Scarthgap requires `:` overrides (`FILES:${PN}`, `do_install:append`); old `_append` fails to parse since 3.4 honister. Variables such as `PREFERRED_PROVIDER_virtual/kernel` and `LAYERSERIES_COMPAT_<col>` keep their underscore.
6. **No destructive first fixes.** Never delete `tmp/`, `downloads/` or `sstate-cache/`; prefer `bitbake -f -c <task>`; ask before `cleansstate`/`cleanall`.

## Gather Evidence (agent-safe)

```bash
bitbake-layers show-layers
bitbake-layers show-recipes <pn>
bitbake-layers show-appends
bitbake-getvar -r <recipe> <VAR>         # final value plus assignment history
bitbake -c listtasks <recipe>
bitbake -n <target>                      # dry run
bitbake -g <target>                      # task-depends.dot, pn-buildlist
oe-pkgdata-util list-pkgs '<pattern>*'  # only for packages already built
oe-pkgdata-util find-path '*/path/or/file'
```

For a human only (interactive): `bitbake -c devshell <recipe>`, `bitbake -c menuconfig virtual/kernel`. Agents read `run.do_<task>` and rerun with `bitbake -f -c <task> <recipe>`.

Fix commands that need consent (destructive): `bitbake -c cleansstate <recipe>`, `bitbake -c cleanall <recipe>`.

Logs and outputs:

```text
tmp/work/<arch>/<pn>/<pv>/temp/log.do_<task>   and run.do_<task>
tmp/work/<arch>/<pn>/<pv>/image/                 (${D})
tmp/work/<arch>/<pn>/<pv>/packages-split/        (needs rm_work disabled)
tmp/deploy/images/<machine>/
tmp/deploy/licenses/   tmp/deploy/spdx/   tmp/deploy/cve/
tmp/log/cooker/<machine>/console-latest.log
```

## Workflow

1. Classify: build failure, recipe, layer, image, machine/kernel, compliance, release/migration.
2. Use the per-task playbook in [references/shared/yocto-field-guide.md](references/shared/yocto-field-guide.md) (the only copy of it).
3. Look up semantics in the references below, cite the manual section, propose a minimal change, give the validation command.

## References

- [references/shared/yocto-field-guide.md](references/shared/yocto-field-guide.md): playbook, checklists, clean commands, red flags.
- [references/bitbake/variables-core.md](references/bitbake/variables-core.md): operators, override order, key variables.
- [references/bitbake/tasks-reference.md](references/bitbake/tasks-reference.md): task chain and flags.
- [references/bitbake/classes-core.md](references/bitbake/classes-core.md): scarthgap classes.
- [references/bitbake/debug-tools.md](references/bitbake/debug-tools.md): bitbake-getvar, signatures, sstate, devtool, buildhistory.
- [references/yocto/qa-errors.md](references/yocto/qa-errors.md): every QA check.
- [references/yocto/image-rootfs.md](references/yocto/image-rootfs.md), [references/yocto/bsp-kernel.md](references/yocto/bsp-kernel.md), [references/yocto/security-sbom.md](references/yocto/security-sbom.md), [references/yocto/migration.md](references/yocto/migration.md).

## Output Style

Troubleshooting: (1) most likely cause, (2) evidence observed or needed, (3) exact command or metadata change, (4) why it works in Yocto terms, (5) manual section. Code changes: minimal, release-aware snippet plus the validation command.
