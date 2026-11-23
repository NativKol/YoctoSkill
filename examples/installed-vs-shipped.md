# Example: installed-vs-shipped QA Error

Skill: `yocto-recipe-review` (or `bitbake-debug` when only the log is given).

## User Prompt

```text
do_package_qa fails: "foo: Files/directories were installed but not shipped in any package: /opt/foo/bin/foo-daemon /opt/foo/etc/foo.conf [installed-vs-shipped]". How do I fix it?
```

## Evidence to Request

- the full QA message and the recipe (class, `EXTRA_OECMAKE`/`EXTRA_OECONF`, `do_install`)
- `bitbake-getvar -r foo PACKAGES` and `bitbake-getvar -r foo FILES:foo`
- the contents of `${D}` (`tmp/work/*/foo/*/image/`)

## Bad Answer Pattern

- `INSANE_SKIP:${PN} += "installed-vs-shipped"` (the files would silently vanish from every image).
- Adding random paths to `FILES:${PN}` without checking the package split, or adding paths that an earlier package (`${PN}-dev`, `${PN}-dbg`) already matches: the leftmost package in `PACKAGES` wins, so that line has no effect.

## Expected Answer Pattern

- Explain that `/opt` is covered by no default `FILES` entry, so nothing owns the files.
- Preferred fix: stop overriding the install prefix so the build uses `${bindir}` and `${sysconfdir}` (default `FILES:${PN}` covers them).
- If `/opt` is a product requirement: `FILES:${PN} += "/opt/foo"`, and mark `/opt/foo/etc/foo.conf` in `CONFFILES:${PN}` if users edit it.
- If the files are not needed: delete them at the end of `do_install`.

## Validation

```bash
bitbake -c package_qa foo
oe-pkgdata-util list-pkg-files -p foo
```
