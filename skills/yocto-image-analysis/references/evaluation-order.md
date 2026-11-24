# Configuration and Evaluation Order (scarthgap 5.0 / BitBake 2.8)

How BitBake turns layers, configuration files, classes, recipes and appends into the one
value a variable has when a task runs. Read this before claiming that a line "adds",
"sets" or "removes" something: whether a line has any effect depends on where it is
parsed relative to every other assignment of the same variable, and on the operator.

Sources are cited as `<manual>/<page>.md: <section>`, paths under the offline scarthgap
manuals in `yocto-manuals/references/manuals/` (read one section with
`python3 scripts/ylookup.py --section <manual>/<page>.md "<section>"`, one keyword with
`ylookup.py <NAME>`; online citation only:
`https://docs.yoctoproject.org/scarthgap/<manual>/<page>.html`). Where the manual does not
spell a detail out, the claim is marked **source** and was read from the scarthgap branch
of poky (`meta/...`) or the BitBake 2.8 branch (`lib/bb/...`); confirm those on the user's
tree with `bitbake-getvar` history, because a vendor fork can differ.

## Contents

1. Two kinds of datastore
2. Stage 1 — layers: `bblayers.conf` and `layer.conf`
3. Stage 2 — `bitbake.conf` and the configuration include chain
4. Stage 3 — global classes
5. Stage 4 — one recipe: recipe, classes, includes, bbappends
6. Stage 5 — finalization: deferred inherits, key expansion, anonymous Python
7. Operators: what is immediate and what is deferred
8. How the final value is computed (overrides, `:append`, `:prepend`, `:remove`)
9. Ordering pitfalls that change image content
10. Release notes for this material

---

## 1. Two kinds of datastore

- **Global (configuration) datastore**: built once from `bblayers.conf`, every
  `layer.conf`, `bitbake.conf` and the files it includes, plus globally inherited classes.
  `bitbake-getvar VAR` and plain `bitbake -e` show it.
- **Per-recipe datastore**: "after parsing the configuration, a copy of the resulting
  datastore is made prior to parsing each recipe", so variables set in one recipe are not
  visible to others; each task also gets a private copy
  (dev-manual/debugging.md: Viewing Variable Values). `bitbake-getvar -r <recipe> VAR` and
  `bitbake -e <recipe>` show it.

Consequence: an image's `IMAGE_INSTALL`, `IMAGE_FEATURES` or a recipe's `PACKAGECONFIG`
only exist with their final value in that recipe's datastore. Always query with `-r <image>`
or `-r <recipe>` when the question is about one image or recipe.

## 2. Stage 1 — layers: `bblayers.conf` and `layer.conf`

BitBake first reads `conf/bblayers.conf` from the Build Directory; its `BBLAYERS` lists the
layer directories. For each layer, `conf/layer.conf` is parsed with `LAYERDIR` set to that
layer (bitbake-user-manual/bitbake-user-manual-execution.md: Parsing the Base Configuration
Metadata). Each `layer.conf` typically:

- extends `BBPATH` (search path for `conf/` and `classes*/` files, and for
  `include`/`require` with relative paths),
- extends `BBFILES` (globs for `.bb` and `.bbappend` files),
- declares its collection in `BBFILE_COLLECTIONS` with `BBFILE_PATTERN_<name>` and
  `BBFILE_PRIORITY_<name>`,
- states `LAYERDEPENDS_<name>`, `LAYERSERIES_COMPAT_<name>` and optionally
  `BBFILES_DYNAMIC` (recipes enabled only when another layer is present).

What this stage decides for an image analysis:

- **Which recipe file wins** when the same recipe name exists in several layers: the
  higher `BBFILE_PRIORITY` wins "regardless of a recipe's version (PV)"
  (ref-manual/variables.md: BBFILE_PRIORITY). `DEFAULT_PREFERENCE` is a weak bias that
  `BBFILE_PRIORITY` overrides (ref-manual/variables.md: DEFAULT_PREFERENCE);
  `PREFERRED_VERSION` overrides `DEFAULT_PREFERENCE`
  (bitbake-user-manual-execution.md: Preferences). See which file won with
  `bitbake-layers show-overlayed` and `bitbake-layers show-recipes <pn>`.
