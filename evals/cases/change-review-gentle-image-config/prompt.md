A new teammate opened their first merge request on our product layer. Please review it,
and be gentle with them - they are new to Yocto. We are on scarthgap.

```diff
diff --git a/meta-company/conf/templates/default/local.conf.sample b/meta-company/conf/templates/default/local.conf.sample
--- a/meta-company/conf/templates/default/local.conf.sample
+++ b/meta-company/conf/templates/default/local.conf.sample
@@ -12,6 +12,8 @@ MACHINE ??= "company-board"
 DISTRO ?= "company-distro"
 PACKAGE_CLASSES ?= "package_ipk"
+IMAGE_INSTALL += "htop"
+EXTRA_IMAGE_FEATURES ?= "debug-tweaks"
diff --git a/meta-company/conf/distro/company-distro.conf b/meta-company/conf/distro/company-distro.conf
--- a/meta-company/conf/distro/company-distro.conf
+++ b/meta-company/conf/distro/company-distro.conf
@@ -8,4 +8,5 @@ DISTRO_VERSION = "2.1"
 require conf/distro/poky.conf
 DISTRO_FEATURES:append = " systemd usrmerge"
+DISTRO_FEATURES:append = "wifi"
diff --git a/meta-company/recipes-core/images/company-image.bb b/meta-company/recipes-core/images/company-image.bb
--- a/meta-company/recipes-core/images/company-image.bb
+++ b/meta-company/recipes-core/images/company-image.bb
@@ -4,3 +4,4 @@ LICENSE = "MIT"
 inherit core-image
 IMAGE_INSTALL:append = " company-app"
+DEPENDS += "iw"
```

The commit message is "add wifi stuff".
