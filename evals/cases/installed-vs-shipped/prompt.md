I'm on scarthgap, building for a 64-bit Arm board. My libfoo recipe first failed with
installed-vs-shipped for everything under /usr/lib64, so I added a FILES line. Now I get this:

```text
WARNING: libfoo-1.2.0-r0 do_package_qa: QA Issue: libfoo: found library in wrong location [libdir]
ERROR: libfoo-1.2.0-r0 do_package_qa: QA Issue: non -dev/-dbg/nativesdk- package contains symlink .so: libfoo path '/usr/lib64/libfoo.so' [dev-so]
ERROR: libfoo-1.2.0-r0 do_package_qa: Fatal QA errors were found, failing task.
```

The recipe:

```bitbake
SUMMARY = "Foo library"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://COPYING;md5=0123456789abcdef0123456789abcdef"

SRC_URI = "git://example.com/foo.git;branch=main;protocol=https"
SRCREV = "0123456789abcdef0123456789abcdef01234567"
S = "${WORKDIR}/git"

inherit cmake

EXTRA_OECMAKE = "-DCMAKE_INSTALL_LIBDIR=lib64"

FILES:${PN} += "/usr/lib64/*"
```

`bitbake-getvar -r libfoo --value libdir` prints `/usr/lib`. Should I just add dev-so to INSANE_SKIP?
