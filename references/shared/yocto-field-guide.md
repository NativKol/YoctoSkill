# Yocto Field Guide for Agents

The one place for the task-failure playbook, the recipe and layer checklists, and review red flags. Release: Yocto Project 5.0 "scarthgap" / BitBake 2.8. Operators and overrides are explained in `variables-core.md`, tasks in `tasks-reference.md`, QA tags in `qa-errors.md` (each skill ships the ones it needs).

## 1. Mental Model

- BitBake parses configuration (`bitbake.conf`, `local.conf`, `bblayers.conf`, machine and distro conf), then each recipe with its classes, includes and appends, then runs tasks. Every recipe has a private copy of the datastore.
- Recipes produce packages; images install packages. Recipe names, package names and image names are different namespaces.
- Layers decide which metadata exists and which wins (`BBFILE_PRIORITY`, appends, `BBMASK`).
- The truth about a failure is in `tmp/work/<arch>/<pn>/<pv>/temp/log.do_<task>` and `run.do_<task>`; the truth about a value is `bitbake-getvar -r <recipe> VAR`.
- Shared state can skip tasks entirely (restored from sstate). "My change did nothing" is often a signature question (`debug-tools.md`).

## 2. File Types

`.bb` recipe; `.bbappend` append from another layer (`foo_%.bbappend` matches any version); `.bbclass` class; `.inc` shared include (`require` it); `conf/layer.conf`; `conf/local.conf` and `conf/bblayers.conf` (build dir, not product metadata); `conf/machine/*.conf`; `conf/distro/*.conf`; `conf/multiconfig/*.conf`; `.wks` wic kickstart; `.cfg` / `.scc` kernel fragments and features; `files/` or `${PN}/` directories for `file://` sources.

## 3. Gather Evidence (agent-safe commands)

```bash
bitbake-layers show-layers
bitbake-layers show-recipes <pn>
bitbake-layers show-appends
bitbake-getvar -r <recipe> <VAR>             # final value with history
bitbake -c listtasks <recipe>
bitbake -n <target>                          # dry run
bitbake -k <target>                          # build and keep going to collect every failure
grep -n -E 'ERROR|error:|QA Issue' tmp/work/*/<pn>/*/temp/log.do_<task>
oe-pkgdata-util list-pkgs '<pattern>*'      # packages already built
oe-pkgdata-util find-path '*/usr/bin/<tool>'
```

Not evidence gathering: `bitbake -c devshell` (interactive, for a human), `bitbake -c cleansstate` / `cleanall` (destructive; see section 6). Never pipe to `less`.

## 4. Task Failure Playbook

Always start from the first failing task and its first error.

### do_fetch
- Evidence: `log.do_fetch`, `bitbake-getvar -r <pn> SRC_URI`, `SRCREV`, `DL_DIR`, `PREMIRRORS`/`MIRRORS`, `BB_NO_NETWORK`.
- Git URIs need `branch=` (or `nobranch=1`) and usually `protocol=https`; `SRCREV` must exist on that branch. Archives need `SRC_URI[sha256sum]`; update it only after confirming upstream really changed.
- Corporate networks: mirrors and `PREMIRRORS`, not edits to the fetcher. Refetch with `bitbake -f -c fetch <pn>`, not `cleanall`.

### do_unpack
- Evidence: the `WORKDIR` listing and `S`.
- Scarthgap git sources unpack to `${WORKDIR}/git`: set `S = "${WORKDIR}/git"`. (From 5.1 styhead this becomes `${UNPACKDIR}/git`; not for scarthgap.) Archives with a different top directory: set `S`; colliding multi-source URIs: `subdir=`/`destsuffix=`.

### do_patch
- Evidence: `log.do_patch`, the patch list in `SRC_URI`, `FILESPATH`/`FILESEXTRAPATHS`.
- Refresh failing or fuzzy patches with `devtool modify <pn>` + `devtool finish --force-patch-refresh <pn> <layer>` and review the diff. Every patch needs a valid `Upstream-Status:` header (`patch-status`). `apply=no` only for files that must not be applied; `striplevel=` for non-`-p1` patches.

