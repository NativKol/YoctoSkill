# Yocto QA Checks (insane class) for Scarthgap

Release: Yocto Project 5.0 "scarthgap". Sources: ref-manual "Classes > insane" (5.61, the list of every check name) and ref-manual "QA Error and Warning Messages" (chapter 9, the message text). Verbatim manual text for a check, offline: `python3 scripts/ylookup.py --kind qa <check>` (46 checks have a documented message; the class entry is `--kind class insane`).

## 1. How QA Works

- QA checks run mostly in `do_package_qa` (packaged files), plus checks hooked into `do_configure`, `do_compile`, `do_install` (log scans) and `do_patch` (patch checks). Every message ends with the check name in brackets, e.g. `[installed-vs-shipped]` (chapter 9 note). Search the log for `QA Issue` and that bracket.
- Severity is policy: a check listed in `ERROR_QA` fails the task, one in `WARN_QA` only warns. Both are set in the distro configuration; the default lists live in `meta/classes-global/insane.bbclass`. Read the real values with `bitbake-getvar -r <recipe> ERROR_QA WARN_QA` before telling a user whether something "is" an error. Changing severity belongs in a distro conf (`ERROR_QA:remove = "x"`, `WARN_QA:append = " x"`), never in a recipe.
- `INSANE_SKIP:<pkg> += "<check>"` skips a check for one package. It needs the package override (`INSANE_SKIP:${PN}`), a comment explaining why, and should be the last resort after fixing the cause (insane 5.61). `INSANE_SKIP` without a package suffix has no effect for package checks.
- Some checks are disabled by default and therefore not in chapter 9 (e.g. `cve_status_not_in_db`).

Triage commands (all read-only):

```bash
grep -n 'QA Issue' tmp/work/*/<recipe>/*/temp/log.do_package_qa
bitbake-getvar -r <recipe> ERROR_QA
bitbake-getvar -r <recipe> PACKAGES
bitbake-getvar -r <recipe> FILES:<package>
find tmp/work/*/<recipe>/*/image -type f | head          # what do_install put in ${D}
ls tmp/work/*/<recipe>/*/packages-split/                  # how do_package split it (rm_work disabled)
oe-pkgdata-util list-pkg-files -p <package>               # only for packages already built
```

Validate a fix with `bitbake -c package_qa <recipe>` (and `bitbake <recipe>` for log-scan checks).

## 2. Packaging and File Layout

| Check | Message (chapter 9) | Meaning and fix |
| --- | --- | --- |
| `installed-vs-shipped` | `<recipename>: Files/directories were installed but not shipped in any package` | A file in `${D}` matched no `FILES:<pkg>`. Add it to the right package's `FILES` (remember the leftmost package in `PACKAGES` wins) or stop installing / delete it at the end of `do_install`. Common causes: non-standard prefix (`/opt`, `/usr/local`), a new upstream file, libraries under `lib64` vs `lib`. |
| `files-invalid` | `FILES variable for package <packagename> contains '//' which is invalid. ...` | A `FILES` entry contains `//`, usually `${D}${bindir}` copied into `FILES`, a stray trailing `/`, or an empty variable between two slashes. Use `${bindir}/foo` without `${D}`. |
| `empty-dirs` | `<packagename> installs files in <path>, but it is expected to be empty` | Files under a directory listed in `QA_EMPTY_DIRS` (default list set in insane.bbclass, e.g. `/tmp`). Install elsewhere or create at runtime (tmpfiles, init script). |
| `dev-so` | `non -dev/-dbg/nativesdk- package contains symlink .so: <packagename> path '<path>'` | A `lib*.so` development symlink is in a runtime package. Leave it to `${PN}-dev` (default). Only `dlopen()` plugins loaded by the unversioned name legitimately need it in `${PN}`; then `INSANE_SKIP:${PN} += "dev-so"` with a comment. |
| `staticdev` | `non -staticdev package contains static .a library: <packagename> path '<path>'` | `.a` files belong in `${PN}-staticdev`. |
| `debug-files` | `non debug package contains .debug directory: <packagename> path <path>` | `.debug` dirs only in `${PN}-dbg`; usually a too-broad `FILES` glob such as `${libdir}/foo/*`. |
| `libdir` | `<packagename>: found library in wrong location` | Hardcoded `/lib`, `/usr/lib64`, etc. that do not match `${base_libdir}`/`${libdir}`; pass the right libdir to the build system. |
| `libexec` | `<packagename>: <path> is using libexec please relocate to <libexecdir>` | Files in `/usr/libexec` while the distro's `libexecdir` differs. |
| `usrmerge` | `<packagename> package is not obeying usrmerge distro feature. /<path> should be relocated to /usr.` | With `usrmerge` in `DISTRO_FEATURES`, nothing may go to `/bin`, `/sbin`, `/lib`, `/lib64`; use `${base_bindir}` etc. |
| `packages-list` | `<packagename> is listed in PACKAGES multiple times, this leads to packaging errors.` | Duplicate entry in `PACKAGES` (often `PACKAGES += "${PN}-foo"` in both recipe and bbappend). |
| `pkgname` | `<packagename> doesn't match the [a-z0-9.+-]+ regex` | Package names may contain only `0-9 a-z . + -`. |
| `infodir` | `The /usr/share/info/dir file is not meant to be shipped in a particular package.` | Add `rm ${D}${infodir}/dir` to `do_install`. |
| `perllocalpod` | `<packagename> contains perllocal.pod (<files>), should not be installed` | Delete `perllocal.pod` in `do_install`. |
| `symlink-to-sysroot` | `Symlink <path> in <packagename> points to TMPDIR` | An absolute symlink into the build tree; make it relative or target-absolute. |