- **Which bbappends apply and in which order**: a `.bbappend` applies to the recipe file
  with the same base name; a `%` in the append name matches any version suffix
  (dev-manual/layers.md: Appending Other Layers Metadata With Your Layer). The BitBake
  manual says "append files are applied in the order they are encountered in BBFILES"
  (bitbake-user-manual-execution.md: Locating and Parsing Recipes). **source** (BitBake 2.8
  `lib/bb/cooker.py`, `collect_bbfiles`): the `BBFILES` entries are first sorted by their
  collection priority, lowest first, so appends from the highest-priority layer are parsed
  **last** and their plain `=` assignments win. Confirm on the tree with
  `bitbake-layers show-appends <pn>` and the history from `bitbake-getvar -r <pn> VAR`.
- **What is invisible**: files matching `BBMASK` (Python regular expressions matched against
  full paths) are not parsed at all, recipes and appends alike
  (ref-manual/variables.md: BBMASK). A changed `BBMASK` can silently drop a bbappend.
- `LAYERSERIES_COMPAT` does not change values; it gates whether the layer is accepted for
  this OE-Core release (bitbake-user-manual-ref-variables.md: LAYERSERIES_COMPAT). For
  scarthgap it must contain `scarthgap`.

## 3. Stage 2 — `bitbake.conf` and the configuration include chain

`conf/bitbake.conf` is located through `BBPATH` and "generally has include directives to
pull in any other metadata such as files specific to the architecture, the machine, the
local environment" (bitbake-user-manual-execution.md). Only variable definitions and
include directives are allowed in `.conf` files (same section).

**source** — the scarthgap `meta/conf/bitbake.conf` defines `OVERRIDES` and most defaults
first, then includes, in this exact order:

```text
require conf/abi_version.conf
include conf/site.conf
include conf/auto.conf
include conf/local.conf
require conf/multiconfig/${BB_CURRENT_MC}.conf
include conf/machine/${MACHINE}.conf
include conf/machine-sdk/${SDKMACHINE}.conf
include conf/distro/${DISTRO}.conf
include conf/distro/defaultsetup.conf
include conf/documentation.conf
include conf/licenses.conf
require conf/sanity.conf
require conf/cve-check-map.conf
include conf/bblock.conf
```

after which it sets "weak" fallbacks such as `DISTRO_FEATURES ?= ""`,
`MACHINE_FEATURES ?= ""`, `EXTRA_IMAGE_FEATURES ??= ""`,
`IMAGE_FEATURES += "${EXTRA_IMAGE_FEATURES}"`,
`DISTRO_FEATURES_BACKFILL = "pulseaudio sysvinit gobject-introspection-data ldconfig"`,
`MACHINE_FEATURES_BACKFILL = "rtc qemu-usermode"` and
`COMBINED_FEATURES = "${@oe.utils.set_intersect('DISTRO_FEATURES', 'MACHINE_FEATURES', d)}"`.

`include` silently skips a missing file; `require` fails parsing
(bitbake-user-manual-metadata.md: include Directive / require Directive). Both insert the
file at that point, so everything in it is parsed in place.

### What the order means

`local.conf` is parsed **before** the machine and distro configuration. That single fact
explains most surprising results:

| Operator in `local.conf` | Distro/machine file later does | Result |
|---|---|---|
| `VAR = "x"` | `VAR ?= "d"` | `x` (the later `?=` sees a value and does nothing) |
| `VAR = "x"` | `VAR = "d"` | `d` (later plain assignment wins) |
| `VAR ?= "x"` | `VAR ?= "d"` | `x` ("if multiple `?=` assignments … exist, the first of those ends up getting used", bitbake-user-manual-metadata.md: Setting a default value) |
| `VAR += "x"` | `VAR ?= "d"` | `" x"`: the default is lost, because `+=` is immediate and made `VAR` set |
| `VAR:append = " x"` | `VAR ?= "d"` or `VAR = "d"` | `d x`: `:append` is applied when the variable is read |

Same logic between `site.conf` → `auto.conf` → `local.conf`: for `=` the later file wins
(`local.conf`), for `?=` the earlier file wins (`site.conf`).

### Example chain: poky on scarthgap (**source**)

1. `local.conf` (from `meta-poky/conf/templates/default/local.conf.sample`):
   `MACHINE ??= "qemux86-64"`, `DISTRO ?= "poky"`, `EXTRA_IMAGE_FEATURES ?= "debug-tweaks"`,
   `USER_CLASSES ?= "buildstats"`.
