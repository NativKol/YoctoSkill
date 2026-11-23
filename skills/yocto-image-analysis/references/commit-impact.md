# Commit Impact Analysis: What Did This Change Do to the Image? (scarthgap 5.0)

A procedure for explaining a commit (or a range, or two branches) in terms of its effect on
the final configuration and image content, and for tracing every observed difference back
to a line of the diff. Built on evaluation-order.md (when a line takes effect),
inclusion-chain.md (how values become packages) and evidence-tools.md (how to prove it).

The workflow follows the Yocto Project's own advice for watching build output quality:
record build history and compare builds, because "subtle changes can occur that you might
not detect until later" (dev-manual/build-quality.md: Maintaining Build Output Quality).

## Contents

1. Inputs to collect
2. Static path (tier 0): read the diff in evaluation order
3. Parse path (tier 1): diff the datastores without building
4. Build path (tier 2): diff what was installed
5. Indirect-effect checklist
6. What each tier can and cannot conclude
7. Report template
8. Worked examples

---

## 1. Inputs to collect

- The diff: `git log --stat A..B` and `git diff A..B` **in every layer repository**, not
  only the one the user mentions. Projects pinned by a manifest (repo, kas, submodules, a
  `bblayers.conf` template) can change several layers in one "commit"; buildhistory's
  `metadata-revs` and `build-id.txt` list the layer revisions actually used.
- The target: image name, `MACHINE`, `DISTRO`, multiconfig if any. A change can affect one
  machine and not another.
- The Build Directory files outside git: `conf/local.conf`, `conf/auto.conf`,
  `conf/site.conf`, `conf/bblayers.conf`. They are parsed too and often differ between a
  developer machine and CI.
- Existing evidence: old and new image manifests, buildhistory, `bitbake -e` dumps, logs.

## 2. Static path (tier 0)

Classify each changed file by the stage at which it is parsed, then reason in that order.

| Changed path | Stage (evaluation-order.md) | Blast radius |
|---|---|---|
| `conf/bblayers.conf`, a layer's `conf/layer.conf` | 1 — layers | which recipes/appends exist, priorities, compat; everything |
| `conf/site.conf`, `auto.conf`, `local.conf` | 2 — before machine/distro | every recipe for this build dir |
| `conf/machine/*.conf`, `conf/machine/include/*.inc` | 2 — machine | every recipe for that `MACHINE`; `MACHINEOVERRIDES`, tunes, `MACHINE_FEATURES` |
| `conf/distro/*.conf`, `conf/distro/include/*.inc` | 2 — distro | every recipe for that `DISTRO`; features, providers, init manager |
| `classes-global/*.bbclass`, classes in `INHERIT` | 3 — global classes | every recipe |
| `classes-recipe/*.bbclass`, `classes/*.bbclass` | 4 — at each `inherit` | every recipe inheriting it (`bitbake-layers show-recipes -i <class>`) |
| image recipe `*.bb` / its `.inc` | 4 — that image | that image (and images that `require` it) |
| `packagegroup-*.bb` | 4 — that recipe | every image installing that group |
| other `*.bb` / `*.inc` | 4 — that recipe | its packages in every image; dependents via shlibdeps |
| `*.bbappend` | 4 — after its recipe | that recipe, ordered by layer priority |
| `files/`, patches, `SRC_URI` / `SRCREV` / `PV` bumps | build | contents and auto-dependencies of that recipe's packages |

For each changed assignment, write down:

1. **Variable and scope**: global or recipe; any override (`:pn-x`, `:<machine>`,
   `:class-target`, `:task-*`) and whether it is active (`OVERRIDES`).
2. **Operator** and therefore when it applies (evaluation-order.md section 7).
3. **Competitors**: every other assignment to the same variable that is parsed before or
   after it — `git grep -n '^VAR\b\|^VAR:' $(all layers)` plus the class defaults. Decide
   who wins with the tables in evaluation-order.md sections 3 and 8.
4. **Consumers**: who reads this variable: search all layers for `${VAR}` and for
   `'VAR'` inside `bb.utils.contains(...)`, `bb.utils.contains_any(...)` and
   `bb.utils.filter(...)` (for example `git grep -nF '${VAR}'` and
   `git grep -n "contains[_any]*('VAR'\|filter('VAR'"`). Repeat for
   variables derived from it (for example `DISTRO_FEATURES` → `COMBINED_FEATURES`,
   `PACKAGECONFIG` defaults, `REQUIRED_DISTRO_FEATURES` skips).
