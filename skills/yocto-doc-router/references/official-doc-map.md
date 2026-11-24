<!-- Generated from references/shared/official-doc-map.md by tools/sync_references.py. Edit the source file, not this copy. -->

# Official Yocto Documentation Map

Use this map to send a question to the right manual and section **offline**. Every page listed here is in the `yocto-manuals` skill folder as Markdown, so no internet access is needed. Pull only the section you need with the skill's lookup script (`python3 scripts/ylookup.py`, run from the skill folder) instead of opening whole pages; some pages are thousands of lines.

- Find a section: `ylookup.py --topic "<words from the heading>"` lists matching headings with their file.
- Read it: `ylookup.py --section <manual>/<page>.md "<heading>"`. Chapter-level headings include every subsection, so pick the narrowest heading from `--topic`.
- Keywords (variables, classes, tasks, features, QA checks): `ylookup.py <NAME>`.

This offline copy is Yocto Project 5.0 "scarthgap" / BitBake 2.8 only. If the project is on another release, tell the user that these manuals may differ for their release rather than looking anything up online. Release status and dates live in `migration.md` (one copy, kept there). Web addresses are given only as citations for the user.

## Manuals

Offline folder: `yocto-manuals/references/manuals/<folder>/` (headings of every page: `yocto-manuals/references/MANUALS.md`).

| Manual | Offline folder | Citation (online) |
| --- | --- | --- |
| Quick Build | `brief-yoctoprojectqs/` | (docs.yoctoproject.org/scarthgap/brief-yoctoprojectqs/) |
| Overview and Concepts | `overview-manual/` | (docs.yoctoproject.org/scarthgap/overview-manual/) |
| Development Tasks | `dev-manual/` | (docs.yoctoproject.org/scarthgap/dev-manual/) |
| Reference Manual (variables, classes, tasks, QA, features, devtool) | `ref-manual/` | (docs.yoctoproject.org/scarthgap/ref-manual/) |
| BitBake User Manual 2.8 | `bitbake-user-manual/` | (docs.yoctoproject.org/bitbake/2.8/) |
| BSP Developer's Guide | `bsp-guide/` | (docs.yoctoproject.org/scarthgap/bsp-guide/) |
| Linux Kernel Development | `kernel-dev/` | (docs.yoctoproject.org/scarthgap/kernel-dev/) |
| SDK (standard and extensible) | `sdk-manual/` | (docs.yoctoproject.org/scarthgap/sdk-manual/) |
| Test Environment (ptest, testimage, reproducibility) | `test-manual/` | (docs.yoctoproject.org/scarthgap/test-manual/) |
| Contributor Guide (recipe style, patches, AI policy) | `contributor-guide/` | (docs.yoctoproject.org/scarthgap/contributor-guide/) |
| Security Reference | `security-reference/` | (docs.yoctoproject.org/scarthgap/security-reference/) |
| Profile and Tracing | `profile-manual/` | (docs.yoctoproject.org/scarthgap/profile-manual/) |
| Migration guides and release notes (5.0 only) | `migration-guides/` | (docs.yoctoproject.org/scarthgap/migration-guides/) |

## Route by Problem

Paths are under `yocto-manuals/references/manuals/`. "Then" names keywords to look up with `ylookup.py <NAME>`.

