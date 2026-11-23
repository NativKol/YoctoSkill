# Grader: += in a conf file wipes defaults

The tempting answer is "`+=` appends, so the problem must be elsewhere" or a generic
rebuild/clean. The real cause is parse order: `auto.conf` is parsed (from `bitbake.conf`)
before the distro configuration and the image recipe, so the immediate `+=` makes the
variables set and the later `?=` defaults never apply.

## Required to pass

1. States that `auto.conf` (like `local.conf`) is parsed before `conf/distro/poky.conf`,
   `defaultsetup.conf` and the image recipe/classes.
2. Explains that `core-image.bbclass` sets `IMAGE_INSTALL ?= "${CORE_IMAGE_BASE_INSTALL}"`
   (packagegroup-core-boot, packagegroup-base-extended, CORE_IMAGE_EXTRA_INSTALL) and
   poky sets `DISTRO_FEATURES ?= ...`; because the variable already has a value (" htop",
   " wifi"), the `?=` does nothing.
3. Gives the fix: `IMAGE_INSTALL:append = " htop"` (or `CORE_IMAGE_EXTRA_INSTALL += "htop"`)
   and `DISTRO_FEATURES:append = " wifi"`, with the leading space.
4. Shows how to prove it: `bitbake-getvar -r core-image-base IMAGE_INSTALL` and
   `bitbake-getvar DISTRO_FEATURES` history showing the `append` from `auto.conf` followed
   by an ineffective `set?`.

## Automatic fail

- Recommends deleting `tmp/` or `sstate-cache/` as the fix.
- Claims `+=` always appends to the final value regardless of order.
- Uses `_append` syntax for scarthgap without qualification.

## Improves the score

- Cites the IMAGE_INSTALL glossary note that `+=` in `local.conf` causes ordering issues.
- Mentions that backfilled features (e.g. `pulseaudio`, `sysvinit`) still appear, which is
  why DISTRO_FEATURES is not completely empty.
- Notes images that set `IMAGE_INSTALL =` themselves (e.g. core-image-minimal) would instead
  silently lose `htop`.
