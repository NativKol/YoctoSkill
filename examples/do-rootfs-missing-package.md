# Example: Missing Package in do_rootfs

Skill: `yocto-image-rootfs`.

## User Prompt

```text
I added foo to IMAGE_INSTALL but do_rootfs says nothing provides foo. There is a foo_1.0.bb recipe in my layer.
```

## Evidence to Request

- where `foo` was added (`local.conf`, image recipe, bbappend) and the exact line
- the first error in `tmp/work/<machine>-*/<image>/*/temp/log.do_rootfs`
- `bitbake-getvar -r <image> IMAGE_INSTALL`
- `oe-pkgdata-util list-pkgs 'foo*'` after `bitbake foo` (pkgdata only knows built packages)

## Bad Answer Pattern

- `DEPENDS += "foo"` in the image recipe (builds it, never installs it).
- Assuming the recipe name equals the package name.
- `IMAGE_INSTALL += "foo"` in `local.conf` (skips the image's `?=` default list).
- Deleting `tmp/`.

## Expected Answer Pattern

- Build `foo`, then list its packages: `oe-pkgdata-util list-pkgs 'foo*'`, `oe-pkgdata-util list-pkg-files -p <pkg>`.
- If the recipe emits `foo-bin`, `foo-utils` or a Debian-renamed library package, put that name in `IMAGE_INSTALL`.
- If no package contains the files, check `PACKAGES`/`FILES:*` (empty packages are not created unless `ALLOW_EMPTY`).
- In `local.conf` use `IMAGE_INSTALL:append = " foo-utils"` (leading space).

## Validation

```bash
oe-pkgdata-util list-pkgs 'foo*'
bitbake -c rootfs -f <image>
grep foo tmp/deploy/images/<machine>/<image>-<machine>.rootfs.manifest
```
