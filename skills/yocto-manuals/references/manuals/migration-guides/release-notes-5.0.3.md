<!-- Source: https://docs.yoctoproject.org/scarthgap/migration-guides/release-notes-5.0.3.html (converted from singleindex.html). License: see LICENSE-docs.md in this folder. -->

##### Release notes for Yocto-5.0.3 (Scarthgap)

###### Security Fixes in Yocto-5.0.3

- bind: Fix CVE-2024-0760, CVE-2024-1737, CVE-2024-1975 and CVE-2024-4076

- busybox: Fix CVE-2023-42366, CVE-2023-42364, CVE-2023-42365, CVE-2021-42380 and CVE-2023-42363

- cpio: Ignore CVE-2023-7216

- curl: Fix CVE-2024-6197

- ffmpeg: Fix CVE-2023-49502, CVE-2024-31578 and CVE-2024-31582

- ghostscript: Fix CVE-2023-52722

- go: Fix CVE-2024-24790

- gstreamer1.0-plugins-base: Fix CVE-2024-4453

- less: Fix CVE-2024-32487

- libxml2: Fix CVE-2024-34459

- libyaml: Ignore CVE-2024-35328

- linux-yocto/6.6: Fix CVE-2024-23307, CVE-2024-24861, CVE-2024-26642, CVE-2024-26643, CVE-2024-26654, CVE-2024-26656 and CVE-2023-47233

