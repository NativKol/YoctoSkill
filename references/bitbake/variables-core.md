# BitBake Operators, Overrides, and Core Variables

Release: Yocto Project 5.0 "scarthgap" with BitBake 2.8. The BitBake User Manual is the authority for operators and overrides; the Yocto Reference Manual "Variables Glossary" is the authority for variable meaning. Section numbers below are from those manuals (offline copy: `yocto-manuals` skill, `references/manuals/bitbake-user-manual/bitbake-user-manual-metadata.md` and `references/manuals/ref-manual/variables.md`).

Contents: 1 Inspecting values - 2 Assignment operators - 3 Overrides - 4 Directives - 5 Variable flags and tasks - 6 Source and fetch - 7 Dependencies and providers - 8 Packaging - 9 Images and features - 10 Layers - 11 Machine, distro, kernel - 12 Runtime integration

## 1. Inspect the Final Value First

Never reason about a value from one file alone. Ask BitBake (dev-manual "Viewing Variable Values", 32.2):

```bash
bitbake-getvar MACHINE                     # value after configuration parsing
bitbake-getvar -r busybox FILES:busybox    # value for one recipe, with the history of every assignment
                                           # (write the real package name; ${PN} is not expanded in the name)
bitbake-getvar -r <recipe> OVERRIDES       # which overrides are active for that recipe
bitbake-getvar -r <recipe> do_install      # final body of a shell task, after :append/:prepend
bitbake -e <recipe> | grep -n '^python do_' # Python functions only appear in bitbake -e
```

`bitbake-getvar` prints how the value was built (file, line, operator) before the final value, including temporary values that were later overridden. It is non-interactive and safe for agents. Use `bitbake -e <recipe>` only for Python functions or a full dump, and always pipe it to `grep`, never to a pager.

Each recipe gets its own copy of the configuration datastore, and each task gets a copy of the recipe datastore, so a value set in one recipe or task is invisible to others (32.2 note).

## 2. Assignment Operators (BitBake manual 3.1)

| Operator | Effect | When applied | Space added? |
| --- | --- | --- | --- |
| `A = "x"` | set; `${...}` references expand when the variable is used | parse (value), expansion later | n/a |
| `A ?= "x"` | set only if `A` has no value at that moment; first `?=` wins | immediately (3.1.5) | n/a |
| `A ??= "x"` | weak default; used only if nothing else assigns `A`; last `??=` wins | end of parsing (3.1.6) | n/a |
| `A := "x"` | expand the right side now | immediately (3.1.7) | n/a |
| `A += "x"` / `A =+ "x"` | append / prepend | immediately (3.1.8) | yes, BitBake inserts one space |
| `A .= "x"` / `A =. "x"` | append / prepend | immediately (3.1.9) | no |
| `A:append = "x"` / `A:prepend = "x"` | append / prepend | at expansion time (3.1.10) | no, you add it yourself |
| `A:remove = "x"` | remove every whitespace-separated occurrence of `x` | at expansion time, after append and prepend (3.1.11) | n/a |
| `unset A`, `unset A[flag]` | delete variable or flag (3.1.15) | immediately | n/a |

Rules that matter in reviews:

- `+=` and `=+` insert the space for you: write `VAR += "value"`, not `VAR += " value"` (the extra space is harmless but noisy).
- You control spacing only for `.=`, `=.`, `:append` and `:prepend`: `IMAGE_INSTALL:append = " strace"` needs the leading space, or the value fuses with the previous word.
- Immediate operators act on the value as it is at that line. A later plain `=` replaces everything, including earlier `+=`. `:append`/`:prepend`/`:remove` survive later `=` because they are applied when the variable is read. This is why classes and `local.conf` should use `:append` (3.1.12): if `foo.bbclass` does `FOO += "val"` and the recipe later does `FOO = "initial"`, the result is `initial`; with `FOO:append = " val"` it is `initial val`.
- It is never necessary to combine `+=` with `:append` (3.1.12 note): `FOO:append += "x"` only adds a leading space.
- Order of override-style operations is always `:append`, then `:prepend`, then `:remove`. A removed string cannot be re-appended. `bitbake -e` may list a `:remove` before an `:append` in the history, but `:remove` still runs last (3.1.11 notes).
- `+=` does not see a `??=` weak default: `W ??= "x"` then `W += "y"` gives `" y"`, while `W:append = "y"` gives `"xy"` (3.1.6).
- Undefined references are kept literally during `:=` expansion (`${C}` stays `${C}`), unlike Make (3.1.7).
- Mixed example from 3.3.3: `A = "1"`, `A:append = "2"`, `A:append = "3"`, `A += "4"`, `A .= "5"` gives `1 4523`: immediate operators first (`1 45`), then the appends.

