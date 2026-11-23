# Effects of a Change

What BitBake actually does with a changed line, who is affected, and what rebuilds. Use
this to turn "this line changed" into "this is what happens in the build". Manual
paths are relative to the scarthgap documentation
(https://docs.yoctoproject.org/scarthgap/).

## Contents

1. Assignment operators and evaluation order
2. Overrides: syntax and scope
3. Dependencies: DEPENDS, RDEPENDS and friends
4. Images: IMAGE_INSTALL, IMAGE_FEATURES, packagegroups
5. Features: DISTRO_FEATURES, MACHINE_FEATURES, PACKAGECONFIG
6. Providers, versions and layer priority
7. Versioning and package feeds: PV, PR, PE, SRCREV, AUTOREV
8. Sources: SRC_URI, checksums, FILESEXTRAPATHS
9. Task signatures, sstate and rebuild blast radius
10. QA checks a change will trigger
11. Layer configuration effects
12. Kernel fragments and wks files
13. Reproducibility

## 1. Assignment operators and evaluation order

Source: bitbake-user-manual/bitbake-user-manual-metadata.md, sections 3.1.1 to 3.1.12.

| Operator | When it applies | Review consequence |
|---|---|---|
| `=` | at parse time, value expanded when used | In a `.bbappend` or `.inc`, `=` *replaces* whatever the recipe set. `DEPENDS = "foo"` in a bbappend removes all of the recipe's own `DEPENDS` (dev-manual/layers.md, 3.2 uses this example). |
| `:=` | expands immediately | Captures values at that point; later changes to referenced variables are ignored. Required for `FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"` so `THISDIR` is the bbappend's directory (ref-manual/variables.md, FILESEXTRAPATHS). |
| `?=` | immediate, only if unset | "if multiple `?=` assignments to a single variable exist, the first of those ends up getting used." Parse order (local.conf before distro/machine? layer order, include order) decides who wins. |
| `??=` | weak default, applied only if nothing else assigned | "Appending and prepending non-override style will not substitute the weak default value": `W ??= "x"` then `W += "y"` gives `" y"` - the default is lost. Override-style `:append` keeps it: `W ??= "x"`, `W:append = "y"` gives `"xy"`. `PACKAGECONFIG ??=` is the usual case. |
| `+=` / `=+` | immediate, inserts a space | Applied at parse time, so a later `=` or a class that assigns after it discards the addition. |
| `.=` / `=.` | immediate, no space | Same timing as `+=`. |
| `:append` / `:prepend` | at expansion time, after all parsing | "You must control all spacing": `FOO:append = "bar"` produces `...lastvaluebar`. Guaranteed to survive later `=` assignments, which is why the manual recommends `IMAGE_INSTALL:append = " pkg"` in `local.conf`. |
| `:remove` | at expansion time, after append and prepend | "The overrides are applied in this order, `:append`, `:prepend`, `:remove`. This implies it is not possible to re-append previously removed strings." Removes every occurrence of the whole word. A `:remove` in a layer cannot be undone by users except through an intermediate variable. |

Worked example from the manual (3.3.3):

```bitbake
A = "1"
A:append = "2"
A:append = "3"
A += "4"
A .= "5"
# result: "1 4523"
```

Review checks:

- `:append`/`:prepend` on a space-separated list without the leading/trailing space is a
  **blocker** when it fuses tokens (`DISTRO_FEATURES:append = "wifi"` turns
  `... x11wifi`), harmless only when appending to a non-list string on purpose.
- `+=` together with `:append` is redundant: "It is never necessary to use `+=` together
  with `:append`" (3.1.12).
- `+=` or `=` in a `.bbclass` against a variable a recipe sets later is lost (3.1.12
  `foo.bbclass` example). Classes should use `:append`.
- `RDEPENDS:${PN}-dev` already contains `${PN}`; using `=` instead of `+=` drops it
  (ref-manual/variables.md, RDEPENDS note).
- `unset VAR` and `VAR[flag]` changes are easy to miss in a diff; check what used them.
- Inline Python `${@...}` with `=` re-evaluates on every expansion; with `:=` once
  (3.1.14). Non-deterministic Python (time, random, host queries) in a value breaks
  signatures and reproducibility.

## 2. Overrides: syntax and scope

Source: bitbake-user-manual-metadata.md 3.3; migration-guides/migration-3.4.md.

- Since honister (3.4, BitBake 1.52) override syntax uses `:`; `_append`, `_prepend`,
  `_remove`, `FILES_${PN}` are the old form. scarthgap BitBake checks for the old
  `_append`/`_prepend`/`_remove` operations and stops with an error (this check is in
  BitBake's datastore code; release-notes-3.4.2.md mentions "Skip old override syntax
  checking for anonymous functions"). Other old forms such as `FILES_${PN}` do not error:
  they silently set an unrelated variable named `FILES_foo`, which is worse. Both are
  **blockers** in a scarthgap layer. *[release-specific]*
- Not overrides, keep `_`: `BBFILE_PATTERN_x`, `BBFILE_PRIORITY_x`, `LAYERDEPENDS_x`,
  `LAYERSERIES_COMPAT_x`, `LAYERVERSION_x`, `SRCREV_name`, `PREFERRED_VERSION_x`,
  `PREFERRED_PROVIDER_x` (migration-3.4.md: "There are some variables which do not use
  override syntax ...").
- Override names: lower case, digits, dashes only; no colons (3.3.1 note).
- `OVERRIDES` is built from `DISTROOVERRIDES`, `MACHINEOVERRIDES`, architecture, `pn-${PN}`,
  `class-target`/`class-native`, `task-<name>` contexts and more. Effects:
  - `VAR:<machine> = "x"` *replaces* VAR for that machine; `VAR:append:<machine>`
    adds to it. Mixing them up changes behavior on that machine only, so it is easy to
    miss in testing on another board.
  - `A:foo:append = "X"` and `A:append:foo = "X"` are different: the first appends to
    the conditional variable `A:foo` which then *replaces* `A`; the second appends to
    `A` only when `foo` is active (3.3.3).
  - Unconditional changes in a BSP bbappend affect every machine when the layer is in
  `bblayers.conf`; the manual's fix is a machine override, e.g. `DEPENDS:append:one = " foo"`
    (dev-manual/layers.md 3.2). This is what `yocto-check-layer`'s
    `bsp.test_machine_signatures` detects.
  - `MACHINEOVERRIDES =. "qemuall:"` style additions in machine conf create new
    override names that every recipe can react to.
  - A recipe whose `PN` equals an override (e.g. a machine name) triggers the
    `pn-overrides` QA check: "`FILES:${PN} = "xyz"` effectively turn into
    `FILES = "xyz"`" (ref-manual/qa-checks.md).
- Package-name overrides (`RDEPENDS:${PN}`, `FILES:${PN}-tools`) are applied in the
  packaging context. Package-specific variables set without one trigger `pkgvarcheck`;
  `DEPENDS:${PN}` is always wrong ("recipe uses DEPENDS:${PN}, should use DEPENDS").
- `:task-<name>` sets a value only during one task.

## 3. Dependencies

Sources: ref-manual/variables.md (DEPENDS, RDEPENDS, RRECOMMENDS, PROVIDES,
RPROVIDES); bitbake-user-manual-metadata.md 3.10; overview-manual/concepts.md 3.6.

- **DEPENDS** lists *recipes* needed at build time. Effect: the files those recipes
  install are in this recipe's sysroot by `do_configure` ("having `do_configure` depend on
  the `do_populate_sysroot` task of each recipe listed in DEPENDS"). Build tools use the
  `-native` variant (`DEPENDS = "codegen-native"`). It does not put anything in the
  image or on the target.
- **RDEPENDS:<pkg>** lists *packages* (not recipe names) needed at runtime. Effect: the
  dependency is written into the package metadata, and a task dependency from
  `do_build` to the providing recipe's `do_package_write_*` ensures it is built. "The most
  common types of package runtime dependencies are automatically detected and added", so
  adding shared-library dependencies manually is usually unnecessary.
- Wrong-kind mistakes: a runtime tool in `DEPENDS` (never installed on target), a library
  in `RDEPENDS` but not `DEPENDS` (link fails or `build-deps` QA), `virtual/` names in
  `RDEPENDS` (`virtual-slash` check; use `VIRTUAL-RUNTIME_*` variables).
- `RRECOMMENDS` are soft: they can be excluded with `BAD_RECOMMENDATIONS` or
  `NO_RECOMMENDATIONS`; use `RDEPENDS` if it is really required.
- `RDEPENDS` on a `-dev` or `-dbg` package triggers `dev-deps` / `debug-deps`.
- Versioned dependencies must use `<`, `=`, `>`, `<=`, `>=` (`dep-cmp`).
- New `DEPENDS` changes the signature of the recipe's tasks from `do_configure`
  onwards and adds the dependency's own task hashes (section 9).

## 4. Images

Sources: ref-manual/variables.md (IMAGE_INSTALL, EXTRA_IMAGE_FEATURES, IMAGE_FEATURES,
PACKAGE_INSTALL, CORE_IMAGE_EXTRA_INSTALL); dev-manual/customizing-images.md 4.1.

- `IMAGE_INSTALL` belongs in image recipes. In `local.conf` use
  `IMAGE_INSTALL:append = " pkg"`: "Since core-image sets IMAGE_INSTALL to a default value
  using the `?=` operator, using a `+=` operation against IMAGE_INSTALL results in
  unexpected behavior when used within `conf/local.conf`." A plain `IMAGE_INSTALL:append`
  in `local.conf` affects *all* images; `IMAGE_INSTALL:append:pn-<image>` limits it.
- `CORE_IMAGE_EXTRA_INSTALL` affects only `core-image-*` images.
- Initramfs images use `PACKAGE_INSTALL`, not `IMAGE_INSTALL`.
- `EXTRA_IMAGE_FEATURES` is meant for `local.conf`; image recipes use `IMAGE_FEATURES`.
- `debug-tweaks` "makes an image suitable for development (e.g. allows root logins, logins
  without passwords - including root ones, and enables post-installation logging)";
  `allow-empty-password`, `allow-root-login`, `empty-root-password`,
  `serial-autologin-root` likewise weaken a production image (ref-manual/features.md;
  dev-manual/securing-images.md 21.3). In a distro conf, an image recipe or a shipped
  `local.conf.sample` these are **blockers** unless the file is clearly development-only.
- `DEPENDS` in an image recipe does not install anything into the rootfs.
- Packagegroups: `RDEPENDS:${PN}` of a packagegroup is what images pull in; changes
  there change every image that includes the group. `PACKAGE_ARCH` must be set before
  `inherit packagegroup` (contributor-guide/recipe-style-guide.md 3.5.2).

## 5. Features

Sources: ref-manual/variables.md (DISTRO_FEATURES, MACHINE_FEATURES, PACKAGECONFIG,
REQUIRED_DISTRO_FEATURES, INIT_MANAGER); ref-manual/classes.md (features_check).

- `DISTRO_FEATURES` is global: "specifying x11 in DISTRO_FEATURES causes every piece of
  software built for the target that can optionally support X11 to have its X11 support
  enabled". A change to it is a distro-wide policy change: it can change dependencies,
  configure options and contents of hundreds of recipes, and changes their signatures
  (rebuild of most of the target world). Expect it only in distro conf; in
  `local.conf.sample` or `layer.conf` it is a layer-compatibility problem
  (test-manual/yocto-project-compatible.md: "Adding a layer to a build should not modify
  that build").
- Enabling a feature alone does nothing for a recipe unless the recipe's `PACKAGECONFIG`
  tracks it, e.g. `PACKAGECONFIG ??= "${@bb.utils.filter('DISTRO_FEATURES', 'x11', d)}"`.
- Switching init system: prefer `INIT_MANAGER = "systemd"` (includes
  `conf/distro/include/init-manager-${INIT_MANAGER}.inc`) over hand-editing
  `DISTRO_FEATURES` and `VIRTUAL-RUNTIME_*`.
- Recipes needing a feature use `REQUIRED_DISTRO_FEATURES` *and* `inherit features_check`;
  without the inherit the QA check `unhandled-features-check` fires.
- `MACHINE_FEATURES` changes affect recipes that test them; with a machine-specific
  result such recipes need `PACKAGE_ARCH = "${MACHINE_ARCH}"`.
- `PACKAGECONFIG` structure: `PACKAGECONFIG[f] = "enable,disable,build-deps,rdeps,rrecommends,conflicts"`.
  Review: every value added to `PACKAGECONFIG` must have a `PACKAGECONFIG[name]`
  definition (`invalid-packageconfig`); use `PACKAGECONFIG:append = " f"` or
  `PACKAGECONFIG:remove` in bbappends so the recipe's `??=` default survives;
  `PACKAGECONFIG = "f"` in a bbappend discards all defaults. Covering auto-detected
  options with PACKAGECONFIG is also a reproducibility rule
  (test-manual/reproducible-builds.md 6.3).

## 6. Providers, versions and layer priority

Sources: ref-manual/variables.md (BBFILE_PRIORITY, PREFERRED_PROVIDER,
PREFERRED_VERSION); dev-manual/layers.md 3.6.

- `BBFILE_PRIORITY_<x>` decides which layer's recipe wins when the same recipe exists in
  several layers, "regardless of a recipe's version (PV variable)", and the order
  bbappends are applied. It does not affect `.conf` or `.bbclass` precedence. Raising
  it can silently replace another layer's recipe: check with
  `bitbake-layers show-overlayed`.
- `PREFERRED_PROVIDER_virtual/kernel` and similar belong in machine or distro conf;
  "Providing unconditional global level configuration from the layer.conf file is not a
  good practice" (dev-manual/layers.md 3.6.1).
- `PREFERRED_VERSION_<recipe>` pins a version, matched against `PV` (`%` only at the
  end). "If a recipe with the specified version is not available, a warning message will
  be shown"; `REQUIRED_VERSION` makes it an error. `:forcevariable` pins are a smell.
- A copied ("overlayed") recipe instead of a bbappend means upstream fixes stop applying
  (dev-manual/layers.md 3.2, first bullet). Flag at **major**.

## 7. Versioning and package feeds

Sources: contributor-guide/recipe-style-guide.md 3.2-3.3; ref-manual/variables.md (PV,
PR, PE, SRCREV, AUTOREV, SRCPV).

- `PV` normally comes from the file name; hyphens are not allowed in the version part of
  the file name. Pre-releases use `~` (`1.5~rc2` sorts before `1.5`).
- A git revision that is not a release uses `PV = "<last-release>+git"`; the `+` makes
  BitBake add source revision information to `PKGV` during packaging. `SRCPV` is
  deprecated in scarthgap and no longer needed *[release-specific]*.
- "When PV increases, any existing PR value can and should be removed." Leaving
  `PR = "r1"` after an upgrade is a minor.
- "If PV changes in such a way that it does not increase with respect to the previous
  value, you need to increase PE"; set `PE = "1"` if unset. Downgrades without `PE` break
  upgrades from package feeds (`version-going-backwards` QA if buildhistory is on).
- `PR` is not needed to trigger rebuilds: "The build system uses the task input
  checksums along with the stamp and Shared State Cache mechanisms." It only matters
  for package feed upgrades, and the PR service can manage it.
- `SRCREV` should be a full hash, not a tag, "to avoid performing a query on the remote
  repository every time BitBake parses your recipe".
- `SRCREV = "${AUTOREV}"` makes builds non-reproducible and queries the network at parse;
  the style guide calls it "not recommended for published layers". **Major** in any
  layer that is released or used by CI.

## 8. Sources

Sources: bitbake-user-manual/bitbake-user-manual-fetching.md; ref-manual/qa-checks.md
(src-uri-bad); ref-manual/variables.md (SRC_URI, FILESEXTRAPATHS).

- Non-local downloads need `SRC_URI[sha256sum]`; a version bump that changes the
  tarball must change it. `BB_STRICT_CHECKSUM` makes a missing checksum an error.
- Git URLs: `branch=` is mandatory unless `nobranch=1`; the manual's examples use
  `protocol=https` for GitHub.
- GitHub "archive" tarballs are unstable (`src-uri-bad`); use a release tarball or git.
- Paths in `SRC_URI` should use `${BPN}`, not `${PN}` (`src-uri-bad`), so that native,
  nativesdk and multilib variants fetch the same thing.
- Adding a `file://` patch in a bbappend needs `FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"`
  (note `:=` and the trailing colon). Machine-specific files belong in a
  machine-named subdirectory or they apply to every machine (dev-manual/layers.md 3.2).
- A patch that applies with fuzz triggers `patch-fuzz` (in default `ERROR_QA` since 4.2;
  migration-guides/migration-4.2.md) *[release-specific]*.

## 9. Task signatures, sstate and rebuild blast radius

Sources: bitbake-user-manual-execution.md 2.8; overview-manual/concepts.md 3.5;
bitbake-user-manual-metadata.md 3.7, 3.12; dev-manual/debugging.md 32.6-32.8.

How it works:

- Each task has a signature (checksum) of its inputs: the task's code, the variables it
  references (found automatically for shell and Python), and the hashes of the tasks it
  depends on. "Any changes to this variable would invalidate the stamp and cause the
  do_compile task to run." With `OEBasicHash`, "any metadata change will change the task
  hash ... This removes the need to bump PR values, and changes to metadata automatically
  ripple across the build."
- A changed task hash re-runs that task and every task depending on it, unless Hash
  Equivalence finds the output identical and stops the ripple (concepts.md 3.5.4).
- Variables in `BB_BASEHASH_IGNORE_VARS` (e.g. `TMPDIR`, `DL_DIR`, `SSTATE_DIR`,
  `PARALLEL_MAKE`) never enter signatures.
- Varflags control signatures: `[vardeps]` adds dependencies BitBake cannot see (e.g.
  variables read indirectly by Python), `[vardepsexclude]` removes ones that should not
  matter, `[vardepvalue]` fixes the value used, `[vardepvalueexclude]` strips substrings.

Estimating blast radius from the diff:

| Where the change is | Who re-runs |
|---|---|
| One recipe's task function or variable used by it | that recipe from the changed task on, plus dependents whose inputs include its output (often damped by hash equivalence) |
| An `.inc` file | every recipe that `require`s it |
| A class inherited by some recipes | all inheriting recipes, for every task that references the changed function/variable |
| A class in `INHERIT`/`USER_CLASSES`, `bitbake.conf`-level variable, distro conf (`DISTRO_FEATURES`, `TARGET_CFLAGS`, toolchain settings) | effectively all target recipes: a world rebuild |
| Machine conf (`TUNE_*`, `MACHINE_FEATURES`) | everything for that machine; `yocto-check-layer` `bsp.test_machine_signatures` requires that only machine-specific tasks change between machines |
| `layer.conf` of a BSP/distro layer | `common.test_signatures`: adding the layer must not change signatures |
| A `[nostamp]` task | it and every task depending on it always re-run ("This can cause unnecessary rebuilding") |

Review checks:

- Is the blast radius proportional to the intent? A one-recipe fix placed in a distro
  conf or a global class is **major**; recommend scoping it with `:pn-<recipe>` or moving
  it into a bbappend.
- Python that reads a variable through a computed name (`d.getVar(name)`) hides the
  dependency: missing `[vardeps]` means stale sstate reuse (dangerous, **major**).
- Volatile inputs (`DATE`, `TIME`, `DATETIME`, host state) in a task without
  `[vardepsexclude]` force re-runs every build; with exclusion they make output
  non-reproducible. Either way, ask why.
- `SIGGEN_EXCLUDERECIPES_ABISAFE` additions: "If you add an inappropriate variable to
  this list, the software might break at runtime" - require justification.
- Machine-specific output in a recipe without `PACKAGE_ARCH = "${MACHINE_ARCH}"` lets
  one machine's package be reused for another.

Prove it with `bitbake -S printdiff <target>` or `bitbake-diffsigs` (verification.md).

## 10. QA checks a change will trigger

Source: ref-manual/qa-checks.md and the `insane` class (ref-manual/classes.md 5.61). The
check name appears in brackets at the end of each message. Whether it errors or warns
depends on `ERROR_QA` / `WARN_QA`; read them with `bitbake-getvar`.

| Change in the diff | Likely QA check |
|---|---|
| `FILES:${PN} += "${libdir}/*.so"` or `*.so*` | `dev-so` |
| `do_install` installs files no `FILES` pattern covers | `installed-vs-shipped` |
| `.a` into main package | `staticdev` |
| `.debug` dirs outside `-dbg` | `debug-files` |
| upstream build strips binaries | `already-stripped` |
| custom compile/link without `${LDFLAGS}` | `ldflags` |
| hard-coded `/usr/lib64`, `/lib` paths | `libdir`; with usrmerge, `usrmerge` |
| installs into `/usr/libexec` when `libexecdir` differs | `libexec` |
| `-rpath` to build dirs | `rpaths`, `useless-rpaths` |
| generated `.pc`/`.la` with TMPDIR paths | `pkgconfig`, `la`, `buildpaths` |
| new patch without/with bad `Upstream-Status` | `patch-status` |
| refreshed patch that no longer matches | `patch-fuzz` |
| `RDEPENDS` missing for a `#!/bin/bash` script | `file-rdeps` |
| `PACKAGECONFIG` value without definition | `invalid-packageconfig` |
| `REQUIRED_DISTRO_FEATURES` without `inherit features_check` | `unhandled-features-check` |
| `ALTERNATIVE:*` without `inherit update-alternatives` | `missing-update-alternatives` |
| `LICENSE:<pkg>` not in recipe `LICENSE` | `unlisted-pkg-lics` |
| `RDEPENDS`/`RPROVIDES` with `virtual/` | `virtual-slash` |
| duplicate in `PACKAGES` | `packages-list` |
| `//` in `FILES` | `files-invalid` |
| package var without package override | `pkgvarcheck` |
| `SRC_URI` uses `${PN}` or GitHub archive | `src-uri-bad` |
| upstream has a test suite but no ptest | `unimplemented-ptest` |
| `INSANE_SKIP` added | the check is hidden, not fixed: ask for the reason |

`INSANE_SKIP` must use a package override (`INSANE_SKIP:${PN} += "dev-so"`) and needs a
reason in a comment; the manual: "exercise caution when disabling these checks".

## 11. Layer configuration effects

Sources: dev-manual/layers.md; ref-manual/variables.md; bitbake-user-manual ref
variables (LAYERSERIES_COMPAT, BBFILES_DYNAMIC).

- `LAYERSERIES_COMPAT_<x>` must list the release names the layer is tested with
  (`"scarthgap"`). The manual says the variable lets the system "detect when a layer has
  not been tested with new releases of OE-Core" and that a missing value produces a
  warning; in practice a list without the current core series makes the build refuse
  the layer (observed BitBake behavior, not quoted in the manual). Adding a release name
  without testing is a claim reviewers should question.
- `LAYERDEPENDS_<x>` errors if a dependency is missing; a new `require` of another
  layer's file or a bbappend to another layer's recipe needs it, or `BBFILES_DYNAMIC`
  for optional layers.
- A `.bbappend` must match the recipe's name and version; `%` matches any version
  (`xserver-xf86-config_%.bbappend`). A version-specific append becomes dangling on the
  next upgrade, which is fatal unless `BB_DANGLINGAPPENDS_WARNONLY` is set; a `%`
  append silently applies to a new version that may need different changes.
- `BBFILE_COLLECTIONS`, `BBFILE_PATTERN_<x>`, `BBFILES` globs decide what BitBake sees; a
  wrong glob hides files with no error.
- Global settings in `layer.conf` change every build that adds the layer; the manual's
  conditional pattern uses a class added to `USER_CLASSES` that `require`s an include
  only when a feature is enabled (dev-manual/layers.md 3.6.1.1).

## 12. Kernel fragments and wks files

Sources: kernel-dev/common.md; ref-manual/tasks.md (do_kernel_configcheck);
dev-manual/wic.md.

- A `.cfg` fragment in `SRC_URI` or a `.scc` in `KERNEL_FEATURES` changes the kernel
  config for every machine the recipe/bbappend applies to; scope with machine overrides.
- Options that do not end up in the final `.config` are reported by
  `do_kernel_configcheck` ("produces warnings when a requested configuration does not
  appear in the final `.config` file"); run `bitbake <kernel> -c kernel_configcheck -f`.
- Kernel metadata kept in a separate `type=kmeta` repository needs `SRCREV_meta` updated
  with it (kernel-dev/advanced.md).
- `.wks` changes alter the partition layout: check `WKS_FILE`/`WKS_FILES` selection,
  that `IMAGE_FSTYPES` contains `wic`, and that bootloader and partition sizes still
  fit. Layout changes on deployed devices need an update/migration story: ask.

## 13. Reproducibility

Source: test-manual/reproducible-builds.md.

The project defines reproducibility as the same output "regardless of when it is built
..., regardless of the path ..., and regardless of the distro and tools on the underlying
host". Changes that break it: timestamps or host names embedded in output (use
`SOURCE_DATE_EPOCH`), absolute build paths (`buildpaths` QA), auto-detected optional
dependencies not pinned by `PACKAGECONFIG`, host tools outside `HOSTTOOLS`, `AUTOREV`,
network access outside `do_fetch` ("By default, only the `do_fetch` task is granted
network access"; a task needing it must set `do_<task>[network] = "1"`,
bitbake-user-manual-metadata.md 3.7, migration-guides/migration-4.0.md). Test with
`oe-selftest -r reproducible.ReproducibleTests.test_reproducible_builds` and
`OEQA_REPRODUCIBLE_TEST_TARGET`. Only OE-Core guarantees reproducibility; "The moment you
add another layer, this warranty is voided."

Derived from the Yocto Project scarthgap (5.0) documentation, CC BY-SA 2.0 UK.
