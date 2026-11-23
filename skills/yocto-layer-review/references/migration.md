<!-- Generated from references/yocto/migration.md by tools/sync_references.py. Edit the source file, not this copy. -->

# Release Awareness and Migration (Scarthgap Baseline)

This collection is written against Yocto Project 5.0 "scarthgap" (LTS) with BitBake 2.8. Sources: ref-manual "Yocto Project Releases and the Stable Release Process" (chapter 3), migration-guides "Release 5.0 LTS (scarthgap)", "General Migration Considerations", and the 5.0 release notes. Other releases' migration guides are online at https://docs.yoctoproject.org/migration-guides/.

## 1. Release Facts You Can Rely On

- Cadence: a major release roughly every April and October; stable (non-LTS) releases are supported for seven months; a Long Term Support release comes every two years and is supported for four (ref-manual 3.1, 3.5). LTS support started with 3.1 "dunfell".
- Stable branches take bug and security fixes only, not features or generic version upgrades (3.4).
- LTS releases named in the scarthgap manuals: 4.0 "kirkstone", 5.0 "scarthgap" (released April 2024, supported until April 2028), and 6.0 "wrynose" (released May 2026, supported until April 2030, per the latest scarthgap ref-manual 3.5). Kirkstone (April 2022 + four years) has reached end of life.
- Releases between the LTSes: 4.1 langdale, 4.2 mickledore, 4.3 nanbield (before scarthgap); 5.1 styhead, 5.2 walnascar, 5.3 whinlatter (after it; the 5.0.16 release notes mark styhead and walnascar EOL). Version numbers jump at an LTS: there is no 5.4.
- Scarthgap uses the BitBake 2.8 branch (release-notes-5.0 "bitbake: Branch: 2.8"). Scarthgap point releases are 5.0.x; the offline manuals are from 5.0.21.
- Anything newer than this, including whether a release after 6.0 has shipped, is not in these manuals. Do not guess codenames or dates: check https://wiki.yoctoproject.org/wiki/Releases (and https://docs.yoctoproject.org/releases.html) and say you checked.

## 2. Detect the Release from the Build, Not from Memory

```bash
bitbake --version                                  # "BitBake Build Tool Core version 2.8.x" => scarthgap
bitbake-getvar --value DISTRO_VERSION              # e.g. 5.0.x for poky (custom distros set their own)
bitbake-getvar --value LAYERSERIES_CORENAMES       # series name(s) of the OE-Core in use, e.g. "scarthgap"
grep -h LAYERSERIES_COMPAT */conf/layer.conf       # what each layer claims to support
git -C <poky-or-oe-core> branch --show-current     # branch name, if the checkout is a git clone
```

`LAYERSERIES_CORENAMES` is set by OE-Core's `layer.conf` but has no glossary entry; treat it as a hint and cross-check with the branch.

If the user runs an EOL release, say so once, then answer for the release they actually run.

## 3. Syntax Boundaries

| Boundary | Change | What to do |
| --- | --- | --- |
| 3.4 honister (BitBake 1.52) | Override separator `_` replaced by `:` (`FILES:${PN}`, `do_install:append`, `RDEPENDS:${PN}`); the old `_append`/`_prepend`/`_remove` forms fail to parse from 3.4 on (BitBake manual 3.3.1 note). | Convert with `scripts/contrib/convert-overrides.py` from OE-Core, then review: names like `PREFERRED_PROVIDER_virtual/kernel`, `LAYERSERIES_COMPAT_<col>`, `SRCREV_<name>` keep their underscore. Layers for 3.3 hardknott or older use the old syntax. |
| 4.0 kirkstone | `LICENSE_FLAGS_WHITELIST` became `LICENSE_FLAGS_ACCEPTED` and SPDX license identifiers (`GPL-2.0-only`) are expected in `LICENSE` (4.0 migration guide, online only). | Rename variables in distro/local conf; update `LICENSE` strings. |
| 5.0 scarthgap | `CVE_CHECK_IGNORE` deprecated for `CVE_STATUS`; `virtual/` in runtime variables warns. | See section 4. |
| 5.1 styhead (after scarthgap) | Sources unpack into `UNPACKDIR`; git recipes use `S = "${UNPACKDIR}/git"`. | A layer claiming both scarthgap and a 5.1+ series needs per-release handling; keep `S = "${WORKDIR}/git"` on scarthgap. |

