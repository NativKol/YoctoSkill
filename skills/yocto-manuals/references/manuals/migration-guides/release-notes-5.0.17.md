<!-- Source: https://docs.yoctoproject.org/scarthgap/migration-guides/release-notes-5.0.17.html (converted from singleindex.html). License: see LICENSE-docs.md in this folder. -->

##### Release notes for Yocto-5.0.17 (Scarthgap)

Openssl 3.2 has reached EOL. Some projects would like to use LTS version due to criticality and exposure of this component, so upgrade to 3.5 branch.

###### Security Fixes in Yocto-5.0.17

- alsa-lib: Fix CVE-2026-25068

- avahi: Fix CVE-2025-68276, CVE-2025-68468, CVE-2025-68471 and CVE-2026-24401

- bind: Fix CVE-2025-13878

- busybox: Fix CVE-2025-60876

- ffmpeg: ignore CVE-2025-1594, CVE-2025-10256, CVE-2025-12343 and CVE-2025-25468

- freetype: Fix CVE-2026-23865

- gdk-pixbuf: Fix CVE-2025-6199

- glib-2.0: Fix CVE-2026-1484, CVE-2026-1485 and CVE-2026-1489

- gnupg: Fix CVE-2025-68973

- gnutls: Fix CVE-2025-14831

- go 1.22.12: Fix CVE-2025-61726, CVE-2025-61728, CVE-2025-61730, CVE-2025-61731, CVE-2025-61732, CVE-2025-68119 and CVE-2025-68121

- harfbuzz: Fix CVE-2026-22693

- inetutils: Fix CVE-2026-28372 and CVE-2026-32746

- libpng: Fix CVE-2026-25646

- libsndfile1: Fix CVE-2025-56226

- libtheora: Ignore CVE-2024-56431

