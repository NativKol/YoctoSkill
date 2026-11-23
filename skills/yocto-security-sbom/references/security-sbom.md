<!-- Generated from references/yocto/security-sbom.md by tools/sync_references.py. Edit the source file, not this copy. -->

# Yocto License, CVE, SBOM, and Source Compliance (Scarthgap)

Release: Yocto Project 5.0 "scarthgap". Sources: dev-manual "Working With Licenses" (33), "Checking for Vulnerabilities" (34), "Creating a Software Bill of Materials" (35); ref-manual classes `license`, `create-spdx`, `cve-check`, `vex`, `archiver`; variables `LICENSE`, `LIC_FILES_CHKSUM`, `LICENSE_FLAGS`, `INCOMPATIBLE_LICENSE`, `CVE_STATUS`, `SPDX_*`; contributor-guide "Recipe Style Guide" (3.5.3 license fields, 3.7 CVE patches); migration-5.0. Do not give legal advice: give the metadata, the artifacts, and what a compliance reviewer must check.

## 1. Scarthgap Defaults at a Glance

| Topic | Scarthgap fact |
| --- | --- |
| License manifests | `license` class on by default (`INHERIT_DISTRO`); manifest per image in `${DEPLOY_DIR}/licenses/<image>-<machine>.rootfs-<datestamp>/` (dev-manual 33.3 note). |
| SBOM | `create-spdx` (SPDX 2.2) inherited by default through `INHERIT_DISTRO`; image SBOM `tmp/deploy/images/<machine>/<image>-<machine>.spdx.json` (plus related files there), per-recipe/package documents in `tmp/deploy/spdx/`. Disable with `INHERIT_DISTRO:remove = "create-spdx"`. |
| SPDX 3.0 | Available but off: `INHERIT_DISTRO:remove = "create-spdx"` and `INHERIT_DISTRO:append = " create-spdx-3.0"` (dev-manual 35). The 5.0.14 release notes record backported SPDX 3.0 fixes, so keep scarthgap point releases current if you use it. |
| SBOM options | `SPDX_PRETTY = "1"` (readable JSON), `SPDX_INCLUDE_SOURCES = "1"` (describe source files; large), `SPDX_ARCHIVE_SOURCES`, `SPDX_ARCHIVE_PACKAGED`, `SPDX_CUSTOM_ANNOTATION_VARS`. |
| CVE scan | Off by default: `INHERIT += "cve-check"`; optional `include conf/distro/include/cve-extra-exclusions.inc`. Reports: `tmp/deploy/cve/<recipe>_cve.json`; image summary JSON in `tmp/deploy/images/`. One recipe: `bitbake -c cve_check <recipe>`. Build warning: `do_cve_check: Found unpatched CVE (CVE-...)`. |
| CVE triage | `CVE_STATUS[CVE-ID] = "reason: description"` (reason mapped by `CVE_CHECK_STATUSMAP`, e.g. `not-applicable-platform`, `cpe-incorrect`, `upstream-wontfix`); `CVE_STATUS_GROUPS` for many CVEs; `CVE_CHECK_SKIP_RECIPE` to skip a recipe. `CVE_CHECK_IGNORE` is deprecated in 5.0. |
| CVE mapping | `CVE_PRODUCT = "vendor:product"` (default `BPN`), `CVE_VERSION` when `PV` does not match upstream numbering. |
| VEX | `vex` class (`INHERIT += "vex"`, task `generate_vex`): emits data for external scanners instead of scanning; reuses `CVE_CHECK_*` variables. |
| Patched detection | A patch is credited when its file name is `CVE-YYYY-NNNN.patch` or its header has `CVE: CVE-YYYY-NNNN` (only for local `file://` patches; remote patch headers are not scanned in 5.0). |

## 2. License Metadata

- `LICENSE`: SPDX-style names from `meta/files/common-licenses/` or `SPDXLICENSEMAP` in `meta/conf/licenses.conf`. `|` = choice, `&` = several licenses for different parts; no spaces inside a name. Per-package licenses: `LICENSE:${PN}-doc = "GFDL-1.2"`; each must also appear in the recipe `LICENSE` (QA `unlisted-pkg-lics`).
- `LIC_FILES_CHKSUM`: mandatory unless `LICENSE = "CLOSED"`. Files are relative to `S`; `beginline`/`endline` (1-based, inclusive) select a header; `md5=` is the checksum. It is checked at the end of `do_configure`; a mismatch fails the build and prints the selected text and the new checksum (dev-manual 33.1).
- On a mismatch after an upgrade: diff the license text between old and new source first. Update the checksum only after review, and state the reason with a `License-Update:` line in the commit (recipe style guide 3.5.3.1). A changed license may also require changing `LICENSE`.
- Non-standard license text: put it in the layer and point `LICENSE_PATH` at it, or use `NO_GENERIC_LICENSE[Name] = "file-in-source"` so the text is copied into manifests.

