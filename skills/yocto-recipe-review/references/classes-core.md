<!-- Generated from references/bitbake/classes-core.md by tools/sync_references.py. Edit the source file, not this copy. -->

# Core Yocto Classes (Scarthgap)

Release: Yocto Project 5.0 "scarthgap". Source: ref-manual "Classes" (chapter 5; section numbers below). Every class named here exists in the scarthgap Classes chapter unless marked otherwise. Verbatim entries: `yocto-manuals` skill, `references/classes/<name>.md`.

How classes arrive: `inherit foo` in a recipe or class; `INHERIT += "foo"` in a `.conf` (global); `INHERIT_DISTRO` for distro defaults (scarthgap: `debian devshell sstate license remove-libtool create-spdx`); `USER_CLASSES` in `local.conf` (default includes `buildstats`). Every recipe inherits `base` (which pulls `utility-tasks`, `utils`, `patch`, `staging`, ...) and `package`. Check what a recipe really inherits: the top of `bitbake -e <recipe>` lists every included and inherited file.

Rule for reviews: a class variable without the class is dead metadata (e.g. `SYSTEMD_SERVICE` without `inherit systemd`, `ALTERNATIVE` without `update-alternatives`, which triggers `missing-update-alternatives`; `REQUIRED_DISTRO_FEATURES` without `features_check`, which triggers `unhandled-features-check`).

## 1. Build-System Classes

- **`autotools`** (5.3): GNU Autotools. `do_configure` runs `autoreconf` then `configure` with cross arguments plus `EXTRA_OECONF` and `PACKAGECONFIG_CONFARGS`; `do_compile` runs `make` with `EXTRA_OEMAKE`; `do_install` runs `make install DESTDIR=${D}`. Builds out of tree (`B != S`); use `autotools-brokensep` only when upstream cannot build out of tree. Unknown configure options trigger `unknown-configure-option`.
- **`cmake`** (5.18): passes `EXTRA_OECMAKE`; uses Ninja by default (`OECMAKE_GENERATOR = "Unix Makefiles"` to switch); custom CMake modules go to `${D}${datadir}/cmake/modules/`.
- **`cmake-qemu`** (5.19): like `cmake` plus `CMAKE_CROSSCOMPILING_EMULATOR` so cross-built binaries (for example CTest unit tests) run under QEMU user mode. Only works for machines with `qemu-usermode` in `MACHINE_FEATURES`.
- **`meson`** (5.78): Meson builds; options via `EXTRA_OEMESON` and `PACKAGECONFIG`.
- **`scons`** (5.135), **`waf`** (5.167): SCons and Waf builds (`EXTRA_OESCONS`; Waf takes `EXTRA_OECONF`).
- **`bin_package`** (5.6): repackages prebuilt binaries: disables `do_configure`/`do_compile` and copies `${S}` into `${D}` (use `subdir=${BP}` on archives without a top directory).
- **`pkgconfig`** (5.112): adds `pkgconfig-native` to `DEPENDS`; inherit it instead of depending on host `pkg-config`.
- **`gettext`** (5.42): gettext support; required when `AM_GNU_GETTEXT` is used (`configure-gettext`).
- **`externalsrc`** (5.36): builds from a tree outside the build system (`EXTERNALSRC`, `EXTERNALSRC_BUILD`); fetch, unpack and patch are skipped. `devtool modify` uses it in the workspace layer.
- **`allarch`** (5.1): for recipes whose packages are architecture independent (scripts, data). Do not use for packages that depend on tune-specific packages.

## 2. Language Ecosystems

- **`cargo`** (5.12): Rust via Cargo; crates listed in `SRC_URI` (often in a generated `${BPN}-crates.inc`). **`cargo-update-recipe-crates`** (5.15): `bitbake -c update_crates <recipe>` regenerates that list from `Cargo.lock`. **`cargo_c`** (5.13): Rust libraries with a C ABI. **`cargo_common`** (5.14) is internal. **`ptest-cargo`** (5.119): Cargo tests into `${PN}-ptest`.
- **`go`**, **`go-mod`**, **`go-vendor`** (5.45-5.47): Go builds; `GO_IMPORT` (mandatory) names the import path, `GO_INSTALL` selects what to build; module dependencies must be fetched, not downloaded at compile time (network is only allowed in `do_fetch`).
- **`npm`** (5.90): Node.js packages; recipes must use the `npm://` fetcher so dependencies are fetched and packaged (dev-manual "Creating Node Package Manager (NPM) Packages").
- Python: **`setuptools3`** (5.138, builds a wheel with `setup.py bdist_wheel`), **`setuptools3_legacy`** (5.139, old `setup.py build/install`), **`python_setuptools_build_meta`** (5.137), **`python_pep517`** (5.107, generic PEP 517 wheel build and install), **`python_flit_core`**, **`python_poetry_core`**, **`python_maturin`**, **`python_mesonpy`**, **`python_pyo3`**, **`python-setuptools3_rust`**, plus **`pypi`** (sets `SRC_URI` from PyPI) and **`python3native`** / **`python3targetconfig`**. `python_pdm` is not documented in the scarthgap Classes chapter; do not recommend it for scarthgap.
- Perl: **`cpan`** (`Makefile.PL`) and **`cpan_build`** (`Build.PL`) (5.25).