## 3. Dependencies

| Check | Message | Meaning and fix |
| --- | --- | --- |
| `file-rdeps` | `<packagename> requires <files>, but no providers in its RDEPENDS` | A packaged file needs another file (e.g. `#!/bin/bash` needs `/bin/bash`) that no `RDEPENDS:<pkg>` provides. Add the providing package (`bash`) to `RDEPENDS:<pkg>`, or change the interpreter. |
| `build-deps` | `<packagename1> rdepends on <packagename2>, but it isn't a build dependency?` | A runtime dependency was detected at packaging time but nothing in `DEPENDS`/explicit `RDEPENDS` guarantees it gets built; add the explicit dependency (e.g. `RDEPENDS:${PN} += "initscripts-functions"`). |
| `dev-deps` | `<packagename> rdepends on <dev_packagename>` | A non-dev package depends on a `-dev` package. Typical cause: an unversioned `libfoo.so` (no SONAME) lands in `${PN}-dev` and the main binary links to it; set `SOLIBS = ".so"` and `FILES_SOLIBSDEV = ""` (dev-manual 15.3), or fix the SONAME upstream. Also check hand-written `RDEPENDS` naming `-dev`. |
| `debug-deps` | `<packagename> rdepends on <debug_packagename>` | A non-dbg package depends on `-dbg`; fix `RDEPENDS`. |
| `dep-cmp` | `<var>:<packagename> is invalid: <comparison> (<value>) only comparisons <, =, >, <=, and >= are allowed` | Bad version operator in `RDEPENDS`/`RRECOMMENDS`/`RSUGGESTS`/`RPROVIDES`/`RREPLACES`/`RCONFLICTS`, e.g. `foo (>> 1.0)`. |
| `virtual-slash` | `<variable> is set to <value> but the substring 'virtual/' holds no meaning in this context. ...` (no bracket tag is printed in the documented message) | New in 5.0 (migration-5.0 "Miscellaneous changes"): `virtual/` in `RDEPENDS`/`RPROVIDES`. Use `VIRTUAL-RUNTIME_<name>` variables. |
| `xorg-driver-abi` | `Package <packagename> contains Xorg driver (<driver>) but no xorg-abi- dependencies` | Binary X drivers must `RDEPENDS` on the `xorg-abi-*` they were built against. |
| `pkgvarcheck` | `<recipefile>: Variable <variable> is set as not being package specific, please fix this.` and `recipe uses DEPENDS:${PN}, should use DEPENDS` | `RDEPENDS`, `FILES`, `ALLOW_EMPTY`, `pkg_postinst` etc. set without a package suffix; or `DEPENDS:${PN}` (DEPENDS is recipe-wide). |
| `pn-overrides` | `Recipe <recipefile> has PN of "<recipename>" which is in OVERRIDES, this can result in unexpected behavior.` | Recipe named like the machine or distro: `FILES:${PN} = "x"` then becomes `FILES = "x"`. Rename the recipe. |

