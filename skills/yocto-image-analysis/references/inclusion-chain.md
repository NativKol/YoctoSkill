# How a Package Ends Up in an Image (scarthgap 5.0)

The chain from image recipe variables to the files in the root filesystem, with every
keyword that can add, remove or swap a package along the way. Use it to answer "why is X
in the image", "why is X missing", and "what else did this change pull in".

Citations: `<manual>/<page>.md: <section or glossary entry>` from the local scarthgap
manuals (online: `https://docs.yoctoproject.org/scarthgap/...`). **source** marks details
read from the scarthgap branch of poky (`meta/classes-recipe/image.bbclass`,
`core-image.bbclass`, `packagegroup.bbclass`, `meta/lib/oe/packagegroup.py`,
`meta/conf/bitbake.conf`); confirm with `bitbake-getvar -r <image> <VAR>` on the user's tree.

## Contents

1. The pipeline at a glance
2. Stage A — the image recipe's install lists
3. Stage B — image features
4. Stage C — package groups and distro/machine hooks
5. Stage D — runtime dependency resolution by the package manager
6. Stage E — exclusions and their limits
7. Stage F — complementary and locale packages
8. Upstream of all of this: which recipe, which packages, which dependencies
9. Task dependencies: why the image builds what it builds
10. Name spaces: recipe, recipe-space package, runtime package

---

## 1. The pipeline at a glance

```text
IMAGE_INSTALL ───────────────┐   (core-image default: CORE_IMAGE_BASE_INSTALL =
                             │    packagegroup-core-boot packagegroup-base-extended
                             │    ${CORE_IMAGE_EXTRA_INSTALL})
ROOTFS_BOOTSTRAP_INSTALL ────┤   (run-postinsts)
IMAGE_FEATURES ─► FEATURE_PACKAGES_<f> ─► FEATURE_INSTALL ─┤
                                                          ▼
                                              PACKAGE_INSTALL  (+ PACKAGE_INSTALL_ATTEMPTONLY,
                                                                LINGUAS_INSTALL)
                                                          │
                            package manager (dnf/rpm, opkg, apt/dpkg) in do_rootfs
                                                          │  resolves RDEPENDS, RRECOMMENDS,
                                                          │  RPROVIDES, RCONFLICTS, RREPLACES
                                                          │  minus BAD_RECOMMENDATIONS,
                                                          │  NO_RECOMMENDATIONS, PACKAGE_EXCLUDE
                                                          ▼
                       complementary packages (dev-pkgs, dbg-pkgs, ptest-pkgs, … globs)
                                                          ▼
                     postinstalls, ROOTFS_POSTPROCESS_COMMAND, <image>.manifest
```

"PACKAGE_INSTALL: The final list of packages passed to the package manager for
installation into the image" (overview-manual/concepts.md: Image Generation). It is "not
the final list of packages that are actually installed", because the package manager adds
dependencies (ref-manual/variables.md: PACKAGE_INSTALL). The only complete answer to "what
is installed" is the build output: the image manifest or buildhistory (evidence-tools.md).

## 2. Stage A — the image recipe's install lists

- `IMAGE_INSTALL`: packages to install "through the image class"; recommended form
  `IMAGE_INSTALL:append = " package-name"` with the leading space
  (ref-manual/variables.md: IMAGE_INSTALL).
- **source** `core-image.bbclass`:

  ```bitbake
  CORE_IMAGE_BASE_INSTALL = '\
      packagegroup-core-boot \
      packagegroup-base-extended \
      \
      ${CORE_IMAGE_EXTRA_INSTALL} \
      '
  CORE_IMAGE_EXTRA_INSTALL ?= ""
  IMAGE_INSTALL ?= "${CORE_IMAGE_BASE_INSTALL}"
  inherit image
  ```

  So `CORE_IMAGE_EXTRA_INSTALL` only reaches images whose `IMAGE_INSTALL` references it:
  the class default does, and `core-image-minimal.bb` does
  (`IMAGE_INSTALL = "packagegroup-core-boot ${CORE_IMAGE_EXTRA_INSTALL}"`). A custom image
  that sets its own `IMAGE_INSTALL` without that reference ignores it
  (ref-manual/variables.md: CORE_IMAGE_EXTRA_INSTALL says to set it only in `local.conf`).