## 3. License Policy

- `LICENSE_FLAGS = "commercial"` in a recipe excludes it until `LICENSE_FLAGS_ACCEPTED` matches. Matching appends `_${PN}`: `commercial` in the recipe becomes `commercial_<pn>`; accepting `commercial_gst-plugins-ugly` allows one recipe, `commercial` allows all of them (dev-manual 33.2.1). Accept narrowly. Older releases (before 4.0 kirkstone) called it `LICENSE_FLAGS_WHITELIST`.
- `LICENSE_FLAGS_DETAILS[flag]`: message shown when a flag is not accepted.
- `INCOMPATIBLE_LICENSE`: globally, recipes with no alternative are not built and individually licensed packages are dropped; set in an image recipe, it applies to that image only. Wildcards are limited to `GPL-3.0*`, `LGPL-3.0*`, `AGPL-3.0*`; the regularly tested value is `"GPL-3.0* LGPL-3.0* AGPL-3.0*"`. Exceptions: `INCOMPATIBLE_LICENSE_EXCEPTIONS = "gdbserver:GPL-3.0-only"`. QA `incompatible-license` reports excluded packages.
- Static linking: license manifests list packages, not what was statically linked into them (dev-manual 33.3.4); review static libraries separately.

## 4. Source Release

- `INHERIT += "archiver"` with `ARCHIVER_MODE[src] = "original" | "patched" (default) | "configured"`, `ARCHIVER_MODE[diff] = "1"`, `ARCHIVER_MODE[recipe] = "1"`, `ARCHIVER_MODE[srpm] = "1"`; limit scope with `COPYLEFT_LICENSE_INCLUDE` / `COPYLEFT_LICENSE_EXCLUDE`. Output: `tmp/deploy/sources/`.
- `copyleft_compliance` is deprecated in favor of `archiver`; `copyleft_filter` is internal.
- The manuals list three needs for common FLOSS licenses: source code, license text, and build scripts plus source modifications (dev-manual 33.3); the SBOM covers much of this except publishing the build system and layers.

## 5. Inspect Before Changing

```bash
bitbake-getvar -r <recipe> LICENSE
bitbake-getvar -r <recipe> LIC_FILES_CHKSUM
bitbake-getvar -r <recipe> LICENSE_FLAGS
bitbake-getvar --value LICENSE_FLAGS_ACCEPTED
bitbake-getvar --value INCOMPATIBLE_LICENSE
bitbake-getvar --value INHERIT_DISTRO          # is create-spdx (or create-spdx-3.0) there?
bitbake-getvar --value INHERIT                 # cve-check, vex, archiver?
bitbake-getvar -r <recipe> CVE_PRODUCT
bitbake-getvar -r <recipe> CVE_VERSION
bitbake -e <recipe> | grep -E '^(CVE_[A-Z_]+|SPDX_[A-Z_]+|ARCHIVER_MODE)(\[|=)'   # flags such as CVE_STATUS[...]
bitbake -c populate_lic <recipe>
bitbake -c cve_check <recipe>
ls tmp/deploy/images/<machine>/*.spdx.json tmp/deploy/spdx tmp/deploy/cve tmp/deploy/licenses
```

`bitbake -e` prints flags as `VAR[flag]="..."` lines, so match `CVE_STATUS[` rather than `CVE_STATUS=`.

## 6. Debug Flow

1. Identify the release and which classes are active (section 5): scarthgap facts above do not hold for other releases.
2. License build failure: read the error in `log.do_configure` (checksum) or the parse/skip message (`LICENSE_FLAGS`, `INCOMPATIBLE_LICENSE`).
3. Image composition: check the license manifest and `INCOMPATIBLE_LICENSE` in the image recipe; remember `DEPENDS` (build-only) does not put a package in the manifest, but static linking can embed its code.
4. CVE report: false positive or negative -> fix `CVE_PRODUCT`/`CVE_VERSION`; fixed by patch -> name the patch `CVE-ID.patch` and add `CVE:` and `Upstream-Status: Backport [...]` headers; not applicable -> `CVE_STATUS` with a reason. Wrong NVD data should be reported to NVD.
5. SBOM: confirm the class, then the output paths; rebuild the image to regenerate.

## 7. Common Problems

- Checksum pasted from the error without reading the license change.
- `LICENSE_FLAGS_ACCEPTED = "commercial"` accepting far more than intended.
- `CVE_CHECK_IGNORE` still used (deprecated in 5.0).
- SPDX 3.0 or `vex` assumed active when only default `create-spdx` (SPDX 2.2) is.
- `CVE_PRODUCT` left at `BPN` for a product with a different NVD name.
- Source archiving treated as a complete legal answer.

Derived from the Yocto Project scarthgap (5.0) documentation, CC BY-SA 2.0 UK.
