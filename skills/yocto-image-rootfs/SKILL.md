---
name: yocto-image-rootfs
description: Build and fix Yocto image recipes and root filesystems - IMAGE_INSTALL (and the local.conf "+=" trap), CORE_IMAGE_EXTRA_INSTALL, IMAGE_FEATURES/EXTRA_IMAGE_FEATURES (ssh-server-openssh, tools-debug, read-only-rootfs, debug-tweaks...), package groups, recipe-name vs package-name mix-ups, do_rootfs failures ("nothing provides", conflicts, failing pkg_postinst scripts, pkg_postinst_ontarget), BAD_RECOMMENDATIONS/NO_RECOMMENDATIONS/PACKAGE_EXCLUDE, PACKAGE_CLASSES backends, IMAGE_FSTYPES and wic images (WKS_FILE), initramfs, SDK generation with populate_sdk, package feeds and multiconfig builds. Use it whenever a package is missing from an image, do_rootfs or do_image fails, someone asks how to add software or a feature to a Yocto image, or an image recipe needs review - even if they only say "openssh is not on my board". Targets Yocto 5.0 scarthgap. To explain what an already-built image contains or what a change did to it (buildhistory, manifests, distro analysis) prefer yocto-image-analysis; for compile/package failures of a single recipe use bitbake-debug.
---

# Yocto Image Rootfs

Separate the namespaces first: recipe names, package names, package groups and image features are different things, and `do_rootfs` only knows packages.

## Workflow

1. **Get the error and the request.** `log.do_rootfs` (first error) and exactly where the user added the package or feature (`local.conf`, image recipe, bbappend).
2. **Check the final variables** rather than the files:
   ```bash
   bitbake-getvar -r <image> IMAGE_INSTALL      # history shows who set or replaced it
   bitbake-getvar -r <image> IMAGE_FEATURES
   bitbake-getvar -r <image> PACKAGE_CLASSES
   ```
   `bitbake.conf` adds `EXTRA_IMAGE_FEATURES` into `IMAGE_FEATURES`; whether a hard `IMAGE_FEATURES =` in an image recipe keeps the local extras depends on evaluation order, so read the history instead of assuming.
3. **Is the name a package?** Build the recipe, then `oe-pkgdata-util list-pkgs '<name>*'`, `oe-pkgdata-util lookup-recipe <pkg>`, `oe-pkgdata-util list-pkg-files -p <pkg>`. `oe-pkgdata-util` only knows packages that were already built.
4. **Fix in the right place** ([references/image-rootfs.md](references/image-rootfs.md) section 2):
   - `local.conf`: `IMAGE_INSTALL:append = " pkg"` (leading space). Never `IMAGE_INSTALL += "pkg"` there: `local.conf` is parsed before `core-image`'s `IMAGE_INSTALL ?=`, so `+=` creates the variable and the image's default list is skipped.
   - one image: `IMAGE_INSTALL:append:pn-<image> = " pkg"`.
   - product images: an image recipe or a packagegroup, not `local.conf`.
   - features: `IMAGE_FEATURES` in the image recipe, `EXTRA_IMAGE_FEATURES` in `local.conf`; many need matching `DISTRO_FEATURES`.
   - `DEPENDS` never installs anything into an image.
5. **Postinst failures:** scripts run offline during `do_rootfs` against `$D`; use `pkg_postinst_ontarget` for device-only work and `PACKAGE_WRITE_DEPS` for native tools (section 5 of the reference).
6. **Validate:** `bitbake -c rootfs -f <image>` then `bitbake <image>`; check `tmp/deploy/images/<machine>/<image>-<machine>.rootfs.manifest`.

## Review Rules

- Runtime package names in `IMAGE_INSTALL`, OpenEmbedded names (`glibc-dev`, not Debian `libc6-dev`).
- `debug-tweaks`, `allow-empty-password`, `empty-root-password` never in a production image.
- Exclusions: `BAD_RECOMMENDATIONS`/`NO_RECOMMENDATIONS` (ipk and rpm only; ignored for hard `RDEPENDS`), `PACKAGE_EXCLUDE` (all backends; fatal if something depends on it).
- Wic images: `IMAGE_FSTYPES += "wic"`, `WKS_FILE`, `IMAGE_BOOT_FILES`; boot-file content questions go to `yocto-bsp-kernel`.
- SDK: `bitbake -c populate_sdk <image>`, eSDK `-c populate_sdk_ext`.

## References

- [references/image-rootfs.md](references/image-rootfs.md): adding packages, image feature table, exclusion variables, postinsts, rootfs debug flow, image types, wic, feeds, multiconfig, buildhistory.
- [references/variables-core.md](references/variables-core.md): operators (why `:append` beats `+=`), package and image variables.
- [references/tasks-reference.md](references/tasks-reference.md): `do_rootfs`, `do_image_*`, `do_populate_sdk`, `do_package_index`.
- [references/keywords.md](references/keywords.md): official scarthgap manual entry for every keyword named here; grep `` ## Variable `NAME` `` or `` ## Feature `image:<name>` ``. Others: `yocto-manuals` skill.

## Output

1. recipe name vs package name (with the `oe-pkgdata-util` result)
2. exact variable or image-recipe change, in the right file
3. command proving the package exists
4. rootfs validation command and the manifest to check
5. manual section (dev-manual "Customizing Images")