- linux-yocto/6.6: Ignore CVE-2019-25160, CVE-2019-25162, CVE-2020-36775, CVE-2020-36776, CVE-2020-36777, CVE-2020-36778, CVE-2020-36779, CVE-2020-36780, CVE-2020-36781, CVE-2020-36782, CVE-2020-36783, CVE-2020-36784, CVE-2020-36785, CVE-2020-36786, CVE-2020-36787, CVE-2021-46904, CVE-2021-46905, CVE-2021-46906, CVE-2021-46908, CVE-2021-46909, CVE-2021-46910, CVE-2021-46911, CVE-2021-46912, CVE-2021-46913, CVE-2021-46914, CVE-2021-46915, CVE-2021-46916, CVE-2021-46917, CVE-2021-46918, CVE-2021-46919, CVE-2021-46920, CVE-2021-46921, CVE-2021-46922, CVE-2021-46923, CVE-2021-46924, CVE-2021-46925, CVE-2021-46926, CVE-2021-46927, CVE-2021-46928, CVE-2021-46929, CVE-2021-46930, CVE-2021-46931, CVE-2021-46932, CVE-2021-46933, CVE-2021-46934, CVE-2021-46935, CVE-2021-46936, CVE-2021-46937, CVE-2021-46938, CVE-2021-46939, CVE-2021-46940, CVE-2021-46941, CVE-2021-46942, CVE-2021-46943, CVE-2021-46944, CVE-2021-46945, CVE-2021-46947, CVE-2021-46948, CVE-2021-46949, CVE-2021-46950, CVE-2021-46951, CVE-2021-46952, CVE-2021-46953, CVE-2021-46954, CVE-2021-46955, CVE-2021-46956, CVE-2021-46957, CVE-2021-46958, CVE-2021-46959, CVE-2021-46960, CVE-2021-46961, CVE-2021-46962, CVE-2021-46963, CVE-2021-46964, CVE-2021-46965, CVE-2021-46966, CVE-2021-46967, CVE-2021-46968, CVE-2021-46969, CVE-2021-46970, CVE-2021-46971, CVE-2021-46972, CVE-2021-46973, CVE-2021-46974, CVE-2021-46976, CVE-2021-46977, CVE-2021-46978, CVE-2021-46979, CVE-2021-46980, CVE-2021-46981, CVE-2021-46982, CVE-2021-46983, CVE-2021-46984, CVE-2021-46985, CVE-2021-46986, CVE-2021-46987, CVE-2021-46988, CVE-2021-46989, CVE-2021-46990, CVE-2021-46991, CVE-2021-46992, CVE-2021-46993, CVE-2021-46994, CVE-2021-46995, CVE-2021-46996, CVE-2021-46997, CVE-2021-46998, CVE-2021-46999, CVE-2021-47000, CVE-2021-47001, CVE-2021-47002, CVE-2021-47003, CVE-2021-47004, CVE-2021-47005, CVE-2021-47006, CVE-2021-47007, CVE-2021-47008, CVE-2021-47009, CVE-2021-47010, CVE-2021-47011, CVE-2021-47012, CVE-2021-47013, CVE-2021-47014, CVE-2021-47015, CVE-2021-47016, CVE-2021-47017, CVE-2021-47018, CVE-2021-47019, CVE-2021-47020, CVE-2021-47021, CVE-2021-47022, CVE-2021-47023, CVE-2021-47024, CVE-2021-47025, CVE-2021-47026, CVE-2021-47027, CVE-2021-47028, CVE-2021-47029, CVE-2021-47030, CVE-2021-47031, CVE-2021-47032, CVE-2021-47033, CVE-2021-47034, CVE-2021-47035, CVE-2021-47036, CVE-2021-47037, CVE-2021-47038, CVE-2021-47039, CVE-2021-47040, CVE-2021-47041, CVE-2021-47042, CVE-2021-47043, CVE-2021-47044, CVE-2021-47045, CVE-2021-47046, CVE-2021-47047, CVE-2021-47048, CVE-2021-47049, CVE-2021-47050, CVE-2021-47051, CVE-2021-47052, CVE-2021-47053, CVE-2021-47054, CVE-2021-47055, CVE-2021-47056, CVE-2021-47057, CVE-2021-47058, CVE-2021-47059, CVE-2021-47060, CVE-2021-47061, CVE-2021-47062, CVE-2021-47063, CVE-2021-47064, CVE-2021-47065, CVE-2021-47066, CVE-2021-47067, CVE-2021-47068, CVE-2021-47069, CVE-2021-47070, CVE-2021-47071, CVE-2021-47072, CVE-2021-47073, CVE-2021-47074, CVE-2021-47075, CVE-2021-47076, CVE-2021-47077, CVE-2021-47078, CVE-2021-47079, CVE-2021-47080, CVE-2021-47081, CVE-2021-47082, CVE-2021-47083, CVE-2021-47086, CVE-2021-47087, CVE-2021-47088, CVE-2021-47089, CVE-2021-47090, CVE-2021-47091, CVE-2021-47092, CVE-2021-47093, CVE-2021-47094, CVE-2021-47095, CVE-2021-47096, CVE-2021-47097, CVE-2021-47098, CVE-2021-47099, CVE-2021-47100, CVE-2021-47101, CVE-2021-47102, CVE-2021-47103, CVE-2021-47104, CVE-2021-47105, CVE-2021-47106, CVE-2021-47107, CVE-2021-47108, CVE-2021-47109, CVE-2021-47110, CVE-2021-47111, CVE-2021-47112, CVE-2021-47113, CVE-2021-47114, CVE-2021-47116, CVE-2021-47117, CVE-2021-47118, CVE-2021-47119, CVE-2021-47120, CVE-2021-47121, CVE-2021-47122, CVE-2021-47123, CVE-2021-47124, CVE-2021-47125, CVE-2021-47126, CVE-2021-47127, CVE-2021-47128, CVE-2021-47129, CVE-2021-47130, CVE-2021-47131, CVE-2021-47132, CVE-2021-47133, CVE-2021-47134, CVE-2021-47135, CVE-2021-47136, CVE-2021-47137, CVE-2021-47138, CVE-2021-47139, CVE-2021-47140, CVE-2021-47141, CVE-2021-47142, CVE-2021-47143, CVE-2021-47144, CVE-2021-47145, CVE-2021-47146, CVE-2021-47147, CVE-2021-47148, CVE-2021-47149, CVE-2021-47150, CVE-2021-47151, CVE-2021-47152, CVE-2021-47153, CVE-2021-47158, CVE-2021-47159, CVE-2021-47160, CVE-2021-47161, CVE-2021-47162, CVE-2021-47163, CVE-2021-47164, CVE-2021-47165, CVE-2021-47166, CVE-2021-47167, CVE-2021-47168, CVE-2021-47169, CVE-2021-47170, CVE-2021-47171, CVE-2021-47172, CVE-2021-47173, CVE-2021-47174, CVE-2021-47175, CVE-2021-47176, CVE-2021-47177, CVE-2021-47178, CVE-2021-47179, CVE-2021-47180, CVE-2022-48626, CVE-2022-48627, CVE-2022-48628, CVE-2022-48629 and CVE-2022-48630

