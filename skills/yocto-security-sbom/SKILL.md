---
name: yocto-security-sbom
description: Yocto license compliance, CVE and SBOM work for Yocto 5.0 scarthgap - LICENSE expressions and per-package licenses, LIC_FILES_CHKSUM mismatches after upgrades, LICENSE_FLAGS and LICENSE_FLAGS_ACCEPTED for commercial recipes, INCOMPATIBLE_LICENSE (GPL-3.0* policies) and exceptions, license manifests, SPDX SBOM output from create-spdx (on by default) or create-spdx-3.0, cve-check reports and CVE_STATUS/CVE_PRODUCT/CVE_VERSION triage, the vex class, CVE patch headers, and archiver source release for copyleft obligations. Use it whenever someone asks for an SBOM, a CVE report, whether a license checksum change is safe, how to keep GPLv3 out of an image, how to accept a commercial license, or what to hand to a compliance team, even if they do not mention SPDX. Gives metadata and artifacts, not legal advice. Recipe packaging in general goes to yocto-recipe-review.
---

# Yocto Security SBOM

State the scarthgap facts, verify they apply to the user's build, then fix metadata. Do not give legal advice; say what a compliance reviewer must check.

## Scarthgap Facts

- `create-spdx` (SPDX 2.2) is inherited by default through `INHERIT_DISTRO`; the image SBOM is `tmp/deploy/images/<machine>/<image>-<machine>.spdx.json`, other documents under `tmp/deploy/spdx/`. SPDX 3.0: `INHERIT_DISTRO:remove = "create-spdx"` + `INHERIT_DISTRO:append = " create-spdx-3.0"`.
- `cve-check` is opt-in (`INHERIT += "cve-check"`); reports in `tmp/deploy/cve/`, image summaries in `tmp/deploy/images/`; `bitbake -c cve_check <recipe>` for one recipe.
- `CVE_STATUS[CVE-ID] = "reason: text"` replaces the deprecated `CVE_CHECK_IGNORE` (migration-5.0). `CVE_PRODUCT`/`CVE_VERSION` fix false positives and negatives. The `vex` class is an alternative that emits VEX data.
- License manifests come from the default `license` class: `tmp/deploy/licenses/<image>-<machine>.rootfs-<datestamp>/`.
- Other releases differ (class names, SPDX version, paths): confirm the release first.

## Workflow

1. **Confirm the release and active classes:**
   ```bash
   bitbake --version                              # 2.8.x = scarthgap
   bitbake-getvar --value INHERIT_DISTRO          # create-spdx or create-spdx-3.0?
   bitbake-getvar --value INHERIT                 # cve-check, vex, archiver?
   bitbake-getvar -r <recipe> LICENSE
   bitbake-getvar -r <recipe> LIC_FILES_CHKSUM
   bitbake-getvar --value INCOMPATIBLE_LICENSE
   bitbake -e <recipe> | grep -E '^(CVE_[A-Z_]+|SPDX_[A-Z_]+|ARCHIVER_MODE)(\[|=)'
   ```
2. **License checksum mismatch:** the build fails at the end of `do_configure` and prints the new md5 and the selected text. Diff the license text between old and new source first; update `LICENSE` if terms changed; then the checksum, with a `License-Update:` reason in the commit.
3. **Policy:** accept commercial flags narrowly (`LICENSE_FLAGS_ACCEPTED = "commercial_<pn>"`, not `commercial`); `INCOMPATIBLE_LICENSE = "GPL-3.0* LGPL-3.0* AGPL-3.0*"` is the regularly tested value; use `INCOMPATIBLE_LICENSE_EXCEPTIONS` for justified packages.
4. **CVE triage:** mapping wrong -> `CVE_PRODUCT`/`CVE_VERSION`; fixed by a patch -> `CVE-ID.patch` with `CVE:` and `Upstream-Status: Backport [...]` headers; not applicable -> `CVE_STATUS` with a reason.
5. **Source release:** `INHERIT += "archiver"` with `ARCHIVER_MODE[src]` and `COPYLEFT_LICENSE_INCLUDE`/`EXCLUDE`; `copyleft_filter` is internal and `copyleft_compliance` is deprecated.
6. **Validate:** `bitbake -c populate_lic <recipe>`, `bitbake <image>`, then list the artifacts in `tmp/deploy/{licenses,spdx,cve}` and the image `.spdx.json`.

## Offline lookup

Everything this skill needs is in the repository; it works without internet. Pull only the text you need instead of reading whole files (pages run to thousands of lines). From this skill's folder:

- `python3 scripts/ylookup.py <NAME>...` prints the scarthgap manual entry for any variable, class, task, feature or QA check (`--kind var|class|task|feature|qa` to disambiguate, `--find TEXT` when unsure of the name).
- `--topic TEXT` lists manual sections, `--section <manual/page.md> "<heading>"` prints one, `--grep REGEX [--in ref-manual]` finds anything else.
- URLs in these files are citations for the user, not lookups. The manuals are scarthgap 5.0: if the project is on another release, tell the user rather than going online. Without Python: `` grep -n -A30 '^## Variable `NAME`' references/keywords.md ``.

## References

- [references/security-sbom.md](references/security-sbom.md): defaults table, license fields and policy, CVE workflow, source release, inspection commands.
- [references/classes-core.md](references/classes-core.md): `license`, `create-spdx`, `cve-check`, `vex`, `archiver` behavior.
- [references/variables-core.md](references/variables-core.md): operators (`INHERIT_DISTRO:remove`), `LICENSE` per package.
- [references/migration.md](references/migration.md): release detection and 5.0 changes (`CVE_STATUS`).

## Output

1. artifact or policy being debugged, and the release/classes detected
2. the metadata or policy fix
3. validation command and the artifact path to expect
4. what remains for legal/compliance review