### do_configure
- Evidence: inherited class, `EXTRA_OECONF`/`EXTRA_OECMAKE`/`EXTRA_OEMESON`, `PACKAGECONFIG`, `config.log` or `CMakeCache.txt` in `${B}`, `recipe-sysroot*`.
- Missing library or header: add the providing recipe to `DEPENDS`; missing host tool: `foo-native` in `DEPENDS` or the right class (`pkgconfig`, `gettext`). Feature switches belong in `PACKAGECONFIG`. `configure-unsafe` means host paths were probed. `LIC_FILES_CHKSUM` mismatch errors appear at the end of this task.

### do_compile
- Evidence: the failing command in `log.do_compile`, generated files, `-j` races.
- Fix cross variables through the class (`EXTRA_OEMAKE`, `CC`, `CFLAGS`), add generator tools as `-native`. Only use `PARALLEL_MAKE = ""` for a proven race, in that recipe, with a comment (dev-manual "Debugging Parallel Make Races" 32.13).

### do_install
- Evidence: `run.do_install`, contents of `${D}` (`${WORKDIR}/image`).
- Install with `install -d`/`install -m` into `${D}${bindir}` etc.; never to host paths. Avoid `cp -a` (host ownership, `host-user-contaminated`): use `cp --no-preserve=ownership` or `tar --no-same-owner`.

### do_package / do_package_qa
- Evidence: the bracketed QA tag, `PACKAGES`, `FILES:<pkg>`, `${WORKDIR}/packages-split/`.
- Remember leftmost-package-wins (`variables-core.md` section 8). See `qa-errors.md` for each tag. `INSANE_SKIP` only with a stated reason.

### do_populate_sysroot / do_prepare_recipe_sysroot
- Files another recipe needs at build time must be installed into `${D}` in a directory listed in `SYSROOT_DIRS` (add with `SYSROOT_DIRS += "/opt"`); recipes never write into sysroots directly.

### do_rootfs, do_image*
- Owned by `yocto-image-rootfs`: package names, `IMAGE_INSTALL`, recommendations, postinsts, `IMAGE_FSTYPES`, wic.

### Parse errors (before any task)
- "No recipes available for: .../foo_1.2.bbappend": dangling append (fatal by default; `BB_DANGLINGAPPENDS_WARNONLY = "1"` downgrades it). Rename to the new version or `foo_%.bbappend`.
- "Layer X is not compatible with the core layer": `LAYERSERIES_COMPAT_X` does not list `scarthgap`.
- Old `_append`/`_prepend` syntax: parse error since 3.4; convert to `:`.
- "Nothing PROVIDES 'foo'": no recipe provides it (layer missing, `BBMASK`, `COMPATIBLE_MACHINE`, `features_check` skip). `bitbake-layers show-recipes foo` and the skip reason in the error help.

## 5. Recipe Checklist

```bitbake
SUMMARY = "Short summary"
HOMEPAGE = "https://example.org"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=<md5>"

SRC_URI = "git://example.org/project.git;protocol=https;branch=main"
SRCREV = "<full commit hash>"
S = "${WORKDIR}/git"            # scarthgap; 5.1+ uses ${UNPACKDIR}/git

inherit cmake pkgconfig systemd

DEPENDS = "openssl"
PACKAGECONFIG ??= "foo"
PACKAGECONFIG[foo] = "-DWITH_FOO=ON,-DWITH_FOO=OFF,libfoo"

SYSTEMD_SERVICE:${PN} = "example.service"   # the systemd class packages the unit; no FILES line needed
RDEPENDS:${PN} += "bash"                    # because a shipped script uses #!/bin/bash
```

