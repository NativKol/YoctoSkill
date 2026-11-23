<!-- Source: https://docs.yoctoproject.org/scarthgap/kernel-dev/faq.html (converted from singleindex.html). License: see LICENSE-docs.md in this folder. -->

#### 6 Kernel Development FAQ

##### 6.1 Common Questions and Solutions

Here are some solutions for common questions.

###### 6.1.1 How do I use my own Linux kernel `.config` file?

Refer to the “Changing the Configuration” section for information.

###### 6.1.2 How do I create configuration fragments?

A: Refer to the “Creating Configuration Fragments” section for information.

###### 6.1.3 How do I use my own Linux kernel sources?

Refer to the “Working With Your Own Sources” section for information.

###### 6.1.4 How do I install/not-install the kernel image on the root filesystem?

The kernel image (e.g. `vmlinuz`) is provided by the `kernel-image` package. Image recipes depend on `kernel-base`. To specify whether or not the kernel image is installed in the generated root filesystem, override `RRECOMMENDS:${KERNEL_PACKAGE_NAME}-base` to include or not include “kernel-image”. See the “Appending Other Layers Metadata With Your Layer” section in the Yocto Project Development Tasks Manual for information on how to use an append file to override metadata.

###### 6.1.5 How do I install a specific kernel module?

Linux kernel modules are packaged individually. To ensure a specific kernel module is included in an image, include it in the appropriate machine RRECOMMENDS variable. These other variables are useful for installing specific modules: - MACHINE_ESSENTIAL_EXTRA_RDEPENDS - MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS - MACHINE_EXTRA_RDEPENDS - MACHINE_EXTRA_RRECOMMENDS

For example, set the following in the `qemux86.conf` file to include the `ab123` kernel modules with images built for the `qemux86` machine:

```
MACHINE_EXTRA_RRECOMMENDS += "kernel-module-ab123"

```

For more information, see the “Incorporating Out-of-Tree Modules” section.

###### 6.1.6 How do I change the Linux kernel command line?

The Linux kernel command line is typically specified in the machine config using the APPEND variable. For example, you can add some helpful debug information doing the following:

```
APPEND += "printk.time=y initcall_debug debug"

```

The Yocto Project ®

<docs@lists.yoctoproject.org>

Permission is granted to copy, distribute and/or modify this document under the terms of the Creative Commons Attribution-Share Alike 2.0 UK: England & Wales as published by Creative Commons.

To report any inaccuracies or problems with this (or any other Yocto Project) manual, or to send additions or changes, please send email/patches to the Yocto Project documentation mailing list at `docs@lists.yoctoproject.org` or log into the Libera Chat `#yocto` channel.
