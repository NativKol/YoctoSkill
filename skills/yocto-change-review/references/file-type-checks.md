# Per-File-Type Checks for Changed Files

Classify every changed path, then run the matching list. Each item names the effect
section in change-effects.md (E§n) or the convention in conventions.md (C§n) /
commit-and-patch-rules.md (P§n) that explains it. For a *newly added* recipe or layer,
also apply the full checklist of `yocto-recipe-review` or `yocto-layer-review`.

## Classifying paths

| Path pattern | Type |
|---|---|
| `recipes-*/*/<name>_<ver>.bb`, `<name>_git.bb` | recipe |
| `*.bbappend` | bbappend |
| `*.inc` under `recipes-*` | recipe include |
| `classes/`, `classes-recipe/`, `classes-global/` `*.bbclass` | class |
| `conf/layer.conf` | layer config |
| `conf/distro/*.conf`, `conf/distro/include/*` | distro config |
| `conf/machine/*.conf`, `conf/machine/include/*` | machine config |
| `conf/templates/*/local.conf.sample`, `bblayers.conf.sample`, `conf-notes.txt` | build config template |
| recipe that inherits `image` or `core-image` | image recipe |
| recipe that inherits `packagegroup` | packagegroup |
| `*.patch`, `*.diff` referenced from `SRC_URI` | source patch |
| `*.cfg`, `*.scc`, `defconfig` in kernel recipe dirs | kernel config |
| `*.wks`, `*.wks.in` | wic kickstart |
| `lib/`, `scripts/`, Python in `lib/oe` | code (review as Python, plus effect on metadata) |

Removed files: check who still references them (`require`, `SRC_URI`, bbappends,
`BBFILES_DYNAMIC`, `PREFERRED_VERSION`).

## Recipe (.bb) or include (.inc)

- Name and version: `name_version.bb`, no hyphen in version; `PV` for git (E§7, C§1).
- Upgrade: old recipe removed in the same commit; `PR` dropped; `PE` bumped if the
  version sorts lower; `SRC_URI[sha256sum]` and `SRCREV` updated; `LIC_FILES_CHKSUM`
  re-checked and `License-Update:` in the commit if it changed (E§7, P§3).
- `LICENSE` uses SPDX-style names from `meta/files/common-licenses` with `&`/`|`;
  `LIC_FILES_CHKSUM` covers all license files; `CLOSED` only for proprietary code (C§3).
- `SRC_URI`: checksum, `branch=` for git, `${BPN}` in paths, no GitHub archive tarballs,
  patches listed exist and carry headers (E§8, P§4).
- `SRCREV` full hash, no `${AUTOREV}` in published layers (E§7).
- `DEPENDS` vs `RDEPENDS:<pkg>` kinds right; `-native` for build tools; no `DEPENDS:${PN}`
  (E§3).
- `PACKAGECONFIG ??=` defaults, every option defined, options cover auto-detection (E§5).
- Tasks: install with `${D}${bindir}` style variables, no hard-coded `/usr/lib`;
  `do_install:append` rather than replacing class tasks without reason; idempotent
  file edits (C§2); no network outside `do_fetch` (E§13).
- Packaging: `FILES:<pkg>` patterns precise; `.so` symlinks stay in `-dev`; `PACKAGES`
  additions unique; `ALLOW_EMPTY` only if needed (E§10).
- Machine-specific output sets `PACKAGE_ARCH = "${MACHINE_ARCH}"`; `COMPATIBLE_MACHINE`
  where the recipe only works on some machines (E§9).
- systemd/sysvinit integration: `inherit systemd` with `SYSTEMD_SERVICE:${PN}`, or
  `update-rc.d` with `INITSCRIPT_NAME`; users created with `useradd`, not in
  `do_install` scripts.
- `INSANE_SKIP` additions need a package override and a reason (E§10).
- Old override syntax anywhere is a blocker in scarthgap (E§2).
- Style: variable order, quoting, indentation, required `SUMMARY`/`HOMEPAGE` (C§2).
- `.inc` edits: find every recipe that requires it and judge the change for all of them
  (E§9 blast radius).

## bbappend

- Matches the target recipe name and version; `%` used deliberately (E§11). Verify with
  `bitbake-layers show-appends`.
- Uses `:append`/`:prepend`/`:remove` or `+=` against recipe-owned values, never `=` on a
  list the recipe defines (E§1).
- `FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"` present when adding files; machine-
  specific files in a machine subdirectory (E§8).
- Changes that only make sense for one machine/distro are scoped with an override
  (dev-manual/layers.md 3.2) - unscoped changes in BSP layers are a
  `yocto-check-layer` failure (E§9).
- Does not duplicate the whole recipe; if it rewrites most of it, ask whether an upstream
  change is the better fix.
- For appends to recipes in optional layers, the layer uses `BBFILES_DYNAMIC` (E§11).

## Class (.bbclass)

- Who inherits it: grep `inherit <name>`, `INHERIT`, `USER_CLASSES`, `IMAGE_CLASSES`.
  Blast radius follows (E§9).
- Uses `:append`/`:prepend` on variables that recipes also set (E§1, the `foo.bbclass`
  example).
- New variables referenced by task functions get sensible `[vardeps]` /
  `[vardepsexclude]`; Python that reads computed variable names declares them (E§9).
- Exported functions: `EXPORT_FUNCTIONS` and naming `<class>_do_<task>` consistent
  (bitbake-user-manual-metadata.md 3.5.6).
