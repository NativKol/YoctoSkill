# Evaluation Prompts

Manual forward-test prompts. Use them to check that the skills trigger on their own (the
prompts do not name a skill), route to the right evidence, and avoid the mistakes general
models make on Yocto. The section heading says which skill should win.

Each prompt lists what a good answer must do. A wrong answer here is usually not a
missing fact but a plausible-sounding Linux answer that ignores BitBake metadata.

## Doc Router

```text
Where do I find the current list of QA checks and what each one means?
```

Good: routes to ref-manual "QA Error and Warning Messages" (chapter 9) and the insane class
list (5.61), detects or asks for the release before quoting check names.

```text
Is scarthgap still supported, and what should I upgrade to?
```

Good: states scarthgap is the 5.0 LTS supported until April 2028 (BitBake 2.8), that the
next LTS named in the scarthgap docs is 6.0 wrynose, points to the migration guides for every
release in between, and checks https://wiki.yoctoproject.org/wiki/Releases for anything newer
instead of inventing codenames.

## BitBake Debug

```text
My build fails with "Fetcher failure for URL" on a git SRC_URI. What now?
```

Good: asks for the first fatal error and `log.do_fetch`, checks `SRC_URI` protocol, branch,
`SRCREV`, and mirrors. Does not open with "delete downloads/".

```text
do_compile fails with "command not found: pkg-config". Should I install it on my host?
```

Good: says no. Points at `DEPENDS` and native tooling rather than the build host, and explains
why host installs cause non-reproducible builds.

## Recipe and QA

```text
This recipe installs /usr/lib/libfoo.so and gets dev-so plus installed-vs-shipped.
```

Good: checks whether the library has a versioned SONAME; explains the leftmost-package rule
(`${PN}-dev` before `${PN}`); for a genuinely unversioned library uses `SOLIBS = ".so"` and
`FILES_SOLIBSDEV = ""`; does not reach for `INSANE_SKIP`.

```text
Convert this old syntax: FILES_${PN} += "${bindir}/foo"; do_install_append() { ... }
```

Good: produces `FILES:${PN}` and `do_install:append()`, says the `:` syntax is required since
3.4 honister, and mentions `scripts/contrib/convert-overrides.py`.

```text
My recipe needs openssl at runtime. Should that go in DEPENDS or RDEPENDS?
```

Good: `RDEPENDS:${PN}`, explains build-time versus runtime, and warns that the value is a
package name, not a recipe name.

## Layer

```text
My meta-company bbappend exists but bitbake does not apply it.
```

Good: checks `bitbake-layers show-appends`, `BBFILES`, and version matching between the append
filename and the recipe; knows a dangling append is a fatal parse error unless
`BB_DANGLINGAPPENDS_WARNONLY` is set, so "silently ignored" points to a different recipe, a
`BBMASK`, or a later override.

```text
I added my layer to bblayers.conf and bitbake says it is not compatible.
```

Good: goes to `LAYERSERIES_COMPAT_*` and the release series, not to a generic path fix.

## Image and Rootfs

```text
I added openssh to DEPENDS in my image recipe but it is not in the final image. What should I check?
```

Good: identifies `DEPENDS` as the wrong variable for image content and moves to
`IMAGE_INSTALL`.

```text
do_rootfs says nothing provides my-tool, but I have a recipe named my-tool.bb.
```

Good: separates recipe name from package name, suggests `oe-pkgdata-util` to confirm what
the recipe actually produces.

```text
My postinstall script fails during do_rootfs but works on the target.
```

Good: explains that `pkg_postinst` runs offline during `do_rootfs` against `$D`, suggests
`pkg_postinst_ontarget` for device-only work and `PACKAGE_WRITE_DEPS` for native tools.

## BSP and Kernel

```text
My custom machine builds an image but no DTB appears in deploy/images.
```

Good: checks `KERNEL_DEVICETREE`, the kernel provider, and machine config rather than
assuming a kernel build failure.

```text
I edited defconfig in my kernel source tree and my change disappeared after a rebuild.
```

Good: explains that the kernel source in `work-shared` is regenerated, uses
`kernel_configme`/`menuconfig`/`diffconfig` to make a `.cfg` fragment added through `SRC_URI`
in a bbappend, and checks with `bitbake -c listtasks` that the kernel is kernel-yocto based.

## Security and SBOM

```text
LIC_FILES_CHKSUM changed after an upstream upgrade. Is it safe to update the checksum?
```

Good: treats the change as a signal to read the license diff first, not as a value to paste in.

```text
How do I produce an SBOM for my image, and where does it end up?
```

Good: confirms the release, then states the scarthgap facts: `create-spdx` is on by default
through `INHERIT_DISTRO`, output `tmp/deploy/images/<machine>/<image>-<machine>.spdx.json`
plus `tmp/deploy/spdx`, SPDX 3.0 is opt-in via `create-spdx-3.0`.

## Trigger Tests

Paste each query without naming a skill. "Expect" is the skill that should load; "none"
means no Yocto skill should load.

| Query | Expect |
| --- | --- |
| `ERROR: openssl-native-3.2.1-r0 do_configure: Execution of '.../run.do_configure.1234' failed with exit code 1` - what does this mean? | bitbake-debug |
| everything rebuilds after I touched a comment in my distro conf, how do I find which variable changed the hash? | bitbake-debug |
| my bitbake parse fails with "No recipes available for: meta-company/recipes-core/busybox/busybox_1.35.0.bbappend" | yocto-layer-review |
| how do I make meta-mycompany work with scarthgap, bitbake says it is not compatible with the core layer | yocto-layer-review |
| review this recipe for me before I push it (pastes a .bb with SRCREV = "${AUTOREV}") | yocto-recipe-review |
| what is the difference between `FOO += "x"` and `FOO:append = " x"` in a bbappend? | yocto-recipe-review |
| I put htop in IMAGE_INSTALL in local.conf with += and now my image is missing busybox | yocto-image-rootfs |
| how do I get a wic image with a separate boot partition for my board | yocto-image-rootfs |
| my menuconfig change to CONFIG_USB_SERIAL was gone after bitbake rebuilt the kernel | yocto-bsp-kernel |
| u-boot builds but the fitImage has no signature on our imx8 board | yocto-bsp-kernel |
| legal wants an SPDX file for our product image, where does Yocto put it | yocto-security-sbom |
| how do I keep all GPLv3 code out of my image | yocto-security-sbom |
| which manual explains devtool on scarthgap? | yocto-doc-router |
| is kirkstone still supported, and what should we move to? | yocto-doc-router |
| can you review this PR to meta-company? (pastes a git diff touching two recipes) | yocto-change-review |
| what packages ended up in my core-image-base and why is python3 in there? | yocto-image-analysis |
| Buildroot fails with "make: *** [package/busybox/busybox.mk] Error 2" | none |
| dpkg-buildpackage complains that debian/control has an unknown field | none |
| my Ubuntu kernel module fails to load after apt upgrade | none |
| how do I write a systemd unit file that restarts on failure (plain Linux server) | none |