5. **Package effect**: which packagegroups, `RDEPENDS`, `RRECOMMENDS`, `PACKAGECONFIG`
   options, providers or `IMAGE_FEATURES` change, and therefore which packages should
   appear or disappear (inclusion-chain.md).

The result is a set of **hypotheses** with a predicted mechanism each. Mark them as such.

## 3. Parse path (tier 1): no build needed

Run the same queries at the old and the new revision (check out both, or use two
worktrees; keep `conf/` identical between the two runs unless the conf change is the
subject):

```bash
# 1. Full datastore of the image, before and after
git -C <layer> checkout A && bitbake -e <image> > /tmp/A.env
git -C <layer> checkout B && bitbake -e <image> > /tmp/B.env
python3 scripts/yocto_diff.py env /tmp/A.env /tmp/B.env \
    --only '^(IMAGE_|EXTRA_IMAGE_FEATURES|PACKAGE_INSTALL|PACKAGE_EXCLUDE|BAD_RECOMMENDATIONS|NO_RECOMMENDATIONS|DISTRO_FEATURES|MACHINE_FEATURES|COMBINED_FEATURES|MACHINEOVERRIDES|DISTROOVERRIDES|OVERRIDES|PREFERRED_|VIRTUAL-RUNTIME|INIT_MANAGER|PACKAGE_CLASSES|INHERIT|CORE_IMAGE_EXTRA_INSTALL|FEATURE_PACKAGES_)'

# 2. The same for every recipe the static path flagged (packagegroups, PACKAGECONFIG users)
bitbake -e packagegroup-core-boot > A.pg.env     # ... and B
python3 scripts/yocto_diff.py env A.pg.env B.pg.env --only '^(RDEPENDS|RRECOMMENDS|PACKAGECONFIG|DEPENDS|PACKAGES)'

# 3. One variable with full history (which line won)
bitbake-getvar -r <image> IMAGE_FEATURES

# 4. Recipe set and append application
bitbake -g <image> && cp pn-buildlist A.pn-buildlist      # ... and B; then diff
bitbake-layers show-appends > A.appends                    # ... and B; then diff
bitbake-layers show-overlayed > A.overlayed                # ... and B; then diff
```

Map each changed variable to a diff line using the `history:` lines that
`yocto_diff.py env` prints: the `file:line` of the last effective operation in B is
usually the commit's line; if the commit's line does not appear in the history at all, it
never took effect (masked file, inactive override, overwritten later, `?=` that lost).

## 4. Build path (tier 2): what was really installed

```bash
# local.conf (both builds): INHERIT += "buildhistory"  BUILDHISTORY_COMMIT = "1"
git -C <layer> checkout A && bitbake <image>
git -C <layer> checkout B && bitbake <image>
buildhistory-diff -p buildhistory                 # previous build vs last build
python3 scripts/yocto_diff.py manifest A.manifest B.manifest
python3 scripts/yocto_diff.py why buildhistory/images/<arch>/<libc>/<image>/depends.dot <new-package>
oe-pkgdata-util read-value RDEPENDS <package>     # includes automatic shlib dependencies
```

Without buildhistory, copy `${DEPLOY_DIR_IMAGE}/<image>-<machine>.rootfs.manifest` after
each build (the symlink is replaced by the next build). For a range of commits, build
selected points and use `buildhistory-diff <rev1> <rev2>` between buildhistory commits.

For each added or removed package, find the chain with `why` (in the build that has it),
then find the edge in that chain that changed — a packagegroup `RDEPENDS`, a
`PACKAGECONFIG` option (check `bitbake -e <recipe>` diff), an automatic shlib dependency
(new `RDEPENDS` in `read-value` or buildhistory `packages/.../latest`, with no metadata
change), or a provider switch.

## 5. Indirect-effect checklist

Go through this list for every commit; each item is a way a small diff changes a lot.

- [ ] **Feature lists**: does the change touch `DISTRO_FEATURES`, `MACHINE_FEATURES`,
      `INIT_MANAGER`, an `init-manager-*.inc`, or `*_BACKFILL_CONSIDERED`? Then follow
      `COMBINED_FEATURES`, every `bb.utils.contains/filter` on it, `PACKAGECONFIG`
      defaults, `features_check` skips, and packagegroup conditionals.
- [ ] **Backfill**: removing `pulseaudio`, `sysvinit`, `gobject-introspection-data` or
      `ldconfig` from `DISTRO_FEATURES` has no effect unless it is also in
      `DISTRO_FEATURES_BACKFILL_CONSIDERED`; same for `rtc`, `qemu-usermode` with
      `MACHINE_FEATURES_BACKFILL_CONSIDERED` (ref-manual/features.md: Feature Backfilling;
      scarthgap backfill lists from `bitbake.conf`, **source**).