- linux-yocto/6.6: Fix CVE-2025-38593, CVE-2025-38643, CVE-2025-38678, CVE-2025-40039, CVE-2025-40040, CVE-2025-40149, CVE-2025-40164, CVE-2025-40251, CVE-2025-68211, CVE-2025-68214, CVE-2025-68223, CVE-2025-68340, CVE-2025-68365, CVE-2025-68725, CVE-2025-68817, CVE-2025-71068, CVE-2025-71071, CVE-2025-71075, CVE-2025-71077, CVE-2025-71078, CVE-2025-71079, CVE-2025-71081, CVE-2025-71082, CVE-2025-71083, CVE-2025-71084, CVE-2025-71085, CVE-2025-71086, CVE-2025-71087, CVE-2025-71088, CVE-2025-71089, CVE-2025-71091, CVE-2025-71093, CVE-2025-71094, CVE-2025-71095, CVE-2025-71096, CVE-2025-71097, CVE-2025-71098, CVE-2025-71101, CVE-2025-71102, CVE-2025-71104, CVE-2025-71105, CVE-2025-71107, CVE-2025-71108, CVE-2025-71111, CVE-2025-71112, CVE-2025-71113, CVE-2025-71114, CVE-2025-71116, CVE-2025-71118, CVE-2025-71119, CVE-2025-71120, CVE-2025-71121, CVE-2025-71122, CVE-2025-71125, CVE-2025-71126, CVE-2025-71127, CVE-2025-71129, CVE-2025-71130, CVE-2025-71131, CVE-2025-71132, CVE-2025-71133, CVE-2025-71136, CVE-2025-71137, CVE-2025-71138, CVE-2025-71141, CVE-2025-71143, CVE-2025-71147, CVE-2025-71148, CVE-2025-71149, CVE-2025-71150, CVE-2025-71151, CVE-2025-71153, CVE-2025-71154, CVE-2025-71160, CVE-2025-71162, CVE-2025-71163, CVE-2025-71180, CVE-2025-71182, CVE-2025-71183, CVE-2025-71185, CVE-2025-71186, CVE-2025-71188, CVE-2025-71189, CVE-2025-71190, CVE-2025-71191, CVE-2025-71200, CVE-2026-22976, CVE-2026-22977, CVE-2026-22978, CVE-2026-22979, CVE-2026-22980, CVE-2026-22982, CVE-2026-22984, CVE-2026-22990, CVE-2026-22991, CVE-2026-22992, CVE-2026-22994, CVE-2026-22997, CVE-2026-22998, CVE-2026-22999, CVE-2026-23001, CVE-2026-23003, CVE-2026-23005, CVE-2026-23006, CVE-2026-23010, CVE-2026-23011, CVE-2026-23019, CVE-2026-23020, CVE-2026-23021, CVE-2026-23025, CVE-2026-23026, CVE-2026-23060, CVE-2026-23061, CVE-2026-23062, CVE-2026-23063, CVE-2026-23064, CVE-2026-23068, CVE-2026-23069, CVE-2026-23071, CVE-2026-23073, CVE-2026-23074, CVE-2026-23075, CVE-2026-23076, CVE-2026-23078, CVE-2026-23080, CVE-2026-23083, CVE-2026-23084, CVE-2026-23085, CVE-2026-23086, CVE-2026-23087, CVE-2026-23088, CVE-2026-23089, CVE-2026-23090, CVE-2026-23091, CVE-2026-23093, CVE-2026-23094, CVE-2026-23095, CVE-2026-23096, CVE-2026-23097, CVE-2026-23098, CVE-2026-23099, CVE-2026-23101, CVE-2026-23102, CVE-2026-23103, CVE-2026-23105, CVE-2026-23107, CVE-2026-23108, CVE-2026-23110, CVE-2026-23113, CVE-2026-23116, CVE-2026-23119, CVE-2026-23120, CVE-2026-23121, CVE-2026-23123, CVE-2026-23124, CVE-2026-23125, CVE-2026-23126, CVE-2026-23128, CVE-2026-23131, CVE-2026-23133, CVE-2026-23135, CVE-2026-23136, CVE-2026-23139, CVE-2026-23140, CVE-2026-23141, CVE-2026-23142, CVE-2026-23144, CVE-2026-23146, CVE-2026-23150, CVE-2026-23156, CVE-2026-23160, CVE-2026-23163, CVE-2026-23164, CVE-2026-23167, CVE-2026-23168, CVE-2026-23170, CVE-2026-23172, CVE-2026-23173 and CVE-2026-23212

- openssl: fix CVE-2025-15468 and CVE-2025-69419

- python3-cryptography: Fix CVE-2026-26007

- python3-pip: Fix CVE-2026-1703

- python3-pyopenssl: Fix CVE-2026-27448 and CVE-2026-27459

- tiff: ignore CVE-2025-61144 and CVE-2025-61145

- vim: ignore CVE-2025-66476

- zlib: Fix CVE-2026-27171

###### Fixes in Yocto-5.0.17

- README: Add scarthgap subject-prefix to git-send-email suggestion

- bind: upgrade to 9.18.44

- bitbake: COW: Fix hardcoded magic numbers and work with python 3.13

- bitbake: fetch2: Fix LFS object checkout in submodules

- bitbake: fetch2: Fix incorrect lfs parametrization for submodules

- bitbake: fetch2: don’t try to preserve all attributes when unpacking files

- bitbake: gitsm: Add clean function

- build-appliance-image: Update to scarthgap head revision

- classes/buildhistory: Do not sign buildhistory commits

- create-pull-request: Keep commit hash to be pulled in cover email

- dev-manual: delete references to “tar” package format

- docs: Makefile: pass -silent to latexmk

- go-vendor: Fix absolute paths issue

- improve_kernel_cve_report: add option to read debugsources.zstd

- improve_kernel_cve_report: do not override backported-patch

- improve_kernel_cve_report: do not use custom version

