# Yocto Image and Rootfs Reference

Release: Yocto Project 5.0 "scarthgap". Sources: dev-manual "Customizing Images" (4), "Writing a New Recipe > Post-Installation Scripts" (5.19), "Debugging > oe-pkgdata-util" (32.3), "Creating Partitioned Images Using Wic" (19), "Building > Multiple Configurations" (12.2); ref-manual "Image Features" (11.3), "Classes" (`image`, `core-image`, `packagegroup`, `rootfs*`), "Tasks" (6.3), variables `IMAGE_INSTALL`, `BAD_RECOMMENDATIONS`, `NO_RECOMMENDATIONS`, `PACKAGE_EXCLUDE`.

For "what is in my built image and why" or "what did this change do to the image" (buildhistory diffs, distro configuration analysis), the separate `yocto-image-analysis` skill is the better fit.

## 1. Mental Model

- Recipes build packages; images install packages. `IMAGE_INSTALL` takes package names, which often differ from recipe names (`${PN}-utils`, `lib_package`'s `${PN}-bin`, `debian`-class renames like `libc6`).
- `DEPENDS` in an image recipe only builds things; it never installs anything into the rootfs.
- Package groups are recipes (`inherit packagegroup`) whose packages are empty and pull others through `RDEPENDS`/`RRECOMMENDS`.
- `do_rootfs` uses the package manager of the first `PACKAGE_CLASSES` entry (`package_rpm` -> dnf, `package_ipk` -> opkg, `package_deb` -> apt) against the packages already written to `tmp/deploy/{rpm,ipk,deb}`. Then `ROOTFS_POSTPROCESS_COMMAND`, then `do_image` and one `do_image_<type>` per `IMAGE_FSTYPES` entry, then `do_image_complete` (ref-manual 6.1.8-6.1.9, 6.3).

## 2. Adding Packages Correctly

| Where | Do | Why |
| --- | --- | --- |
| `local.conf` / `auto.conf` | `IMAGE_INSTALL:append = " strace"` | `.conf` files are parsed before recipes; `core-image` sets `IMAGE_INSTALL ?=`. A `+=` in `local.conf` creates the variable first, so the class default is skipped and the image loses its base packages (ref-manual `IMAGE_INSTALL` note). `:append` is applied after everything else. The leading space is required. |
| one image only | `IMAGE_INSTALL:append:pn-core-image-minimal = " strace"` | `pn-<image>` override (dev-manual 4.1). |
| `core-image-*` only | `CORE_IMAGE_EXTRA_INSTALL += "strace"` | Read by `core-image` only. |
| your image recipe | `IMAGE_INSTALL = "packagegroup-core-boot packagegroup-base-extended myapp"` then `inherit core-image` (or `:append` to an inherited list) | The manual warns that `+=` in an image recipe "may or may not succeed" depending on ordering. |
| a set of packages | a packagegroup recipe, listed in `IMAGE_INSTALL` | Reusable and reviewable. |

Prove the result with `bitbake-getvar -r <image> IMAGE_INSTALL`, which shows the history of each assignment.

## 3. Image Features

`IMAGE_FEATURES` belongs in image recipes; `EXTRA_IMAGE_FEATURES` belongs in `local.conf`. `bitbake.conf` adds `EXTRA_IMAGE_FEATURES` to `IMAGE_FEATURES` (dev-manual 4.2), so an image recipe that hard-sets `IMAGE_FEATURES = "..."` can still pick up local extras, or not, depending on evaluation order; check with `bitbake-getvar -r <image> IMAGE_FEATURES` instead of assuming. Most features map to package groups in `image.bbclass`/`core-image.bbclass`; some are configuration switches. Scarthgap image features (ref-manual 11.3):

| Feature | Effect |
| --- | --- |
| `ssh-server-openssh` / `ssh-server-dropbear` | Install that SSH server (OpenSSH wins if both are set). |
| `package-management` | Keep package manager tools and database on target. |
| `tools-debug` / `tools-profile` / `perf` / `tools-sdk` / `tools-testapps` | gdb/strace; profiling tools; perf/systemtap/LTTng; on-target SDK; test tools. |
| `dev-pkgs` / `dbg-pkgs` / `staticdev-pkgs` / `doc-pkgs` / `lic-pkgs` / `ptest-pkgs` | Add the `-dev`, `-dbg`, `-staticdev`, `-doc`, `-lic`, `-ptest` package of every installed package. |
| `debug-tweaks` | Development only: `allow-empty-password`, `allow-root-login`, `empty-root-password`, `post-install-logging`. Never in production. |
| `allow-empty-password`, `allow-root-login`, `empty-root-password`, `serial-autologin-root` | Login relaxations; without `empty-root-password`/`debug-tweaks` a non-empty root password is forced. |
| `read-only-rootfs` (+ `read-only-rootfs-delayed-postinsts`) | Read-only rootfs; postinsts must run at build time unless the delayed variant is set. |
| `overlayfs-etc`, `stateless-rootfs` | `/etc` on overlayfs; image left for systemd to populate at runtime. |
| `post-install-logging` | Log first-boot postinsts to `/var/log/postinstall.log`. |
| `splash`, `hwcodecs`, `nfs-server`, `x11`, `x11-base`, `x11-sato`, `weston` | Splash screen, codecs, NFS server, graphics stacks. |

Many graphics or service features also need the matching `DISTRO_FEATURES` (`x11`, `wayland`, `systemd`); a feature that installs nothing usually means the distro feature or a layer is missing.

## 4. Excluding Packages

| Variable | Scope | Backends | Behavior |
| --- | --- | --- | --- |
| `BAD_RECOMMENDATIONS` | listed packages pulled only by `RRECOMMENDS` | ipk, rpm (not deb) | Ignored when something `RDEPENDS` on the package. |
| `NO_RECOMMENDATIONS = "1"` | all recommend-only packages | ipk, rpm (not deb) | Same; may drop things you need (kernel modules), add them explicitly. |
| `PACKAGE_EXCLUDE` | listed packages | rpm, deb, ipk | Fatal install error if something `RDEPENDS` on them: use it to find who pulls a package in. |

Scope any of them to one image with `:pn-<image>`.

## 5. Post-Installation Scripts (dev-manual 5.19)

- `pkg_postinst:<pkg>()` runs when the package is installed: during `do_rootfs` (offline, against `$D`, on the build host) or on the target for runtime installs. The script must work in both contexts: use `$D` prefixes and no target-only commands. Any failure (non-zero exit) fails `do_rootfs`.
- To defer to first boot use `pkg_postinst_ontarget:<pkg>()` or call `postinst_intercept delay_to_first_boot` from `pkg_postinst`. Deferred scripts are impossible on a read-only rootfs (unless `read-only-rootfs-delayed-postinsts`).
- Native tools a postinst needs at rootfs time go in `PACKAGE_WRITE_DEPS`; otherwise the script may be deferred to first boot silently.
- `pkg_preinst`, `pkg_prerm`, `pkg_postrm` work the same but do not run at image creation.
- "Works on the target but fails in do_rootfs" is almost always a script that assumes it runs on the device.

## 6. Rootfs Debug Flow

1. Read `tmp/work/<machine>-*/<image>/*/temp/log.do_rootfs` from the first error (the package manager output is there).
2. Classify: "nothing provides X" / "Unable to find package X" (name), conflict / file clash (`RCONFLICTS`, two packages owning one path), postinst failure (section 5), license exclusion (`INCOMPATIBLE_LICENSE`, `LICENSE_FLAGS_ACCEPTED`).
3. For a missing name, check whether it is a package: `oe-pkgdata-util list-pkgs '<name>*'`. `oe-pkgdata-util` only sees packages that have been built (it reads `PKGDATA_DIR`), so build the recipe first: `bitbake <recipe>`.
4. Map package to recipe and back: `oe-pkgdata-util lookup-recipe <pkg>`, `oe-pkgdata-util list-pkg-files -p <pkg>`, `oe-pkgdata-util find-path /usr/bin/<tool>`.
5. If the recipe exists but emits no such package: inspect `PACKAGES` and `FILES:*` (`bitbake-getvar -r <recipe> PACKAGES`) and `${WORKDIR}/packages-split/` (needs `rm_work` disabled). Empty packages are not created unless `ALLOW_EMPTY`.
6. Check who requires it: `PACKAGE_EXCLUDE:pn-<image> = "<pkg>"` turns hidden pulls into an explicit error; `bitbake -g <image>` writes `task-depends.dot`.
7. Rebuild only the rootfs: `bitbake -c rootfs -f <image>`, then `bitbake <image>`.

```bash
bitbake-getvar -r <image> IMAGE_INSTALL
bitbake-getvar -r <image> IMAGE_FEATURES
bitbake-getvar -r <image> PACKAGE_CLASSES
oe-pkgdata-util list-pkgs '<pattern>*'
oe-pkgdata-util lookup-recipe <package>
oe-pkgdata-util list-pkg-files -p <package>
oe-pkgdata-util find-path '*/usr/bin/<tool>'
grep -n -i 'error\|nothing provides\|conflict' tmp/work/*/<image>/*/temp/log.do_rootfs
ls tmp/deploy/images/<machine>/
cat tmp/deploy/images/<machine>/<image>-<machine>.rootfs.manifest   # installed packages and versions
```

## 7. Image Types and Outputs

- `IMAGE_FSTYPES`: `ext4`, `tar.bz2`, `tar.zst`, `cpio.gz`, `squashfs`, `wic`, `wic.gz`, `wic.bmap`, `wic.vmdk`/`wic.vdi`/`wic.qcow2`, `live` (image-live: HDDIMG/ISO via `do_bootimg`), `container` (image-container). The `image_types` class lists every type and compression.
- Outputs go to `tmp/deploy/images/<machine>/` with a `.manifest` and, by default in scarthgap, `IMAGE-MACHINE.spdx.json`. License manifests: `tmp/deploy/licenses/<image>-<machine>.rootfs-<datestamp>/` (dev-manual 33.3).
- Wic (dev-manual 19): add `wic` to `IMAGE_FSTYPES` and set `WKS_FILE` (a `.wks` kickstart in a layer's `wic/` dir or `scripts/lib/wic/canned-wks`); `WKS_FILE_DEPENDS` builds extra tools; the `bootimg-partition` plugin copies `IMAGE_BOOT_FILES` (from `DEPLOY_DIR_IMAGE`) into the boot partition. Standalone: `wic create <wks> -e <image>` ("cooked" mode) and `wic ls`/`wic cp` to inspect an image. Kickstart syntax: ref-manual "OpenEmbedded Kickstart (.wks) Reference".
- Initramfs: `INITRAMFS_IMAGE` and `PACKAGE_INSTALL` (not `IMAGE_INSTALL`) for `core-image-minimal-initramfs`-style images; bundling with `INITRAMFS_IMAGE_BUNDLE = "1"`.
- SDK: `bitbake -c populate_sdk <image>` (standard), `bitbake -c populate_sdk_ext <image>` (eSDK), output in `tmp/deploy/sdk/`.

## 8. Feeds, Multiconfig, Build History

- Package feeds: `bitbake package-index` regenerates feed indexes (not `bitbake -c package_index`); runtime installs need `package-management` in `IMAGE_FEATURES`.
- Multiconfig (dev-manual 12.2): `conf/multiconfig/<name>.conf` (usually its own `MACHINE` and `TMPDIR`), `BBMULTICONFIG = "x86 arm"` in `local.conf`, build `bitbake mc:x86:core-image-minimal mc:arm:core-image-sato`; cross dependencies with `do_image[mcdepends] = "mc:x86:arm:core-image-minimal:do_rootfs"`. Scarthgap multiconfig builds do not share sstate optimizations between multiconfigs.
- Buildhistory (dev-manual 31): `INHERIT += "buildhistory"` and `BUILDHISTORY_COMMIT = "1"`; `buildhistory/images/<machine>/<libc>/<image>/installed-package-names.txt` and `files-in-image.txt` answer "is it in the image"; `buildhistory-diff` compares builds.

## 9. Common Problems

- Recipe name used instead of the package name.
- `DEPENDS` used to put software in an image.
- `IMAGE_INSTALL +=` in `local.conf` replaces the image's default list (section 2).
- Feature set in `IMAGE_FEATURES` but the matching `DISTRO_FEATURES` or layer is missing.
- Package only recommended and removed by `BAD_RECOMMENDATIONS`/`NO_RECOMMENDATIONS`.
- Postinst assumes it runs on the target.
- Two packages ship the same file; fix packaging rather than forcing install order.
- `oe-pkgdata-util` queried before the recipe was built.

Derived from the Yocto Project scarthgap (5.0) documentation, CC BY-SA 2.0 UK.
