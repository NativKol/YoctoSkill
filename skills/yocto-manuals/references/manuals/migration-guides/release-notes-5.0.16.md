<!-- Source: https://docs.yoctoproject.org/scarthgap/migration-guides/release-notes-5.0.16.html (converted from singleindex.html). License: see LICENSE-docs.md in this folder. -->

##### Release notes for Yocto-5.0.16 (Scarthgap)

This release breaks support for Ubuntu 20.04 as a compatible host. The Ubuntu 20.04 Linux kernel headers are not recent enough to support the latest pseudo fixes.

Ubuntu 20.04 is End-of-Life since 31 May 2025. Impacted users are encouraged to upgrade to an actively supported host distribution. See System Requirements for more information on compatible hosts.

Alternatively, a fix has been merged to scarthgap branch and can be applied on top of this release:

- https://git.openembedded.org/openembedded-core/commit/?h=scarthgap&id=fe2666749094e896736ff24d6885419905488723

- https://git.yoctoproject.org/poky/commit/?h=scarthgap&id=65c3ebea05dde5cbc9d249e7949fabbc0047313e

###### Security Fixes in Yocto-5.0.16

- curl: Fix CVE-2025-10148, CVE-2025-14017, CVE-2025-14524, CVE-2025-14819, CVE-2025-15079 and CVE-2025-15224

- dropbear: Fix CVE-2019-6111

- expat: Fix CVE-2026-24515 and CVE-2026-25210

- ffmpeg: Ignore CVE-2025-25469

- glib-2.0: Fix CVE-2025-13601, CVE-2025-14087, CVE-2025-14512 and CVE-2026-0988

- glibc: FIx CVE-2025-15281, CVE-2026-0861 and CVE-2026-0915

- inetutils: Fix CVE-2026-24061

- libarchive: Fix CVE-2025-60753 (follow-up fix)

- libpcap: Fix CVE-2025-11961 and CVE-2025-11964

- libpng: Fix CVE-2026-22695 and CVE-2026-22801

- libtasn1: Fix CVE-2025-13151

- libxml2: Fix CVE-2026-0989, CVE-2026-0990 and CVE-2026-0992

- python-urllib3: Fix for CVE-2026-21441

- python3: Fix CVE-2025-12084, CVE-2025-13836 and CVE-2025-13837

- qemu: Ignore CVE-2025-54566 and CVE-2025-54567

- util-linux: Fix CVE-2025-14104

- zlib: Ignore CVE-2026-22184

###### Fixes in Yocto-5.0.16

- bitbake: knotty: Make sure getTerminalColumns() returns two integers

- bitbake: knotty: fix TIOCGWINSZ call for Python 3.14 and later

- build-appliance-image: Update to scarthgap head revision

- contributor-guide/recipe-style-guide.rst: explain difference between layer and recipe license(s)

- contributor-guide/submit-changes.rst: remove mention of Upstream-Status

- cups: allow unknown directives in conf files

- dev-manual/packages.rst: fix example recipe version

- dev-manual/packages.rst: pr server: fix and explain why r0.X increments on SRCREV change

- dev-manual/packages.rst: rename r0.0 to r0 when PR server is not enabled

- dev-manual/temporary-source-code.rst: fix definition of WORKDIR

- docbook-xml-dtd4: fix the fetching failure

- docs: Add a new “Security” section

- docs: Makefile: fix rsvg-convert –format capitalization

- ffmpeg: upgrade to 6.1.4

- glibc: stable 2.39 branch updates

- improve_kernel_cve_report: add script for postprocesing of kernel CVE data

- libtheora: set CVE_PRODUCT

- lighttpd: Fix trailing slash on files in mod_dirlisting

- meta/classes: fix missing vardeps for CVE status variables

- migration-guides: add release notes for 4.0.32, 5.0.14 and 5.0.15

- overview-manual/yp-intro.rst: change removed ECOSYSTEM to ABOUT

- overview-manual/yp-intro.rst: fix SDK type in bullet list

