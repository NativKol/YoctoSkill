# Conventions: Recipe Style, Licensing, Layers, Security

The written conventions a Yocto change is held to. Each rule says where it comes from so
the review can cite it. Severities given are defaults (see strictness-levels.md).

## Contents

1. Naming and versions
2. Recipe formatting and ordering
3. Licensing
4. Layer best practices and Yocto Project Compatible
5. Security conventions
6. Packaging conventions
7. What is *not* a convention

## 1. Naming and versions

Source: contributor-guide/recipe-style-guide.md 3.1-3.3.

- File path `recipes-category/recipename/recipename_version.bb`. "`recipename` and
  `category` may contain hyphens, but hyphens are not allowed in `version`." (minor;
  blocker if it breaks PV parsing).
- Git-tracking recipes: `recipename_git.bb` with `PV = "<version>+git"`.
- Versions must sort correctly for upgrades; use `~` for pre-releases (`1.5~rc2`).
- `PR` removed when `PV` increases; `PE` raised when the version goes backwards.
- Layer names: Git repository in `meta-<layer_name>` form (dev-manual/layers.md 3.2).
- Package names: lower case, `[a-z0-9.+-]` (`pkgname` QA check).

## 2. Recipe formatting and ordering

Source: contributor-guide/recipe-style-guide.md 3.4-3.5.

Formatting (nits unless they change meaning):

