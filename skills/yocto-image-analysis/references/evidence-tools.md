# Evidence Tools: What Each One Proves (scarthgap 5.0)

Every conclusion about an image or distro should rest on one of these. They fall in three
tiers; say which tier a conclusion came from.

| Tier | Needs | Proves | Cannot prove |
|---|---|---|---|
| 0 — static | the layer sources and `git` | what text changed, and (by reasoning with evaluation-order.md) what it *should* do | anything the parser or the build decides |
| 1 — parse | an initialized Build Directory (`source oe-init-build-env`), no build | final variable values with history, chosen recipes and appends, the task graph | automatic runtime dependencies, package splitting results, package manager resolution, file lists |
| 2 — build | a completed build of the image (ideally with buildhistory) | the installed package list, versions, files, sizes, why-chains, licenses | — |

Citations: offline scarthgap manuals as `<manual>/<page>.md: <section>` (under
`yocto-manuals/references/manuals/`; `python3 scripts/ylookup.py --section ...`); **source** = read
from the scarthgap/BitBake 2.8 tool sources.

## Contents

1. bitbake-getvar
2. bitbake -e
3. bitbake-layers
4. bitbake -g and oe-depends-dot
5. oe-pkgdata-util
6. buildhistory and buildhistory-diff
7. Image manifest, license manifest, SPDX
8. scripts/yocto_diff.py (this skill)

---

## 1. `bitbake-getvar` (tier 1)

```bash
bitbake-getvar DISTRO_FEATURES                 # global datastore, with history
bitbake-getvar -r core-image-minimal IMAGE_INSTALL   # one recipe's datastore
bitbake-getvar -r <image> --value PACKAGE_INSTALL    # value only
bitbake-getvar -r <recipe> -f vardeps --value do_install   # a flag (-f) of a variable
bitbake-getvar -r <recipe> -u --value PACKAGECONFIG  # unexpanded (with --value)
bitbake-getvar -r <recipe> OVERRIDES           # which overrides are active
```

Options (**source**, BitBake 2.8 `bin/bitbake-getvar`): `-r/--recipe`, `-u/--unexpand`,
`-f/--flag`, `--value`, `-q/--quiet`, `--ignore-undefined`.

Reading the output: "the line containing the value of the variable is preceded by a
description of how the variable got its value, including temporary values that were later
overridden. This description also includes variable flags" (dev-manual/debugging.md:
Viewing Variable Values). The format (**source**, `lib/bb/data_smart.py`; paths and line numbers illustrative):

```text
# $IMAGE_INSTALL [3 operations]
#   set /path/meta/recipes-core/images/core-image-minimal.bb:3
#     "packagegroup-core-boot ${CORE_IMAGE_EXTRA_INSTALL}"
#   set? /path/meta/classes-recipe/core-image.bbclass:76
#     "${CORE_IMAGE_BASE_INSTALL}"
#   :append /path/build/conf/local.conf:300
#     " htop"
# pre-expansion value:
#   "packagegroup-core-boot ${CORE_IMAGE_EXTRA_INSTALL} htop"
IMAGE_INSTALL="packagegroup-core-boot  htop"
```

- Each event is `op file:line`, then the text of that assignment. Ops: `set`, `set?`
  (`?=`), `immediate` (`:=`), `append`/`prepend` (`+=`/`=+`), `postdot`/`predot`
  (`.=`/`=.`), `:append`, `:prepend`, `:remove`, `:append[<override>]` (conditional), and
  `override[<o>]:<op>` for assignments to `VAR:<o>`. A weak default (`??=`) is recorded as a
  `set` with `[_defaultval]` before the value.
- Events from code have the file reduced to its base name and the function in brackets,
  e.g. `append base.bbclass:414 [features_backfill]`.
- A `set?` that appears after the variable already had a value did nothing.
- The listed order is the order operations were recorded; `:append`/`:prepend`/`:remove`
  are still applied in that fixed order at the end (evaluation-order.md section 7).
- This history is the most direct way to tie a value to a file and line — use it to attach
  each change in a commit to its effect.

## 2. `bitbake -e` (tier 1)

```bash
bitbake -e > global.env                 # configuration datastore
bitbake -e <image> > image.env          # the image recipe's datastore
grep '^IMAGE_FEATURES=' image.env
```

- "The output starts with a tree listing all configuration files and classes included
  globally, recursively listing the files they include or inherit" — read the top of the
  file to confirm the real include chain (machine conf and its `require`s, distro conf,
  init-manager include, global classes) (dev-manual/debugging.md: Viewing Variable Values;
  bitbake-user-manual-execution.md).
- Every variable is printed with the same history block as `bitbake-getvar`, followed by
  `VAR="value"` (`export VAR=...` for exported ones). Shell functions follow with the final
  assembled body, then Python functions.