- **source** `image.bbclass`:

  ```bitbake
  ROOTFS_BOOTSTRAP_INSTALL = "run-postinsts"
  FEATURE_INSTALL = "${@' '.join(oe.packagegroup.required_packages(oe.data.typed_value('IMAGE_FEATURES', d), d))}"
  FEATURE_INSTALL_OPTIONAL = "${@' '.join(oe.packagegroup.optional_packages(oe.data.typed_value('IMAGE_FEATURES', d), d))}"
  export PACKAGE_INSTALL ?= "${IMAGE_INSTALL} ${ROOTFS_BOOTSTRAP_INSTALL} ${FEATURE_INSTALL}"
  PACKAGE_INSTALL_ATTEMPTONLY ?= "${FEATURE_INSTALL_OPTIONAL}"
  LINGUAS_INSTALL ?= "${@" ".join(map(lambda s: "locale-base-%s" % s, d.getVar('IMAGE_LINGUAS').split()))}"
  RDEPENDS += "${PACKAGE_INSTALL} ${LINGUAS_INSTALL} ${IMAGE_INSTALL_DEBUGFS}"
  RRECOMMENDS += "${PACKAGE_INSTALL_ATTEMPTONLY}"
  ```

  The image's own `RDEPENDS`/`RRECOMMENDS` are what make BitBake build those packages
  (section 9).
- Initramfs images (`core-image-minimal-initramfs`) set `PACKAGE_INSTALL` directly so they
  are not affected by `IMAGE_INSTALL` (ref-manual/variables.md: IMAGE_INSTALL note,
  PACKAGE_INSTALL).
- Recipe names are not package names: `IMAGE_INSTALL` takes runtime package names in
  OpenEmbedded notation (`glibc-dev`, not `libc6-dev`) (dev-manual/customizing-images.md:
  Customizing Images Using Custom .bb Files).

## 3. Stage B — image features

- `IMAGE_FEATURES` is set in the image recipe; `EXTRA_IMAGE_FEATURES` in `local.conf`;
  "The value of EXTRA_IMAGE_FEATURES is added to IMAGE_FEATURES within
  meta/conf/bitbake.conf" (dev-manual/customizing-images.md: Customizing Images Using
  Custom IMAGE_FEATURES and EXTRA_IMAGE_FEATURES). **source**: the line is
  `IMAGE_FEATURES += "${EXTRA_IMAGE_FEATURES}"`, parsed before any recipe — see
  evaluation-order.md pitfall 3.
- Most features map to packages through `FEATURE_PACKAGES_<feature>` ("should have the name
  of the feature item as an override" — written with `_`, ref-manual/variables.md:
  FEATURE_PACKAGES); some are configuration switches handled in
  `rootfs-postcommands`/`image.bbclass` (`debug-tweaks`, `read-only-rootfs`,
  `empty-root-password`, `allow-root-login`, `post-install-logging`, …)
  (ref-manual/features.md: Image Features).
- **source** scarthgap `core-image.bbclass` mappings:

  | Feature | Packages |
  |---|---|
  | `weston` | `packagegroup-core-weston` |
  | `x11` / `x11-base` / `x11-sato` | `packagegroup-core-x11` / `-x11-base` / `-x11-sato` |
  | `tools-debug` / `tools-profile` / `tools-testapps` | `packagegroup-core-tools-debug` / `-tools-profile` / `-tools-testapps` |
  | `tools-sdk` | `packagegroup-core-sdk packagegroup-core-standalone-sdk-target` |
  | `eclipse-debug` | `packagegroup-core-eclipse-debug` |
  | `nfs-server` / `nfs-client` | `packagegroup-core-nfs-server` / `-nfs-client` |
  | `ssh-server-dropbear` / `ssh-server-openssh` | `packagegroup-core-ssh-dropbear` / `-ssh-openssh` |
  | `hwcodecs` | `${MACHINE_HWCODECS}` |

  and in `image.bbclass`: `package-management` → `${ROOTFS_PKGMANAGE}`, `splash` →
  `${SPLASH}` (psplash when `MACHINE_FEATURES` has `screen`).