- Placement: `classes-global/` for classes used via `INHERIT +=`, `PACKAGE_CLASSES`,
  `USER_CLASSES` or `INHERIT_DISTRO`; `classes-recipe/` for `inherit` in recipes,
  `IMAGE_CLASSES` or `KERNEL_CLASSES`; plain `classes/` works in any context. Using a
  class in the wrong context is a parse error (migration-guides/migration-4.1.md)
  *[release-specific: split exists since langdale 4.1]*.
- Python: 4-space indentation, `d.getVar("X")` expands by default, no `os.system` on host
  paths.

## layer.conf

Apply the `yocto-layer-review` checklist, plus:

- `LAYERSERIES_COMPAT_<x>` contains `scarthgap` (and only releases that were tested).
- `LAYERDEPENDS_<x>` updated for any new cross-layer `require`, bbappend, or class use.
- `BBFILE_PRIORITY_<x>` changes: run `bitbake-layers show-overlayed` (E§6).
- No unconditional global configuration (`PREFERRED_PROVIDER_*`, `DISTRO_FEATURES`,
  `IMAGE_INSTALL`, `MACHINE`, `DISTRO`): use the conditional pattern (E§11).
- `BBFILES` / `BBFILES_DYNAMIC` globs match the actual directory layout.

## Distro config

- Feature changes are world-wide (E§5, E§9): state the rebuild in the summary.
- Init system via `INIT_MANAGER` (E§5).
- QA policy edits (`ERROR_QA`, `WARN_QA`): removing an error-level check is a
  **major** policy decision; ask for the reason.
- Security: no `debug-tweaks`, `allow-empty-password`, `empty-root-password` in a
  production distro; security flags via `require conf/distro/include/security_flags.inc`
  if hardening is a goal (dev-manual/securing-images.md 21.2-21.3).
- License policy: `INCOMPATIBLE_LICENSE`, `LICENSE_FLAGS_ACCEPTED` changes have
  compliance impact; flag for the owner of compliance (C§3).
- A distro layer must not set `DISTRO` by being added (`distro.test_distro_no_set_distros`).

## Machine config

- Does not set `DISTRO_FEATURES` or image content; BSPs describe hardware
  (test-manual/yocto-project-compatible.md: BSP layers "usually correspond to a MACHINE
  setting").
- `MACHINE_FEATURES`, `MACHINEOVERRIDES`, tune includes, `PREFERRED_PROVIDER_virtual/kernel`,
  `KERNEL_IMAGETYPE`, `SERIAL_CONSOLES`, `IMAGE_FSTYPES`, `WKS_FILE` consistent.
- A BSP layer must not set `MACHINE` by being added (`bsp.test_bsp_no_set_machine`).
- Delegate deep BSP/kernel questions to `yocto-bsp-kernel` if installed.

## Build config templates (local.conf.sample, bblayers.conf.sample)

- `IMAGE_INSTALL:append = " pkg"`, never `+=` (E§4).
- Development conveniences (`debug-tweaks`, `EXTRA_IMAGE_FEATURES`) acceptable only if the
  template is clearly for development; production templates must not enable them.
- No absolute personal paths; `BBLAYERS` uses `##OEROOT##`-style placeholders if the
  template mechanism provides them.
- Changing a template affects only *new* build directories; existing builds keep their
  `conf/local.conf`. Say so when the change is meant to fix existing builds.

## Image recipe

- `IMAGE_INSTALL` set in the recipe (`=` or `+=` is fine in the image recipe itself
  after `inherit`); `IMAGE_FEATURES` not `EXTRA_IMAGE_FEATURES` (E§4).
- `DEPENDS` does not install packages (E§4).
- Root password / users via `extrausers` and `EXTRA_USERS_PARAMS`; hashes, not clear
  text; no shared password baked for all devices (dev-manual/securing-images.md 21.3).
- `IMAGE_FSTYPES`, `IMAGE_ROOTFS_SIZE`, `IMAGE_LINGUAS` changes alter deploy artifacts.
- Delegate rootfs questions to `yocto-image-rootfs` if installed.

## Packagegroup

- `inherit packagegroup` after `PACKAGE_ARCH` if set (C§2).
- `RDEPENDS:${PN}` lists packages (not recipes); `RRECOMMENDS` for optional parts.
- Adding to a widely used packagegroup changes every image that includes it.

## Source patch (.patch)

- Header has description, `Upstream-Status:` with a valid value and the reason/where,
  `Signed-off-by:` of the author of the patch in the layer, `CVE:` tag for CVE fixes
  (P§4).
- Patch applies without fuzz on the new version (E§8).
- Prefer upstream-able changes; `Inappropriate [oe specific]` only for real OE specifics.
- Verbatim upstream patches: do not review their code style.

## Kernel config (.cfg, .scc, defconfig)

- Scope via machine override or machine directory (E§12).
- Options requested actually land in `.config` (`do_kernel_configcheck`).
- `type=kmeta` repositories bump `SRCREV_meta` together.

## wic kickstart (.wks)

- Selected by `WKS_FILE`; `IMAGE_FSTYPES` includes `wic` (E§12).
- Partition sizes, alignment, bootloader source plugin and `--ondisk` names match the
  machine; layout changes need an update story.

Derived from the Yocto Project scarthgap (5.0) documentation, CC BY-SA 2.0 UK.