- overview-manual/yp-intro.rst: link to YP members and participants

- overview-manual: convert YP-flow-diagram.png to SVG

- pseudo: Add hard sstate dependencies for pseudo-native

- pseudo: Update to 1.9.3 release

- ref-manual/classes.rst: document the image-container class

- ref-manual/release-process.rst: add a “Development Cycle” section

- ref-manual/svg/releases.svg: mark styhead and walnascar EOL

- ref-manual/svg/releases.svg: mark whinlatter as current release

- ref-manual/variables.rst: document the CCACHE_TOP_DIR variable

- sdk-manual: appending-customizing: use none lexer for BitBake code blocks

- sdk-manual: appendix-obtain: fix default path for eSDK installer script

- sdk-manual: appendix-obtain: replace directory structure PNG with a parsed-literal block

- sdk-manual: appendix-obtain: replace eSDK directory structure PNG with a parsed-literal block

- sdk-manual: appendix-obtain: use parsed-literal block for naming convention of the installer scripts

- sdk-manual: delete sdk-title PNG

- sdk-manual: fix improper indent of general form of tarball installer scripts

- sdk-manual: fix incorrect highlight language for console code-blocks

- sdk-manual: fix incorrect highlight language for text code-blocks

- sdk-manual: replace sdk-environment PNG with SVG

- sdk-manual: using: fix SDK filename example

- sdk-manual: working-projects: properly highlight code code-blocks

- test-manual/ptest.rst: detail the exit code and output requirements

- zlib: Add CVE_PRODUCT to exclude false positives

- zlib: cleanup obsolete CVE_STATUS[CVE-2023-45853]

###### Known Issues in Yocto-5.0.16

The poky DISTRO_VERSION was incorrectly left at 5.0.15. This is a minor issue, if a workaround is needed please cherry-pick:

- poky commit https://git.yoctoproject.org/poky/commit/?h=scarthgap&id=06210079b2e10d6d3fb943afe87864267e329821

- meta-yocto commit https://git.yoctoproject.org/meta-yocto/commit/?h=scarthgap&id=03f93c769ec99e5086e492d8145eb308a718e8d3

###### Contributors to Yocto-5.0.16

Thanks to the following people who contributed to this release:

- Adarsh Jagadish Kamini

- Amaury Couderc

- Ankur Tyagi

- Antonin Godard

- Benjamin Robin (Schneider Electric)

- Daniel Turull

- Enrico Scholz

- Fred Bacon

- Het Patel

- Hitendra Prajapati

- Hugo SIMELIERE

- Ken Kurematsu

- Khai Dang

- Lee Chee Yang

- Paul Barker

- Peter Marko

- Quentin Schulz

- Richard Purdie

- Robert Yang

- Vijay Anusuri

- Yoann Congal

- Zoltan Boszormenyi

###### Repositories / Downloads for Yocto-5.0.16

yocto-docs

- Repository Location: https://git.yoctoproject.org/yocto-docs

- Branch: scarthgap

- Tag: yocto-5.0.16

- Git Revision: 369f3307368eaea605983e80047377fd19ebd6bf

- Release Artefact: yocto-docs-369f3307368eaea605983e80047377fd19ebd6bf

- sha: e8ea8e2d5da2bfad868178d6fb37093c4f9ff06553f68970f0f730d6fb5cbd26

- Download Locations:

https://downloads.yoctoproject.org/releases/yocto/yocto-5.0.16/yocto-docs-369f3307368eaea605983e80047377fd19ebd6bf.tar.bz2

https://mirrors.edge.kernel.org/yocto/yocto/yocto-5.0.16/yocto-docs-369f3307368eaea605983e80047377fd19ebd6bf.tar.bz2

poky

- Repository Location: https://git.yoctoproject.org/poky

- Branch: scarthgap

- Tag: yocto-5.0.16

- Git Revision: 1d54d1c4736a114e1cecbe85a0306e3814d5ce70

- Release Artefact: poky-1d54d1c4736a114e1cecbe85a0306e3814d5ce70