- `IMAGE_FEATURES_REPLACES_ssh-server-openssh = "ssh-server-dropbear"`: enabling openssh
  drops dropbear (**source**). `IMAGE_FEATURES_CONFLICTS_<f>` makes the build fail.
- A `FEATURE_PACKAGES_<f>[optional]` flag moves those packages to
  `PACKAGE_INSTALL_ATTEMPTONLY` (installed if possible) (**source**, `oe/packagegroup.py`).
- An unknown feature name skips the image recipe with "'<f>' in IMAGE_FEATURES … is not a
  valid image feature" (**source**).
- `REQUIRED_IMAGE_FEATURES` / `CONFLICT_IMAGE_FEATURES` with `features_check` gate recipes
  on image features (ref-manual/variables.md).

## 4. Stage C — package groups and distro/machine hooks

- A package group is a recipe that inherits `packagegroup`; each package in its `PACKAGES`
  lists members in `RDEPENDS:<pkg>` (hard) and `RRECOMMENDS:<pkg>` (soft). The class adds
  `-dev`, `-dbg` (and `-ptest`) variants and marks all packages `ALLOW_EMPTY`
  (dev-manual/customizing-images.md: Customizing Images Using Custom Package Groups;
  ref-manual/classes.md: packagegroup).
- Member lists are usually conditional — that is where distro and machine policy enters the
  image. **source** scarthgap `packagegroup-core-boot.bb`:

  ```bitbake
  RDEPENDS:${PN} = "base-files base-passwd ${VIRTUAL-RUNTIME_base-utils} \
      ${@bb.utils.contains("DISTRO_FEATURES", "sysvinit", "${SYSVINIT_SCRIPTS}", "", d)} \
      ${@bb.utils.contains("MACHINE_FEATURES", "keyboard", "${VIRTUAL-RUNTIME_keymaps}", "", d)} \
      ${@bb.utils.contains("MACHINE_FEATURES", "efi", "${EFI_PROVIDER} kernel", "", d)} \
      netbase ${VIRTUAL-RUNTIME_login_manager} ${VIRTUAL-RUNTIME_init_manager} \
      ${VIRTUAL-RUNTIME_dev_manager} ${VIRTUAL-RUNTIME_update-alternatives} \
      ${MACHINE_ESSENTIAL_EXTRA_RDEPENDS}"
  ```

  `packagegroup-base` adds `packagegroup-base-<f>` for each `COMBINED_FEATURES` entry
  (alsa, ext2, vfat, pci, usbhost, bluetooth, wifi, …) and carries
  `DISTRO_EXTRA_RDEPENDS`/`DISTRO_EXTRA_RRECOMMENDS` (in `packagegroup-distro-base`) and
  `MACHINE_EXTRA_RDEPENDS`/`MACHINE_EXTRA_RRECOMMENDS` (in `packagegroup-machine-base`).
- Hook variables and where they act (ref-manual/variables.md entries):
  - `MACHINE_ESSENTIAL_EXTRA_RDEPENDS` / `_RRECOMMENDS`: through `packagegroup-core-boot`,
    so even `core-image-minimal`.
  - `MACHINE_EXTRA_RDEPENDS` / `_RRECOMMENDS`, `DISTRO_EXTRA_RDEPENDS` / `_RRECOMMENDS`: only
    images that include `packagegroup-base` (not `core-image-minimal`).
- `bb.utils.contains('VAR', 'a b', truevalue, falsevalue, d)` returns `truevalue` only if
  **all** listed words are in `VAR`; `bb.utils.contains_any` if any is. The manuals point to
  the definition in `bitbake/lib/bb/utils.py` rather than documenting it
  (dev-manual/layers.md; ref-manual/classes.md: utils; **source** for the all/any rule).
- `COMBINED_FEATURES` is the intersection of `DISTRO_FEATURES` and `MACHINE_FEATURES`
  (ref-manual/variables.md: COMBINED_FEATURES), so removing a distro feature can remove
  machine-related packagegroups even though the machine did not change.

## 5. Stage D — runtime dependency resolution

The package manager installs `PACKAGE_INSTALL` plus everything their metadata requires:

- `RDEPENDS:<pkg>`: hard runtime dependencies; installation fails if missing.
- `RRECOMMENDS:<pkg>`: installed automatically unless excluded; "need not actually be
  produced" as long as some recipe could provide them (ref-manual/variables.md:
  RRECOMMENDS).
- `RPROVIDES:<pkg>`: aliases a package also satisfies; a package's own name is implicit
  (ref-manual/variables.md: RPROVIDES).
- `RCONFLICTS` / `RREPLACES`: conflicting packages cannot be co-installed; `RREPLACES` is for
  upgrades and needs `RCONFLICTS` to also remove the other package (ref-manual/variables.md).
- **Automatically added dependencies** at `do_package` (overview-manual/concepts.md:
  Automatically Added Runtime Dependencies):
  - `shlibdeps`: a binary linking a shared library gets an `RDEPENDS` on the package that
    ships that soname, with `(>= version)`; `PRIVATE_LIBS` opts libraries out.
  - `pcdeps`: `.pc` `Requires:` lines become dependencies (mostly between `-dev` packages).
  - `depchains`: `foo-dev`/`foo-dbg` get `RRECOMMENDS` on `bar-dev`/`bar-dbg` when `foo`
    depends on `bar`.
  These never appear in any recipe text — a static reading of metadata cannot see them. A
  new upstream version that links an extra library adds a package to the image with no
  metadata change at all (dev-manual/build-quality.md: Maintaining Build Output Quality).
- `PACKAGECONFIG[f] = "enable,disable,DEPENDS,RDEPENDS,RRECOMMENDS,conflicts"`: an enabled
  option adds build and runtime dependencies (ref-manual/variables.md: PACKAGECONFIG). The
  default list is often derived from features, e.g.
  `PACKAGECONFIG ??= "${@bb.utils.filter('DISTRO_FEATURES', 'x11 wayland', d)}"`, so a
  feature change flips options in many recipes at once.
- `VIRTUAL-RUNTIME_<name>`: a variable holding a runtime package name, used in `RDEPENDS`
  and images to pick an implementation (busybox vs `packagegroup-core-base-utils` for
  `VIRTUAL-RUNTIME_base-utils`) (ref-manual/variables.md: VIRTUAL-RUNTIME). Init-manager
  includes set the init-related ones with `??=` (evaluation-order.md section 3).

## 6. Stage E — exclusions and their limits

From ref-manual/variables.md (all three can be scoped with `:pn-<image>`):

| Variable | Effect | Limit |
|---|---|---|
| `BAD_RECOMMENDATIONS` | do not install the listed recommended-only packages | ignored when something `RDEPENDS` on them; IPK and RPM only, not DEB |
| `NO_RECOMMENDATIONS = "1"` | install no recommended-only packages | same; may drop kernel modules and other needed recommends |
| `PACKAGE_EXCLUDE` | never install the listed packages | fatal error if something `RDEPENDS` on them; all backends |
| `PACKAGE_EXCLUDE_COMPLEMENTARY` | regexes excluded from complementary installs | complementary step only |

So "I added it to BAD_RECOMMENDATIONS but it is still there" means a hard dependency exists;
find it with `yocto_diff.py why` on buildhistory `depends.dot`.

## 7. Stage F — complementary and locale packages

- `COMPLEMENTARY_GLOB[<feature>] = '<glob>'` ties an image feature to a glob applied to
  every installed package, e.g. `dev-pkgs` → `*-dev`; recommends are ignored for
  complementary installs (ref-manual/variables.md: COMPLEMENTARY_GLOB). **source**:
  `IMAGE_INSTALL_COMPLEMENTARY = '${@complementary_globs("IMAGE_FEATURES", d)}'`.
- `IMAGE_LINGUAS` installs `*-locale-<lang>` packages for packages already selected, and
  `locale-base-<lang>` through `LINGUAS_INSTALL` (ref-manual/variables.md: IMAGE_LINGUAS;
  **source** for `LINGUAS_INSTALL`). `core-image-minimal` sets `IMAGE_LINGUAS = " "`.

## 8. Upstream: which recipe, which packages, which dependencies

