# Example: Old Override Modernization

Skill: `yocto-recipe-review`.

## User Prompt

```text
We are moving a layer from dunfell to scarthgap. Convert this: FILES_${PN} += "${bindir}/foo"; do_install_append() { ... }; PREFERRED_VERSION_linux-yocto_mymachine = "5.4%"
```

## Evidence to Request

- target release (scarthgap) and the current parse error, if any
- the full recipe/bbappend and any vendor BSP layers involved

## Bad Answer Pattern

- Converting blindly, including underscore-suffixed variable names (`PREFERRED_VERSION:linux-yocto` is wrong).
- Adding or removing spaces in `:append` values (changes behavior; `:append` adds no space).
- Quoting variable behavior from memory, or reading a whole manual page instead of the one entry.

## Expected Answer Pattern

- State that `:` is required from 3.4 honister on; old `_append` fails to parse on scarthgap.
- Run `scripts/contrib/convert-overrides.py <layer>` and review the diff.
- Result: `FILES:${PN} += "${bindir}/foo"`, `do_install:append() { ... }`, `PREFERRED_VERSION_linux-yocto:mymachine = "6.6%"` (the variable name keeps `_linux-yocto`; only the machine override uses `:`; scarthgap ships linux-yocto 6.6).
- Update `LAYERSERIES_COMPAT_<col>` to `scarthgap` after testing.
- Grounds each keyword claim in the offline manual entry (`python3 scripts/ylookup.py --topic "Conditional Syntax"`, run from the skill folder) and cites it; it does not fetch docs online.

## Validation

```bash
bitbake -p
bitbake-getvar -r <recipe> FILES:<recipe>
bitbake-getvar --value PREFERRED_VERSION_linux-yocto
```
