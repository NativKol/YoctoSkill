<!-- Source: https://docs.yoctoproject.org/scarthgap/migration-guides/release-notes-5.0.8.html (converted from singleindex.html). License: see LICENSE-docs.md in this folder. -->

##### Release notes for Yocto-5.0.8 (Scarthgap)

###### Security Fixes in Yocto-5.0.8

- binutils: Fix CVE-2025-0840

- curl: Ignore CVE-2025-0725

- elfutils: Fix CVE-2025-1352, CVE-2025-1365 and CVE-2025-1372

- ffmpeg: Fix CVE-2024-35365, CVE-2024-35369, CVE-2024-36613, CVE-2024-36616, CVE-2024-36617, CVE-2024-36618, CVE-2024-36619, CVE-2025-0518, CVE-2025-22919, CVE-2025-22921 and CVE-2025-25473

- glibc: Fix CVE-2025-0395

- gnutls: Fix CVE-2024-12243

- go: Fix CVE-2024-45336, CVE-2024-45341 and CVE-2025-22866

- gstreamer1.0-rtsp-server: Fix CVE-2024-44331

- libcap: Fix CVE-2025-1390

- libtasn1: Fix CVE-2024-12133

- libxml2: Fix CVE-2024-56171 and CVE-2025-24928

- linux-yocto/6.6: Fix CVE-2024-36476, CVE-2024-53179, CVE-2024-56582, CVE-2024-56703, CVE-2024-57801, CVE-2024-57802, CVE-2024-57841, CVE-2024-57882, CVE-2024-57887, CVE-2024-57890, CVE-2024-57892, CVE-2024-57895, CVE-2024-57896, CVE-2024-57900, CVE-2024-57901, CVE-2024-57902, CVE-2024-57906, CVE-2024-57907, CVE-2024-57908, CVE-2024-57910, CVE-2024-57911, CVE-2024-57912, CVE-2024-57913, CVE-2024-57916, CVE-2024-57922, CVE-2024-57925, CVE-2024-57926, CVE-2024-57933, CVE-2024-57938, CVE-2024-57939, CVE-2024-57940, CVE-2024-57949, CVE-2024-57951, CVE-2025-21631, CVE-2025-21636, CVE-2025-21637, CVE-2025-21638, CVE-2025-21639, CVE-2025-21640, CVE-2025-21642, CVE-2025-21652, CVE-2025-21658, CVE-2025-21665, CVE-2025-21666, CVE-2025-21667, CVE-2025-21669, CVE-2025-21670, CVE-2025-21671, CVE-2025-21673, CVE-2025-21674, CVE-2025-21675, CVE-2025-21676, CVE-2025-21680, CVE-2025-21681, CVE-2025-21683, CVE-2025-21684, CVE-2025-21687, CVE-2025-21689, CVE-2025-21690, CVE-2025-21692, CVE-2025-21694, CVE-2025-21697 and CVE-2025-21699

- openssh: Fix CVE-2025-26466

- openssl: Fix CVE-2024-9143, CVE-2024-12797 and CVE-2024-13176

- pyhton3: Fix CVE-2024-12254 and CVE-2025-0938

- subversion: Ignore CVE-2024-45720

- u-boot: Fix CVE-2024-57254, CVE-2024-57255, CVE-2024-57256, CVE-2024-57257, CVE-2024-57258 and CVE-2024-57259

- vim: Fix CVE-2025-22134 and CVE-2025-24014

- xwayland: Fix CVE-2024-9632, CVE-2025-26594, CVE-2025-26595, CVE-2025-26596, CVE-2025-26597, CVE-2025-26598, CVE-2025-26599, CVE-2025-26600 and CVE-2025-26601

###### Fixes in Yocto-5.0.8

- base-files: Drop /bin/sh dependency

- bind: upgrade to 9.18.33

- binutils: File name too long causing failure to open temporary head file in dlltool

- binutils: stable 2.42 branch update

- bitbake: bblayers/query: Fix using “removeprefix” string method

- bitbake: bitbake-diffsigs: fix handling when finding only a single sigfile

- bitbake: data_smart.py: clear expand_cache in _setvar_update_overridevars