- sha: efb75697fa7a8e35a3f46abcfa706400f56ae1d1b5e360b48d6ffa81f6a675e8

- Download Locations:

https://downloads.yoctoproject.org/releases/yocto/yocto-5.0.16/poky-1d54d1c4736a114e1cecbe85a0306e3814d5ce70.tar.bz2

https://mirrors.edge.kernel.org/yocto/yocto/yocto-5.0.16/poky-1d54d1c4736a114e1cecbe85a0306e3814d5ce70.tar.bz2

openembedded-core

- Repository Location: https://git.openembedded.org/openembedded-core

- Branch: scarthgap

- Tag: yocto-5.0.16

- Git Revision: a1f4ae4e569bc0e36c27c1e4651e502e54d63b28

- Release Artefact: oecore-a1f4ae4e569bc0e36c27c1e4651e502e54d63b28

- sha: 10eefd2296206e5cbaf138de7dbd0dbe7bfc413618e924a123cd3f7f9a8418e0

- Download Locations:

https://downloads.yoctoproject.org/releases/yocto/yocto-5.0.16/oecore-a1f4ae4e569bc0e36c27c1e4651e502e54d63b28.tar.bz2

https://mirrors.edge.kernel.org/yocto/yocto/yocto-5.0.16/oecore-a1f4ae4e569bc0e36c27c1e4651e502e54d63b28.tar.bz2

meta-yocto

- Repository Location: https://git.yoctoproject.org/meta-yocto

- Branch: scarthgap

- Tag: yocto-5.0.16

- Git Revision: 9bb6e6e8b016a0c9dfe290369a6ed91ef4020535

- Release Artefact: meta-yocto-9bb6e6e8b016a0c9dfe290369a6ed91ef4020535

- sha: d9cfd2192d12ebc55553bc421f3ab00d1f49c5f5c4c70e48923da695d19e8e2a

- Download Locations:

https://downloads.yoctoproject.org/releases/yocto/yocto-5.0.16/meta-yocto-9bb6e6e8b016a0c9dfe290369a6ed91ef4020535.tar.bz2

https://mirrors.edge.kernel.org/yocto/yocto/yocto-5.0.16/meta-yocto-9bb6e6e8b016a0c9dfe290369a6ed91ef4020535.tar.bz2

meta-mingw

- Repository Location: https://git.yoctoproject.org/meta-mingw

- Branch: scarthgap

- Tag: yocto-5.0.16

- Git Revision: bd9fef71ec005be3c3a6d7f8b99d8116daf70c4f

- Release Artefact: meta-mingw-bd9fef71ec005be3c3a6d7f8b99d8116daf70c4f

- sha: ab073def6487f237ac125d239b3739bf02415270959546b6b287778664f0ae65

- Download Locations:

https://downloads.yoctoproject.org/releases/yocto/yocto-5.0.16/meta-mingw-bd9fef71ec005be3c3a6d7f8b99d8116daf70c4f.tar.bz2

https://mirrors.edge.kernel.org/yocto/yocto/yocto-5.0.16/meta-mingw-bd9fef71ec005be3c3a6d7f8b99d8116daf70c4f.tar.bz2

bitbake

- Repository Location: https://git.openembedded.org/bitbake

- Branch: 2.8

- Tag: yocto-5.0.16

- Git Revision: 10118785e4a670bce4980e1044c0888a8b6e84af

- Release Artefact: bitbake-10118785e4a670bce4980e1044c0888a8b6e84af

- sha: 601a16210d7dc9b7a7306240d3e7013b3f950db8953fdd972151d715e050cc39

- Download Locations:

https://downloads.yoctoproject.org/releases/yocto/yocto-5.0.16/bitbake-10118785e4a670bce4980e1044c0888a8b6e84af.tar.bz2

https://mirrors.edge.kernel.org/yocto/yocto/yocto-5.0.16/bitbake-10118785e4a670bce4980e1044c0888a8b6e84af.tar.bz2