## 3. Overrides (BitBake manual 3.3)

### 3.1 How they work

`OVERRIDES` is a colon-separated list of active override names. At the end of parsing, for every variable `VAR:name` where `name` is in `OVERRIDES`, the conditional value replaces `VAR` (3.3.1). Override names may use only lower-case letters, digits and dashes.

Scarthgap's default `OVERRIDES` (ref-manual `OVERRIDES`) contains `CLASSOVERRIDE` (`class-target`, `class-native`, `class-nativesdk`), `MACHINEOVERRIDES` (the `MACHINE` name plus SoC/family names the machine adds, e.g. `qemuall`), `DISTROOVERRIDES` (normally the `DISTRO` name), `pn-${PN}`, the `task-<name>` override inside a running task, and `forcevariable`. Check the real list with `bitbake-getvar -r <recipe> OVERRIDES`.

Priority: when several matching conditional values exist for one variable, BitBake uses the one whose override appears last (rightmost) in `OVERRIDES`. This is implementation behavior rather than an explicit manual sentence; prove it in a disputed case with `bitbake-getvar`. `forcevariable` is the strongest only because it is placed last in the default `OVERRIDES` (ref-manual `PREFERRED_VERSION` note).

### 3.2 Forms you will see

```bitbake
KBRANCH = "standard/base"
KBRANCH:qemuarm64 = "standard/qemuarm64"          # select: replaces KBRANCH when building for qemuarm64
SRC_URI:append:qemuall = " file://wired.config"   # conditional append for every QEMU machine
FOO:pn-myrecipe = "x"                             # in a .conf: affects only recipe myrecipe
DEPENDS:append:class-target = " libfoo"           # only the target variant of a BBCLASSEXTEND recipe
EXTRA_OEMAKE:prepend:task-compile = "${PARALLEL_MAKE} "   # only while do_compile runs
FILES:${PN}-tools = "${bindir}/foo-*"             # package-name "override" used by packaging variables
```

Write a real override name such as `VAR:qemuarm64` or `VAR:mymachine`, never a literal `VAR:machine` (unless `machine` is in your `OVERRIDES`).

### 3.3 Order of operators and overrides (3.3.3)

```bitbake
OVERRIDES = "foo"
A = "Z"
A:foo:append = "X"    # appends to the variable A:foo; A:foo then replaces A  -> A = "X"

A = "Z"
A:append:foo = "X"    # conditional append to A                               -> A = "ZX"
```

`VAR:foo:append` modifies the conditional variable `VAR:foo` (which then replaces `VAR` wholesale); `VAR:append:foo` appends to `VAR` only when `foo` is active. Reviewers should flag `:machine:append` style lines that silently discard the base value.

### 3.4 Key expansion (3.3.2)

Variable names containing `${...}` are expanded when the datastore is finalized: `A${B} = "X"` with `B = "2"` overwrites `A2`.

### 3.5 Variables that look like overrides but are not

Some variables take a suffix joined with `_`, and that underscore is part of the name, not override syntax. Converting them to `:` breaks them silently:

- `PREFERRED_PROVIDER_virtual/kernel`, `PREFERRED_PROVIDER_<item>` (ref-manual `PREFERRED_PROVIDER`)
- `PREFERRED_VERSION_<pn>` (ref-manual `PREFERRED_VERSION`)
- `LAYERSERIES_COMPAT_<collection>`, `LAYERDEPENDS_<collection>`, `BBFILE_PATTERN_<collection>`, `BBFILE_PRIORITY_<collection>`, `LAYERVERSION_<collection>`
- `SRCREV_<name>`, `SRC_URI[<name>.sha256sum]` (flag form)

