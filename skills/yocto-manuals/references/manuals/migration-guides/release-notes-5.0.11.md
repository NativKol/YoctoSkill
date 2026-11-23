<!-- Source: https://docs.yoctoproject.org/scarthgap/migration-guides/release-notes-5.0.11.html (converted from singleindex.html). License: see LICENSE-docs.md in this folder. -->

##### Release notes for Yocto-5.0.11 (Scarthgap)

###### Security Fixes in Yocto-5.0.11

- binutils: Fix CVE-2025-5244 and CVE-2025-5245

- busybox: Fix CVE-2022-48174

- coreutils: Fix CVE-2025-5278

- curl: Ignore CVE-2025-5025 if PACKAGECONFIG set with openssl

- ffmpeg: Fix CVE-2025-1373

- glibc: fix CVE-2025-4802 and CVE-2025-5702

- gnupg: Fix CVE-2025-30258

- go: Fix CVE-2025-4673

- go: Ignore CVE-2024-3566

- icu: Fix CVE-2025-5222

- kea: Fix CVE-2025-32801, CVE-2025-32802 and CVE-2025-32803

- libarchive: fix CVE-2025-5914, CVE-2025-5915, CVE-2025-5916, CVE-2025-5917 and CVE-2025-5918

- libsoup-2.4: Fix CVE-2025-2784, CVE-2025-4476, CVE-2025-4945, CVE-2025-4948, CVE-2025-4969, CVE-2025-32050, CVE-2025-32052, CVE-2025-32053, CVE-2025-32907 and CVE-2025-46421

- libsoup-3.4: Fix CVE-2025-2784, CVE-2025-4945, CVE-2025-4948, CVE-2025-4969, CVE-2025-32050, CVE-2025-32051, CVE-2025-32052, CVE-2025-32053, CVE-2025-32907, CVE-2025-32908 and CVE-2025-46421

- libxml2: Fix CVE-2025-6021

- linux-yocto-6.6: Fix CVE-2025-21995, CVE-2025-21996, CVE-2025-21997, CVE-2025-21999, CVE-2025-22001, CVE-2025-22003, CVE-2025-22004, CVE-2025-22005, CVE-2025-22007, CVE-2025-22009, CVE-2025-22010, CVE-2025-22014, CVE-2025-22018, CVE-2025-22020, CVE-2025-22027, CVE-2025-22033, CVE-2025-22035, CVE-2025-22038, CVE-2025-22040, CVE-2025-22041, CVE-2025-22054, CVE-2025-22056, CVE-2025-22063, CVE-2025-22066, CVE-2025-22080, CVE-2025-22081, CVE-2025-22088, CVE-2025-22097, CVE-2025-23136, CVE-2025-37785, CVE-2025-37800, CVE-2025-37801, CVE-2025-37803, CVE-2025-37805, CVE-2025-37838, CVE-2025-37893, CVE-2025-38152, CVE-2025-39728 and CVE-2025-39735

- net-tools: Fix CVE-2025-46836

- python3-setuptools: Fix CVE-2025-47273

- python3-requests: fix CVE-2024-47081

- python3-urllib3: Fix CVE-2025-50181

- python3: Fix CVE 2024-12718 CVE 2025-4138 CVE 2025-4330 CVE 2025-4435 CVE-2025-4516 CVE 2025-4517

- screen: fix CVE-2025-46802, CVE-2025-46804 and CVE-2025-46805

- sudo: Fix CVE-2025-32462

- xwayland: Fix CVE-2025-49175, CVE-2025-49176, CVE-2025-49177, CVE-2025-49178, CVE-2025-49179 and CVE-2025-49180

###### Fixes in Yocto-5.0.11

- bitbake: ast: Change deferred inherits to happen per recipe

- bitbake: fetch2: Avoid deprecation warning

- bitbake: gcp.py: remove slow calls to gsutil stat

- bitbake: toaster/tests/buildtest: Switch to new CDN

- brief-yoctoprojectqs/ref-manual: Switch to new CDN

- bsp-guide: update kernel version example to 6.12

- bsp-guide: update all of section 1.8.2 to reflect current beaglebone conf file

- bsp-guide: update lonely “4.12” kernel reference to “6.12”

- build-appliance-image: Update to scarthgap head revision

- cmake: Correctly handle cost data of tests with arbitrary chars in name

- conf.py: improve SearchEnglish to handle terms with dots

- docs: Clean up explanation of minimum required version numbers

- docs: README: specify how to contribute instead of pointing at another file

- docs: conf.py: silence SyntaxWarning on js_splitter_code

- gcc: Upgrade to GCC 13.4

- ghostscript: upgrade to 10.05.1

- glibc: stable 2.39 branch updates (06a70769fd…)

- gnupg: update to 2.4.8

- gtk+: add missing libdrm dependency

- kea: upgrade to 2.4.2

- libpng: Add ptest

- libsoup-2.4: fix do_compile failure

- linux-yocto/6.6: fix beaglebone ethernet

- linux-yocto/6.6: update to v6.6.96

- local.conf.sample: Switch to new CDN

- ltp: backport patch to fix compilation error for x86_64

- migration-guides: add release notes for 4.0.27, 4.0.28, 5.0.10

- minicom: correct the SRC_URI

- nfs-utils: don’t use signals to shut down nfs server.

- overview-manual/concepts.rst: fix sayhello hardcoded bindir

- overview-manual: small number of pedantic cleanups

- package: export debugsources in PKGDESTWORK as json

- poky.conf: bump version for 5.0.11

- python3-requests: upgrade to 2.32.4

- python3: upgrade to 3.12.11

