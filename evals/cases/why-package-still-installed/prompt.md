I'm trying to slim down our scarthgap image. I put this in local.conf:

```bitbake
BAD_RECOMMENDATIONS:pn-our-image = "busybox-syslog"
```

but `busybox-syslog` is still in `tmp/deploy/images/<machine>/our-image-<machine>.rootfs.manifest`
after rebuilding. We use the default poky PACKAGE_CLASSES. How do I find out what is
pulling it in and get rid of it?