## 4. Kirkstone (4.0) to Scarthgap (5.0) Checklist

Read every migration guide in between: 4.1, 4.2, 4.3 and 5.0 (migration-5.0 says so explicitly). Concrete 5.0 items from the scarthgap guide:

- `CVE_CHECK_IGNORE` is deprecated: rewrite as `CVE_STATUS[CVE-ID] = "reason: description"`.
- Removed variables: `DEPLOY_DIR_TAR`, `PYTHON_PN` (use `python3-` directly), `oldincludedir`, `USE_L10N`, `CVE_SOCKET_TIMEOUT`, `SERIAL_CONSOLES_CHECK` (use `SERIAL_CONSOLES`).
- New warning when `virtual/` is used in `RDEPENDS`/`RPROVIDES` (QA `virtual-slash`); use `VIRTUAL-RUNTIME_*`.
- ipk packages now use zstd compression; old target opkg builds without zstd cannot read them. Opkg's internal solver is deprecated (use `libsolv`).
- `DISTRO = "poky"` now adds a warning to `/etc/motd`: Poky is a reference distro, create your own distribution for products (dev-manual "Creating Your Own Distribution").
- ptest now fails at runtime if a ptest returns no results.
- `recipetool` prefixes Python module recipes with `python3-`; `bmap-tools` became `bmaptool`; `scripts/sstate-cache-management.sh` became `sstate-cache-management.py`; `bitbake-whatchanged` was removed.
- systemd: `systemd-resolved` feature now needs the `nss-resolve` PACKAGECONFIG.
- Removed recipes include `linux-yocto` 6.1 (6.6 is provided), `libcroco`, `liberror-perl`, `systemtap-uprobes`, `zvariant`.
- `OLDEST_KERNEL` stays 5.15. Host distro support changed (Rocky 9 added; Fedora 37, Ubuntu 22.10, OpenSUSE Leap 15.3 dropped).
- cve-check no longer fetches remote patches to scan them; CVE IDs in remote patch file names are still picked up.
- `-f{file,macro,debug}-prefix-map` no longer contain `PE`/`PR` (`TARGET_DBGSRC_DIR` added).

## 5. General Migration Rules (migration-general)

- Keep customizations in `.bbappend` files rather than copied recipes; copies break when included `.inc` files change.
- A version-specific `foo_1.2.bbappend` must be renamed (or use `foo_%.bbappend`) when the recipe version changes; otherwise parsing fails because of the dangling append (default fatal, `BB_DANGLINGAPPENDS_WARNONLY`).
- Patches carried in appends may stop applying after a version bump; refresh them (`devtool modify`/`devtool finish`).
- Use buildhistory across the migration: enable it before, build, tag the buildhistory git repo, migrate, rebuild, then `buildhistory-diff` against the tag.
- Every layer's `LAYERSERIES_COMPAT_<col>` must list the target series; add a series only after the layer was built and tested on it.
- Vendor BSP layers often lag OE-Core; check their branch for the target series before modernizing them.

## 6. Validation Ladder (cheapest first)

```bash
bitbake -p                                   # parse everything: syntax, dangling appends, LAYERSERIES_COMPAT
bitbake-layers show-layers
bitbake-layers show-appends
bitbake-getvar -r <critical-recipe> SRC_URI
bitbake -c package_qa <critical-recipe>
bitbake -k <image>                           # see every failure in one run
```

## 7. Migration Review Output

1. detected source and target release (and how you detected them)
2. layers whose `LAYERSERIES_COMPAT` or branch does not match
3. syntax and variable renames required (cite the boundary above)
4. scarthgap-specific items from section 4 that apply
5. the validation commands to run

Derived from the Yocto Project scarthgap (5.0) documentation, CC BY-SA 2.0 UK.