2. `conf/machine/${MACHINE}.conf`: machine files usually `require` tune and common include
   files (for example `conf/machine/include/qemu.inc`, which does
   `MACHINEOVERRIDES =. "qemuall:"`, ref-manual/variables.md: MACHINEOVERRIDES). They set
   `MACHINE_FEATURES`, `PREFERRED_PROVIDER_virtual/kernel`, `MACHINE_ESSENTIAL_EXTRA_*`,
   `DEFAULTTUNE`/`TUNE_FEATURES`, `IMAGE_FSTYPES`, `SERIAL_CONSOLES`.
3. `conf/distro/poky.conf`: `DISTRO = "poky"`,
   `DISTRO_FEATURES ?= "${DISTRO_FEATURES_DEFAULT} ${POKY_DEFAULT_DISTRO_FEATURES}"` with
   `POKY_DEFAULT_DISTRO_FEATURES = "opengl ptest multiarch wayland vulkan"`,
   `DISTRO_EXTRA_RDEPENDS += "${POKY_DEFAULT_EXTRA_RDEPENDS}"` (`packagegroup-core-boot`),
   `PACKAGE_CLASSES ?= "package_rpm"`, `INIT_MANAGER ?= "${POKY_INIT_MANAGER}"`
   (`sysvinit`), `PREFERRED_VERSION_linux-yocto ?= "6.6%"`, several `require`d includes,
   `INHERIT += "poky-sanity uninative create-spdx"`.
4. `conf/distro/defaultsetup.conf` (always included, even with an empty `DISTRO`;
   ref-manual/variables.md: DISTRO): includes `default-providers.inc`,
   `default-versions.inc`, `default-distrovars.inc` (which sets
   `DISTRO_FEATURES_DEFAULT ?= "acl alsa bluetooth debuginfod ext2 ipv4 ipv6 pcmcia usbgadget usbhost wifi xattr nfs zeroconf pci 3g nfc x11 vfat seccomp"`
   and `DISTRO_FEATURES ?= "${DISTRO_FEATURES_DEFAULT}"`), `tcmode-${TCMODE}.inc`,
   `tclibc-${TCLIBC}.inc`; sets `PACKAGE_CLASSES ?= "package_ipk"`,
   `INHERIT_DISTRO ?= "debian devshell sstate license remove-libtool create-spdx"`,
   `INHERIT += "${PACKAGE_CLASSES} ${USER_CLASSES} ${INHERIT_DISTRO}"`,
   `INIT_MANAGER ??= "none"` and finally
   `require conf/distro/include/init-manager-${INIT_MANAGER}.inc`.

Note how poky's `DISTRO_FEATURES ?=` references `DISTRO_FEATURES_DEFAULT`, which is only
defined later in `default-distrovars.inc`: that works because `=`/`?=` store the
unexpanded text and `${...}` is expanded when the variable is read
(bitbake-user-manual-metadata.md: Variable Expansion). The `?=` in `default-distrovars.inc`
does nothing because poky already set `DISTRO_FEATURES`.

`init-manager-systemd.inc` (**source**) does
`DISTRO_FEATURES:append = " systemd usrmerge"`,
`DISTRO_FEATURES_BACKFILL_CONSIDERED:append = " sysvinit"` and
`VIRTUAL-RUNTIME_init_manager ??= "systemd"` (plus `initscripts`, `login_manager`,
`dev_manager`). One `INIT_MANAGER = "systemd"` line therefore changes features, backfill,
runtime providers and, through them, packagegroup contents (see commit-impact.md).

## 4. Stage 3 — global classes

After the configuration files, `base.bbclass` is always inherited and every class named in
`INHERIT` is inherited, so they apply to all recipes
(bitbake-user-manual-execution.md; bitbake-user-manual-metadata.md: INHERIT Configuration
Directive). In poky this includes `${PACKAGE_CLASSES}`, `${USER_CLASSES}`,
`${INHERIT_DISTRO}` and anything a user adds, such as `INHERIT += "buildhistory"`.
Since langdale (4.1), global classes live in `classes-global/` and
recipe classes in `classes-recipe/`; `classes/` works in both contexts
(migration-guides/migration-4.1.md).

## 5. Stage 4 — one recipe: recipe, classes, includes, bbappends