- linux-yocto/6.6: upgrade to v6.6.123

- lsb.py: strip ‘ from os-release file

- migration-guides: add release notes for 5.0.16

- mobile-broadband-provider-info: upgrade to 20251101

- oe-setup-build: Fix typo

- oeqa/selftest/wic: test recursive dir copy on ext partitions

- openssl: upgrade to 3.5.5

- overview-manual/concepts: list other possible class directories

- overview-manual: escape wildcard in inline markup

- poky.conf: Bump version for 5.0.17 release

- poky.conf: add Centos Stream 9, fedora-41, rocky-8 to SANITY_TESTED_DISTROS

- pseudo: Update to include a fix for systems with kernel <5.6

- python3-pip: drop unused Windows distlib launcher templates

- python3-setuptools: drop Windows launcher executables on non-mingw builds

- ref-manual/classes.rst: fix broken links to U-Boot documentation

- ref-manual/system-requirements.rst: update supported, end-of-life and untested distros

- scripts/install-buildtools: Update to 5.0.15

- spdx30_tasks: Exclude ‘doc’ when exporting PACKAGECONFIG to SPDX

- spdx: add option to include only compiled sources

- systemd-systemctl: Fix instance name parsing with escapes or periods

- tzdata,tzcode-native: upgrade to 2025c

- u-boot: move CVE Fixes out of the common .inc file

- uboot-config: Fix devtool modify

- weston: fix a touch-calibrator issue

- what-i-wish-id-known.rst: replace figure by the new SVG

- wic/engine: error on old host debugfs for standalone directory copy

- wic/engine: fix copying directories into wic image with ext* partition

- wireless-regdb: upgrade to 2026.02.04

###### Known Issues in Yocto-5.0.17

- N/A

###### Contributors to Yocto-5.0.17

- Aleksandar Nikolic

- Amaury Couderc

- Ankur Tyagi

- Antonin Godard

- Benjamin Robin (Schneider Electric)

- Bruce Ashfield

- Daniel Dragomir

- Daniel Turull

- Deepak Rathore

- Dragomir, Daniel

- Eduardo Ferreira

- Fabio Berton

- Hitendra Prajapati

- Hugo SIMELIERE

- João Marcos Costa (Schneider Electric)

- Kristiyan Chakarov

- Krupal Ka Patel

- Lee Chee Yang

- Livin Sunny

- Martin Jansa

- Michael Opdenacker

- Ming Liu

- Nguyen Dat Tho

- Paul Barker

- Peter Marko

- Philip Lorenz

- Quentin Schulz

- Richard Purdie

- Robert P. J. Day

- Robert Yang

- Ross Burton

- Ryan Eatmon

- Shaik Moin

- Tom Hochstein

- Trent Piepho

- Vijay Anusuri

- Yoann Congal

###### Repositories / Downloads for Yocto-5.0.17

yocto-docs

- Repository Location: https://git.yoctoproject.org/yocto-docs

- Branch: scarthgap

- Tag: yocto-5.0.17

- Git Revision: aa7226705451e6c1ef964d49963bbed29b267c27

- Release Artefact: yocto-docs-aa7226705451e6c1ef964d49963bbed29b267c27

- sha: d429833609637657f213611317dfadbd70293fff2f9e22753d1f71ef8515a6c0

- Download Locations:

https://downloads.yoctoproject.org/releases/yocto/yocto-5.0.17/yocto-docs-aa7226705451e6c1ef964d49963bbed29b267c27.tar.bz2

https://mirrors.edge.kernel.org/yocto/yocto/yocto-5.0.17/yocto-docs-aa7226705451e6c1ef964d49963bbed29b267c27.tar.bz2

poky

- Repository Location: https://git.yoctoproject.org/poky

- Branch: scarthgap

- Tag: yocto-5.0.17

- Git Revision: 1e8099846661571ede077f533eb1b6c86818ddce

