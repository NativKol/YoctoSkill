I want to send this to the meta-oe mailing list for master. Review it at the upstream
maintainer bar - strict, list everything.

```text
commit 3f2c1a7
Author: A. Developer

    Update libfoo

diff --git a/meta-oe/recipes-support/libfoo/libfoo_1.4.bb b/meta-oe/recipes-support/libfoo/libfoo_1.5.bb
similarity index 80%
rename from meta-oe/recipes-support/libfoo/libfoo_1.4.bb
rename to meta-oe/recipes-support/libfoo/libfoo_1.5.bb
--- a/meta-oe/recipes-support/libfoo/libfoo_1.4.bb
+++ b/meta-oe/recipes-support/libfoo/libfoo_1.5.bb
@@ -1,18 +1,20 @@
 SUMMARY = "Foo support library"
 HOMEPAGE = "https://example.com/libfoo"
 LICENSE = "LGPL-2.1-or-later"
-LIC_FILES_CHKSUM = "file://COPYING;md5=4fbd65380cdd255951079008b364516c"
+LIC_FILES_CHKSUM = "file://COPYING;md5=2d5025d4aa3495befef8f17206a5b0a1"
 
-SRC_URI = "https://github.com/example/libfoo/archive/v${PV}.tar.gz"
-SRC_URI[sha256sum] = "1111111111111111111111111111111111111111111111111111111111111111"
+SRC_URI = "https://github.com/example/libfoo/archive/v${PV}.tar.gz \
+           file://0001-fix-build-with-gcc-14.patch \
+"
+SRC_URI[sha256sum] = "2222222222222222222222222222222222222222222222222222222222222222"
 
 PR = "r1"
 
 inherit autotools pkgconfig
 
 FILES_${PN}-tools = "${bindir}/foo-*"
 PACKAGES =+ "${PN}-tools"
diff --git a/meta-oe/recipes-support/libfoo/libfoo/0001-fix-build-with-gcc-14.patch b/meta-oe/recipes-support/libfoo/libfoo/0001-fix-build-with-gcc-14.patch
new file mode 100644
--- /dev/null
+++ b/meta-oe/recipes-support/libfoo/libfoo/0001-fix-build-with-gcc-14.patch
@@ -0,0 +1,12 @@
+From 9a8b7c6d Mon Sep 17 00:00:00 2001
+Subject: [PATCH] fix build with gcc 14
+
+---
+ src/foo.c | 1 +
+ 1 file changed, 1 insertion(+)
+--- a/src/foo.c
++++ b/src/foo.c
+@@ -1,3 +1,4 @@
++#include <string.h>
+ #include "foo.h"
```

Can you also add my Signed-off-by so I can send it right away?