Untagged packaging message: `<oldpackage>-<oldpkgversion> was registered as shlib provider for <library>, changing it to <newpackage>-<newpkgversion> because it was built later`. Two packages ship the same library. Expected after a recipe rename; otherwise a private copy is being picked up as provider, so add its `.so` name to `PRIVATE_LIBS` in the recipe that ships the private copy. There is no `[shlib-provider]` tag.

## 4. Host Contamination and Reproducibility

| Check | Message | Meaning and fix |
| --- | --- | --- |
| `configure-unsafe` | `This autoconf log indicates errors, it looked at host include and/or library paths while determining system capabilities. ...` | configure probed `/usr/include` or `/usr/lib`; add the missing `DEPENDS` or fix configure flags. |
| `compile-host-path` | `<recipename>: The compile log indicates that host include and/or library paths were used. ...` | Same, found in `log.do_compile`. |
| `install-host-path` | `<recipename>: The install log indicates that host include and/or library paths were used. ...` | Same, in `log.do_install`. |
| `buildpaths` | `File <filename> in package <packagename> contains reference to TMPDIR` | Build paths baked into output; hurts reproducibility. Find how the path enters (configure-time defines, scripts, `__FILE__`) and make it relative or runtime-configured. |
| `host-user-contaminated` | (no message listed in chapter 9) | Files outside `/home` owned by the UID/GID running BitBake: `cp -a`/`tar` preserved host ownership in `do_install`. Use `install`, `cp --no-preserve=ownership`, `tar --no-same-owner` (ref-manual `do_install`). |
| `la` | `<file> failed sanity test (workdir) in path <path>` | `.la` contains build paths; usually delete `.la` files (remove-libtool class does this by default via `INHERIT_DISTRO`). |
| `pkgconfig` | `<file> failed sanity test (tmpdir) in path <path>` | `.pc` contains `TMPDIR`/`WORKDIR` paths; fix the prefix variables passed to the build. |
| `rpaths` | `package <packagename> contains bad RPATH <rpath> in file <file>` | RPATH points into the build tree (security issue); disable rpath in the build system. |
| `useless-rpaths` | `<packagename>: <file> contains probably-redundant RPATH <rpath>` | RPATH to `/lib` or `/usr/lib`; remove it. |
| `already-stripped` | `File '<file>' from <recipename> was already stripped, this will prevent future debugging!` | Upstream strips (`-s`, `install -s`, `STRIP`); disable it so OE can split debug info. The final package is still stripped. |
| `ldflags` | `File '<file>' in package '<package>' doesn't have GNU_HASH (didn't pass LDFLAGS?)` | Build system ignores `LDFLAGS`; pass them (workaround `TARGET_CC_ARCH += "${LDFLAGS}"`). For prebuilt binaries `INSANE_SKIP:${PN} += "ldflags"` is the documented choice (dev-manual 15.2). |
| `textrel` | `ELF binary '<file>' has relocations in .text` | Add `-fPIC` (e.g. `CFLAGS:append = " -fPIC "`). |
| `arch` | `Architecture did not match (<file_arch>, expected <machine_arch>) in <file>` (also `Bit size ...`, `Endianness ...`) | Wrong compiler or prebuilt binary for another architecture; bootloader/firmware blobs may need a narrow skip. |
| `split-strip` | (not listed in chapter 9) | Splitting or stripping debug info failed. |
| `shebang-size` | `<packagename>: <file> maximum shebang size exceeded, the maximum size is 128.` | Shorten the `#!` line (often a long native sysroot path; use `/usr/bin/env` or fix the install-time rewrite). |

## 5. Source, Patches, Licenses