Check: required fields (`SUMMARY`, `DESCRIPTION` or default, `HOMEPAGE`, `LICENSE`, `LIC_FILES_CHKSUM`; recipe style guide 3.5.1); fixed `SRCREV` (no `${AUTOREV}` in production); checksums for archives; correct `S`; build class instead of hand-rolled configure/compile; build deps in `DEPENDS`, runtime deps in `RDEPENDS:<pkg>` as package names; installs only under `${D}`; every installed file packaged; no unexplained `INSANE_SKIP`; `${BPN}` (not `${PN}`) in `SRC_URI`; `BBCLASSEXTEND` instead of separate `-native` recipes; idempotent tasks.

## 6. Clean Commands and Their Cost

| Command | Removes | When |
| --- | --- | --- |
| `bitbake -f -c <task> <pn>` | nothing; forces the task | first choice to rerun |
| `bitbake -c clean <pn>` | work dir output | stale work dir; sstate may restore it |
| `bitbake -c cleansstate <pn>` | work dir + recipe sstate | ask first; not with shared `SSTATE_DIR` |
| `bitbake -c cleanall <pn>` | + downloads | ask first; almost never (use `bitbake -f -c fetch`) |

Never recommend deleting `tmp/`, `sstate-cache/` or `downloads/` as a fix.

## 7. Layer Checklist

```bitbake
BBPATH .= ":${LAYERDIR}"
BBFILES += "${LAYERDIR}/recipes-*/*/*.bb ${LAYERDIR}/recipes-*/*/*.bbappend"
BBFILE_COLLECTIONS += "mylayer"
BBFILE_PATTERN_mylayer = "^${LAYERDIR}/"
BBFILE_PRIORITY_mylayer = "6"
LAYERDEPENDS_mylayer = "core"
LAYERSERIES_COMPAT_mylayer = "scarthgap"   # list only series you have built and tested
BBFILES_DYNAMIC += "openembedded-layer:${LAYERDIR}/dynamic-layers/meta-oe/*/*/*.bbappend"
```

Check: unique, stable collection name; `LAYERSERIES_COMPAT` names only tested series; `LAYERDEPENDS` complete; globs cover the files; appends verified with `bitbake-layers show-appends`; optional appends behind `BBFILES_DYNAMIC`; priority not used to paper over provider or version policy (use `PREFERRED_PROVIDER_*` / `PREFERRED_VERSION_*`).

## 8. Provider Rules

- `PROVIDES` + `PREFERRED_PROVIDER_<item>`: build-time choice. Keep the underscore: `PREFERRED_PROVIDER_virtual/kernel`, never `PREFERRED_PROVIDER:virtual/kernel`.
- `RPROVIDES`: runtime alternatives; no `virtual/` names at runtime (use `VIRTUAL-RUNTIME_*`).
- `PREFERRED_VERSION_<pn> = "1.2%"`: matched against `PV`.
- `bitbake -DDD -v <target>` shows why a provider or version was chosen.

## 9. Review Red Flags

- Old `_append`/`FILES_${PN}` syntax in a scarthgap layer (parse error since 3.4).
- `PREFERRED_PROVIDER:` / `PREFERRED_VERSION:` / `LAYERSERIES_COMPAT:` written with a colon.
- `INSANE_SKIP` without a linked root cause.
- `SRCREV = "${AUTOREV}"` in production metadata.
- Missing or vague `LICENSE` / `LIC_FILES_CHKSUM`, or a checksum change without `License-Update:`.
- Host tools assumed instead of `-native` dependencies; installing outside `${D}`.
- `IMAGE_INSTALL +=` in `local.conf`; product policy in `local.conf`.
- Version-pinned bbappend where `%` was intended (or the reverse).
- `DEPENDS` used to put something in an image; recipe names used as package names.
- Patches without `Upstream-Status`.
- Destructive cleans or deleting `tmp`/`sstate-cache` as routine.

## 10. Response Template

```text
Most likely cause: ...
Evidence (observed / needed): ...
Fix (metadata change or command): ...
Why this is the Yocto/BitBake fix: ...
Validate: bitbake -c <task> <recipe>, then bitbake <target>
Manual: <manual> "<section>"
```

Derived from the Yocto Project scarthgap (5.0) documentation, CC BY-SA 2.0 UK.
