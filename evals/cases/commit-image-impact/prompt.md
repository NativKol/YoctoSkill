We are on Yocto scarthgap with poky plus our own distro layer. A colleague pushed this
commit and I need to know what it changes in `core-image-base` for our board before we
merge. I have not built it yet.

```diff
diff --git a/meta-company/conf/distro/company.conf b/meta-company/conf/distro/company.conf
@@
 require conf/distro/poky.conf
 DISTRO = "company"
-DISTRO_FEATURES:append = " wifi"
+DISTRO_FEATURES:append = " wifi"
+DISTRO_FEATURES:remove = "x11 pulseaudio"
+INIT_MANAGER = "systemd"
diff --git a/meta-company/recipes-core/packagegroups/packagegroup-company.bb b/meta-company/recipes-core/packagegroups/packagegroup-company.bb
@@
 RDEPENDS:${PN} = "\
     htop \
+    iperf3 \
 "
diff --git a/meta-company/recipes-connectivity/connman/connman_%.bbappend b/meta-company/recipes-connectivity/connman/connman_%.bbappend
+PACKAGECONFIG += "openvpn"
```

`packagegroup-company` is in `IMAGE_INSTALL` of our image via a bbappend. What will
actually change in the image, and how do I prove it?