- bitbake: data_smart.py: remove unnecessary ? from __expand_var_regexp__

- bitbake: data_smart.py: simple clean up

- build-appliance-image: Update to scarthgap head revision

- ccache.conf: Add include_file_ctime to sloppiness

- cmake: apply parallel build settings to ptest tasks

- contributor-guide/submit-changes: add policy on AI generated code

- dev-manual/building: document the initramfs-framework recipe

- devtool: ide-sdk recommend DEBUG_BUILD

- devtool: ide-sdk remove the plugin from eSDK installer

- devtool: ide-sdk sort cmake preset

- devtool: modify support debug-builds

- docs: Add favicon for the documentation html

- docs: Fix typo in standards.md

- docs: Remove all mention of core-image-lsb

- docs: vulnerabilities/classes: remove references to cve-check text format

- files: Amend overlayfs unit descriptions with path information

- files: overlayfs-create-dirs: Improve mount unit dependency

- glibc: stable 2.39 branch updates

- gnupg: upgrade to 2.4.5

- go: upgrade 1.22.12

- icu: remove host references in nativesdk to fix reproducibility

- libtasn1: upgrade to 4.20.0

- libxml2: upgrade to 2.12.10

- linux-yocto/6.6: upgrade to v6.6.75

- meta: Enable ‘-o pipefail’ for the SDK installer

- migration-guides: add release notes for 4.0.24, 4.0.25 and 5.0.7

- oe-selftest: devtool ide-sdk use modify debug-build

- oeqa/sdk/context: fix for gtk3 test failure during do_testsdk

- oeqa/selftest/rust: skip on all MIPS platforms

- openssl: upgrade to 3.2.4

- pkg-config-native: pick additional search paths from $EXTRA_NATIVE_PKGCONFIG_PATH

- poky.conf: add ubuntu2404 to SANITY_TESTED_DISTROS

- poky.conf: bump version for 5.0.8

- ppp: Revert lock path to /var/lock

- python3-setuptools-scm: respect GIT_CEILING_DIRECTORIES

- python3: upgrade to 3.12.9

- qemu: Do not define sched_attr with glibc >= 2.41

- ref-manual/faq: add q&a on systemd as default

- ref-manual: Add missing variable IMAGE_ROOTFS_MAXSIZE

- ref-manual: don’t refer to poky-lsb

- ref-manual: remove OE_IMPORTS

- rust-common.bbclass: soft assignment for RUSTLIB path

- rust: fix for rust multilib sdk configuration

- rust: remove redundant cargo config file

- scripts/install-buildtools: Update to 5.0.7

- sdk-manual: extensible.rst: devtool ide-sdk improve

- sdk-manual: extensible.rst: update devtool ide-sdk

- selftest/rust: correctly form the PATH environment variable

- systemd: add libpcre2 as RRECOMMENDS if pcre2 is enabled

- systemd: upgrade to 255.17

- test-manual/ptest: link to common framework ptest classes

- tzcode-native: Fix compiler setting from 2023d version

- tzdata/tzcode-native: upgrade to 2025a

- u-boot: kernel-fitimage: Fix dependency loop if UBOOT_SIGN_ENABLE and UBOOT_ENV enabled

- u-boot: kernel-fitimage: Restore FIT_SIGN_INDIVIDUAL=”1” behavior

- uboot-config: fix devtool modify with kernel-fitimage

- vim: upgrade to 9.1.1043

###### Known Issues in Yocto-5.0.8

- N/A

###### Contributors to Yocto-5.0.8

Thanks to the following people who contributed to this release:

- Adrian Freihofer

- Aleksandar Nikolic

- Alessio Cascone

- Alexander Kanavin

- Alexis Cellier

- Antonin Godard

- Archana Polampalli

- Bruce Ashfield

- Chen Qi

- Deepesh Varatharajan

- Divya Chellam

- Enrico Jörns

- Esben Haabendal

- Etienne Cordonnier

- Fabio Berton

- Guðni Már Gilbert

- Harish Sadineni

- Hitendra Prajapati

- Hongxu Jia

- Jiaying Song