## 3. Runtime Integration

- **`systemd`** (5.147): disabled unless `systemd` is in `DISTRO_FEATURES`. Units installed to `${D}${systemd_unitdir}/system` (`${systemd_system_unitdir}`); list them in `SYSTEMD_SERVICE:<pkg>`; units outside the main package need `SYSTEMD_PACKAGES` (default `${PN}`). Services are enabled at boot unless `SYSTEMD_AUTO_ENABLE:<pkg> = "disable"`. The class packages the listed units itself.
- **`update-rc.d`** (5.161): installs SysV init scripts with `update-rc.d`, stopping before removal and starting after install. Variables `INITSCRIPT_PACKAGES`, `INITSCRIPT_NAME`, `INITSCRIPT_PARAMS`. A recipe supporting both init systems can inherit both `systemd` and `update-rc.d`.
- **`update-alternatives`** (5.160): lets several packages provide the same path (`ar` from busybox, binutils, elfutils). `ALTERNATIVE:<pkg> = "name"`, `ALTERNATIVE_LINK_NAME[name] = "${bindir}/name"`, `ALTERNATIVE_TARGET[name]`, `ALTERNATIVE_PRIORITY` (highest wins).
- **`useradd`** (5.162): creates users and groups at package install time. `USERADD_PACKAGES = "${PN}"`, `USERADD_PARAM:${PN} = "--system --no-create-home myuser"`, `GROUPADD_PARAM:${PN}`, `GROUPMEMS_PARAM:${PN}`. UIDs are dynamic unless `useradd-staticids` is enabled through `USERADDEXTENSION` with `USERADD_UID_TABLES`/`USERADD_GID_TABLES`. Do not `chown` to names the class has not created.
- **`extrausers`** (5.37): image-level user changes via `EXTRA_USERS_PARAMS`; avoid hardcoded passwords in production images.
- **`features_check`** (5.38): skips the recipe (and errors if something needs it) when `REQUIRED_DISTRO_FEATURES`, `CONFLICT_DISTRO_FEATURES`, `ANY_OF_DISTRO_FEATURES` (and `_MACHINE_`, `_COMBINED_` variants) are not met.
- **`mime`**, **`mime-xdg`**, **`gtk-icon-cache`**, **`fontcache`**, **`gsettings`**, **`pixbufcache`**: update desktop caches at install time; QA `mime` and `mime-xdg` catch missing inherits.

## 4. Kernel, BSP, Bootloader