"For each file, a fresh copy of the base configuration is made, then the recipe is parsed
line by line. Any inherit statements cause BitBake to find and then parse class files …
Finally, BitBake parses in order any append files found in BBFILES"
(bitbake-user-manual-execution.md: Locating and Parsing Recipes).

So inside an image recipe:

```bitbake
IMAGE_INSTALL = "packagegroup-core-boot ${CORE_IMAGE_EXTRA_INSTALL}"   # parsed 1st
inherit core-image          # core-image.bbclass parsed here: IMAGE_INSTALL ?= ... is a no-op now
IMAGE_INSTALL += "strace"   # parsed after the class: appends to the recipe's value
```

The class is parsed at the `inherit` line; "you can override any values and functions of
the inherited class within your recipe by doing so after the inherit statement"
(bitbake-user-manual-metadata.md: inherit Directive). A `require`d `.inc` behaves as if
pasted in place. The bbappends are parsed after the whole recipe, in the order described in
section 2, and can therefore replace anything the recipe set with plain `=`.

## 6. Stage 5 — finalization

**source** (BitBake 2.8 `lib/bb/parse/ast.py`, `finalize`), after the last append:

1. **Deferred inherits**: classes named with `inherit_defer` (new in 5.0,
   migration-guides/release-notes-5.0.md) are inherited now, at the end of parsing. The
   scarthgap `image.bbclass` uses `inherit_defer ${IMGCLASSES}` (rootfs backend, image
   types, `IMAGE_CLASSES`), so `IMAGE_CLASSES` set anywhere in the image recipe or its
   appends is honored.
2. **Key expansion**: variable *names* containing `${...}` are expanded and may replace an
   existing variable (bitbake-user-manual-metadata.md: Key Expansion).
3. **Anonymous Python** (`python () { ... }`) runs. Image-relevant ones (**source**):
   - `base.bbclass` calls `oe.utils.features_backfill()` for `DISTRO_FEATURES` and
     `MACHINE_FEATURES`: every feature in `*_BACKFILL` that is neither already present nor
     listed in `*_BACKFILL_CONSIDERED` is appended (ref-manual/features.md: Feature
     Backfilling).
   - `image.bbclass` removes features named by `IMAGE_FEATURES_REPLACES_<feature>`, fails on
     `IMAGE_FEATURES_CONFLICTS_<feature>`, rewrites `IMAGE_FEATURES` sorted, and skips the
     recipe if a feature is not valid (not a `FEATURE_PACKAGES_*`, `COMPLEMENTARY_GLOB` flag
     or listed `validitems`).
   - `packagegroup.bbclass` expands `PACKAGES` with `-dbg`, `-dev` (and `-ptest` when the
     `ptest` distro feature is on) and sets `ALLOW_EMPTY` for each.
   - `features_check.bbclass` skips recipes whose `REQUIRED_DISTRO_FEATURES`,
     `ANY_OF_DISTRO_FEATURES` or `CONFLICT_DISTRO_FEATURES` (and machine/image/combined
     variants) are not satisfied (ref-manual/variables.md: REQUIRED_DISTRO_FEATURES).
4. Tasks are added; dependency flags (`deptask`, `rdeptask`, `recrdeptask`, `depends`) are
   evaluated when the task graph is built (bitbake-user-manual-metadata.md: Dependencies).

Values changed by anonymous Python show up in history with the function name in brackets,
for example `append base.bbclass:414 [features_backfill]`.

## 7. Operators: what is immediate and what is deferred

From bitbake-user-manual-metadata.md, sections 3.1.1–3.1.11. The "history op" column is
the word `bitbake -e` / `bitbake-getvar` prints for that operation (**source**, BitBake 2.8
`lib/bb/parse/ast.py` and `data_smart.py`).

| Syntax | Meaning | When it takes effect | History op |
|---|---|---|---|
| `A = "v"` | set | immediately, replaces the current value | `set` |
| `A ?= "v"` | set only if `A` has no value at this point; first `?=` wins | immediately | `set?` |
| `A ??= "v"` | weak default: used only if nothing else assigns `A` by the end of parsing; the last `??=` wins | end of parsing | `set` with `[_defaultval]` |
| `A := "v"` | set, expanding `${...}` now | immediately | `immediate` |
| `A += "v"` / `A =+ "v"` | append / prepend with a space | immediately | `append` / `prepend` |
| `A .= "v"` / `A =. "v"` | append / prepend without a space | immediately | `postdot` / `predot` |
| `A:append = "v"` / `A:prepend = "v"` | append / prepend, no space added | when `A` is read | `:append` / `:prepend` |
| `A:remove = "v"` | remove every whitespace-separated occurrence | when `A` is read | `:remove` |
| `A:<override> = "v"` | replaces `A` if `<override>` is active | when `A` is read | `set` on `A:<override>`, shown under `A` as `override[<override>]:set` |

