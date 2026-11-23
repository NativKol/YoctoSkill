<!-- Generated from references/yocto/bsp-kernel.md by tools/sync_references.py. Edit the source file, not this copy. -->

# Yocto BSP, Kernel, Devicetree, and Bootloader Reference

Release: Yocto Project 5.0 "scarthgap". Sources: BSP Developer's Guide; kernel-dev "Common Tasks" (2.3 modifying a recipe, 2.6 configuring, 2.10 out-of-tree modules); ref-manual classes `kernel`, `kernel-yocto`, `kernel-devicetree`, `kernel-fitimage`, `devicetree`, `uboot-config`, `uboot-sign`, `deploy`; ref-manual tasks 6.1.6 (`do_deploy`) and 6.4 (kernel tasks); variables listed below.

## 1. Mental Model

- `MACHINE` selects `conf/machine/<machine>.conf` from some layer's `BBPATH`. It sets tune (`DEFAULTTUNE`, `require conf/machine/include/...`), `MACHINE_FEATURES`, `MACHINEOVERRIDES` (often SoC family names), kernel and bootloader providers, `KERNEL_IMAGETYPE`, `KERNEL_DEVICETREE`, `SERIAL_CONSOLES`, `IMAGE_FSTYPES`, `WKS_FILE`, `IMAGE_BOOT_FILES`, `MACHINE_ESSENTIAL_EXTRA_RDEPENDS`/`RRECOMMENDS`.
- Machine config expresses hardware; distro config expresses product policy. Do not set `DISTRO_FEATURES` in a machine file.
- `PREFERRED_PROVIDER_virtual/kernel` (and `virtual/bootloader`) picks the recipe; other `virtual/kernel` providers are then prevented from building. `PREFERRED_VERSION_<pn>` picks a version (`%` wildcard at the end).
- The kernel source for `kernel`-class recipes lives in the shared work dir (`STAGING_KERNEL_DIR`, `tmp/work-shared/<machine>/kernel-source`) and is regenerated from `SRC_URI` on rebuild. Edits made there, or with `menuconfig`, are lost after a clean; only metadata in your layer (patches, `.cfg` fragments, `defconfig`) persists.
- Proof of what was built is in `tmp/deploy/images/${MACHINE}/` (kernel image, DTBs, modules tarball, bootloader, images).

## 2. Kernel Configuration: defconfig vs Fragments vs In-Tree

| Mechanism | How | Applies |
| --- | --- | --- |
| Out-of-tree `defconfig` | `SRC_URI += "file://defconfig"` with `FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"` in a bbappend | Full `.config`, or a minimal `savedefconfig` file with `KCONFIG_MODE = "alldefconfig"` (or `allnoconfig`) (kernel-dev 2.3.3). For plain `kernel`-class recipes, `do_configure` copies a `defconfig` from `SRC_URI` to `.config` unless one exists (ref-manual `kernel`). |
| Config fragment | `file://my.cfg` in `SRC_URI` (must end in `.cfg`); content uses `.config` syntax (`CONFIG_FOO=y`, `# CONFIG_BAR is not set`) | Merged after the defconfig by `do_kernel_configme`: kernel-yocto (linux-yocto style) recipes only (kernel-dev 2.6.3). |
| In-tree defconfig | `KBUILD_DEFCONFIG:<machine> ?= "bcm2709_defconfig"` | kernel-yocto; takes precedence over an out-of-tree `defconfig` (kernel-dev 2.3.4). |
| Kernel metadata features | `KERNEL_FEATURES:append = " features/netfilter/netfilter.scc"`; `.scc` files group patches and fragments; `KMACHINE`, `KBRANCH`, `LINUX_KERNEL_TYPE` (`standard`, `tiny`, `preempt-rt`) select the BSP description | kernel-yocto only. |

Workflow to create a fragment (kernel-dev 2.6.3), human-interactive step marked:

```bash
bitbake -f -c kernel_configme virtual/kernel   # known starting .config
bitbake -c menuconfig virtual/kernel           # interactive: human only
bitbake -c diffconfig virtual/kernel           # writes fragment.cfg in ${WORKDIR}
# copy fragment.cfg into the layer as files/my.cfg and add file://my.cfg to SRC_URI
bitbake -f -c kernel_configcheck virtual/kernel   # warns about requested options missing from the final .config
```

`kernel_configcheck` warnings ("specified values did not make it into the kernel's final configuration") usually mean a dependency of the option is off or the option name changed in this kernel version. Before suggesting `kernel_*` tasks for a vendor kernel, run `bitbake -c listtasks virtual/kernel`: recipes that only inherit `kernel` (not `kernel-yocto`) do not have them and do not merge `.cfg` fragments unless the vendor added that support.

## 3. Devicetree

- `KERNEL_DEVICETREE` lists DTB names to build and deploy (kernel-devicetree class). Plain names (`imx8mm-evk.dtb`) are preferred; full paths with the vendor directory (`freescale/imx8mm-evk.dtb`) are legacy but still accepted.
- `KERNEL_DTBVENDORED` (default `false`): whether installed/deployed DTBs keep the vendor subdirectory; boot scripts and `IMAGE_BOOT_FILES` must use the matching path.
- `KERNEL_DTBDEST`, `KERNEL_DTC_FLAGS` (e.g. `-@` for overlays), `KERNEL_DEVICETREE_BUNDLE` (32-bit arm only).
- A DTB name that the kernel's Makefiles do not know fails in `do_compile` of the kernel; a DTB that builds but does not appear in deploy usually means a different kernel provider or machine is active, or the name/path differs from what the boot files expect.
- Out-of-tree device trees and overlays: `inherit devicetree` recipe with `COMPATIBLE_MACHINE`, `DT_FILES_PATH`, `DT_FILES`; output in `${DEPLOY_DIR_IMAGE}/devicetree/`.

