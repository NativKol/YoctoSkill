# Example: bbappend Not Applied

Skill: `yocto-layer-review`.

## User Prompt

```text
My meta-company layer has recipes-core/busybox/busybox_1.35.0.bbappend but none of its changes show up. Why is it not applied?
```

## Evidence to Request

- the append's path and file name, and the recipe version actually selected
- `conf/bblayers.conf` and the layer's `conf/layer.conf`
- `bitbake-layers show-layers`, `bitbake-layers show-recipes busybox`, `bitbake-layers show-appends`
- whether `BB_DANGLINGAPPENDS_WARNONLY` is set (`bitbake-getvar --value BB_DANGLINGAPPENDS_WARNONLY`)

## Bad Answer Pattern

- Raising `BBFILE_PRIORITY` first.
- Assuming the layer is enabled because it exists on disk.
- Saying a version mismatch is silently ignored. By default an append with no matching recipe is a fatal parse error ("No recipes available for ..."); it only becomes a warning when `BB_DANGLINGAPPENDS_WARNONLY = "1"`.
- Quoting variable behavior from memory, or reading a whole manual page instead of the one entry.

## Expected Answer Pattern

- Verify the layer is in `bblayers.conf` and `BBFILES` covers `recipes-*/*/*.bbappend`.
- Compare the append's version with the selected recipe's version. If they differ and the build still parses, check for `BB_DANGLINGAPPENDS_WARNONLY` (the warning is in the parse output). Rename to `busybox_%.bbappend` if any version should match.
- If the append is listed by `show-appends` but has no effect: another append with higher layer priority overrides the same variable, a `BBMASK` entry hides it, or the values are overwritten later (check with `bitbake-getvar`).
- Check `BBFILES_DYNAMIC` collection names for appends under `dynamic-layers/`.
- Grounds each keyword claim in the offline manual entry (`python3 scripts/ylookup.py BB_DANGLINGAPPENDS_WARNONLY BBFILES_DYNAMIC`, run from the skill folder) and cites it; it does not fetch docs online.

## Validation

```bash
bitbake -p
bitbake-layers show-appends | grep -A3 '^busybox'
bitbake-getvar -r busybox SRC_URI
```