Rules that matter for analysis:

- Non-override appends do **not** substitute a weak default: `W ??= "x"` then `W += "y"`
  gives `" y"`; but `W:append = "y"` gives `"xy"` (bitbake-user-manual-metadata.md:
  Setting a weak default value).
- "The overrides are applied in this order, `:append`, `:prepend`, `:remove`", so a
  `:remove` cannot be undone with a later `:append`; the history listing order does not
  reflect application order (bitbake-user-manual-metadata.md: Removal).
- Override-style operations are "guaranteed": a class `FOO += "val"` is lost if the recipe
  later does `FOO = "initial"`, while `FOO:append = " val"` survives
  (bitbake-user-manual-metadata.md: Override Style Operation Advantages).
- Combining `:append`/`:remove`/`:prepend` with `+=`, `.=`, `?=` on the same line
  (`A:append += "x"`) triggers the BitBake warning "is not a recommended operator
  combination" (**source**, `ast.py`).
- `unset A` and `A[flag]` exist too (bitbake-user-manual-metadata.md: Unsetting variables,
  Variable Flag Syntax).

## 8. How the final value is computed

When a variable is read, conceptually:

1. Start from the value left by the immediate operations, in parse order (sections 3–5).
   If nothing assigned it, use the weak default (`??=`).
2. **Override selection**: if `A:<o>` exists for an override `<o>` that is in `OVERRIDES`,
   it replaces `A`. `OVERRIDES` is colon-separated and "processed left to right, so the
   ones that are named later take precedence" (**source**, comment above `OVERRIDES` in
   scarthgap `bitbake.conf`). Its default value there is:

   ```text
   OVERRIDES = "${TARGET_OS}:${TRANSLATED_TARGET_ARCH}:pn-${PN}:layer-${FILE_LAYERNAME}:${MACHINEOVERRIDES}:${DISTROOVERRIDES}:${CLASSOVERRIDE}${LIBCOVERRIDE}:forcevariable"
   ```

   so precedence rises from OS, arch, `pn-<recipe>`, `layer-<layername>`, machine overrides
   (`MACHINE` plus anything prepended, e.g. `qemuall`), distro overrides (`DISTRO`),
   class (`class-target`, `class-native`, …), libc (`libc-glibc`), up to `forcevariable`
   (ref-manual/variables.md: OVERRIDES, MACHINEOVERRIDES, DISTROOVERRIDES; PREFERRED_VERSION
   for `forcevariable`; bitbake-user-manual-ref-variables.md: FILE_LAYERNAME).
   Override names are lower-case letters, digits and dashes only
   (bitbake-user-manual-metadata.md: Conditional Metadata). See the live list with
   `bitbake-getvar -r <recipe> OVERRIDES`.
3. Apply `:append`, then `:prepend`, then `:remove` — including conditional ones such as
   `A:append:qemuall`, which apply only when that override is active.
4. Expand `${...}` and `${@...}` references (recursively, with the same rules).

Order of the words matters: `A:foo:append = "X"` appends to the variable `A:foo` (which then
replaces `A` if `foo` is active), whereas `A:append:foo = "X"` appends `X` to `A` only when
`foo` is active (bitbake-user-manual-metadata.md: Examples). With `A = "1"`,
`A:append = "2"`, `A:append = "3"`, `A += "4"`, `A .= "5"`, the result is `1 4523`.

Task-scoped overrides exist too: `FOO:task-compile = "..."` applies only while
`do_compile` runs (bitbake-user-manual-metadata.md: Conditional Metadata), so a variable can
have a different value inside `do_rootfs` than `bitbake -e` shows.

## 9. Ordering pitfalls that change image content

Each item: the mechanism, then how to prove it.