- Release Artefact: poky-1e8099846661571ede077f533eb1b6c86818ddce

- sha: b56890576f593cc881ea8e467562d842cfca248099ce653d28ca14d250f6219e

- Download Locations:

https://downloads.yoctoproject.org/releases/yocto/yocto-5.0.17/poky-1e8099846661571ede077f533eb1b6c86818ddce.tar.bz2

https://mirrors.edge.kernel.org/yocto/yocto/yocto-5.0.17/poky-1e8099846661571ede077f533eb1b6c86818ddce.tar.bz2

openembedded-core

- Repository Location: https://git.openembedded.org/openembedded-core

- Branch: scarthgap

- Tag: yocto-5.0.17

- Git Revision: 52380df998b3a8fe6a091f8547434a3231320a8e

- Release Artefact: oecore-52380df998b3a8fe6a091f8547434a3231320a8e

- sha: a948d75acf76a392d170129ce6eb6f5fe45082d95b4fd28045aac58b8373cb26

- Download Locations:

https://downloads.yoctoproject.org/releases/yocto/yocto-5.0.17/oecore-52380df998b3a8fe6a091f8547434a3231320a8e.tar.bz

https://mirrors.edge.kernel.org/yocto/yocto/yocto-5.0.17/oecore-52380df998b3a8fe6a091f8547434a3231320a8e.tar.bz2

meta-yocto

- Repository Location: https://git.yoctoproject.org/meta-yocto

- Branch: scarthgap

- Tag: yocto-5.0.17

- Git Revision: c7c38663a1cafb1fa8593c0b246811e51d3bbe20

- Release Artefact: meta-yocto-c7c38663a1cafb1fa8593c0b246811e51d3bbe20

- sha: 5a2a9360249e639694cc2a75985e3907085512b3eb236e8491cb07f1e0cb0f19

- Download Locations:

https://downloads.yoctoproject.org/releases/yocto/yocto-5.0.17/meta-yocto-c7c38663a1cafb1fa8593c0b246811e51d3bbe20.tar.bz2

https://mirrors.edge.kernel.org/yocto/yocto/yocto-5.0.17/meta-yocto-c7c38663a1cafb1fa8593c0b246811e51d3bbe20.tar.bz2

meta-mingw

- Repository Location: https://git.yoctoproject.org/meta-mingw

- Branch: scarthgap

- Tag: yocto-5.0.17

- Git Revision: bd9fef71ec005be3c3a6d7f8b99d8116daf70c4f

- Release Artefact: meta-mingw-bd9fef71ec005be3c3a6d7f8b99d8116daf70c4f

- sha: ab073def6487f237ac125d239b3739bf02415270959546b6b287778664f0ae65

- Download Locations:

https://downloads.yoctoproject.org/releases/yocto/yocto-5.0.17/meta-mingw-bd9fef71ec005be3c3a6d7f8b99d8116daf70c4f.tar.bz2

https://mirrors.edge.kernel.org/yocto/yocto/yocto-5.0.17/meta-mingw-bd9fef71ec005be3c3a6d7f8b99d8116daf70c4f.tar.bz2

bitbake

- Repository Location: https://git.openembedded.org/bitbake

- Branch: 2.8

- Tag: yocto-5.0.17

- Git Revision: d3b4c352dd33fca90cd31649eda054b884478739

- Release Artefact: bitbake-d3b4c352dd33fca90cd31649eda054b884478739

- sha: 1021fc412780e21b25ccb045b66368ebe3fc4e785a65066ac0cafb9bdd5492fa

- Download Locations:

https://downloads.yoctoproject.org/releases/yocto/yocto-5.0.17/bitbake-d3b4c352dd33fca90cd31649eda054b884478739.tar.bz2

https://mirrors.edge.kernel.org/yocto/yocto/yocto-5.0.17/bitbake-d3b4c352dd33fca90cd31649eda054b884478739.tar.bz2