- Joerg Schmidt

- Johannes Schneider

- Khem Raj

- Lee Chee Yang

- Marek Vasut

- Marta Rybczynska

- Moritz Haase

- Oleksandr Hnatiuk

- Pedro Ferreira

- Peter Marko

- Poonam Jadhav

- Priyal Doshi

- Ross Burton

- Simon A. Eugster

- Steve Sakoman

- Vijay Anusuri

- Wang Mingyu

- Weisser, Pascal

###### Repositories / Downloads for Yocto-5.0.8

poky

- Repository Location: https://git.yoctoproject.org/poky

- Branch: scarthgap

- Tag: yocto-5.0.8

- Git Revision: dc4827b3660bc1a03a2bc3b0672615b50e9137ff

- Release Artefact: poky-dc4827b3660bc1a03a2bc3b0672615b50e9137ff

- sha: ace7264e16e18ed02ef0ad2935fa10b5fad2c4de38b2356f4192b38ef2184504

- Download Locations: https://downloads.yoctoproject.org/releases/yocto/yocto-5.0.8/poky-dc4827b3660bc1a03a2bc3b0672615b50e9137ff.tar.bz2 https://mirrors.kernel.org/yocto/yocto/yocto-5.0.8/poky-dc4827b3660bc1a03a2bc3b0672615b50e9137ff.tar.bz2

openembedded-core

- Repository Location: https://git.openembedded.org/openembedded-core

- Branch: scarthgap

- Tag: yocto-5.0.8

- Git Revision: cd2b6080a4c0f2ed2c9939ec0b87763aef595048

- Release Artefact: oecore-cd2b6080a4c0f2ed2c9939ec0b87763aef595048

- sha: 14c7cd5c62a96ceb9c2141164ea0f087fdbaed99ca3e9a722977a3f12d6381f6

- Download Locations: https://downloads.yoctoproject.org/releases/yocto/yocto-5.0.8/oecore-cd2b6080a4c0f2ed2c9939ec0b87763aef595048.tar.bz2 https://mirrors.kernel.org/yocto/yocto/yocto-5.0.8/oecore-cd2b6080a4c0f2ed2c9939ec0b87763aef595048.tar.bz2

meta-mingw

- Repository Location: https://git.yoctoproject.org/meta-mingw

- Branch: scarthgap

- Tag: yocto-5.0.8

- Git Revision: bd9fef71ec005be3c3a6d7f8b99d8116daf70c4f

- Release Artefact: meta-mingw-bd9fef71ec005be3c3a6d7f8b99d8116daf70c4f

- sha: ab073def6487f237ac125d239b3739bf02415270959546b6b287778664f0ae65

- Download Locations: https://downloads.yoctoproject.org/releases/yocto/yocto-5.0.8/meta-mingw-bd9fef71ec005be3c3a6d7f8b99d8116daf70c4f.tar.bz2 https://mirrors.kernel.org/yocto/yocto/yocto-5.0.8/meta-mingw-bd9fef71ec005be3c3a6d7f8b99d8116daf70c4f.tar.bz2

bitbake

- Repository Location: https://git.openembedded.org/bitbake

- Branch: 2.8

- Tag: yocto-5.0.8

- Git Revision: 7375d32e8c1af20c51abec4eb3b072b4ca58b239

- Release Artefact: bitbake-7375d32e8c1af20c51abec4eb3b072b4ca58b239

- sha: 13dffbc162c5b6e2c95fa72936a430b9a542d52d81d502a5d0afc592fbf4a16b

- Download Locations: https://downloads.yoctoproject.org/releases/yocto/yocto-5.0.8/bitbake-7375d32e8c1af20c51abec4eb3b072b4ca58b239.tar.bz2 https://mirrors.kernel.org/yocto/yocto/yocto-5.0.8/bitbake-7375d32e8c1af20c51abec4eb3b072b4ca58b239.tar.bz2

yocto-docs

- Repository Location: https://git.yoctoproject.org/yocto-docs

- Branch: scarthgap

- Tag: yocto-5.0.8

- Git Revision: 7d3cce5b962ca9f73b29affceb7ebc6710627739