- **`kernel`** (5.62): builds Linux; stages headers in `STAGING_KERNEL_DIR` for out-of-tree modules; a `defconfig` in `SRC_URI` is copied to `.config` unless `.config` already exists; each module is its own package (`kernel-module-<name>`), `kernel-modules` pulls all. Inherits `kernel-devicetree` and `kernel-arch`.
- **`kernel-yocto`** (5.70): linux-yocto style trees: kernel metadata (`.scc`), `KERNEL_FEATURES`, `KMACHINE`, `KBRANCH`, `LINUX_KERNEL_TYPE`, config fragments (`.cfg` in `SRC_URI`), `KBUILD_DEFCONFIG`, `KCONFIG_MODE`, and the `kernel_checkout`, `validate_branches`, `kernel_metadata`, `kernel_configme`, `kernel_configcheck` tasks. A vendor kernel that only inherits `kernel` lacks these.
- **`kernel-devicetree`** (5.64): builds and installs the DTBs named in `KERNEL_DEVICETREE`; `KERNEL_DTBVENDORED` (default false) controls vendor subdirectories, `KERNEL_DTBDEST`, `KERNEL_DEVICETREE_BUNDLE`, `KERNEL_DTC_FLAGS`.
- **`kernel-fitimage`** (5.65): packs kernel, DTBs, optional U-Boot script, initramfs bundle or ramdisk into a FIT image. Enable with `KERNEL_CLASSES += "kernel-fitimage"` and `fitImage` in `KERNEL_IMAGETYPE`/`KERNEL_IMAGETYPES`. Load addresses: `UBOOT_LOADADDRESS`, `UBOOT_ENTRYPOINT`, `UBOOT_DTB_LOADADDRESS`, `UBOOT_RD_LOADADDRESS`; signing with `UBOOT_SIGN_ENABLE`, `UBOOT_SIGN_KEYDIR`, `UBOOT_SIGN_KEYNAME`, `UBOOT_MKIMAGE_DTCOPTS` (defaults `FIT_HASH_ALG = "sha256"`, `FIT_SIGN_ALG = "rsa2048"`). The class name in scarthgap is `kernel-fitimage`; there is no `kernel-fit-image` class in this release.
- **`kernel-module-split`** (5.67): splits modules into packages. **`module`** (5.84): out-of-tree kernel modules (`inherit module`).
- **`kernel-uimage`**, **`kernel-uboot`**, **`kernel-grub`**: uImage/vmlinux-style packaging.
- **`devicetree`** (5.33): compiles device trees outside the kernel tree (`DT_FILES_PATH`, `DT_FILES`, `DT_PADDING_SIZE`), handles overlays, deploys to `${DEPLOY_DIR_IMAGE}/devicetree/`, needs `COMPATIBLE_MACHINE`.
- **`uboot-config`** (5.157): `UBOOT_MACHINE` or `UBOOT_CONFIG ??= "<default>"` with `UBOOT_CONFIG[name] = "config,images,binary"` for several U-Boot builds.
- **`uboot-sign`** (5.158): U-Boot verified boot (`UBOOT_FITIMAGE_ENABLE`, `SPL_SIGN_ENABLE`, `SPL_SIGN_KEYDIR`, `UBOOT_FIT_*`); mirrors `kernel-fitimage`.
- **`deploy`** (5.32): makes `do_deploy` an sstate task: write to `${DEPLOYDIR}`, add with `addtask deploy after do_compile` (or `do_install`); the class copies to `DEPLOY_DIR_IMAGE`.

## 5. Image and Packaging

- **`image`** (5.56): image recipes. Builds the rootfs with `rootfs_<pkgtype>` from `IMAGE_INSTALL`, then image files for `IMAGE_FSTYPES`; also pulls `image_types`, `image_types_wic`, `rootfs-postcommands`, `populate_sdk_base` and (when the fstypes ask for it) `image-live` / `image-container`.
- **`core-image`** (5.24): base for `core-image-*` recipes; adds support for extra `IMAGE_FEATURES` (`ssh-server-openssh`, `tools-debug`, `x11-base`...) and honors `CORE_IMAGE_EXTRA_INSTALL`.
- **`image_types`** (5.58): implementation of every `IMAGE_FSTYPES` type and the compression suffixes (`.gz`, `.xz`, `.zst`, `wic.vmdk`, `wic.qcow2`...).
- **`image-live`** (5.60): live HDDIMG/ISO via `IMAGE_FSTYPES += "live"`. **`image-container`** (5.59): OCI-ready tarball for `container` fstype; requires `PREFERRED_PROVIDER_virtual/kernel = "linux-dummy"` (or `IMAGE_CONTAINER_NO_DUMMY = "1"`). **`image-buildinfo`** (5.57): writes `/etc/buildinfo`.
- **`packagegroup`** (5.100): sets `PACKAGES`, `PACKAGE_ARCH`, `ALLOW_EMPTY` for package-group recipes; if you need `PACKAGE_ARCH = "${MACHINE_ARCH}"`, set it before `inherit packagegroup`.
- **`package`** (5.95) with **`package_ipk`**, **`package_rpm`**, **`package_deb`**: package writing; the first entry of `PACKAGE_CLASSES` is used for images. **`packagedata`** (5.99): reads pkgdata.
- **`rootfs*`** (5.131): rootfs construction per backend plus `rootfs-postcommands`.
- **`insane`** (5.61): QA checks, controlled by `ERROR_QA`, `WARN_QA`, `INSANE_SKIP`; see `qa-errors.md`.
- **`lib_package`** (5.72): puts a library recipe's executables into `${PN}-bin`.
- **`debian`** (5.31): renames library packages Debian-style (`libc6`); `LEAD_SONAME`. Inherited through `INHERIT_DISTRO`, which is why package names may differ from recipe names.
- **`overlayfs`** (5.92), **`overlayfs-etc`** (5.93): writable overlays on a read-only rootfs.

## 6. Build Infrastructure and Debugging