- Spaces around the operator: `FOO = "bar"`, not `FOO="bar"`.
- Double quotes on the right-hand side.
- Spaces for indentation, "4 spaces per tab"; Python must use spaces.
- Long values split with `\`; continuation lines aligned with the opening quote:

  ```bitbake
  FOO = "this line is \
         long \
         "
  ```

- Shell functions: tabs or spaces, but "consistent within layers".

Required metadata (minor when missing): `SUMMARY`, `DESCRIPTION` (may default to
`SUMMARY`), `HOMEPAGE`, `BUGTRACKER` if applicable.

Variable order "when possible": `SUMMARY`, `DESCRIPTION`, `HOMEPAGE`, `BUGTRACKER`,
`SECTION`, `LICENSE`, `LIC_FILES_CHKSUM`, `DEPENDS`, `PROVIDES`, `PV`, `SRC_URI`,
`SRCREV`, `S`, `inherit ...`, `PACKAGECONFIG`, build-class variables (`EXTRA_OECONF`,
`EXTRA_QMAKEVARS_POST`), tasks, `PACKAGE_ARCH`, `PACKAGES`, `FILES`, `RDEPENDS`,
`RRECOMMENDS`, `RSUGGESTS`, `RPROVIDES`, `RCONFLICTS`, `BBCLASSEXTEND`.
Exceptions where order matters win, e.g. "`PACKAGE_ARCH` needing to be set before
`inherit packagegroup`". Tasks in execution order (`do_fetch` ... `do_package`).
Package-specific variables grouped by variable. Order deviations are nits; an order that
changes the result (an assignment before `inherit` that the class then overwrites) is
a bug, report it under its effect.

Writing guidelines (3.5.4):

- "Use BBCLASSEXTEND instead of creating separate recipes such as `-native` and
  `-nativesdk` ones, whenever possible." (minor)
- Tasks must be idempotent; when modifying a file in a task, copy `X` to `X.orig` once,
  restore from `X.orig`, then modify. A non-idempotent `sed -i` in `do_configure:append`
  is a **major** ("breaking it can cause obscure build failures").

## 3. Licensing

Sources: recipe-style-guide.md 3.5.3; ref-manual/variables.md (LICENSE,
LIC_FILES_CHKSUM, LICENSE_FLAGS, INCOMPATIBLE_LICENSE); dev-manual/licenses.md.

- Every recipe defines `LICENSE` and `LIC_FILES_CHKSUM` ("except in the special case where
  the LICENSE value is set to CLOSED").
- License names: no spaces inside a name; `|` for a choice, `&` for several licenses
  covering different parts; use the names of files in `meta/files/common-licenses/` or
  `SPDXLICENSEMAP` names from `meta/conf/licenses.conf`. SPDX identifiers with
  `-only`/`-or-later` (`GPL-2.0-only`) are required since kirkstone: "LICENSE variable
  values should now use SPDX identifiers. If they do not, by default a warning will be
  shown" (migration-guides/migration-4.0.md); a `convert-spdx-licenses.py` script
  converts old names such as `GPLv2` *[release-specific]*.
- `LICENSE` of the recipe must be a superset of every `LICENSE:<pkg>` (`unlisted-pkg-lics`).
- `LIC_FILES_CHKSUM` lists "all applicable licensing files"; `beginline`/`endline` are
  1-based and inclusive. A changed checksum without explanation is a red flag: the
  commit must carry `License-Update: <reason>` (e.g. "copyright years refreshed"), with a
  link to upstream if terms changed. Not needed when fixing incorrect metadata.
- The recipe's `LICENSE` is the software's license, not the recipe file's; the layer
  should state its own license (usually a file at the layer root).
- `LICENSE_FLAGS` (e.g. `commercial`) requires users to accept via
  `LICENSE_FLAGS_ACCEPTED`; adding `LICENSE_FLAGS_ACCEPTED = "commercial"` to a shared
  config accepts every commercial-flagged recipe - flag for compliance owner.
- Changes to `INCOMPATIBLE_LICENSE` alter which recipes can build at all.
- Wrong or guessed `LICENSE` values are **blockers**: they propagate into license
  manifests and SBOMs. Delegate deep compliance work to `yocto-security-sbom` if installed.

## 4. Layer best practices and Yocto Project Compatible

Sources: dev-manual/layers.md 3.2-3.6; test-manual/yocto-project-compatible.md.

- Use `.bbappend` instead of copying recipes; do not duplicate include files - `require
  recipes-core/<pkg>/<file>.inc` from the original layer.
- Machine-specific changes behind machine overrides; machine-specific files in a
  machine-named subdirectory.
- "Adding a layer to a build should not modify that build, unless the user changes a
  configuration setting to activate the layer, by selecting a MACHINE, a DISTRO or a
  DISTRO_FEATURES setting."
- A layer has a `README` saying who maintains it and where to send patches
  (`common.test_readme`).
- Separate functionality into sublayers where users may need only part.
- Document unsupported core functionality (no debug symbols, no SDK, ...).
- `yocto-check-layer` tests: `common.test_readme`, `test_parse`,
  `test_show_environment`, `test_world`, `test_signatures`, `test_layerseries_compat`;
  `bsp.test_bsp_defines_machines`, `test_bsp_no_set_machine`, `test_machine_world`,
  `test_machine_signatures`; `distro.test_distro_defines_distros`,
  `test_distro_no_set_distros`.

## 5. Security conventions

Sources: dev-manual/securing-images.md; ref-manual/features.md; dev-manual/vulnerabilities.md.

- No `debug-tweaks` (or `allow-empty-password`, `allow-root-login`,
  `empty-root-password`, `serial-autologin-root`) in production images or distros.
- Passwords via the `extrausers` class; never the same password on every device; never
  clear-text passwords, private keys, tokens or default credentials committed in a layer
  (**blocker**, and ask for rotation if it was ever pushed).
- "Ensure you have no network services listening that are not needed"; "Remove any
  software from the image that is not needed."
- Optional hardening: `require conf/distro/include/security_flags.inc`.
- CVE handling: CVE fixes as patches with a `CVE:` tag; ignoring a CVE uses
  `CVE_STATUS[CVE-ID] = "<reason>: <description>"` (e.g. `not-applicable-platform`,
  `cpe-incorrect`); `CVE_CHECK_IGNORE` is deprecated in scarthgap
  (migration-guides/migration-5.0.md) *[release-specific]*. Shared reasons use
  `CVE_STATUS_GROUPS`. Wrong `CVE_PRODUCT` causes false positives or negatives.
  A `CVE_STATUS` without a real description is a **major** (it silences the scanner).

## 6. Packaging conventions

Sources: ref-manual/qa-checks.md; ref-manual/variables.md (FILES, PACKAGES, PACKAGE_ARCH).

- Default splits (`-dev`, `-dbg`, `-staticdev`, `-doc`, `-locale`) are right in most
  cases; override `FILES` only for files the defaults miss.
- Unversioned `.so` symlinks and headers go to `-dev`; plugins that are genuinely
  unversioned `.so` files are the narrow exception (`INSANE_SKIP:${PN} += "dev-so"`
  with a comment).
- Use `${PN}`-relative package names and the path variables (`${bindir}`, `${libdir}`,
  `${sysconfdir}`, `${systemd_unitdir}`), not literal paths.

## 7. What is *not* a convention

Do not raise these as findings: personal taste in shell style when the layer is
consistent; `+=` inside the recipe that owns a variable; absence of `DESCRIPTION` when
`SUMMARY` says it all; using `require` vs `include` when both are fine for the case
(`require` fails if the file is missing, `include` does not - choose by whether absence is
an error, bitbake-user-manual-metadata.md 3.4.3-3.4.4).

Derived from the Yocto Project scarthgap (5.0) documentation, CC BY-SA 2.0 UK.
