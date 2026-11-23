---
name: yocto-image-analysis
description: Analyze what a Yocto/OpenEmbedded distro and image actually contain and why, by walking the BitBake evaluation order (bblayers.conf, layer.conf priorities, local.conf/auto.conf, DISTRO and MACHINE conf require chains, image recipe, classes, bbappends, overrides and :append/:remove/?=/??= operators) and the inclusion chain (IMAGE_INSTALL, IMAGE_FEATURES/EXTRA_IMAGE_FEATURES, FEATURE_PACKAGES, packagegroups, RDEPENDS/RRECOMMENDS, DISTRO_FEATURES/MACHINE_FEATURES, backfill, PACKAGECONFIG, PREFERRED_PROVIDER, VIRTUAL-RUNTIME, BAD_RECOMMENDATIONS, PACKAGE_EXCLUDE). Also explains what a commit, branch or layer update changed in the effective configuration and image content, with static diff reading plus bitbake-getvar history, bitbake -e diffs, bitbake-layers, bitbake -g, oe-pkgdata-util, buildhistory/buildhistory-diff and manifest diffs. Use whenever someone asks why a package is (or is not) in an image, what an image or distro includes, where a variable value comes from, what a Yocto commit/upgrade/bbappend/distro change does to the rootfs, or wants a before/after comparison of two builds — even if they only paste a diff or a manifest.
---

# Yocto Image and Distro Analysis

Answer two questions with evidence: **what ends up in this image/distro and why**, and
**what did this change do to it**. Target release: Yocto Project 5.0 "scarthgap" /
BitBake 2.8 (still check the project's release first — `LAYERSERIES_COMPAT_*` in
`conf/layer.conf`, the poky/openembedded-core branch, or `DISTRO_VERSION`). Facts that
differ in other releases are flagged "scarthgap" in the references.

The central idea: a line in a `.conf`, `.bb`, `.bbclass` or `.bbappend` has an effect only
relative to every other assignment of the same variable, in parse order, under the
operator and override rules. Most wrong Yocto answers come from reading a line in
isolation. So reconstruct the order first, then reason, then prove it with a tool.

## Workflow

### 1. Pin down the target

Image recipe, `MACHINE`, `DISTRO`, multiconfig, release, layer list and revisions, and the
Build Directory `conf/` files (`local.conf`, `auto.conf`, `site.conf`, `bblayers.conf`).
Ask for them if missing — the answer depends on all of them. For a commit question, get the
diff for every layer repository involved, not just one.

### 2. Reconstruct the evaluation order

Read [references/evaluation-order.md](references/evaluation-order.md). In short, for
scarthgap:

```text
bblayers.conf -> each layer.conf (BBPATH, BBFILES, BBFILE_PRIORITY, LAYERSERIES_COMPAT)
-> bitbake.conf: site.conf, auto.conf, local.conf, machine/${MACHINE}.conf (+ its require'd tune/include files),
   distro/${DISTRO}.conf (+ includes), distro/defaultsetup.conf (+ init-manager-${INIT_MANAGER}.inc)
-> base.bbclass + INHERIT classes (PACKAGE_CLASSES, USER_CLASSES, INHERIT_DISTRO, buildhistory...)
-> per recipe: fresh copy, recipe lines in order (inherit/require/include inline), bbappends (lowest layer priority first)
-> finalize: inherit_defer, key expansion, anonymous Python (feature backfill, IMAGE_FEATURES checks, packagegroup PACKAGES)
-> reading a variable: value from immediate ops (or ??= default) -> active override wins -> :append, :prepend, :remove -> expand ${}
```

`local.conf` is parsed **before** the machine and distro files: its `?=` and `+=` beat the
distro's `?=`, its `=` loses to the distro's `=`, and only `:append`/`:remove` behave
"additively" from there. Keep that in mind for every conf change.

### 3. Walk the inclusion chain

Read [references/inclusion-chain.md](references/inclusion-chain.md). Trace from the image
recipe outward:

`IMAGE_INSTALL` (core-image default `packagegroup-core-boot packagegroup-base-extended ${CORE_IMAGE_EXTRA_INSTALL}`)
+ `IMAGE_FEATURES`/`EXTRA_IMAGE_FEATURES` → `FEATURE_PACKAGES_<f>` + `run-postinsts`
→ `PACKAGE_INSTALL` → package manager resolves `RDEPENDS`/`RRECOMMENDS` (including
automatic shlib/pkgconfig dependencies), `RPROVIDES`, conflicts, minus
`BAD_RECOMMENDATIONS`/`NO_RECOMMENDATIONS`/`PACKAGE_EXCLUDE` → complementary
(`dev-pkgs`…) and locale packages → manifest.

At each packagegroup or recipe, note which `DISTRO_FEATURES`, `MACHINE_FEATURES`,
`COMBINED_FEATURES`, `PACKAGECONFIG`, `VIRTUAL-RUNTIME_*` or `PREFERRED_PROVIDER_*`
decides the content. Keep recipe names, recipe-space package names and runtime package
names apart (`oe-pkgdata-util lookup-pkg`, `lookup-recipe`).

