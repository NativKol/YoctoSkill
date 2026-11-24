---
name: yocto-doc-router
description: Answer "which Yocto/BitBake manual, section or release applies" questions - where the official docs for a topic live, which docs version matches the user's branch, how to tell which Yocto release a build uses (bitbake --version, DISTRO_VERSION, LAYERSERIES_COMPAT), whether a release such as scarthgap or kirkstone is still supported, what LTS policy is, and which migration guides to read before upgrading. Use it when the user wants a documentation pointer or release/upgrade orientation rather than a fix, or before quoting release-specific behavior you are unsure of. For actual debugging, recipe, layer, image, kernel or license work, use the focused skill (bitbake-debug, yocto-recipe-review, yocto-layer-review, yocto-image-rootfs, yocto-bsp-kernel, yocto-security-sbom); for the manual text itself use yocto-manuals.
---

# Yocto Doc Router

Route to the smallest correct piece of official documentation for the user's release, and say which release you assumed.

## Workflow

1. **Detect the release from the build** (do not guess):
   ```bash
   bitbake --version                          # BitBake 2.8.x = Yocto 5.0 scarthgap
   bitbake-getvar --value DISTRO_VERSION
   bitbake-getvar --value LAYERSERIES_CORENAMES
   grep -h LAYERSERIES_COMPAT */conf/layer.conf
   ```
   If none is available, say you assume scarthgap (this collection's baseline, and the release of the offline manuals).
2. **Route by problem** with [references/official-doc-map.md](references/official-doc-map.md): it gives the offline page, the section and the `ylookup.py` command that prints it. Quote the section, not the whole page.
3. **Release status and upgrades:** [references/migration.md](references/migration.md) has the LTS policy, the releases named in the scarthgap manuals, the syntax boundaries (3.4 override syntax, 5.1 `UNPACKDIR`) and the kirkstone-to-scarthgap checklist. For anything newer than the manuals, say the offline copy does not cover it and let the user confirm; do not invent codenames or dates.
4. **Hand off** to the focused skill once the user needs a fix.

## Facts Worth Stating Directly

- Scarthgap is Yocto 5.0, an LTS released April 2024 and supported until April 2028, with BitBake 2.8.
- LTS releases come every two years with four years of support; other releases get seven months.
- The latest scarthgap manuals name 6.0 "wrynose" (May 2026, to April 2030) as the other supported LTS.
- `bitbake-setup` is not part of scarthgap; scarthgap builds start with `oe-init-build-env`.

## Offline lookup

Everything this skill needs is in the repository; it works without internet. Pull only the text you need instead of reading whole files (pages run to thousands of lines). From this skill's folder:

- `python3 scripts/ylookup.py <NAME>...` prints the scarthgap manual entry for any variable, class, task, feature or QA check (`--kind var|class|task|feature|qa` to disambiguate, `--find TEXT` when unsure of the name).
- `--topic TEXT` lists manual sections, `--section <manual/page.md> "<heading>"` prints one, `--grep REGEX [--in ref-manual]` finds anything else.
- URLs in these files are citations for the user, not lookups. The manuals are scarthgap 5.0: if the project is on another release, tell the user rather than going online. Without Python: `` grep -n -A30 '^## Variable `NAME`' references/keywords.md ``.

## References

- [references/official-doc-map.md](references/official-doc-map.md): manuals table and problem-to-section routing.
- [references/migration.md](references/migration.md): release facts, detection, migration checklist.

## Output

1. detected or assumed release (and how it was detected)
2. manual and section, with the offline path (URL only as a citation)
3. the local file, log or command that confirms the issue
4. the focused skill to use next, if any