- linux-yocto/6.6 (cont.): Ignore CVE-2023-6270, CVE-2023-6356, CVE-2023-6536, CVE-2023-7042, CVE-2023-28746, CVE-2023-52465, CVE-2023-52467, CVE-2023-52468, CVE-2023-52469, CVE-2023-52470, CVE-2023-52471, CVE-2023-52472, CVE-2023-52473, CVE-2023-52474, CVE-2023-52475, CVE-2023-52476, CVE-2023-52477, CVE-2023-52478, CVE-2023-52479, CVE-2023-52480, CVE-2023-52481, CVE-2023-52482, CVE-2023-52483, CVE-2023-52484, CVE-2023-52486, CVE-2023-52487, CVE-2023-52488, CVE-2023-52489, CVE-2023-52490, CVE-2023-52491, CVE-2023-52492, CVE-2023-52493, CVE-2023-52494, CVE-2023-52495, CVE-2023-52497, CVE-2023-52498, CVE-2023-52499, CVE-2023-52500, CVE-2023-52501, CVE-2023-52502, CVE-2023-52503, CVE-2023-52504, CVE-2023-52505, CVE-2023-52506, CVE-2023-52507, CVE-2023-52508, CVE-2023-52509, CVE-2023-52510, CVE-2023-52511, CVE-2023-52512, CVE-2023-52513, CVE-2023-52515, CVE-2023-52516, CVE-2023-52517, CVE-2023-52518, CVE-2023-52519, CVE-2023-52520, CVE-2023-52522, CVE-2023-52523, CVE-2023-52524, CVE-2023-52525, CVE-2023-52526, CVE-2023-52527, CVE-2023-52528, CVE-2023-52529, CVE-2023-52530, CVE-2023-52531, CVE-2023-52532, CVE-2023-52559, CVE-2023-52560, CVE-2023-52561, CVE-2023-52562, CVE-2023-52563, CVE-2023-52564, CVE-2023-52565, CVE-2023-52566, CVE-2023-52567, CVE-2023-52568, CVE-2023-52569, CVE-2023-52570, CVE-2023-52571, CVE-2023-52572, CVE-2023-52573, CVE-2023-52574, CVE-2023-52575, CVE-2023-52576, CVE-2023-52577, CVE-2023-52578, CVE-2023-52580, CVE-2023-52581, CVE-2023-52582, CVE-2023-52583, CVE-2023-52584, CVE-2023-52587, CVE-2023-52588, CVE-2023-52589, CVE-2023-52591, CVE-2023-52593, CVE-2023-52594, CVE-2023-52595, CVE-2023-52596, CVE-2023-52597, CVE-2023-52598, CVE-2023-52599, CVE-2023-52600, CVE-2023-52601, CVE-2023-52602, CVE-2023-52603, CVE-2023-52604, CVE-2023-52606, CVE-2023-52607, CVE-2023-52608, CVE-2023-52609, CVE-2023-52610, CVE-2023-52611, CVE-2023-52612, CVE-2023-52613, CVE-2023-52614, CVE-2023-52615, CVE-2023-52616, CVE-2023-52617, CVE-2023-52618, CVE-2023-52619, CVE-2023-52620, CVE-2023-52621, CVE-2023-52622, CVE-2023-52623, CVE-2023-52626, CVE-2023-52627, CVE-2023-52628, CVE-2023-52629, CVE-2023-52630, CVE-2023-52631, CVE-2023-52632, CVE-2023-52633, CVE-2023-52635, CVE-2023-52636, CVE-2023-52637, CVE-2023-52638, CVE-2023-52639, CVE-2023-52640, CVE-2023-52641, CVE-2024-0841, CVE-2024-22099, CVE-2024-23196, CVE-2024-26600, CVE-2024-26601, CVE-2024-26602, CVE-2024-26603, CVE-2024-26604, CVE-2024-26605, CVE-2024-26606, CVE-2024-26607, CVE-2024-26608, CVE-2024-26610, CVE-2024-26611, CVE-2024-26612, CVE-2024-26614, CVE-2024-26615, CVE-2024-26616, CVE-2024-26617, CVE-2024-26618, CVE-2024-26619, CVE-2024-26620, CVE-2024-26621, CVE-2024-26622, CVE-2024-26623, CVE-2024-26625, CVE-2024-26626, CVE-2024-26627, CVE-2024-26629, CVE-2024-26630, CVE-2024-26631, CVE-2024-26632, CVE-2024-26633, CVE-2024-26634, CVE-2024-26635, CVE-2024-26636, CVE-2024-26637, CVE-2024-26638, CVE-2024-26639, CVE-2024-26640, CVE-2024-26641, CVE-2024-26644, CVE-2024-26645, CVE-2024-26646, CVE-2024-26647, CVE-2024-26648, CVE-2024-26649, CVE-2024-26650, CVE-2024-26651, CVE-2024-26652, CVE-2024-26653, CVE-2024-26657, CVE-2024-26659, CVE-2024-26660, CVE-2024-26661, CVE-2024-26662, CVE-2024-26663, CVE-2024-26664, CVE-2024-26665, CVE-2024-26666, CVE-2024-26667, CVE-2024-26668, CVE-2024-26669, CVE-2024-26670, CVE-2024-26671, CVE-2024-26673, CVE-2024-26674, CVE-2024-26675, CVE-2024-26676, CVE-2024-26677, CVE-2024-26678, CVE-2024-26679, CVE-2024-26680, CVE-2024-26681, CVE-2024-26682, CVE-2024-26683, CVE-2024-26684, CVE-2024-26685, CVE-2024-26687, CVE-2024-26688, CVE-2024-26689, CVE-2024-26690, CVE-2024-26691, CVE-2024-26692, CVE-2024-26693, CVE-2024-26694, CVE-2024-26695, CVE-2024-26696, CVE-2024-26697, CVE-2024-26698, CVE-2024-26700, CVE-2024-26702, CVE-2024-26703, CVE-2024-26704, CVE-2024-26705, CVE-2024-26706, CVE-2024-26707, CVE-2024-26708, CVE-2024-26709, CVE-2024-26710, CVE-2024-26711, CVE-2024-26712, CVE-2024-26713, CVE-2024-26714, CVE-2024-26715, CVE-2024-26716, CVE-2024-26717, CVE-2024-26718, CVE-2024-26719, CVE-2024-26720, CVE-2024-26721, CVE-2024-26722, CVE-2024-26723, CVE-2024-26724, CVE-2024-26725, CVE-2024-26726, CVE-2024-26727, CVE-2024-26728, CVE-2024-26729, CVE-2024-26730, CVE-2024-26731, CVE-2024-26732, CVE-2024-26733, CVE-2024-26734, CVE-2024-26735, CVE-2024-26736, CVE-2024-26737, CVE-2024-26738, CVE-2024-26739, CVE-2024-26740, CVE-2024-26741, CVE-2024-26742, CVE-2024-26743, CVE-2024-26744, CVE-2024-26745, CVE-2024-26746, CVE-2024-26747, CVE-2024-26748, CVE-2024-26749, CVE-2024-26750, CVE-2024-26751, CVE-2024-26752, CVE-2024-26753, CVE-2024-26754, CVE-2024-26755, CVE-2024-26759, CVE-2024-26760, CVE-2024-26761, CVE-2024-26762, CVE-2024-26763, CVE-2024-26764, CVE-2024-26765, CVE-2024-26766, CVE-2024-26767, CVE-2024-26768, CVE-2024-26769, CVE-2024-26770, CVE-2024-26771, CVE-2024-26772, CVE-2024-26773, CVE-2024-26774, CVE-2024-26775, CVE-2024-26776, CVE-2024-26777, CVE-2024-26778, CVE-2024-26779, CVE-2024-26780, CVE-2024-26781, CVE-2024-26782, CVE-2024-26783, CVE-2024-26786, CVE-2024-26787, CVE-2024-26788, CVE-2024-26789, CVE-2024-26790, CVE-2024-26791, CVE-2024-26792, CVE-2024-26793, CVE-2024-26794, CVE-2024-26795, CVE-2024-26796, CVE-2024-26798, CVE-2024-26799, CVE-2024-26800, CVE-2024-26801, CVE-2024-26802, CVE-2024-26803, CVE-2024-26804, CVE-2024-26805, CVE-2024-26807, CVE-2024-26808 and CVE-2024-26809