- **`sstate`** (5.144): shared state; enabled via `INHERIT_DISTRO`.
- **`staging`** (5.145): `do_populate_sysroot` and `do_prepare_recipe_sysroot`; recipes must install into `${D}`, never into sysroots directly.
- **`buildhistory`** (5.9): records package, image and SDK contents in a git repository at `BUILDHISTORY_DIR` (default `${TOPDIR}/buildhistory`). Enable with `INHERIT += "buildhistory"` and `BUILDHISTORY_COMMIT = "1"`; compare builds with `buildhistory-diff`. Required for `version-going-backwards`.
- **`buildstats`** (5.10): per-task timing in `${TMPDIR}/buildstats/`; on by default via `USER_CLASSES`.
- **`rm_work`** (5.130): deletes `WORKDIR` after a recipe finishes; exclude recipes under investigation with `RM_WORK_EXCLUDE += "<pn>"`. With it enabled, `packages-split/` and logs other than `temp/` disappear.
- **`ccache`** (5.16): "not recommended". **`devshell`** (5.34): the interactive `do_devshell` task.
- **`native`** (5.87) / **`nativesdk`** (5.88): host and SDK variants. Prefer `BBCLASSEXTEND = "native nativesdk"` over separate recipes; a hand-written `foo-native.bb` must inherit `native` last.
- **`ptest`** (5.118): packages upstream tests in `${PN}-ptest`; largely disabled unless `ptest` is in `DISTRO_FEATURES`. In 5.0, runtime ptest fails if a ptest returns no results (migration-5.0 "Recipe changes"). **`ptest-gnome`** (5.120) for `gnome-desktop-testing`.
- **`testimage`** (5.151), **`testsdk`** (5.152): runtime image and SDK tests.
- **`populate_sdk`** (5.113) / **`populate_sdk_ext`**: `bitbake -c populate_sdk <image>` and `-c populate_sdk_ext`.

## 7. License, Security, SBOM, Source Archiving

- **`license`** (5.74): license manifests and license exclusion (`INCOMPATIBLE_LICENSE`, `LICENSE_FLAGS`); enabled by default via `INHERIT_DISTRO`.
- **`create-spdx`** (5.26): SPDX 2.2 SBOM, enabled by default in scarthgap via `INHERIT_DISTRO`. Top-level `IMAGE-MACHINE.spdx.json` in `tmp/deploy/images/MACHINE/`, the rest in `tmp/deploy/spdx`. Tuned by `SPDX_PRETTY`, `SPDX_ARCHIVE_PACKAGED`, `SPDX_ARCHIVE_SOURCES`, `SPDX_INCLUDE_SOURCES`. SPDX 3.0 output is available but off by default: `INHERIT_DISTRO:remove = "create-spdx"` plus `INHERIT_DISTRO:append = " create-spdx-3.0"` (dev-manual "Creating a Software Bill of Materials"). `create-spdx-3.0` has no own entry in the scarthgap Classes chapter.
- **`cve-check`** (5.30): `INHERIT += "cve-check"`; per-recipe reports in `tmp/deploy/cve`, image summaries as JSON in `tmp/deploy/images`; statuses `Patched`, `Unpatched`, `Ignored`. Tune with `CVE_PRODUCT`, `CVE_VERSION`, `CVE_STATUS[CVE-ID] = "reason: text"` (replaces the deprecated `CVE_CHECK_IGNORE` in 5.0), `CVE_STATUS_GROUPS`, `CVE_CHECK_SKIP_RECIPE`; `include conf/distro/include/cve-extra-exclusions.inc` drops known-irrelevant entries. Run for one recipe: `bitbake -c cve_check <recipe>`.
- **`vex`** (5.166): alternative to `cve-check`: `INHERIT += "vex"` adds a `generate_vex` task per recipe and writes VEX data for external scanners; reports land in `DEPLOY_DIR_IMAGE` for images. It reuses the `CVE_CHECK_*` variables.
- **`archiver`** (5.2): source release for compliance; `ARCHIVER_MODE[src] = "original" | "patched" | "configured"`, `ARCHIVER_MODE[diff]`, `ARCHIVER_MODE[recipe]`, `ARCHIVER_MODE[srpm]`; filter with `COPYLEFT_LICENSE_INCLUDE` / `COPYLEFT_LICENSE_EXCLUDE`. Output in `tmp/deploy/sources` (dev-manual "Providing the Source Code" 33.3.1).
- **`copyleft_compliance`** (5.22): older alternative to `archiver`, deprecated in favor of it.
- **`copyleft_filter`** (5.23): internal class used by `archiver` and `copyleft_compliance`; not meant to be inherited directly.

Derived from the Yocto Project scarthgap (5.0) documentation, CC BY-SA 2.0 UK.