You can still put an override after them: `PREFERRED_VERSION_linux-yocto:qemux86 = "6.6%"`.

### 3.6 History of the syntax

Before BitBake 1.52 (Yocto 3.4 "honister") overrides used `_` (`FILES_${PN}`, `do_install_append`). From 3.4 on, `:` is the separator and the old `_append`/`_prepend`/`_remove` forms are rejected with a parse error (BitBake manual 3.3.1 note; migration notes for 3.4, online at https://docs.yoctoproject.org/migration-guides/migration-3.4.html). Scarthgap layers must use `:`. OE-Core ships `scripts/contrib/convert-overrides.py` for mechanical conversion; review its output, because it cannot know which `_suffix` names (section 3.5) must keep the underscore.

## 4. Directives (BitBake manual 3.4)

- `inherit foo` (recipes and classes only): loads `classes*/foo.bbclass` from `BBPATH`. Values set after the `inherit` override the class. A variable expression is allowed (`inherit ${@'foo' if cond else ''}`), set before the line.
- `INHERIT += "foo"` (configuration files only): inherits the class globally, for every recipe (3.4.5). Distro-level defaults use `INHERIT_DISTRO` (scarthgap default `debian devshell sstate license remove-libtool create-spdx`).
- `include file.inc`: inserts the file; no error if it is missing (3.4.3).
- `require file.inc`: same, but a missing file is a parse error (3.4.4). Prefer `require` for files that must exist.
- `export VAR`: exports to the task environment; `bitbake-getvar` shows `export` before it (3.2).

## 5. Variable Flags, Functions, and Tasks (BitBake manual 3.5-3.7, 3.10)

- Flags: `VAR[flag] = "x"`; all operators except override-style ones work on flags (3.1.13).
- `addtask mytask after do_compile before do_install` creates a task; a task that nothing depends on runs only with `bitbake -c mytask` (3.6.1, 3.10.1).
- `deltask do_x` removes the task and does not reconnect its dependencies; use `do_x[noexec] = "1"` to keep the chain intact (3.6.2).
- Dependency flags: `[deptask]` (task of every `DEPENDS` item, e.g. `do_configure[deptask] = "do_populate_sysroot"`), `[rdeptask]` (task of every runtime dependency), `[recrdeptask]` (recursive, e.g. `do_rootfs[recrdeptask] += "do_packagedata"`), `[depends]` (`do_patch[depends] = "quilt-native:do_populate_sysroot"`), `[rdepends]`, `[mcdepends]` (multiconfig).
- Execution flags: `[dirs]` (last one is the cwd), `[cleandirs]`, `[nostamp]` (always rerun; everything depending on it reruns too), `[noexec]`, `[network]` (only `do_fetch` has network by default), `[lockfiles]`, `[prefuncs]`, `[postfuncs]`, `[umask]`.
- Signature flags: `[vardeps]`, `[vardepsexclude]`, `[vardepvalue]`, `[vardepvalueexclude]`, `[file-checksums]`. Use them when a task reads a variable in a way BitBake cannot see; the effect is visible with `bitbake-dumpsig` (see `debug-tools.md`).
- Anonymous Python `python () { ... }` runs at the end of parsing each recipe (3.5.5); keep it cheap and side-effect free.
- `BBCLASSEXTEND = "native nativesdk"` creates extra variants of the recipe (3.9); use `:class-native` / `:class-target` overrides for variant-specific values.

## 6. Source and Fetch

- `SRC_URI`: space-separated source URIs plus patches and local files. Common parameters: `protocol=https`, `branch=` (mandatory for git URIs unless `nobranch=1`, BitBake manual "Git Fetcher"), `name=`, `subdir=`, `destsuffix=`, `apply=yes|no`, `striplevel=`. Archives need `SRC_URI[sha256sum]` (or `SRC_URI[<name>.sha256sum]`).
- `SRCREV`: fixed commit for SCM fetches; `SRCREV_<name>` per named URI, combined by `SRCREV_FORMAT`. `${AUTOREV}` follows the branch head and forces a network lookup at parse time: fine for development, not reproducible.
- `S`: where tasks find the unpacked source; default `${WORKDIR}/${BPN}-${PV}`. In scarthgap git sources are unpacked to `${WORKDIR}/git`, so git recipes set `S = "${WORKDIR}/git"`. Release note: from 5.1 "styhead" sources are unpacked into `UNPACKDIR` and git recipes use `S = "${UNPACKDIR}/git"`; do not use that form on scarthgap.
- `B`: build directory (out-of-tree for autotools/cmake/meson by default). `WORKDIR`: `${TMPDIR}/work/${MULTIMACH_TARGET_SYS}/${PN}/${EXTENDPE}${PV}-${PR}`. `D`: install destination used by `do_install`.
- `FILESEXTRAPATHS:prepend := "${THISDIR}/files:"` in a bbappend adds a search directory for `file://` entries; the `:=` matters because `THISDIR` changes per file.
- `DL_DIR`, `PREMIRRORS`, `MIRRORS`, `BB_NO_NETWORK`, `BB_GENERATE_MIRROR_TARBALLS`: download cache and mirror policy.

## 7. Dependencies and Providers

- `DEPENDS`: build-time, recipe namespace. Each item's `do_populate_sysroot` must finish before this recipe's `do_configure`, and its output is staged into `recipe-sysroot` / `recipe-sysroot-native`. Host tools must be `foo-native`. It installs nothing into an image. `DEPENDS:${PN}` is wrong and caught by `pkgvarcheck`.
- `RDEPENDS:<pkg>`: runtime, package namespace (package names, not recipe names). Shared-library and some file dependencies are added automatically at packaging time; explicit entries are still needed for scripts, `dlopen()` modules and tools called at runtime (`file-rdeps`, `build-deps` QA).
- `RRECOMMENDS:<pkg>`: soft dependency; can be suppressed by `BAD_RECOMMENDATIONS` or `NO_RECOMMENDATIONS`. `RSUGGESTS`, `RPROVIDES`, `RCONFLICTS`, `RREPLACES`: package-manager relationships. Do not put `virtual/` names in `RDEPENDS`/`RPROVIDES` (`virtual-slash` warning in 5.0); use `VIRTUAL-RUNTIME_<name>` variables instead.
- `PROVIDES`: extra build-time names (often `virtual/...`). `PREFERRED_PROVIDER_<item> = "<pn>"` chooses between providers; for a `virtual/*` item, the providers that are not selected are prevented from building.
- `PREFERRED_VERSION_<pn> = "1.2%"`: matched against `PV` (not the file name); `%` is allowed only at the end. A missing version is a warning unless `REQUIRED_VERSION` is used.
- `ASSUME_PROVIDED`: names BitBake must not build because the host supplies them.
- `BBCLASSEXTEND`: native/nativesdk/multilib variants.

## 8. Packaging

- `PACKAGES` default: `${PN}-src ${PN}-dbg ${PN}-staticdev ${PN}-dev ${PN}-doc ${PN}-locale ${PACKAGE_BEFORE_PN} ${PN}`. `do_package` walks this list left to right and each file goes to the first (leftmost) package whose `FILES:<pkg>` matches. A file can be in only one package (ref-manual `PACKAGES`; overview-manual "Package Splitting").
- Consequence: adding a path to `FILES:${PN}` does nothing if `${PN}-dev` or `${PN}-dbg` already matches it, because those come first. To move files out of the main package into a new one, add the package with `PACKAGE_BEFORE_PN` or `PACKAGES =+ "${PN}-tools"`, so it is left of `${PN}`.
- `FILES:<pkg>`: globs (Python glob syntax), use path variables (`${bindir}`, `${libdir}`, `${sysconfdir}`, `${datadir}`, `${systemd_system_unitdir}`). Defaults live in `meta/conf/bitbake.conf`. `${PN}-dev` gets headers, `.pc` files and `FILES_SOLIBSDEV` (`${base_libdir}/lib*${SOLIBSDEV} ${libdir}/lib*${SOLIBSDEV}`, i.e. unversioned `lib*.so`); `${PN}` gets `${libdir}/lib*${SOLIBS}` (versioned `.so.*`), `${bindir}/*`, `${sysconfdir}` and more.
- Unversioned library (no SONAME version) used at runtime: set `SOLIBS = ".so"` and `FILES_SOLIBSDEV = ""` so the `.so` goes to `${PN}` (dev-manual "Non-Versioned Libraries" 15.3). A real fix upstream (setting a SONAME) is better when possible.
- Empty packages are not created unless `ALLOW_EMPTY:<pkg> = "1"`.
- `CONFFILES:<pkg>`: files the package manager must not overwrite on upgrade.
- `PACKAGE_ARCH`: `${MACHINE_ARCH}` for machine-specific packages, `inherit allarch` for architecture-independent ones.
- `PACKAGES_DYNAMIC`: regex of package names created at packaging time (for example by `do_split_packages`).
- `PRIVATE_LIBS`: libraries that must not be registered as shlib providers (fixes the untagged "was registered as shlib provider ... changing it" message).
- `INSANE_SKIP:<pkg> += "<check>"`: package-scoped QA skip; always with a comment stating why (see `qa-errors.md`).
- Scriptlets: `pkg_postinst:<pkg>()`, `pkg_postinst_ontarget:<pkg>()`, `pkg_preinst`, `pkg_prerm`, `pkg_postrm`; tools they need at rootfs time go in `PACKAGE_WRITE_DEPS`.

## 9. Images and Features

- `IMAGE_INSTALL`: runtime package names for an image. `core-image` sets its default with `?=`, and `local.conf` is parsed before any recipe. So `IMAGE_INSTALL += "pkg"` in `local.conf` creates the variable first, the class's `?=` default is then skipped, and the image loses its base packages (ref-manual `IMAGE_INSTALL` note; dev-manual "Customizing Images Using local.conf" 4.1). Use `IMAGE_INSTALL:append = " pkg"` (leading space), or `IMAGE_INSTALL:append:pn-core-image-minimal = " pkg"` for one image. In your own image recipe write the full list with `IMAGE_INSTALL = "..."`, or `:append` to an inherited default; the manual warns that `+=` in an image recipe "may or may not succeed".
- `CORE_IMAGE_EXTRA_INSTALL`: extra packages for `core-image-*` images only.
- `IMAGE_FEATURES` (image recipe) and `EXTRA_IMAGE_FEATURES` (local.conf; added to `IMAGE_FEATURES` in `bitbake.conf`): named features, most mapping to package groups (`ssh-server-openssh`, `tools-debug`, `dev-pkgs`, `package-management`, `read-only-rootfs`). Names are listed in ref-manual "Image Features".
- `IMAGE_FSTYPES`: output types (`ext4`, `tar.bz2`, `wic`, `wic.gz`, `squashfs`, `cpio.gz`, `live`, `container`...). `IMAGE_ROOTFS`, `ROOTFS_POSTPROCESS_COMMAND`, `IMAGE_PREPROCESS_COMMAND`, `IMAGE_POSTPROCESS_COMMAND`: image construction hooks.
- `PACKAGE_CLASSES`: package backends; the first one is used to build images.
- `DISTRO_FEATURES`: distro policy (`systemd`, `x11`, `wayland`, `pam`, `usrmerge`, `ptest`...). `MACHINE_FEATURES`: hardware capabilities. `COMBINED_FEATURES`: features in both. `DISTRO_FEATURES_BACKFILL` / `DISTRO_FEATURES_BACKFILL_CONSIDERED`: features added automatically unless opted out.
- `PACKAGECONFIG`: per-recipe feature switches. Each `PACKAGECONFIG[name] = "enable-flag,disable-flag,build-deps,runtime-deps,runtime-recommends,conflicts"`; defaults often derive from `DISTRO_FEATURES`. Change from outside with `PACKAGECONFIG:append:pn-foo = " name"` or in a bbappend. Unknown names trigger `invalid-packageconfig`.

## 10. Layers and Metadata Visibility

- `BBLAYERS` (in `conf/bblayers.conf`): enabled layers. `BBPATH`: search path for classes, `.conf` and includes.
- `BBFILES`: globs for `.bb` and `.bbappend`; `BBFILE_COLLECTIONS`, `BBFILE_PATTERN_<col>` (regex matching files of the layer), `BBFILE_PRIORITY_<col>` (higher wins when the same recipe exists in several layers; it also orders bbappend application).
- `BBFILES_DYNAMIC`: `<collection>:<glob>` entries activated only when that collection is present.
- `LAYERSERIES_COMPAT_<col>`: release names the layer is tested with, e.g. `"scarthgap"`. A layer not listing the current core series is refused at parse time.
- `LAYERDEPENDS_<col>`, `LAYERRECOMMENDS_<col>`, `LAYERVERSION_<col>`.
- `BBMASK`: regex of files to ignore (masking a recipe also hides its appends).
- `BB_DANGLINGAPPENDS_WARNONLY`: by default a `.bbappend` with no matching recipe is a fatal parse error ("No recipes available for"); setting this to `1` downgrades it to a warning.

## 11. Machine, Distro, Kernel, and Boot

- `MACHINE`, `DISTRO`, `DISTRO_VERSION`, `TUNE_FEATURES`, `DEFAULTTUNE`, `MACHINEOVERRIDES`, `DISTROOVERRIDES`.
- `INIT_MANAGER`: `sysvinit` (Poky default), `systemd` or `mdev-busybox`; it includes `conf/distro/include/init-manager-${INIT_MANAGER}.inc` (ref-manual `INIT_MANAGER`; dev-manual "Selecting an Initialization Manager"). `VIRTUAL-RUNTIME_*` variables select runtime providers (init manager, login manager, device manager) without `virtual/`.
- `PREFERRED_PROVIDER_virtual/kernel`, `PREFERRED_VERSION_linux-yocto`, `KERNEL_IMAGETYPE`, `KERNEL_DEVICETREE`, `KERNEL_FEATURES`, `KBUILD_DEFCONFIG`, `KMACHINE`, `LINUX_KERNEL_TYPE`, `KERNEL_MODULE_AUTOLOAD`, `KERNEL_CLASSES`, `COMPATIBLE_MACHINE`; `PREFERRED_PROVIDER_virtual/bootloader`, `UBOOT_MACHINE`, `UBOOT_CONFIG`, `UBOOT_BINARY`. Details in `bsp-kernel.md`.

## 12. Runtime Integration

- systemd class: `SYSTEMD_PACKAGES` (default `${PN}`), `SYSTEMD_SERVICE:<pkg>`, `SYSTEMD_AUTO_ENABLE:<pkg>` (`??= "enable"`). Does nothing unless `systemd` is in `DISTRO_FEATURES`. The class adds the listed units to the package itself; you do not need `FILES:${PN} += "${systemd_system_unitdir}/foo.service"` unless the unit is installed to a non-standard path.
- update-rc.d class: `INITSCRIPT_PACKAGES`, `INITSCRIPT_NAME`, `INITSCRIPT_PARAMS`.
- update-alternatives class: `ALTERNATIVE:<pkg>`, `ALTERNATIVE_LINK_NAME[name]`, `ALTERNATIVE_TARGET[name]`, `ALTERNATIVE_PRIORITY`.
- useradd class: `USERADD_PACKAGES`, `USERADD_PARAM:<pkg>`, `GROUPADD_PARAM:<pkg>`, `GROUPMEMS_PARAM:<pkg>`.
- features_check class: `REQUIRED_DISTRO_FEATURES`, `CONFLICT_DISTRO_FEATURES`, `ANY_OF_DISTRO_FEATURES` (and `_MACHINE_` / `_COMBINED_` variants).

Derived from the Yocto Project scarthgap (5.0) documentation, CC BY-SA 2.0 UK.
