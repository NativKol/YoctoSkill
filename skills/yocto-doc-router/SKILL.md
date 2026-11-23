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
   If none is available, say you assume scarthgap (this collection's baseline) and use the scarthgap docs URLs.
2. **Route by problem** with [references/official-doc-map.md](references/official-doc-map.md): it gives the manual, the section and the offline path in the `yocto-manuals` skill.
3. **Release status and upgrades:** [references/migration.md](references/migration.md) has the LTS policy, the releases named in the scarthgap manuals, the syntax boundaries (3.4 override syntax, 5.1 `UNPACKDIR`) and the kirkstone-to-scarthgap checklist. For anything newer than the manuals, check https://wiki.yoctoproject.org/wiki/Releases and say that you did; do not invent codenames or dates.
4. **Hand off** to the focused skill once the user needs a fix.

## Facts Worth Stating Directly

- Scarthgap is Yocto 5.0, an LTS released April 2024 and supported until April 2028, with BitBake 2.8.
- LTS releases come every two years with four years of support; other releases get seven months.
- The latest scarthgap manuals name 6.0 "wrynose" (May 2026, to April 2030) as the other supported LTS.
- `bitbake-setup` is not part of scarthgap; scarthgap builds start with `oe-init-build-env`.

## References

- [references/official-doc-map.md](references/official-doc-map.md): manuals table and problem-to-section routing.
- [references/migration.md](references/migration.md): release facts, detection, migration checklist.
- [references/keywords.md](references/keywords.md): official scarthgap manual entry for every keyword named here; grep `` ## Variable `NAME` ``. Other keywords and full pages: `yocto-manuals` skill.

## Output

1. detected or assumed release (and how it was detected)
2. manual and section, with URL for that release
3. the local file, log or command that confirms the issue
4. the focused skill to use next, if any
