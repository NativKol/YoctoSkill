# Grader: commit image impact

The user asks what a three-file commit changes in an image, before building. The tempting
answer just restates each diff line ("adds systemd, removes x11, adds iperf3, enables
openvpn"). The skill should reason through the evaluation order and the indirect effects,
and say which conclusions need a parse or a build to confirm.

## Required to pass

1. `INIT_MANAGER = "systemd"`: explains that it selects
   `conf/distro/include/init-manager-systemd.inc` (via `defaultsetup.conf`), which adds
   `systemd` (and `usrmerge`) to `DISTRO_FEATURES`, stops `sysvinit` being backfilled
   (`DISTRO_FEATURES_BACKFILL_CONSIDERED`) and switches the `VIRTUAL-RUNTIME_*` init
   providers — so sysvinit scripts/packages leave the image and systemd packages arrive.
2. `DISTRO_FEATURES:remove = "pulseaudio"`: notes `pulseaudio` is a backfilled distro
   feature, so removing it via `:remove` does work (`:remove` is applied after backfill's
   append when the variable is read) **or** recommends the documented
   `DISTRO_FEATURES_BACKFILL_CONSIDERED` route; either way it must not ignore backfill.
   It also notes `x11` removal propagates (COMBINED_FEATURES, PACKAGECONFIG defaults,
   recipes requiring x11 being skipped).
3. `PACKAGECONFIG += "openvpn"` in the bbappend: flags that connman's default is set with
   `??=`, so `+=` replaces the default and drops the other default options; recommends
   `PACKAGECONFIG:append = " openvpn"`.
4. Gives tier-1 commands to confirm without building: `bitbake-getvar -r core-image-base
   DISTRO_FEATURES` (history) and/or `bitbake -e` before/after diffs,
   `bitbake-getvar -r connman PACKAGECONFIG`.
5. Says the final package list (including iperf3's automatic shared-library dependencies)
   needs a build, and gives the build-backed comparison: buildhistory/`buildhistory-diff`
   or a manifest diff.

## Automatic fail

- Claims `PACKAGECONFIG += "openvpn"` simply adds one option with no side effect.
- Uses `_append`/`_remove` syntax as correct for scarthgap.
- Presents the exact list of added/removed packages as certain without any build or
  parse evidence.

## Improves the score

- Points out the `wifi` line is a no-op change (same text).
- Mentions `usrmerge` changing file paths in the rootfs.
- Uses or suggests the skill's `yocto_diff.py env` / `manifest` / `why` helpers.
- Notes packagegroup changes affect every image that installs `packagegroup-company`.