- ref-manual: clarify KCONFIG_MODE default behaviour

- ref-manual: classes: nativesdk: move note to appropriate section

- ref-manual: classes: reword to clarify that native/nativesdk options are exclusive

- ref-manual: document KERNEL_SPLIT_MODULES variable

- scripts/install-buildtools: Update to 5.0.10

- spdx: add option to include only compiled sources

- sstatetests: Switch to new CDN

- systemd: Rename systemd_v255.21 to systemd_255.21

- systemd: upgrade to 255.21

- tcf-agent: correct the SRC_URI

- testimage: get real os-release file

- tune-cortexr52: Remove aarch64 for ARM Cortex-R52

- uboot: Allow for customizing installed/deployed file names

###### Known Issues in Yocto-5.0.11

- N/A

###### Contributors to Yocto-5.0.11

Thanks to the following people who contributed to this release: - Aleksandar Nikolic - Andrew Fernandes - Antonin Godard - Archana Polampalli - Ashish Sharma - Bruce Ashfield - Carlos Sánchez de La Lama - Changqing Li - Chen Qi - Colin Pinnell McAllister - Daniel Turull - Deepesh Varatharajan - Divya Chellam - Dixit Parmar - Enrico Jörns - Etienne Cordonnier - Guocai He - Guðni Már Gilbert - Hitendra Prajapati - Jiaying Song - Lee Chee Yang - Moritz Haase - NeilBrown - Peter Marko - Poonam Jadhav - Praveen Kumar - Preeti Sachan - Quentin Schulz - Richard Purdie - Robert P. J. Day - Roland Kovacs - Ryan Eatmon - Sandeep Gundlupet Raju - Savvas Etairidis - Steve Sakoman - Victor Giraud - Vijay Anusuri - Virendra Thakur - Wang Mingyu - Yogita Urade

###### Repositories / Downloads for Yocto-5.0.11

poky

- Repository Location: https://git.yoctoproject.org/poky

- Branch: scarthgap

- Tag: yocto-5.0.11

- Git Revision: ae2d52758fc2fcb0ed996aa234430464ebf4b310

- Release Artefact: poky-ae2d52758fc2fcb0ed996aa234430464ebf4b310

- sha: 48dec434dd51e5c9c626abdccc334da300fa2b4975137d526f5df6703e5a930e

- Download Locations: https://downloads.yoctoproject.org/releases/yocto/yocto-5.0.11/poky-ae2d52758fc2fcb0ed996aa234430464ebf4b310.tar.bz2 https://mirrors.kernel.org/yocto/yocto/yocto-5.0.11/poky-ae2d52758fc2fcb0ed996aa234430464ebf4b310.tar.bz2

openembedded-core

- Repository Location: https://git.openembedded.org/openembedded-core

- Branch: scarthgap

- Tag: yocto-5.0.11

- Git Revision: 7a59dc5ee6edd9596e87c2fbcd1f2594c06b3d1b

- Release Artefact: oecore-7a59dc5ee6edd9596e87c2fbcd1f2594c06b3d1b

- sha: fb50992a28298915fe195e327628d6d5872fd2dbc74189c2d840178cd860bb2e

- Download Locations: https://downloads.yoctoproject.org/releases/yocto/yocto-5.0.11/oecore-7a59dc5ee6edd9596e87c2fbcd1f2594c06b3d1b.tar.bz2 https://mirrors.kernel.org/yocto/yocto/yocto-5.0.11/oecore-7a59dc5ee6edd9596e87c2fbcd1f2594c06b3d1b.tar.bz2

meta-mingw

- Repository Location: https://git.yoctoproject.org/meta-mingw

- Branch: scarthgap

- Tag: yocto-5.0.11

- Git Revision: bd9fef71ec005be3c3a6d7f8b99d8116daf70c4f

- Release Artefact: meta-mingw-bd9fef71ec005be3c3a6d7f8b99d8116daf70c4f

- sha: ab073def6487f237ac125d239b3739bf02415270959546b6b287778664f0ae65

- Download Locations: https://downloads.yoctoproject.org/releases/yocto/yocto-5.0.11/meta-mingw-bd9fef71ec005be3c3a6d7f8b99d8116daf70c4f.tar.bz2 https://mirrors.kernel.org/yocto/yocto/yocto-5.0.11/meta-mingw-bd9fef71ec005be3c3a6d7f8b99d8116daf70c4f.tar.bz2

bitbake

- Repository Location: https://git.openembedded.org/bitbake

- Branch: 2.8

- Tag: yocto-5.0.11

- Git Revision: 139f61fe9eec221745184a14b3618d2dfa650b91

- Release Artefact: bitbake-139f61fe9eec221745184a14b3618d2dfa650b91

- sha: 86669d4220c50d35c0703f151571954ad9c6285cc91a870afbb878d2e555d2ca

- Download Locations: https://downloads.yoctoproject.org/releases/yocto/yocto-5.0.11/bitbake-139f61fe9eec221745184a14b3618d2dfa650b91.tar.bz2 https://mirrors.kernel.org/yocto/yocto/yocto-5.0.11/bitbake-139f61fe9eec221745184a14b3618d2dfa650b91.tar.bz2

meta-yocto

- Repository Location: https://git.yoctoproject.org/meta-yocto

- Branch: scarthgap

- Tag: yocto-5.0.11

- Git Revision: 50e5c0d85d3775ac1294bdcd7f11deaa382c9d08

yocto-docs

- Repository Location: https://git.yoctoproject.org/yocto-docs

- Branch: scarthgap

- Tag: yocto-5.0.11

- Git Revision: 3f88cb85cca8f9128cfaab36882c4563457b03d9