## 4. Deploy, FIT, U-Boot, Boot Files

- `do_deploy` (ref-manual 6.1.6): recipes `inherit deploy`, write to `${DEPLOYDIR}` and `addtask deploy after do_compile` (or `do_install`). The class copies to `DEPLOY_DIR_IMAGE` via sstate. Writing directly into `DEPLOY_DIR_IMAGE` breaks sstate; rerunning `do_deploy` cleans its previous output.
- Kernel image type: `KERNEL_IMAGETYPE` (+ `KERNEL_IMAGETYPES`). FIT: `KERNEL_CLASSES += "kernel-fitimage"` and `KERNEL_IMAGETYPE = "fitImage"`; addresses `UBOOT_LOADADDRESS`, `UBOOT_ENTRYPOINT`, `UBOOT_DTB_LOADADDRESS`; initramfs via `INITRAMFS_IMAGE` (+ `INITRAMFS_IMAGE_BUNDLE = "1"` for a bundle); signing via `UBOOT_SIGN_ENABLE`, `UBOOT_SIGN_KEYDIR`, `UBOOT_SIGN_KEYNAME`. The scarthgap class is `kernel-fitimage`.
- U-Boot: `UBOOT_MACHINE` (one config) or `UBOOT_CONFIG` with flags `UBOOT_CONFIG[name] = "config,images,binary"` (uboot-config class); `UBOOT_BINARY`, `UBOOT_SUFFIX`; verified boot with `uboot-sign` (`UBOOT_FITIMAGE_ENABLE`, `SPL_SIGN_ENABLE`).
- Boot partition contents for wic images: `IMAGE_BOOT_FILES` (files from `DEPLOY_DIR_IMAGE`, `src;dest` renames, globs), with `WKS_FILE` choosing the kickstart.
- Modules: `KERNEL_MODULE_AUTOLOAD += "foo"` loads at boot; `KERNEL_MODULE_PROBECONF`/`module_conf_<name>` for options; each module is packaged as `kernel-module-<name>`; `MACHINE_EXTRA_RRECOMMENDS += "kernel-module-foo"` or `IMAGE_INSTALL` to install. Out-of-tree modules: `inherit module` recipe (kernel-dev 2.10.2).

## 5. Debug Flow

1. Confirm the machine and providers:
   ```bash
   bitbake-getvar --value MACHINE
   bitbake-getvar --value PREFERRED_PROVIDER_virtual/kernel
   bitbake-getvar --value PREFERRED_PROVIDER_virtual/bootloader
   bitbake-getvar -r virtual/kernel KERNEL_DEVICETREE    # with history: who set it, where
   bitbake-getvar -r virtual/kernel KERNEL_IMAGETYPE
   bitbake-getvar -r virtual/kernel SRC_URI
   ```
2. Confirm the BSP layer is enabled and compatible: `bitbake-layers show-layers`; `LAYERSERIES_COMPAT_<bsp>` must include `scarthgap`.
3. Confirm the recipe and its appends: `bitbake-layers show-recipes 'linux-*'`, `bitbake-layers show-appends | grep -E 'linux|u-boot'`. A version-specific `linux-foo_6.1.bbappend` against a 6.6 recipe is a fatal "No recipes available for" parse error (unless `BB_DANGLINGAPPENDS_WARNONLY`).
4. Check the available tasks: `bitbake -c listtasks virtual/kernel`.
5. Validate config: `bitbake -f -c kernel_configcheck virtual/kernel` (kernel-yocto), or inspect `${B}/.config`: `grep CONFIG_FOO tmp/work/*/linux-*/*/build/.config` (path varies per recipe; find it with `bitbake-getvar -r virtual/kernel --value B`).
6. Build and inspect deploy: `bitbake virtual/kernel`, then `ls -l tmp/deploy/images/<machine>/`.

When `bitbake -e` output is needed, filter by full variable names; for example `bitbake -e virtual/kernel | grep -E '^(MACHINE|PREFERRED_PROVIDER_virtual/kernel|KERNEL_[A-Z_]+|UBOOT_[A-Z_]+|SRC_URI|S)='`. `bitbake-getvar` is simpler and shows history.

## 6. Common Problems

- Wrong `MACHINE` (typo, or set in `local.conf` and also in a multiconfig).
- BSP layer missing from `bblayers.conf` or not compatible with scarthgap.
- Kernel bbappend version mismatch (fatal parse error) or append aimed at a recipe that is not the selected provider (silently unused).
- `.cfg` fragment ignored because the kernel recipe is not kernel-yocto based.
- Config option requested but its dependencies are off (`kernel_configcheck` warning).
- `menuconfig`/in-tree edits lost after rebuild (section 1).
- DTB path mismatch between `KERNEL_DEVICETREE`, `KERNEL_DTBVENDORED` and `IMAGE_BOOT_FILES`/boot script.
- U-Boot `UBOOT_CONFIG` variant produces a binary name other than the one the wic file expects.
- Recipe writes into `DEPLOY_DIR_IMAGE` directly instead of `${DEPLOYDIR}`.
- `kernel-fit-image` (wrong name for scarthgap) used instead of `kernel-fitimage`.

Derived from the Yocto Project scarthgap (5.0) documentation, CC BY-SA 2.0 UK.