- llvm: Fix CVE-2024-0151

- ofono: Fix CVE-2023-2794

- openssh: Fix CVE-2024-6387 and CVE-2024-39894

- openssl: Fix CVE-2024-5535

- pam: Fix CVE-2024-22365

- python3-idna: Fix CVE-2024-3651

- qemu: Fix CVE-2023-6683, CVE-2024-3446, CVE-2024-3447, CVE-2024-3567, CVE-2024-26327 and CVE-2024-26328

- ruby: Fix CVE-2023-36617 and CVE-2024-27281

- vte: Fix CVE-2024-37535

- wget: Fix for CVE-2024-38428

###### Fixes in Yocto-5.0.3

- apt-native: don’t let dpkg overwrite files by default

- archiver.bbclass: Fix work-shared checking for kernel recipes

- automake: mark new_rt_path_for_test-driver.patch as Inappropriate

- bash: fix configure checks that fail with GCC 14.1

- bind: upgrade to 9.18.28

- binutils: stable 2.42 branch updates

- bitbake: codeparser/data: Ensure module function contents changing is accounted for

- bitbake: codeparser: Skip non-local functions for module dependencies

- build-appliance-image: Update to scarthgap head revision

- cargo: remove True option to getVar calls

- classes/create-spdx-2.2: Fix SPDX Namespace Prefix

