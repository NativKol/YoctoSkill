<!-- Source: https://docs.yoctoproject.org/scarthgap/sdk-manual/appendix-customizing-standard.html (converted from singleindex.html). License: see LICENSE-docs.md in this folder. -->

#### 7 Customizing the Standard SDK

This appendix presents customizations you can apply to the standard SDK.

##### 7.1 Adding Individual Packages to the Standard SDK

When you build a standard SDK using the `bitbake -c populate_sdk`, a default set of packages is included in the resulting SDK. The TOOLCHAIN_HOST_TASK and TOOLCHAIN_TARGET_TASK variables control the set of packages adding to the SDK.

If you want to add individual packages to the toolchain that runs on the host, simply add those packages to the TOOLCHAIN_HOST_TASK variable. Similarly, if you want to add packages to the default set that is part of the toolchain that runs on the target, add the packages to the TOOLCHAIN_TARGET_TASK variable.

##### 7.2 Adding API Documentation to the Standard SDK

You can include API documentation as well as any other documentation provided by recipes with the standard SDK by adding “api-documentation” to the DISTRO_FEATURES variable: DISTRO_FEATURES:append = “ api-documentation” Setting this variable as shown here causes the OpenEmbedded build system to build the documentation and then include it in the standard SDK.

The Yocto Project ®

<docs@lists.yoctoproject.org>

Permission is granted to copy, distribute and/or modify this document under the terms of the Creative Commons Attribution-Share Alike 2.0 UK: England & Wales as published by Creative Commons.

To report any inaccuracies or problems with this (or any other Yocto Project) manual, or to send additions or changes, please send email/patches to the Yocto Project documentation mailing list at `docs@lists.yoctoproject.org` or log into the Libera Chat `#yocto` channel.
