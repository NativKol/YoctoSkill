# Official Yocto Documentation Map

Use this map to send a question to the right manual and section. URLs below are the scarthgap (5.0) versions; replace `scarthgap` with the user's series for another release, or use `https://docs.yoctoproject.org/` for the latest. The `yocto-manuals` skill holds an offline copy of every scarthgap page (`references/manuals/<manual>/<page>.md`, table of contents in `references/MANUALS.md`). For release status and dates, see `migration.md` (one copy of that information, kept there).

## Manuals

| Manual | URL | Offline folder (yocto-manuals) |
| --- | --- | --- |
| Quick Build | https://docs.yoctoproject.org/scarthgap/brief-yoctoprojectqs/index.html | `brief-yoctoprojectqs/` |
| Overview and Concepts | https://docs.yoctoproject.org/scarthgap/overview-manual/index.html | `overview-manual/` |
| Development Tasks | https://docs.yoctoproject.org/scarthgap/dev-manual/index.html | `dev-manual/` |
| Reference Manual (variables, classes, tasks, QA, features, devtool) | https://docs.yoctoproject.org/scarthgap/ref-manual/index.html | `ref-manual/` |
| BitBake User Manual 2.8 | https://docs.yoctoproject.org/bitbake/2.8/index.html | `bitbake-user-manual/` |
| BSP Developer's Guide | https://docs.yoctoproject.org/scarthgap/bsp-guide/index.html | `bsp-guide/` |
| Linux Kernel Development | https://docs.yoctoproject.org/scarthgap/kernel-dev/index.html | `kernel-dev/` |
| SDK (standard and extensible) | https://docs.yoctoproject.org/scarthgap/sdk-manual/index.html | `sdk-manual/` |
| Test Environment (ptest, testimage, reproducibility) | https://docs.yoctoproject.org/scarthgap/test-manual/index.html | `test-manual/` |
| Contributor Guide (recipe style, patches) | https://docs.yoctoproject.org/scarthgap/contributor-guide/index.html | `contributor-guide/` |
| Security Reference | https://docs.yoctoproject.org/scarthgap/security-reference/index.html | `security-reference/` |
| Profile and Tracing | https://docs.yoctoproject.org/scarthgap/profile-manual/index.html | `profile-manual/` |
| Migration guides and release notes | https://docs.yoctoproject.org/scarthgap/migration-guides/index.html | `migration-guides/` (5.0 only) |

## Route by Problem

| Problem | Read first | Then |
| --- | --- | --- |
| Build setup, host requirements | Quick Build; ref-manual "System Requirements" | dev-manual "Setting Up to Use the Yocto Project" (`start.md`); `oe-init-build-env`, `conf/local.conf`, `conf/bblayers.conf` |
| Operators, overrides, functions, tasks, flags | BitBake manual "Syntax and Operators" (3.1), "Conditional Syntax (Overrides)" (3.3), "Functions" (3.5), "Tasks" (3.6), "Variable Flags" (3.7), "Dependencies" (3.10) | ref-manual `OVERRIDES`; `variables-core.md` |
| What a variable means | ref-manual "Variables Glossary" | BitBake "Variables Glossary"; `bitbake-getvar -r <recipe> VAR` for the real value |
| Writing or reviewing a recipe | dev-manual "Writing a New Recipe" (5), contributor-guide "Recipe Style Guide" (3) | ref-manual "Classes", "Tasks"; BitBake "File Download Support" (fetchers) |
| Fetch, patch, license checksum | BitBake "File Download Support"; ref-manual `do_fetch`, `do_patch` | dev-manual "Working With Licenses" (33.1) |
| QA message | ref-manual "QA Error and Warning Messages" (9) | ref-manual "Classes > insane" (5.61); `qa-errors.md` |
| Build failure, variable values, dependencies, signatures | dev-manual "Debugging Tools and Techniques" (32) | overview-manual "Shared State Cache"; BitBake "Task Checksums and Setscene" (3.12) |
| devtool workflow | ref-manual "devtool Quick Reference" (7) | sdk-manual "Using devtool in Your SDK Workflow" |
| Layers, bbappends | dev-manual "Understanding and Creating Layers" (`layers.md`) | ref-manual `LAYERSERIES_COMPAT`, `BBFILE_PRIORITY`, `BBFILES_DYNAMIC`, `BB_DANGLINGAPPENDS_WARNONLY` |
| Image content, package selection | dev-manual "Customizing Images" (4), "Working with Packages" (`packages.md`) | ref-manual "Images", "Features"; `IMAGE_INSTALL`, `IMAGE_FEATURES` |
| Partitioned images (wic) | dev-manual "Creating Partitioned Images Using Wic" (19) | ref-manual "OpenEmbedded Kickstart (.wks) Reference" (`kickstart.md`) |
| Multiple configurations | dev-manual "Building Images for Multiple Targets Using Multiple Configurations" (12.2) | `BBMULTICONFIG`, `mcdepends` |
| Distro policy, init system | dev-manual "Creating Your Own Distribution" (22), "Selecting an Initialization Manager" (27) | ref-manual "Distro Features" |
| Machine, BSP | BSP Guide; dev-manual "Adding a New Machine" (`new-machine.md`) | ref-manual "Machine Features" |
| Kernel config, fragments, devicetree | kernel-dev "Common Tasks" (2.3 config, 2.6 configuring) | ref-manual classes `kernel`, `kernel-yocto`, `kernel-devicetree`, `kernel-fitimage`, `devicetree`, `uboot-config`, `uboot-sign` |
| SBOM / SPDX | dev-manual "Creating a Software Bill of Materials" (35) | ref-manual class `create-spdx`; `SPDX_*` variables |
| CVE checking | dev-manual "Checking for Vulnerabilities" (34) | ref-manual classes `cve-check`, `vex`; `CVE_STATUS` |
| License compliance and source release | dev-manual "Working With Licenses" (33) | ref-manual classes `license`, `archiver` |
| Build output regressions | dev-manual "Maintaining Build Output Quality" (31, buildhistory) | migration-general "Checking Image / SDK Changes" |
| SDK / eSDK | sdk-manual | ref-manual `do_populate_sdk`, `do_populate_sdk_ext` |
| Testing | test-manual "Testing Packages With ptest", "Performing Automated Runtime Testing" | ref-manual classes `ptest`, `testimage` |
| Upgrading release | migration-guides for each release between source and target | `migration.md` |

## Tools That Changed Around Scarthgap

- Scarthgap sets up a build with `source oe-init-build-env` (Poky) and `bitbake-layers add-layer` / `bitbake-layers layerindex-fetch`. `bitbake-setup` is not part of the scarthgap / BitBake 2.8 manuals; if a user mentions it, they use a later release, so route to that release's docs.
- `bitbake-getvar` is the documented way to inspect values (dev-manual 32.2); prefer it to `bitbake -e | less`.
- Signature tools: the dev-manual (32.5-32.6) uses `bitbake-dumpsig` and `bitbake-diffsigs`; the BitBake manual 3.12 spells the first one `bitbake-dumpsigs`. The installed script is `bitbake-dumpsig`.

## Release Awareness Checklist

- Detect the release from the build (`bitbake --version`, `DISTRO_VERSION`, layer branches) before giving version-specific advice; see `migration.md`.
- Match the docs URL to that release.
- Check migration guides before changing override syntax, class names, variable names, host distro assumptions, or SBOM/CVE tooling.
- Vendor BSP layers may lag OE-Core; check their branch.

Derived from the Yocto Project scarthgap (5.0) documentation, CC BY-SA 2.0 UK.