| Problem | Read first (offline page: section) | Then |
| --- | --- | --- |
| Build setup, host requirements | `brief-yoctoprojectqs/index.md`; `ref-manual/system-requirements.md`: "System Requirements" | `dev-manual/start.md`; `oe-init-build-env`, `conf/local.conf`, `conf/bblayers.conf` |
| Operators, overrides, functions, tasks, flags | `bitbake-user-manual/bitbake-user-manual-metadata.md`: "Syntax and Operators" (3.1), "Conditional Syntax (Overrides)" (3.3), "Functions" (3.5), "Tasks" (3.6), "Variable Flags" (3.7), "Dependencies" (3.10) | `ylookup.py OVERRIDES`; `variables-core.md` |
| What a variable means | `ylookup.py <VAR>` (ref-manual and BitBake glossary entries) | `bitbake-getvar -r <recipe> VAR` for the real value |
| Writing or reviewing a recipe | `dev-manual/new-recipe.md`: "Writing a New Recipe"; `contributor-guide/recipe-style-guide.md`: "Recipe Style Guide" | `ylookup.py --kind class <name>`, `--kind task <do_x>`; `bitbake-user-manual/bitbake-user-manual-fetching.md` (fetchers) |
| Fetch, patch, license checksum | `bitbake-user-manual/bitbake-user-manual-fetching.md`: "File Download Support"; `ylookup.py do_fetch do_patch` | `dev-manual/licenses.md`: "Working With Licenses" |
| QA message | `ylookup.py --kind qa <check>`; `ref-manual/qa-checks.md`: "QA Error and Warning Messages" | `ylookup.py --kind class insane`; `qa-errors.md` |
| Build failure, variable values, dependencies, signatures | `dev-manual/debugging.md`: "Debugging Tools and Techniques" (pick a 32.x subsection with `--topic`) | `overview-manual/concepts.md`: "Shared State Cache"; `bitbake-user-manual-metadata.md`: "Task Checksums and Setscene" |
| devtool workflow | `ref-manual/devtool-reference.md`: "devtool Quick Reference" | `sdk-manual/extensible.md`: "Using devtool in Your SDK Workflow" |
| Layers, bbappends | `dev-manual/layers.md`: "Understanding and Creating Layers" | `ylookup.py LAYERSERIES_COMPAT BBFILE_PRIORITY BBFILES_DYNAMIC BB_DANGLINGAPPENDS_WARNONLY` |
| Image content, package selection | `dev-manual/customizing-images.md`: "Customizing Images"; `dev-manual/packages.md`: "Working with Packages" | `ref-manual/images.md`, `ref-manual/features.md`; `ylookup.py IMAGE_INSTALL IMAGE_FEATURES` |
| Partitioned images (wic) | `dev-manual/wic.md`: "Creating Partitioned Images Using Wic" | `ref-manual/kickstart.md`: "OpenEmbedded Kickstart" |
| Multiple configurations | `dev-manual/building.md`: "Building Images for Multiple Targets Using Multiple Configurations" | `ylookup.py BBMULTICONFIG`; `--grep mcdepends` |
| Distro policy, init system | `dev-manual/custom-distribution.md`: "Creating Your Own Distribution"; `dev-manual/init-manager.md`: "Selecting an Initialization Manager" | `ref-manual/features.md`: "Distro Features" |
| Machine, BSP | `bsp-guide/bsp.md`; `dev-manual/new-machine.md`: "Adding a New Machine" | `ref-manual/features.md`: "Machine Features" |
| Kernel config, fragments, devicetree | `kernel-dev/common.md`: "Common Tasks" (pick the 2.x subsection with `--topic`) | `ylookup.py --kind class kernel kernel-yocto kernel-devicetree kernel-fitimage devicetree uboot-config uboot-sign` |
| SBOM / SPDX | `dev-manual/sbom.md`: "Creating a Software Bill of Materials" | `ylookup.py --kind class create-spdx`; `ylookup.py --find SPDX_` |
| CVE checking | `dev-manual/vulnerabilities.md`: "Checking for Vulnerabilities" | `ylookup.py --kind class cve-check vex`; `ylookup.py CVE_STATUS` |
| License compliance and source release | `dev-manual/licenses.md`: "Working With Licenses" | `ylookup.py --kind class license archiver` |
| Build output regressions | `dev-manual/build-quality.md`: "Maintaining Build Output Quality" (buildhistory) | `migration-guides/migration-general.md` ("Checking Image / SDK Changes") |
| SDK / eSDK | `sdk-manual/` (`--topic` to pick a page) | `ylookup.py do_populate_sdk do_populate_sdk_ext` |
| Testing | `dev-manual/packages.md`: "Testing Packages With ptest"; `test-manual/runtime-testing.md`: "Performing Automated Runtime Testing" | `ylookup.py --kind class ptest testimage` |
| Upgrading release | `migration-guides/migration-5.0.md` (4.3 to 5.0); guides for older steps are not in the offline copy | `migration.md` |

## Tools That Changed Around Scarthgap

- Scarthgap sets up a build with `source oe-init-build-env` (Poky) and `bitbake-layers add-layer` / `bitbake-layers layerindex-fetch`. `bitbake-setup` is not part of the scarthgap / BitBake 2.8 manuals; if a user mentions it, they use a later release: say so, and that the offline manuals here do not cover it.
- `bitbake-getvar` is the documented way to inspect values (dev-manual 32.2); prefer it to `bitbake -e | less`.
- Signature tools: the dev-manual (32.5-32.6) uses `bitbake-dumpsig` and `bitbake-diffsigs`; the BitBake manual 3.12 spells the first one `bitbake-dumpsigs`. The installed script is `bitbake-dumpsig`.

## Release Awareness Checklist

- Detect the release from the build (`bitbake --version`, `DISTRO_VERSION`, layer branches) before giving version-specific advice; see `migration.md`.
- If it is not scarthgap, say that the offline manuals are scarthgap 5.0 and flag answers that may differ.
- Check the migration guide before changing override syntax, class names, variable names, host distro assumptions, or SBOM/CVE tooling.
- Vendor BSP layers may lag OE-Core; check their branch.

Derived from the Yocto Project scarthgap (5.0) documentation, CC BY-SA 2.0 UK.
