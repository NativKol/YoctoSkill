Can you review this commit on our distro layer before I merge it? We only wanted to add
-fno-omit-frame-pointer to one profiling tool, but a colleague said it was easiest to do
it this way. Scarthgap, standard review is fine.

```diff
commit: "mydistro: add frame pointers for perf-helper"

diff --git a/meta-mydistro/conf/distro/mydistro.conf b/meta-mydistro/conf/distro/mydistro.conf
--- a/meta-mydistro/conf/distro/mydistro.conf
+++ b/meta-mydistro/conf/distro/mydistro.conf
@@ -20,3 +20,4 @@ INIT_MANAGER = "systemd"
 require conf/distro/include/security_flags.inc
+TARGET_CFLAGS += "-fno-omit-frame-pointer"
diff --git a/meta-mydistro/classes-global/mydistro-stamp.bbclass b/meta-mydistro/classes-global/mydistro-stamp.bbclass
--- a/meta-mydistro/classes-global/mydistro-stamp.bbclass
+++ b/meta-mydistro/classes-global/mydistro-stamp.bbclass
@@ -1,6 +1,8 @@
 # inherited via INHERIT += "mydistro-stamp" in mydistro.conf
 do_install:append() {
     install -d ${D}${sysconfdir}
-    echo "${DISTRO_VERSION}" > ${D}${sysconfdir}/mydistro-version
+    echo "${DISTRO_VERSION} built ${DATETIME}" > ${D}${sysconfdir}/mydistro-version
 }
+do_install[vardepsexclude] += "DATETIME"
```