### 4. Prove it — and say how far you got

Read [references/evidence-tools.md](references/evidence-tools.md). Label every conclusion
with its tier:

- **Tier 0, static** (only sources): reasoning from the diff and the order. Hypothesis.
- **Tier 1, parse** (Build Directory, no build): `bitbake-getvar -r <image> VAR` (value
  plus history with `file:line` of each operation), `bitbake -e <image>`,
  `bitbake-layers show-layers|show-appends|show-overlayed|show-recipes`,
  `bitbake -g <image>` (`pn-buildlist`, `task-depends.dot`). Confirms values, recipe and
  append selection, and the recipe set.
- **Tier 2, build**: image manifest in `DEPLOY_DIR_IMAGE`, buildhistory
  (`installed-package-names.txt`, `depends.dot`, `image-info.txt`, `files-in-image.txt`),
  `buildhistory-diff`, `oe-pkgdata-util`, license manifest, SPDX. The only proof of the
  installed package list, automatic dependencies and file contents.

Do not state package-list conclusions as fact from tier 0 or 1; give the command that
would confirm them. When you cannot run commands, give the user the exact commands and
what output would confirm or refute each hypothesis.

### 5. For a commit, branch or upgrade

Follow [references/commit-impact.md](references/commit-impact.md): classify each changed
file by parse stage, find competitors and consumers of each changed variable, run the
indirect-effect checklist (features and backfill, operator/position changes, weak
defaults, `:remove`, overrides, layer priority/`BBMASK`, providers, packagegroups,
packaging, version bumps with new shlib dependencies, image features, exclusions,
package backend), then diff the parse output and, if possible, the build output. Tie every
observed difference to a diff line through the `file:line` history, and list diff lines
that had no effect.

## Helper script

`scripts/yocto_diff.py` (Python 3 standard library only; tests in
`scripts/test_yocto_diff.py`):

```bash
python3 scripts/yocto_diff.py env before.env after.env --only '^(IMAGE_|DISTRO_FEATURES|PACKAGE_INSTALL|PREFERRED_)'
python3 scripts/yocto_diff.py manifest old.manifest new.manifest      # or installed-package-names.txt
python3 scripts/yocto_diff.py why <buildhistory image dir>/depends.dot <package>
```

`env` diffs two `bitbake -e` dumps and prints, for each changed variable, the words
added/removed and the last history operations (`op file:line`). `manifest` diffs package
lists. `why` prints the chains that pull a package in (`->` RDEPENDS, `~>` RRECOMMENDS,
`=>` via RPROVIDES). All accept `--json`.

## Traps to check every time

- `IMAGE_INSTALL +=` or `DISTRO_FEATURES +=` in `local.conf`/`auto.conf` wipes the
  class/distro `?=` default; `:append` does not.
- `IMAGE_FEATURES = "..."` in an image recipe discards `EXTRA_IMAGE_FEATURES` (which
  `bitbake.conf` added with `+=`).
- `PACKAGECONFIG ??=` default plus `PACKAGECONFIG += "x"` in a bbappend drops the default.
- `:remove` is applied after every `:append`, regardless of file order.
- Removing a backfilled feature (`pulseaudio`, `sysvinit`, `gobject-introspection-data`,
  `ldconfig`; machine: `rtc`, `qemu-usermode`) needs `*_BACKFILL_CONSIDERED`.
- `BAD_RECOMMENDATIONS`/`NO_RECOMMENDATIONS` cannot remove a package something
  `RDEPENDS` on (and do nothing with DEB); `PACKAGE_EXCLUDE` then fails the build.
- `DEPENDS` never installs anything; but a library found at build time becomes an
  automatic `RDEPENDS`.
- Underscore names are not overrides: `PREFERRED_PROVIDER_virtual/kernel`,
  `PREFERRED_VERSION_<pn>`, `FEATURE_PACKAGES_<f>`; colon is the override/operator syntax
  since honister (3.4), and scarthgap rejects `_append`.
- Query the right datastore: `bitbake-getvar -r <image>` for image variables; the global
  value can differ.

## Keyword reference

[references/keywords.md](references/keywords.md) holds the verbatim scarthgap manual
glossary entries for every variable, class, task and feature used here. Look a keyword up
there before relying on memory; if it is missing, use the `yocto-manuals` skill, or
`https://docs.yoctoproject.org/scarthgap/ref-manual/variables.html` and
`https://docs.yoctoproject.org/bitbake/2.8/`.

## Output

For "what is in it / why":

1. target and evidence tier reached
2. the evaluation chain relevant to the question (files in parse order, with the winning
   assignment for each key variable)
3. the inclusion chain for the package(s) in question (`image -> packagegroup -> pkg`, with
   the variable or condition at each edge)
4. commands that confirm each unproven step, and the output that would confirm it
5. manual sections that define the keywords involved

For "what did this change do": use the report template in
[references/commit-impact.md](references/commit-impact.md) — effective changes with
`file:line`, image content changes with why-chains, lines with no effect, open risks with
confirming commands.