- classes/kernel: No symlink in postinst without KERNEL_IMAGETYPE_SYMLINK

- cmake-qemu.bbclass: fix if criterion

- create-spdx-3.0/populate_sdk_base: Add SDK_CLASSES inherit mechanism to fix tarball SPDX manifests

- create-spdx-‘*’: Support multilibs via SPDX_MULTILIB_SSTATE_ARCHS

- curl: correct the PACKAGECONFIG for native/nativesdk

- curl: locale-base-en-us isn’t glibc-specific

- curl: skip FTP tests in run-ptest

- cve-check: Introduce CVE_CHECK_MANIFEST_JSON_SUFFIX

- cve-exclusion: Drop the version comparision/warning

- devtool: ide-sdk: correct help typo

- dnf: Fix missing leading whitespace with ‘:append’

- dpkg: mark patches adding custom non-debian architectures as inappropriate for upstream

- ed: upgrade to 1.20.2

- expect: fix configure with GCC 14

- ffmpeg: backport patch to fix errors with GCC 14

- ffmpeg: backport patches to use new Vulkan AV1 codec API

- flac: fix buildpaths warnings

- fribidi: upgrade to 1.0.14

- gawk: Remove References to /usr/local/bin/gawk

- gawk: update patch status

- gettext: fix a parallel build issue