- In the value, `"` is written `\"`, `$` as `\$` and newlines as ` \` + newline
  (**source**, `lib/bb/data.py: emit_var`).
- Use dumps from before and after a change as input to `yocto_diff.py env`.
- The dump is large (every variable of the datastore). Save it to a file and grep it; do not paste it into context.

## 3. `bitbake-layers` (tier 1)

From dev-manual/layers.md (section on the `bitbake-layers` script) and **source** for the
options:

```bash
bitbake-layers show-layers                 # layers, paths, priorities
bitbake-layers show-appends [<pn>]          # which .bbappend files apply to which recipe
bitbake-layers show-overlayed [-f] [-s]     # recipes hidden by a same-name recipe in a higher-priority layer
bitbake-layers show-recipes [-f] [-m] [-i <class>] [-l <layer>] [<pn>]   # versions per layer; -i lists recipes inheriting a class
bitbake-layers show-cross-depends           # dependencies crossing layer boundaries
```

Use them to answer: is my bbappend applied (and which others are), which recipe file won,
did a layer priority change move the winner, which images exist
(`bitbake-layers show-recipes -i image` lists recipes inheriting `image`).

## 4. `bitbake -g` and `oe-depends-dot` (tier 1)

```bash
bitbake -g <image>        # writes pn-buildlist and task-depends.dot in the current directory
oe-depends-dot -k <recipe> -w task-depends.dot   # why is <recipe> built for this target
oe-depends-dot -k <recipe> -d task-depends.dot   # what <recipe> depends on
```

- `pn-buildlist`: recipes with at least one task needed to build the target from scratch;
  `ASSUME_PROVIDED` items are omitted. `task-depends.dot`: task-level edges such as
  `"libxslt.do_configure" -> "libxml2.do_populate_sysroot"` (dev-manual/debugging.md:
  Viewing Dependencies Between Recipes and Tasks). `bitbake -g -u taskexp <image>` opens a
  browser UI.
- `oe-depends-dot` (`scripts/oe-depends-dot`, **source**) analyses `task-depends.dot`.
- For images this is a recipe-level upper bound: includes native tools and recipes whose
  packages are only recommended or excluded later. Diff `pn-buildlist` before/after a
  commit to see recipes entering or leaving the build without building.

## 5. `oe-pkgdata-util` (tier 2: needs packaged recipes)

Queries `PKGDATA_DIR`; only works for packages that have been built
(dev-manual/debugging.md: Viewing Package Information with oe-pkgdata-util). Subcommands
(**source**, scarthgap `scripts/oe-pkgdata-util`):

```bash
oe-pkgdata-util list-pkgs [-p <recipe>] ['pattern*']    # packages a recipe produced
oe-pkgdata-util lookup-recipe <runtime-pkg>             # which recipe made a package
oe-pkgdata-util lookup-pkg [-r] <pkg>                   # recipe-space <-> runtime name (glibc <-> libc6)
oe-pkgdata-util find-path '/usr/bin/htop'               # which package ships a file
oe-pkgdata-util list-pkg-files [-p <recipe>] <pkg>      # files in a package
oe-pkgdata-util package-info <pkg>                      # version, recipe, size
oe-pkgdata-util read-value RDEPENDS <pkg>               # any pkgdata value: RDEPENDS, RRECOMMENDS, RPROVIDES, FILES_INFO, PKGSIZE
```

`read-value RDEPENDS` shows the dependencies *after* shlibdeps/pcdeps were added — the
place where automatic dependencies become visible. `${WORKDIR}/packages-split/<pkg>` holds
the actual split files when `rm_work` is not enabled.

## 6. buildhistory and `buildhistory-diff` (tier 2)

Enable in `local.conf` (dev-manual/build-quality.md: Enabling and Disabling Build History):

```bitbake
INHERIT += "buildhistory"
BUILDHISTORY_COMMIT = "1"
```

Image data lives in `${BUILDHISTORY_DIR}/images/<machine_arch>/<libc>/<image>/`
(**source**: `BUILDHISTORY_DIR_IMAGE`; `BUILDHISTORY_DIR` defaults to
`${TOPDIR}/buildhistory`). Files (dev-manual/build-quality.md: Build History Image
Information):

| File | Contents |
|---|---|
| `image-info.txt` | `DISTRO`, `DISTRO_VERSION`, `USER_CLASSES`, `IMAGE_CLASSES`, `IMAGE_FEATURES`, `IMAGE_LINGUAS`, `IMAGE_INSTALL`, `BAD_RECOMMENDATIONS`, `NO_RECOMMENDATIONS`, `PACKAGE_EXCLUDE`, `ROOTFS_POSTPROCESS_COMMAND`, `IMAGE_POSTPROCESS_COMMAND`, `IMAGESIZE` (KiB) |
| `installed-package-names.txt` | installed package names |
| `installed-packages.txt` | installed package file names |
| `installed-package-sizes.txt` | packages by size |
| `depends.dot` (+ `depends-nokernel*.dot`) | installed-package dependency graph |
| `files-in-image.txt` | every file with mode, owner, size, symlink target |
| `build-id.txt` | build configuration header and layer revisions |
| `image-files/` | copies of files named in `BUILDHISTORY_IMAGE_FILES` |

`depends.dot` edges (**source**, `buildhistory.bbclass`): plain `"a" -> "b"` is an
`RDEPENDS`, `[style=dotted]` an `RRECOMMENDS`, `[style=dashed]` a dependency satisfied
through `RPROVIDES`, `[label=">= 1.2"]` a versioned one.

Per-package data is under `packages/<arch>/<recipe>/<package>/latest` (`PV`, `PR`,
`RPROVIDES`, `RDEPENDS`, `RRECOMMENDS`, `PKGSIZE`, `FILES`, `FILELIST`) and per recipe
`packages/<arch>/<recipe>/latest` (`DEPENDS`, `PACKAGES`); `metadata-revs` at the top
lists layer revisions (dev-manual/build-quality.md: Build History Package Information).

Compare builds:

```bash
buildhistory-diff -p buildhistory                 # last build vs the one before (build-minus-1..HEAD)
buildhistory-diff -p buildhistory <rev1> <rev2>   # any two buildhistory commits
buildhistory-diff -a ...                          # report all changes, not only significant ones
buildhistory-diff -s ...                          # report differing task signatures instead
```

Needs GitPython (`python3-git`) (dev-manual/build-quality.md: Examining Build History
Information). Options are from scarthgap `scripts/buildhistory-diff` (**source**).
Image-only collection: `BUILDHISTORY_FEATURES = "image"`, `BUILDHISTORY_COMMIT = "0"`.

## 7. Image manifest, license manifest, SPDX (tier 2)

- **Manifest**: `${DEPLOY_DIR_IMAGE}/<image>-<machine>.rootfs-<timestamp>.manifest` plus a
  `<image>-<machine>.rootfs.manifest` symlink, one `packagename packagearch version` line
  per installed package (ref-manual/variables.md: IMAGE_MANIFEST, IMAGE_NAME,
  IMAGE_LINK_NAME, IMAGE_NAME_SUFFIX). Available without buildhistory; diff two with
  `yocto_diff.py manifest`.
- **License manifest**: `${DEPLOY_DIR}/licenses/${SSTATE_PKGARCH}/<image>-<machine>.rootfs-<datestamp>/`
  (dev-manual/licenses.md). Packages statically linked through `DEPENDS` only are not in it
  (dev-manual/licenses.md: Compliance Limitations with Executables Built from Static
  Libraries).
- **SPDX/SBOM**: `create-spdx` is inherited by default through `INHERIT_DISTRO`; SPDX 3.0 is
  available in scarthgap via `create-spdx-3.0` but disabled by default; the top-level
  document is written to `tmp/deploy/images/<machine>/`, ancillary files to
  `tmp/deploy/spdx` (dev-manual/sbom.md). Useful to list components and versions of an
  image; the exact file name depends on which class is used.

## 8. `scripts/yocto_diff.py` (this skill; standard library only)

```bash
python3 scripts/yocto_diff.py manifest old.manifest new.manifest
python3 scripts/yocto_diff.py manifest old/installed-package-names.txt new/installed-package-names.txt
python3 scripts/yocto_diff.py env before.env after.env --only '^(IMAGE_|DISTRO_FEATURES|MACHINE_FEATURES|PACKAGE_INSTALL|PREFERRED_|VIRTUAL-RUNTIME)'
python3 scripts/yocto_diff.py why buildhistory/images/<arch>/glibc/<image>/depends.dot <package>
```

- `manifest`: added, removed, version/arch changes. Exit 1 when different.
- `env`: variables whose final value differs; lists words added/removed and the last
  history operations (`--history N`) from the newer dump, so each difference points at a
  file and line. Ignores always-changing variables such as `DATE`/`TIME`/`DATETIME`; add
  more with `--ignore REGEX`.
- `why`: shortest chains from a top-level installed package down to the target, marking
  `->` RDEPENDS, `~>` RRECOMMENDS, `=>` via RPROVIDES. A chain made only of `~>` edges means
  `BAD_RECOMMENDATIONS` can remove the package; any `->` means it cannot.
- All subcommands accept `--json`. Tests: `python3 -m unittest test_yocto_diff` from
  `scripts/`.

---
Derived from the Yocto Project scarthgap (5.0) documentation, CC BY-SA 2.0 UK.
