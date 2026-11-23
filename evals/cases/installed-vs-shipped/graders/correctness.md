# Grader: installed-vs-shipped caused by a hardcoded libdir

The recipe forces CMake to install into `/usr/lib64` while the distro's `${libdir}` is
`/usr/lib`. No default `FILES` pattern covers `/usr/lib64`, which produced the original
`installed-vs-shipped`. The user then added `FILES:${PN} += "/usr/lib64/*"`, which ships
everything, including the `libfoo.so` development symlink, in the runtime package. That is
why `dev-so` now fires: the default `FILES:${PN}-dev` (through `FILES_SOLIBSDEV`, which uses
`${libdir}`) never matched the lib64 path, so the leftmost-package rule could not send the
symlink to `${PN}-dev`. The `libdir` warning names the root cause.

## Required to pass

1. Identify the hardcoded `-DCMAKE_INSTALL_LIBDIR=lib64` (install path not matching
   `${libdir}`) as the root cause, using the `libdir` warning as evidence.
2. Fix it at the source: remove the override (or pass the real `${libdir}`/`${baselib}`
   value) so files install under `${libdir}`, and remove the `FILES:${PN} += "/usr/lib64/*"`
   line.
3. Explain that once paths are standard the default package split applies: versioned
   `libfoo.so.*` in `${PN}`, the `libfoo.so` symlink and headers in `${PN}-dev`.

## Automatic fail

- Recommending `INSANE_SKIP` for `dev-so`, `libdir` or `installed-vs-shipped` as the fix.
- Keeping or widening the `/usr/lib64` `FILES` line as the recommended fix.
- Recommending deletion of `tmp/`, `downloads/` or `sstate-cache/`.
- Using old override syntax (`FILES_${PN}`).

## Improves the score

- Stating the leftmost-package-wins rule for `PACKAGES` and that `${PN}-dev` comes before
  `${PN}`.
- Validating with `bitbake -c package_qa libfoo` and
  `oe-pkgdata-util list-pkg-files -p libfoo libfoo-dev`.
- Noting that a genuinely unversioned library (no SONAME) is a different case, handled with
  `SOLIBS = ".so"` and `FILES_SOLIBSDEV = ""`.
