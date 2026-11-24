---
name: yocto-image-analysis
description: Analyze what a Yocto/OpenEmbedded distro and image actually contain and why, by walking the BitBake evaluation order (bblayers.conf, layer.conf priorities, local.conf/auto.conf, DISTRO and MACHINE conf require chains, image recipe, classes, bbappends, overrides and :append/:remove/?=/??= operators) and the inclusion chain (IMAGE_INSTALL, IMAGE_FEATURES/EXTRA_IMAGE_FEATURES, FEATURE_PACKAGES, packagegroups, RDEPENDS/RRECOMMENDS, DISTRO_FEATURES/MACHINE_FEATURES, backfill, PACKAGECONFIG, PREFERRED_PROVIDER, VIRTUAL-RUNTIME, BAD_RECOMMENDATIONS, PACKAGE_EXCLUDE). Also explains what a commit, branch or layer update changed in the effective configuration and image content, with static diff reading plus bitbake-getvar history, bitbake -e diffs, bitbake-layers, bitbake -g, oe-pkgdata-util, buildhistory/buildhistory-diff and manifest diffs. Use whenever someone asks why a package is (or is not) in an image, what an image or distro includes, where a variable value comes from, what a Yocto commit/upgrade/bbappend/distro change does to the rootfs, or wants a before/after comparison of two builds — even if they only paste a diff or a manifest.
---

# Yocto Image and Distro Analysis

Answer two questions with evidence: **what ends up in this image/distro and why**, and
**what did this change do to it**. Target: Yocto Project 5.0 "scarthgap" / BitBake 2.8;
check the project's release first (`LAYERSERIES_COMPAT_*` in `conf/layer.conf`, the
poky/openembedded-core branch, or `DISTRO_VERSION`). Release-specific facts are flagged
"scarthgap" in the references.

The central idea: a line in a `.conf`, `.bb`, `.bbclass` or `.bbappend` has an effect only
relative to every other assignment of the same variable, in parse order, under the
operator and override rules. Most wrong Yocto answers come from reading a line in
isolation, so reconstruct the order first, then reason, then prove it with a tool.

## Workflow

1. **Pin down the target**: image recipe, `MACHINE`, `DISTRO`, multiconfig, release, layer
   list and revisions, and the Build Directory `conf/` files (`local.conf`, `auto.conf`,
   `site.conf`, `bblayers.conf`). Ask for missing ones; the answer depends on all of them.
   For a commit question, get the diff for every layer repository involved.
2. **Reconstruct the evaluation order** with
   [references/evaluation-order.md](references/evaluation-order.md) (jump to the section
   you need from its Contents). Short form: `bblayers.conf` -> each `layer.conf` ->
   `bitbake.conf` (`site.conf`, `auto.conf`, `local.conf`, then machine and distro conf
   with their includes) -> global classes -> per recipe: recipe lines, then bbappends
   (lowest layer priority first) -> finalization (anonymous Python, backfill) -> overrides,
   then `:append`/`:prepend`/`:remove`. Because `local.conf` is parsed **before** machine and
   distro files, its `?=` and `+=` beat the distro's `?=`, its `=` loses to the distro's
   `=`, and only `:append`/`:remove` behave additively.
3. **Walk the inclusion chain** with [references/inclusion-chain.md](references/inclusion-chain.md):
   `IMAGE_INSTALL` + `IMAGE_FEATURES`/`EXTRA_IMAGE_FEATURES` (`FEATURE_PACKAGES_<f>`) ->
   `PACKAGE_INSTALL` -> package manager resolves `RDEPENDS`/`RRECOMMENDS` (including
   automatic shlib/pkgconfig dependencies), minus `BAD_RECOMMENDATIONS`/`PACKAGE_EXCLUDE`
   -> complementary and locale packages -> manifest. At each packagegroup or recipe, note
   which `DISTRO_FEATURES`, `MACHINE_FEATURES`, `PACKAGECONFIG`, `VIRTUAL-RUNTIME_*` or
   `PREFERRED_PROVIDER_*` decides the content, and keep recipe names and package names apart
   (`oe-pkgdata-util lookup-pkg`, `lookup-recipe`).
4. **Prove it, and say how far you got**
   ([references/evidence-tools.md](references/evidence-tools.md)). Label every conclusion:
   - **Tier 0, static** (sources only): reasoning from the diff and the order. Hypothesis.
   - **Tier 1, parse** (Build Directory, no build): `bitbake-getvar -r <image> VAR` (value
     plus `file:line` history), `bitbake -e`, `bitbake-layers show-*`, `bitbake -g`.
   - **Tier 2, build**: image manifest, buildhistory, `buildhistory-diff`,
     `oe-pkgdata-util`, license manifest, SPDX. The only proof of the installed package list.

   Do not state package-list conclusions as fact from tier 0 or 1; give the command and
   the output that would confirm or refute each hypothesis.
5. **For a commit, branch or upgrade** follow
   [references/commit-impact.md](references/commit-impact.md): classify each changed file
   by parse stage, find competitors and consumers of each changed variable, run its
   indirect-effect checklist, diff the parse (and build) output, tie every difference to a
   diff line through the history, and list diff lines that had no effect.

`scripts/yocto_diff.py` (standard library only) diffs two `bitbake -e` dumps (`env`), two
manifests (`manifest`), and prints why-chains from buildhistory `depends.dot` (`why`);
usage in evidence-tools.md section 8.

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
- Underscore names are not overrides (`PREFERRED_PROVIDER_virtual/kernel`,
  `PREFERRED_VERSION_<pn>`, `FEATURE_PACKAGES_<f>`); scarthgap rejects `_append`.
- Query the right datastore: `bitbake-getvar -r <image>` for image variables; the global
  value can differ.

## Offline lookup

Everything this skill needs is in the repository; it works without internet. Pull only the text you need instead of reading whole files (pages run to thousands of lines). From this skill's folder:

- `python3 scripts/ylookup.py <NAME>...` prints the scarthgap manual entry for any variable, class, task, feature or QA check (`--kind var|class|task|feature|qa` to disambiguate, `--find TEXT` when unsure of the name).
- `--topic TEXT` lists manual sections, `--section <manual/page.md> "<heading>"` prints one, `--grep REGEX [--in ref-manual]` finds anything else.
- URLs in these files are citations for the user, not lookups. The manuals are scarthgap 5.0: if the project is on another release, tell the user rather than going online. Without Python: `` grep -n -A30 '^## Variable `NAME`' references/keywords.md ``.

## Output

For "what is in it / why":

1. target and evidence tier reached
2. the evaluation chain relevant to the question (files in parse order, with the winning
   assignment for each key variable)
3. the inclusion chain for the package(s) in question (`image -> packagegroup -> pkg`, with
   the variable or condition at each edge)
4. commands that confirm each unproven step, and the output that would confirm it
5. manual sections that define the keywords involved (offline path)

For "what did this change do": use the report template in
[references/commit-impact.md](references/commit-impact.md) section 7.