- [ ] **Operator/position**: did a `:append` become `+=`, a `=` become `?=`, a line move
      above an `inherit`, or a value move from distro conf to `local.conf` (parsed earlier)?
      (evaluation-order.md section 9).
- [ ] **Weak defaults**: `+=`/`=` added to a variable whose default is `??=`
      (`PACKAGECONFIG`, many `VIRTUAL-RUNTIME_*`) replaces the default entirely.
- [ ] **`:remove`**: a new `:remove` beats every `:append`, wherever it is.
- [ ] **Overrides**: a new or changed `MACHINEOVERRIDES`/`DISTROOVERRIDES` entry activates
      or deactivates every `VAR:<override>` in all layers (`git grep ':<override>\b'`).
- [ ] **Layers**: added/removed layer, `BBFILE_PRIORITY` change, `BBMASK` change,
      `BBFILES_DYNAMIC` now matching, `LAYERSERIES_COMPAT`: changes which recipe and
      which appends are used, and the order of appends.
- [ ] **Providers**: `PREFERRED_PROVIDER_*`, `PREFERRED_VERSION_*`, `VIRTUAL-RUNTIME_*`,
      `DEFAULT_PREFERENCE`, a new recipe that `PROVIDES`/`RPROVIDES` an existing name.
- [ ] **Packagegroups**: membership changes propagate to every image using the group;
      check `-dev`/`-dbg`/`-ptest` complements and `RRECOMMENDS` vs `RDEPENDS`.
- [ ] **Packaging**: `PACKAGES`/`FILES`/`ALLOW_EMPTY`/`RPROVIDES` changes can move files
      between packages or create/drop a package that is installed by name.
- [ ] **Version bumps** (`PV`, `SRCREV`, new recipe version): new linked libraries mean new
      automatic `RDEPENDS` (overview-manual/concepts.md: Automatically Added Runtime
      Dependencies); only a build shows them.
- [ ] **Image features**: `IMAGE_FEATURES` `=` vs `+=`, `EXTRA_IMAGE_FEATURES`,
      `FEATURE_PACKAGES_*`, `IMAGE_FEATURES_REPLACES_*`, `COMPLEMENTARY_GLOB`.
- [ ] **Exclusions**: `BAD_RECOMMENDATIONS`, `NO_RECOMMENDATIONS`, `PACKAGE_EXCLUDE`,
      `PACKAGE_EXCLUDE_COMPLEMENTARY` — and their limits (inclusion-chain.md section 6).
- [ ] **Package backend**: `PACKAGE_CLASSES` change switches rpm/ipk/deb; recommendation
      handling differs (DEB ignores `BAD_RECOMMENDATIONS`/`NO_RECOMMENDATIONS`).
- [ ] **Postprocessing**: `ROOTFS_POSTPROCESS_COMMAND`, `IMAGE_POSTPROCESS_COMMAND`,
      `read-only-rootfs`, `debug-tweaks` change files, not packages — compare
      `files-in-image.txt`.

## 6. What each tier can and cannot conclude

| Question | Tier 0 (static) | Tier 1 (parse) | Tier 2 (build) |
|---|---|---|---|
| Did this line take effect? | hypothesis | **yes**, via history | — |
| Final value of a variable for this image/recipe | hypothesis | **yes** | — |
| Which recipe/version/append is used | hypothesis | **yes** (`bitbake-layers`, `-e`) | — |
| Which recipes are built for the image | hypothesis | **yes** (`pn-buildlist`, upper bound) | — |
| Which packages are installed | hypothesis | partial (explicit lists only) | **yes** (manifest) |
| Automatic shlib/pkgconfig dependencies | no | no | **yes** (pkgdata, buildhistory) |
| Effect of `BAD_RECOMMENDATIONS`/conflicts/`RPROVIDES` choice | hypothesis | no | **yes** |
| Files, sizes, permissions in the rootfs | no | no | **yes** (`files-in-image.txt`) |
| Licenses / SBOM of the result | no | partial | **yes** (license manifest, SPDX) |

State the tier next to every conclusion. Never present a tier-0 prediction about package
lists as fact; say which command would confirm it.

## 7. Report template

