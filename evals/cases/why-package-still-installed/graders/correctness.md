# Grader: package still installed despite BAD_RECOMMENDATIONS

The tempting answers are "use PACKAGE_EXCLUDE" (which fails the build if something hard
depends on the package), "clean and rebuild", or deleting the files in a postprocess
command. The skill should explain what `BAD_RECOMMENDATIONS` can and cannot do, then trace
the actual dependency chain instead of guessing.

Background for the grader (scarthgap poky): `packagegroup-core-boot` lists
`${VIRTUAL-RUNTIME_base-utils-syslog}` in `RRECOMMENDS`, and `default-providers.inc` sets
`VIRTUAL-RUNTIME_base-utils-syslog ?= "busybox-syslog"`. In stock poky the package is
therefore recommended-only and `BAD_RECOMMENDATIONS` would normally remove it, so if it is
still installed something else must pull it in hard (an `RDEPENDS`, an explicit
`IMAGE_INSTALL`/packagegroup entry, an `RPROVIDES` match) or the setting is not effective
for this image (override name does not match the image recipe name, set elsewhere with `=`).

## Required to pass

1. Explains that `BAD_RECOMMENDATIONS` only blocks packages pulled in solely through
   `RRECOMMENDS`; if anything `RDEPENDS` on the package (or lists it explicitly), it is
   installed anyway.
2. Gives a concrete way to see the chain rather than guessing: buildhistory's image
   `depends.dot` (dotted edges are recommends) or the skill's `yocto_diff.py why` helper,
   and/or `oe-pkgdata-util read-value RDEPENDS` / `RRECOMMENDS` on candidates and
   `oe-pkgdata-util lookup-recipe busybox-syslog`.
3. Verifies the setting reaches the image: `bitbake-getvar -r our-image BAD_RECOMMENDATIONS`
   (and checks that `our-image` is the recipe name used in `:pn-`).
4. Offers the cleaner knob: the syslog provider comes from
   `VIRTUAL-RUNTIME_base-utils-syslog` (packagegroup-core-boot), which can be set
   (for example to `""` or another syslog) instead of fighting the package manager.
5. Notes `PACKAGE_EXCLUDE` makes the build fail if a hard dependency remains.

## Automatic fail

- Claims `BAD_RECOMMENDATIONS` removes a package even when something RDEPENDS on it.
- Asserts a specific RDEPENDS culprit as fact without any way to check it.
- Suggests deleting the files from the rootfs in a postprocess command as the primary fix.
- Recommends deleting `tmp/` or `sstate-cache/`.

## Improves the score

- Mentions that DEB does not support `BAD_RECOMMENDATIONS` and that poky's default
  `PACKAGE_CLASSES` is RPM, which does.
- Mentions `buildhistory-diff` or a manifest diff to confirm the package left the image.