- ghostscript: upgrade to 10.03.1

- glib-networking: submit eagain.patch upstream

- glibc: cleanup old cve status

- glibc: stable 2.39 branch updates

- glslang: mark 0001-generate-glslang-pkg-config.patch as Inappropriate

- go: drop the old 1.4 bootstrap C version

- go: upgrade to 1.22.5

- gpgme: move gpgme-tool to own sub-package

- grub,grub-efi: Remove -mfpmath=sse on x86

- grub: mark grub-module-explicitly-keeps-symbole-.module_license.patch as a workaround

- gstreamer1.0: skip another known flaky test

- gstreamer: upgrade to 1.22.12

- insane.bbclass: fix HOST_ variable names

- insane.bbclass: remove leftover variables and comment

- insane.bbclass: remove skipping of cross-compiled packages

- insane: handle dangling symlinks in the libdir QA check

- iptables: fix memory corruption when parsing nft rules

- iptables: fix save/restore symlinks with libnftnl PACKAGECONFIG enabled

- iptables: submit 0001-configure-Add-option-to-enable-disable-libnfnetlink.patch upstream

- kexec-tools: submit 0003-kexec-ARM-Fix-add_buffer_phys_virt-align-issue.patch upstream

- layer.conf: Add os-release to SIGGEN_EXCLUDERECIPES_ABISAFE

- libacpi: mark patches as inactive-upstream

- libadwaita: upgrade to 1.5.1

- libcap-ng-python: upgrade to 0.8.5

- libcap-ng: upgrade to 0.8.5

- libmnl: explicitly disable doxygen

- libnl: change HOMEPAGE

- libpam: fix runtime error in pam_pwhistory moudle

- libpng: update SRC_URI

- libportal: fix rare build race

- libstd-rs: set CVE_PRODUCT to rust

- libxcrypt: correct the check for a working libucontext.h

- libxml2: upgrade to 2.12.8

- linux-yocto-custom: Fix comment override syntax

- linux-yocto/6.6: cfg: drop obselete options

- linux-yocto/6.6: cfg: introduce Intel NPU fragment

- linux-yocto/6.6: fix AMD boot trace

- linux-yocto/6.6: fix kselftest failures

- linux-yocto/6.6: intel configuration changes

- linux-yocto/6.6: nft: enable veth

- linux-yocto/6.6: update to v6.6.35

- linux-yocto: Enable team net driver

- linuxloader: add -armhf on arm only for TARGET_FPU ‘hard’

- llvm: upgrade to 18.1.6

- maintainers.inc: update self e-mail address

- maintainers: Drop go-native as recipe removed

- mesa: Fix missing leading whitespace with ‘:append’

- mesa: remove obsolete 0001-meson.build-check-for-all-linux-host_os-combinations.patch

- mesa: upgrade to 24.0.7

- meson: don’t use deprecated pkgconfig variable

- migration-guides: add release notes for 4.0.19

- migration-guides: add release notes for 5.0.2

- migration-notes: add release notes for 5.0.1

- mmc-utils: fix URL

- mobile-broadband-provider-info: upgrade to 20240407

- multilib.bbclass: replace deprecated e.data with d

- multilib.conf: remove appending to PKG_CONFIG_PATH

- nasm: upgrade to 2.16.03

- ncurses: switch to new mirror

- oeqa/runtime/scp: requires openssh-sftp-server

- oeqa/runtime: fix race-condition in minidebuginfo test

- oeqa/runtime: fix regression in minidebuginfo test

- oeqa/runtime: make minidebuginfo test work with coreutils

- oeqa/sdk/case: Ensure DL_DIR is populated with artefacts if used

- oeqa/sdk/case: Skip SDK test cases when TCLIBC is newlib

- oeqa/selftest/devtool: Fix for usrmerge in DISTRO_FEATURES