```markdown
## Scope
Commit(s) / range, layers and revisions, image, MACHINE, DISTRO, evidence tier reached.

## Effective changes
| # | Diff line (file:line) | Variable / recipe | Mechanism | Effect on final value | Tier |

## Image content changes
| Package | Added/removed/changed | Chain (why) | Caused by change # | Tier |

## Changes with no effect
Lines that do not take effect, and why (overwritten, inactive override, masked, lost ?=).

## Risks and open questions
Indirect effects not yet confirmed, with the exact command that would confirm each.
```

## 8. Worked examples

### 8.1 `INIT_MANAGER = "systemd"` added to a distro conf (or `local.conf`)

- Stage 2. `defaultsetup.conf` ends with
  `require conf/distro/include/init-manager-${INIT_MANAGER}.inc` (**source**), so the
  systemd include is parsed. It appends `systemd usrmerge` to `DISTRO_FEATURES`, appends
  `sysvinit` to `DISTRO_FEATURES_BACKFILL_CONSIDERED` (so `sysvinit` is no longer
  backfilled), and sets `VIRTUAL-RUNTIME_init_manager ??= "systemd"` and related
  `VIRTUAL-RUNTIME_*`.
- Consumers: `packagegroup-core-boot` drops `${SYSVINIT_SCRIPTS}`, `init-ifupdown`
  recommendations (they depend on `sysvinit` in `DISTRO_FEATURES`), and its
  `${VIRTUAL-RUNTIME_init_manager}` / `_dev_manager` now resolve to systemd packages;
  `packagegroup.bbclass` fails parsing if `VIRTUAL-RUNTIME_init_manager` names an init
  system missing from `DISTRO_FEATURES` (**source**). `usrmerge` changes install paths
  (`root_prefix` in `bitbake.conf`), so `files-in-image.txt` changes broadly.
  `PACKAGECONFIG` defaults that test `systemd` flip in many recipes.
- Confirm: `bitbake-getvar -r <image> DISTRO_FEATURES` (history shows
  `:append init-manager-systemd.inc:<line>`), then build and diff manifests.
- In poky, `local.conf` `INIT_MANAGER = "systemd"` wins over poky.conf's
  `INIT_MANAGER ?= "${POKY_INIT_MANAGER}"` because `local.conf` is parsed first.

### 8.2 `DISTRO_FEATURES:remove = "x11"` in a distro conf

- `:remove` is applied last, so no `:append` elsewhere can bring `x11` back.
- `COMBINED_FEATURES` loses `x11`; recipes with `REQUIRED_DISTRO_FEATURES = "x11"` are
  skipped, so an image that installs one of their packages now fails when BitBake builds
  the task graph, with an error naming the skipped recipe and the missing distro feature; `PACKAGECONFIG` defaults using
  `bb.utils.filter('DISTRO_FEATURES', 'x11 ...')` lose their `x11` option, dropping
  `DEPENDS`/`RDEPENDS` on X libraries.
- Confirm: `yocto_diff.py env` on `bitbake -e <recipe>` for affected recipes
  (`PACKAGECONFIG`, `DEPENDS`), `bitbake -g` `pn-buildlist` diff, then manifest diff.

### 8.3 A packagegroup gains `RDEPENDS:${PN} += "htop"`

- Every image that installs that packagegroup gains `htop` and its runtime dependencies
  (for example its ncurses libraries through shlibdeps — tier 2 only).
- Confirm: `bitbake-getvar -r <packagegroup> RDEPENDS:<packagegroup>`; after the build,
  `yocto_diff.py why depends.dot htop` shows `packagegroup-x -> htop`.

### 8.4 New bbappend in a higher-priority layer sets `PACKAGECONFIG = "foo"`

- The append is parsed after the recipe and after lower-priority appends, so it replaces
  the recipe's `??=` default and any lower-priority append's `+=`. Options that were on by
  default are now off; their runtime dependencies disappear from images.
- Confirm: `bitbake-layers show-appends <pn>`, `bitbake-getvar -r <pn> PACKAGECONFIG`
  (history shows the append's `set` last), then build.

### 8.5 `IMAGE_INSTALL += "htop"` added to CI's `auto.conf`

- `auto.conf` is parsed before the image recipe; for any image relying on the
  `core-image` default (`IMAGE_INSTALL ?=`), the default is lost and the image contains only
  `htop`, `run-postinsts` and feature packages — the boot packagegroups disappear.
  Images that set `IMAGE_INSTALL = ...` themselves (for example `core-image-minimal`)
  overwrite it, so `htop` is missing there instead. Fix: `IMAGE_INSTALL:append = " htop"`
  (ref-manual/variables.md: IMAGE_INSTALL).

---
Derived from the Yocto Project scarthgap (5.0) documentation, CC BY-SA 2.0 UK.
