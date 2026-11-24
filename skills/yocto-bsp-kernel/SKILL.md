---
name: yocto-bsp-kernel
description: Create, review and debug Yocto BSP and boot metadata - MACHINE configuration files, machine features and tunes, PREFERRED_PROVIDER_virtual/kernel and virtual/bootloader, linux-yocto and vendor kernel recipes and bbappends, kernel config (defconfig, .cfg fragments, KBUILD_DEFCONFIG, KERNEL_FEATURES/.scc, menuconfig/diffconfig changes that vanish), KERNEL_DEVICETREE and missing DTBs, out-of-tree devicetree and kernel modules, U-Boot (UBOOT_MACHINE, UBOOT_CONFIG, uboot-sign), FIT images (kernel-fitimage), do_deploy and DEPLOYDIR, IMAGE_BOOT_FILES and files missing from tmp/deploy/images/<machine>. Use it whenever the question is about a board, a kernel option, a devicetree, a bootloader or boot artifacts in Yocto, even if the user only says "my DTB is not there" or "my kernel change disappeared". Targets Yocto 5.0 scarthgap. Generic compile failures of other recipes go to bitbake-debug; image package content to yocto-image-rootfs.
---

# Yocto BSP Kernel

Prove which machine, kernel recipe and bootloader recipe are selected before editing anything; most BSP bugs are "the change went into a recipe that is not being built".

## Workflow

1. **Selection:**
   ```bash
   bitbake-getvar --value MACHINE
   bitbake-getvar --value PREFERRED_PROVIDER_virtual/kernel
   bitbake-getvar --value PREFERRED_PROVIDER_virtual/bootloader
   bitbake-getvar -r virtual/kernel KERNEL_DEVICETREE    # history: which file set it
   bitbake-layers show-recipes 'linux-*'
   bitbake-layers show-appends | grep -E 'linux|u-boot'
   ```
   The BSP layer must be in `bblayers.conf` and list `scarthgap` in `LAYERSERIES_COMPAT`.
2. **Capabilities of this kernel recipe:** `bitbake -c listtasks virtual/kernel`. `kernel_configme`, `kernel_configcheck`, `.cfg` fragment merging and `KERNEL_FEATURES` come from `kernel-yocto`; a vendor recipe that only inherits `kernel` uses a `defconfig` and may not have them.
3. **Config changes:** persist them as layer metadata (fragment `.cfg` or `defconfig` in `SRC_URI`, or `KBUILD_DEFCONFIG` for an in-tree defconfig). Edits in `tmp/work-shared/<machine>/kernel-source` or via `menuconfig` are regenerated away. Fragment workflow: `kernel_configme -f` -> `menuconfig` (human) -> `diffconfig` -> copy `fragment.cfg` to the layer -> `kernel_configcheck -f`.
4. **Devicetree:** plain `.dtb` names in `KERNEL_DEVICETREE` are preferred; `KERNEL_DTBVENDORED` decides whether the vendor subdirectory is kept, which must match `IMAGE_BOOT_FILES` and boot scripts. Out-of-tree DTs use the `devicetree` class.
5. **Deploy:** recipes `inherit deploy`, write to `${DEPLOYDIR}` in `do_deploy` and `addtask deploy after do_compile`; never write into `DEPLOY_DIR_IMAGE` directly. FIT images: `KERNEL_CLASSES += "kernel-fitimage"`, `KERNEL_IMAGETYPE = "fitImage"` (the scarthgap class is `kernel-fitimage`).
6. **Validate:** `bitbake virtual/kernel`, `ls -l tmp/deploy/images/<machine>/`, `grep CONFIG_<X> <B>/.config` (find `B` with `bitbake-getvar -r virtual/kernel --value B`).

Interactive tasks (`menuconfig`, `devshell`) are for the human; tell them to run it and continue from `diffconfig`.

## Review Rules

- Machine config describes hardware; product policy (`DISTRO_FEATURES`, init system) stays in the distro.
- Select kernels and bootloaders with `PREFERRED_PROVIDER_virtual/*` (underscore form), versions with `PREFERRED_VERSION_<pn>`.
- Kernel bbappends should be `linux-foo_%.bbappend` unless pinning is intended; a mismatched version is a fatal parse error.
- Use `FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"` with `:=`.
- Check vendor BSP branch compatibility before modernizing its syntax.

## Offline lookup

Everything this skill needs is in the repository; it works without internet. Pull only the text you need instead of reading whole files (pages run to thousands of lines). From this skill's folder:

- `python3 scripts/ylookup.py <NAME>...` prints the scarthgap manual entry for any variable, class, task, feature or QA check (`--kind var|class|task|feature|qa` to disambiguate, `--find TEXT` when unsure of the name).
- `--topic TEXT` lists manual sections, `--section <manual/page.md> "<heading>"` prints one, `--grep REGEX [--in ref-manual]` finds anything else.
- URLs in these files are citations for the user, not lookups. The manuals are scarthgap 5.0: if the project is on another release, tell the user rather than going online. Without Python: `` grep -n -A30 '^## Variable `NAME`' references/keywords.md ``.

## References

- [references/bsp-kernel.md](references/bsp-kernel.md): machine model, config mechanisms table, devicetree, deploy/FIT/U-Boot/boot files, debug flow, common problems.
- [references/tasks-reference.md](references/tasks-reference.md): kernel tasks and `do_deploy`.
- [references/classes-core.md](references/classes-core.md): `kernel`, `kernel-yocto`, `kernel-devicetree`, `kernel-fitimage`, `devicetree`, `uboot-config`, `uboot-sign`, `deploy`, `module`.
- [references/migration.md](references/migration.md): release detection and scarthgap changes (linux-yocto 6.6).

## Output

1. selected machine, kernel provider and bootloader (with the command output)
2. BSP layer compatibility
3. the kernel/devicetree/bootloader metadata issue
4. minimal metadata change in the right layer
5. validation command and the deploy artifact to expect