1. **`IMAGE_INSTALL +=` in `local.conf`** — `core-image.bbclass` sets
   `IMAGE_INSTALL ?= "${CORE_IMAGE_BASE_INSTALL}"`; `local.conf` is parsed first, so
   `+=` makes `IMAGE_INSTALL` set and the class default (packagegroup-core-boot,
   packagegroup-base-extended, `CORE_IMAGE_EXTRA_INSTALL`) is never applied
   (ref-manual/variables.md: IMAGE_INSTALL; dev-manual/customizing-images.md). Use
   `IMAGE_INSTALL:append = " pkg"` or `CORE_IMAGE_EXTRA_INSTALL += "pkg"`. Proof:
   `bitbake-getvar -r <image> IMAGE_INSTALL` — the history shows `append …/local.conf`
   followed by a no-op `set?` from `core-image.bbclass`.
2. **`DISTRO_FEATURES +=` in `local.conf`** — same mechanism against poky's
   `DISTRO_FEATURES ?=`: the distro defaults disappear and only the added words plus
   backfilled features remain. Use `DISTRO_FEATURES:append = " x"`.
3. **`IMAGE_FEATURES = "..."` in an image recipe** — `bitbake.conf` already did
   `IMAGE_FEATURES += "${EXTRA_IMAGE_FEATURES}"`; a plain `=` in the recipe replaces it, so
   `EXTRA_IMAGE_FEATURES` from `local.conf` stops applying to that image (derived from the
   scarthgap `bitbake.conf` line and operator semantics; prove with
   `bitbake-getvar -r <image> IMAGE_FEATURES`). Image recipes normally use `+=`
   (`core-image-base.bb`: `IMAGE_FEATURES += "splash"`).
4. **Weak-default `PACKAGECONFIG`** — recipes usually do `PACKAGECONFIG ??= "a b"`; a
   bbappend with `PACKAGECONFIG += "c"` yields `" c"` and silently drops `a b`
   (bitbake-user-manual-metadata.md: weak default). `PACKAGECONFIG:append = " c"` keeps
   them. Each dropped option can remove `DEPENDS`, `RDEPENDS`, `RRECOMMENDS` and configure
   flags (ref-manual/variables.md: PACKAGECONFIG).
5. **Assignments before `inherit`** — in an image recipe, a value set before
   `inherit core-image` beats the class's `?=`; one set after it with `=` beats everything
   the class set with `=`. Moving an `inherit` line in a commit can change results.
6. **`:remove` wins** — a `:remove` anywhere (distro conf, bbappend) beats any `:append`,
   regardless of file order. Search the history for `:remove` before concluding a word
   "should be there".
7. **Higher-priority bbappend** — two appends that both use `=` on the same variable: the
   one parsed last (higher `BBFILE_PRIORITY`, see section 2) wins. A commit that changes a
   layer's priority can flip the winner without touching the append.
8. **`?=` in `site.conf`/`auto.conf`** — CI systems often write `auto.conf`; its `?=`
   beats a later `?=` in `local.conf`, and its `=` is overridden by `local.conf`.
9. **`:=` snapshots** — `A := "${B}"` captures `B` at that line; later changes to `B` do not
   propagate (bitbake-user-manual-metadata.md: Immediate variable expansion).
   `packagegroup.bbclass` uses `PACKAGE_ARCH_EXPANDED := "${PACKAGE_ARCH}"`, so a
   packagegroup must set `PACKAGE_ARCH` before `inherit packagegroup`.
10. **Global vs per-recipe** — a change made with `VAR:pn-<recipe>` in a `.conf` affects only
    that recipe; `bitbake-getvar VAR` without `-r` will not show it.

## 10. Release notes for this material

- Override syntax uses `:` (`IMAGE_INSTALL:append`) since BitBake 1.52 / honister (3.4);
  older documentation and layers use `_append`
  (bitbake-user-manual-metadata.md: Conditional Metadata). scarthgap rejects the old form.
- Some variables keep an underscore because the suffix is part of the variable name, not an
  override: `PREFERRED_PROVIDER_virtual/kernel`, `PREFERRED_VERSION_linux-yocto`,
  `FEATURE_PACKAGES_<feature>`, `BBFILE_PRIORITY_<layer>`, `LAYERSERIES_COMPAT_<layer>`
  (ref-manual/variables.md entries of the same names).
- `inherit_defer` is new in 5.0 (migration-guides/release-notes-5.0.md).
- The include list in section 3 is the scarthgap one; later releases changed parts of
  `bitbake.conf` and the image classes, so re-check them for any other release.

---
Derived from the Yocto Project scarthgap (5.0) documentation, CC BY-SA 2.0 UK.