- oeqa/selftest/recipetool: Fix for usrmerge in DISTRO_FEATURES

- openssh: drop rejected patch fixed in 8.6p1 release

- openssh: systemd notification was implemented upstream

- openssh: systemd sd-notify patch was rejected upstream

- orc: upgrade to 0.4.39

- package.py: Fix static debuginfo split

- package.py: Fix static library processing

- pcmanfm: Disable incompatible-pointer-types warning as error

- perl: submit the rest of determinism.patch upstream

- pixman: fixing inline failure with -Og

- poky.conf: bump version for 5.0.3

- populate_sdk_ext.bbclass: Fix undefined variable error

- pseudo: Fix to work with glibc 2.40

- pseudo: Update to include open symlink handling bugfix

- pseudo: Update to pull in python 3.12+ fix

- python3-attrs: drop python3-ctypes from RDEPENDS

- python3-bcrypt: drop python3-six from RDEPENDS

- python3-idna: upgrade to 3.7

- python3-jinja2: upgrade to 3.1.4

- python3-pyopenssl: drop python3-six from RDEPENDS

- python3-requests: cleanup RDEPENDS

- python3-setuptools: drop python3-2to3 from RDEPENDS

- python3: Treat UID/GID overflow as failure

- python3: skip test_concurrent_futures/test_deadlock

- python3: skip test_multiprocessing/test_active_children test

- python3: submit deterministic_imports.patch upstream as a ticket

- python3: upgrade to 3.12.4

- qemu: upgrade to 8.2.3

- rng-tools: ignore incompatible-pointer-types errors for now

- rt-tests: rt_bmark.py: fix TypeError

- rust-cross-canadian: set CVE_PRODUCT to rust

- rust: Add new varaible RUST_ENABLE_EXTRA_TOOLS

- sanity: Check if tar is gnutar

- sdk: Fix path length limit to match reserved size

- selftest-hardlink: Add additional test cases

- selftest/cases/runtime_test: Exclude centos-9 from virgl tests

- selftest: add Upstream-Status to .patch files

- settings-daemon: submit addsoundkeys.patch upstream and update to a revision that has it

- systemd.bbclass: Clarify error message

- tcp-wrappers: mark all patches as inactive-upstream

- tzdata: Add tzdata.zi to tzdata-core package

- vorbis: mark patch as Inactive-Upstream

- vulkan-samples: fix do_compile error when -Og enabled

- watchdog: Set watchdog_module in default config

- webkitgtk: fix do_compile errors on beaglebone-yocto

- webkitgtk: fix do_configure error on beaglebone-yocto

- weston: upgrade to 13.0.1

- wic/partition.py: Set hash_seed for empty ext partition

- wic: bootimg-efi: fix error handling

- wic: engine.py: use raw string for escape sequence

- wireless-regdb: upgrade to 2024.05.08

- xserver-xorg: upgrade to 21.1.13

- xz: Update LICENSE variable for xz packages

###### Known Issues in Yocto-5.0.3

- N/A

###### Contributors to Yocto-5.0.3

- Adithya Balakumar

- Aleksandar Nikolic

- Alexander Kanavin

- Antonin Godard

- Archana Polampalli

- Ashish Sharma

- Benjamin Szőke

- Bruce Ashfield

- Changqing Li

- Chen Qi

- Christian Taedcke

- Deepthi Hemraj

- Denys Dmytriyenko

- Dmitry Baryshkov

- Emil Kronborg

- Enrico Jörns

- Etienne Cordonnier

- Guðni Már Gilbert

- Hitendra Prajapati

- Jonas Gorski

- Jookia

- Jose Quaresma

- Joshua Watt

- Jörg Sommer

- Kai Kang

- Khem Raj

- Kirill Yatsenko

- Lee Chee Yang

- Mark Hatle

- Markus Volk

- Martin Jansa

- Michael Opdenacker

- Mingli Yu

- Niko Mauno

- Patrick Wicki

- Peter Marko