| Check | Message | Meaning and fix |
| --- | --- | --- |
| `src-uri-bad` | `SRC_URI uses PN not BPN` and `<recipename>: SRC_URI uses unstable GitHub archives` | Use `${BPN}` (so native/nativesdk/multilib variants fetch the same URL) and fetch GitHub sources with the git fetcher or release assets, not `/archive/` tarballs. It is not a protocol/checksum check. |
| `patch-fuzz` | `Fuzz detected: <patch output>` | Patch applied with fuzz and may land in the wrong place. Refresh: `devtool modify <recipe>` then `devtool finish --force-patch-refresh <recipe> <layer>`, and review the diff (chapter 9). |
| `patch-status` | `Missing Upstream-Status in patch <patchfile> ...` and `Malformed Upstream-Status in patch <patchfile> ...` | Every patch header needs `Upstream-Status:` with one of `Pending`, `Submitted [where]`, `Backport [version]`, `Denied`, `Inactive-Upstream [lastcommit: when (and/or) lastrelease: when]`, `Inappropriate [reason]` (contributor-guide "Patch Upstream Status" 3.6). Scarthgap documents a single `patch-status` check; release 4.2 (mickledore) briefly split it into `patch-status-core`/`patch-status-noncore`, so older configs may still name those. |
| `unlisted-pkg-lics` | `LICENSE:<packagename> includes licenses (<licenses>) that are not listed in LICENSE` | Every license used in a per-package `LICENSE:<pkg>` must also appear in the recipe-level `LICENSE`. |
| `incompatible-license` | (in the insane list only; no message in chapter 9) | Reports packages not created because their license is in `INCOMPATIBLE_LICENSE`. Fix policy or provide alternatives; see `INCOMPATIBLE_LICENSE_EXCEPTIONS`. |
| `invalid-chars` | (not listed in chapter 9) | `DESCRIPTION`, `SUMMARY`, `LICENSE` or `SECTION` contains non-UTF-8 characters. Invalid package-name characters are `pkgname`, not this. |
| `invalid-packageconfig` | (in the insane list only; no message in chapter 9) | A name in `PACKAGECONFIG` has no `PACKAGECONFIG[name] = "..."` definition: typo, or the option was removed upstream in a newer recipe version. |
| `unknown-configure-option` | `<recipe>: configure was passed unrecognized options: <options>` | An `EXTRA_OECONF`/`PACKAGECONFIG` flag the configure script no longer knows; drop or rename it. |
| `configure-gettext` | `AM_GNU_GETTEXT used but no inherit gettext` | `inherit gettext`. |

License checksum mismatch: not a bracketed insane check in the scarthgap manual. At the end of `do_configure` the build compares `LIC_FILES_CHKSUM` and fails, printing the selected license text and the new md5 (dev-manual "Tracking License Changes" 33.1). Review the upstream license diff before updating the checksum, and record the reason in the commit with a `License-Update:` tag (recipe style guide 3.5.3.1).

## 6. Integration and Tests

| Check | Message | Meaning and fix |
| --- | --- | --- |
| `mime` | `package contains mime types but does not inherit mime: <packagename> path '<file>'` | `inherit mime`. |
| `mime-xdg` | `package contains desktop file with key 'MimeType' but does not inhert mime-xdg: ...` | `inherit mime-xdg`. |
| `desktop` | (not listed in chapter 9) | `desktop-file-validate` rejected a `.desktop` file. |
| `missing-update-alternatives` | `<recipename>: recipe defines ALTERNATIVE:<packagename> but doesn't inherit update-alternatives. ...` | `inherit update-alternatives`. |
| `unhandled-features-check` | `<recipename>: recipe doesn't inherit features_check` | `REQUIRED_DISTRO_FEATURES` etc. are set but have no effect without `inherit features_check`. |
| `unimplemented-ptest` | `<tool> tests detected` | Upstream has a test suite but the recipe has no ptest; implement ptest or ignore if not wanted. |
| `version-going-backwards` | (not listed in chapter 9) | With buildhistory enabled, a package version is lower than the previous build; matters for package feeds (bump `PE` or fix `PV`/`PR`). |
| `cve_status_not_in_db` | (disabled by default) | A `CVE_STATUS` entry names a CVE that NVD does not report for this component. |

## 7. Rarely Seen or Internal

- `pkgv-undefined`: `PKGV` undefined during `do_package`. `var-undefined`: `WORKDIR`, `DEPLOY_DIR`, `D`, `PN` or `PKGD` undefined during `do_package`.
- `perm-config` and `perm-line`: invalid line format in an `fs-perms.txt` table. `perm-link`: an `fs-perms.txt` `link` entry whose target already exists. `perms`: "currently unused but reserved".

Not scarthgap QA checks (do not cite them as tags): `shlib-provider`, `license`, `space-around-equal`, `recipe-naming`.

## 8. Output Rule

Name the tag, the package, the variable to change and the validation command, e.g.:

```text
[installed-vs-shipped] for libfoo: /opt/foo/bin/foo is installed but no FILES entry covers /opt.
Prefer installing to ${bindir} (do not override the prefix); otherwise FILES:${PN} += "/opt/foo".
Validate: bitbake -c package_qa libfoo
```

Derived from the Yocto Project scarthgap (5.0) documentation, CC BY-SA 2.0 UK.
