---
name: yocto-layer-review
description: Create, review and debug Yocto/OpenEmbedded layers and metadata visibility - conf/layer.conf (BBPATH, BBFILES, BBFILE_COLLECTIONS, BBFILE_PATTERN, BBFILE_PRIORITY, LAYERDEPENDS, LAYERSERIES_COMPAT, BBFILES_DYNAMIC), bblayers.conf, BBMASK, bbappend files that are not applied or cause "No recipes available for" errors, overlayed recipes and which layer wins, PREFERRED_PROVIDER/PREFERRED_VERSION selection, and "layer is not compatible with the core layer" errors when moving layers to Yocto 5.0 scarthgap. Use it whenever someone asks why BitBake does not see a recipe or append, which recipe version is picked, how to structure a new meta-* layer, or how to make a layer compatible with a release. For a diff/PR review of layer changes use yocto-change-review; for recipe content use yocto-recipe-review.
---

# Yocto Layer Review

Layer problems look like recipe or package failures. Prove what BitBake sees before changing anything.

## Workflow

1. **Is the layer enabled?** `bitbake-layers show-layers` (name, path, priority). A layer on disk but missing from `conf/bblayers.conf` does not exist for BitBake.
2. **Is it compatible?** `LAYERSERIES_COMPAT_<collection>` must list `scarthgap`; otherwise parsing stops with "Layer ... is not compatible with the core layer". List only series the layer was built and tested on; adding a later series (for example one that unpacks into `UNPACKDIR`) without testing claims compatibility it does not have.
3. **Which recipe wins?** `bitbake-layers show-recipes <pn>` and `show-overlayed`. Same recipe in several layers: higher `BBFILE_PRIORITY_<col>` wins; between versions, `PREFERRED_VERSION_<pn>` (matched against `PV`, `%` only at the end) decides. A recipe with a lower `PV` in a higher-priority layer can still win, and priority does not order `.conf` or `.bbclass` files (dev-manual "Prioritizing Your Layer"). Use provider/version variables for policy, not priority bumps.
4. **Is the append applied?** `bitbake-layers show-appends | grep <pn>`. Rules:
   - `foo_1.2.bbappend` only matches `foo_1.2.bb`; `foo_%.bbappend` matches any version.
   - An append with no matching recipe is a fatal parse error ("No recipes available for ...") by default; it is only a warning if `BB_DANGLINGAPPENDS_WARNONLY = "1"` is set. So a truly silent "not applied" means the append matches a different recipe than the one being built (other provider, other version selected), it is excluded by `BBMASK` or a `BBFILES`/`BBFILES_DYNAMIC` glob, or a devtool workspace recipe shadows it.
   - Several appends for one recipe are applied in layer priority order, so one layer's append can override another's.
5. **Check the value**: `bitbake-getvar -r <pn> <VAR>` shows which append set what.
6. **Fix minimally** and validate with `bitbake -p` (parse only), then `bitbake-layers show-appends`.

The layer.conf template and checklist are in [references/yocto-field-guide.md](references/yocto-field-guide.md) section 7. Keep the underscore in `LAYERSERIES_COMPAT_<col>`, `BBFILE_PATTERN_<col>`, `BBFILE_PRIORITY_<col>`, `LAYERDEPENDS_<col>`, `PREFERRED_PROVIDER_<item>`, `PREFERRED_VERSION_<pn>`: these are variable names, not overrides.

## Common Problems

- layer not in `bblayers.conf`, or `BBFILES` glob that misses the recipe directory
- version-pinned bbappend after a recipe upgrade (fatal parse error)
- append matches a recipe that is not the selected provider or version
- `BBFILES_DYNAMIC` collection name does not match the target layer's `BBFILE_COLLECTIONS`
- priority raised to win a provider conflict instead of `PREFERRED_PROVIDER_*`
- `LAYERSERIES_COMPAT` claiming untested series, or missing `scarthgap`
- vendor BSP layer pinned to an older series with old override syntax
- missing `LAYERDEPENDS` hiding a dependency that only works by accident

Release and migration checks: [references/migration.md](references/migration.md).

## References

- [references/yocto-field-guide.md](references/yocto-field-guide.md): layer.conf template and checklist, parse errors, provider rules.
- [references/variables-core.md](references/variables-core.md): layer variables, underscore-suffixed names, override order.
- [references/migration.md](references/migration.md): release detection and scarthgap migration items.
- [references/keywords.md](references/keywords.md): official scarthgap manual entry for every keyword named here; grep `` ## Variable `NAME` ``. Others: `yocto-manuals` skill.

## Output

1. whether BitBake sees the layer, recipe and append (with the command output that proves it)
2. the exact layer.conf, file name or priority issue
3. minimal fix
4. validation: `bitbake -p`, `bitbake-layers show-appends`, `bitbake-getvar -r <pn> <VAR>`