- **Recipe selection** for build-time names and `virtual/*`: `PREFERRED_PROVIDER_<item>`
  (the recipe `PN`; non-selected providers of a `virtual/*` item are prevented from
  building), `PREFERRED_VERSION_<pn>` (matched against `PV`, `%` wildcard only at the end),
  `REQUIRED_VERSION_<pn>` (error instead of warning), `DEFAULT_PREFERENCE`, and layer
  priority (ref-manual/variables.md entries; bitbake-user-manual-execution.md: Providers,
  Preferences).
- **Recipe availability**: `BBMASK`, `features_check` (`REQUIRED_DISTRO_FEATURES`,
  `ANY_OF_DISTRO_FEATURES`, `CONFLICT_DISTRO_FEATURES`, and `*_MACHINE_FEATURES`,
  `*_COMBINED_FEATURES` variants), `COMPATIBLE_MACHINE`/`COMPATIBLE_HOST`. A skipped
  recipe's packages cannot be installed; the rootfs or task-graph error then names the skip
  reason.
- **Package splitting**: `PACKAGES` lists output packages; each file goes to the leftmost
  package whose `FILES:<pkg>` matches; empty packages are not created unless
  `ALLOW_EMPTY:<pkg>` (ref-manual/variables.md: PACKAGES, FILES). `PACKAGES_DYNAMIC` only
  promises packages (ref-manual/variables.md: PACKAGES_DYNAMIC). A file moving between
  packages (a `FILES` change) can make it appear in or vanish from an image that installs
  only one of them.
- **Package renaming**: the `debian` class renames library packages (`glibc` → `libc6`)
  (ref-manual/classes.md: debian). Translate with `oe-pkgdata-util lookup-pkg`.
- **Build-time vs runtime**: `DEPENDS` makes another recipe's sysroot output available at
  build time; it never installs anything into an image
  (bitbake-user-manual-metadata.md: Build Dependencies). It can still change the image
  indirectly: a library found at configure time becomes linked, and shlibdeps then adds a
  runtime dependency (overview-manual/concepts.md, section 3.6; dev-manual/new-recipe.md).

## 9. Task dependencies: why the image builds what it builds

From bitbake-user-manual-metadata.md: Dependencies:

- `do_X[deptask] = "do_Y"`: `do_Y` of every `DEPENDS` entry runs before `do_X`
  (`do_configure[deptask] = "do_populate_sysroot"`).
- `do_X[rdeptask] = "do_Y"`: same for runtime dependencies (`RDEPENDS`, `RRECOMMENDS`).
- `do_X[recrdeptask] = "do_Y"`: recursively over all build and runtime dependencies;
  `image.bbclass` has `do_rootfs[recrdeptask] += "do_packagedata"`.
- `do_X[depends] = "target:do_Y"` / `[rdepends]`: explicit task edges
  (`do_rootfs[depends]` on `makedevs-native`, `virtual/fakeroot-native`, … — **source**).

Because the image recipe's `RDEPENDS` contains `PACKAGE_INSTALL`, `bitbake -g <image>`
shows every recipe whose packages *can* be needed, plus native tools: an upper bound on
image content at recipe level, available without building (evidence-tools.md).

## 10. Name spaces

| Name | Example | Where it appears | Translate with |
|---|---|---|---|
| recipe (`PN`) | `glibc`, `openssh` | `DEPENDS`, `PREFERRED_PROVIDER_*`, `bitbake <pn>` | `oe-pkgdata-util lookup-recipe <pkg>` |
| recipe-space package | `openssh-sshd`, `glibc` | `PACKAGES`, `RDEPENDS:<pkg>` in recipes | `oe-pkgdata-util list-pkgs -p <pn>` |
| runtime package | `openssh-sshd`, `libc6` | `IMAGE_INSTALL`, manifest, buildhistory | `oe-pkgdata-util lookup-pkg [-r]` |
| virtual build name | `virtual/kernel` | `PROVIDES`, `PREFERRED_PROVIDER_virtual/*` | `bitbake-getvar PREFERRED_PROVIDER_virtual/kernel` |
| runtime alias | `VIRTUAL-RUNTIME_init_manager` value | `RDEPENDS`, `RPROVIDES` | `bitbake-getvar -r <image> VIRTUAL-RUNTIME_init_manager` |

---
Derived from the Yocto Project scarthgap (5.0) documentation, CC BY-SA 2.0 UK.