- Quentin Schulz

- Ranjitsinh Rathod

- Richard Purdie

- Robert Kovacsics

- Ross Burton

- Siddharth Doshi

- Simone Weiß

- Soumya Sambu

- Steve Sakoman

- Sundeep KOKKONDA

- Trevor Gamblin

- Vijay Anusuri

- Wadim Egorov

- Wang Mingyu

- Xiangyu Chen

- Yi Zhao

- Yogita Urade

- Zahir Hussain

###### Repositories / Downloads for Yocto-5.0.3

poky

- Repository Location: https://git.yoctoproject.org/poky

- Branch: scarthgap

- Tag: yocto-5.0.3

- Git Revision: 0b37512fb4b231cc106768e2a7328431009b3b70

- Release Artefact: poky-0b37512fb4b231cc106768e2a7328431009b3b70

- sha: b37fe0b2f6a685ee94b4af55f896cbf52ba69023e10eb21d3e54798ca21ace79

- Download Locations: http://downloads.yoctoproject.org/releases/yocto/yocto-5.0.3/poky-0b37512fb4b231cc106768e2a7328431009b3b70.tar.bz2 http://mirrors.kernel.org/yocto/yocto/yocto-5.0.3/poky-0b37512fb4b231cc106768e2a7328431009b3b70.tar.bz2

openembedded-core

- Repository Location: https://git.openembedded.org/openembedded-core

- Branch: scarthgap

- Tag: yocto-5.0.3

- Git Revision: 236ac1b43308df722a78d3aa20aef065dfae5b2b

- Release Artefact: oecore-236ac1b43308df722a78d3aa20aef065dfae5b2b

- sha: 44b89feba9563c2281c8c2f45037dd7c312fb20e8b7d9289b25f0ea0fe1fc2c4

- Download Locations: http://downloads.yoctoproject.org/releases/yocto/yocto-5.0.3/oecore-236ac1b43308df722a78d3aa20aef065dfae5b2b.tar.bz2 http://mirrors.kernel.org/yocto/yocto/yocto-5.0.3/oecore-236ac1b43308df722a78d3aa20aef065dfae5b2b.tar.bz2

meta-mingw

- Repository Location: https://git.yoctoproject.org/meta-mingw

- Branch: scarthgap

- Tag: yocto-5.0.3

- Git Revision: acbba477893ef87388effc4679b7f40ee49fc852

- Release Artefact: meta-mingw-acbba477893ef87388effc4679b7f40ee49fc852

- sha: 3b7c2f475dad5130bace652b150367f587d44b391218b1364a8bbc430b48c54c

- Download Locations: http://downloads.yoctoproject.org/releases/yocto/yocto-5.0.3/meta-mingw-acbba477893ef87388effc4679b7f40ee49fc852.tar.bz2 http://mirrors.kernel.org/yocto/yocto/yocto-5.0.3/meta-mingw-acbba477893ef87388effc4679b7f40ee49fc852.tar.bz2

bitbake

- Repository Location: https://git.openembedded.org/bitbake

- Branch: 2.8

- Tag: yocto-5.0.3

- Git Revision: 11d83170922a2c6b9db1f6e8c23e533526984b2c

- Release Artefact: bitbake-11d83170922a2c6b9db1f6e8c23e533526984b2c

- sha: 9643433748d7ed80d6334124390271929566b3bc076dad0f6e6be1ec6d753b8d

- Download Locations: http://downloads.yoctoproject.org/releases/yocto/yocto-5.0.3/bitbake-11d83170922a2c6b9db1f6e8c23e533526984b2c.tar.bz2 http://mirrors.kernel.org/yocto/yocto/yocto-5.0.3/bitbake-11d83170922a2c6b9db1f6e8c23e533526984b2c.tar.bz2

yocto-docs

- Repository Location: https://git.yoctoproject.org/yocto-docs

- Branch: scarthgap

- Tag: yocto-5.0.3

- Git Revision: TBD
