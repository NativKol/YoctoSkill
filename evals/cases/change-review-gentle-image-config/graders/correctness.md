# Grader: gentle review of image and distro configuration changes

The diff hides three real defects behind innocent-looking lines. A general model tends to
either miss the spacing bug or bury the newcomer in style nits.

## Required to pass

1. Flags `DISTRO_FEATURES:append = "wifi"` as a blocking defect: `:append` inserts no
   space, so the value fuses with the previous token (`...usrmergewifi`) and the `wifi`
   feature is never enabled. Fix: `DISTRO_FEATURES:append = " wifi"`.
2. Flags `DEPENDS += "iw"` in the image recipe: `DEPENDS` is build-time only and does not
   install `iw` into the rootfs. Fix: add it to `IMAGE_INSTALL` (`IMAGE_INSTALL:append = " iw"`
   or in the recipe's own list).
3. Flags `IMAGE_INSTALL += "htop"` in `local.conf.sample`: core-image sets
   `IMAGE_INSTALL` with `?=`, so `+=` in local.conf causes ordering problems; use
   `IMAGE_INSTALL:append = " htop"` (and note it affects every image).
4. Raises `debug-tweaks` as a security concern (blank root password / root login) that
   must not reach production images, without demanding it be removed from a clearly
   development-only template if the author confirms that.
5. Uses gentle strictness visibly: states the level, gives each finding a paste-ready fix
   and a plain-language reason, and does not list pure style nits.

## Automatic fail

- Misses finding 1 or finding 2.
- Tells the author to put `iw` in `RDEPENDS` of the image recipe as the main fix, or to
  add it with `DEPENDS:${PN}`.
- Recommends deleting `tmp/` or `sstate-cache/`.
- Language aimed at the person ("you clearly don't understand...").

## Improves the score

- Notes that a `DISTRO_FEATURES` change rebuilds most target recipes.
- Notes that changing `local.conf.sample` only affects newly created build directories.
- Suggests a commit message with a prefix and a body saying why, without lecturing.
- Offers `bitbake-getvar DISTRO_FEATURES` / `bitbake-getvar -r company-image IMAGE_INSTALL`
  to verify.
