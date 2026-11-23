# Example: Missing Kernel Devicetree Artifact

Skill: `yocto-bsp-kernel`.

## User Prompt

```text
My custom board's DTB never shows up in tmp/deploy/images.
```

## Evidence to Request

- `MACHINE`, the machine `.conf`, and `KERNEL_DEVICETREE` with its assignment history
- the selected kernel provider and its bbappends
- the deploy directory listing and `log.do_compile` / `log.do_deploy` of the kernel

## Bad Answer Pattern

- Editing the image recipe before proving the kernel built the DTB.
- Guessing the DTB path without checking the kernel source tree and `KERNEL_DTBVENDORED`.
- Grepping `bitbake -e` with a pattern that cannot match full variable names (for example `^(KERNEL|UBOOT)=`).

## Expected Answer Pattern

- Confirm machine and provider: `bitbake-getvar --value MACHINE`, `bitbake-getvar --value PREFERRED_PROVIDER_virtual/kernel`.
- Check `KERNEL_DEVICETREE` (plain `.dtb` names preferred; the vendor subdirectory is dropped on install unless `KERNEL_DTBVENDORED = "true"`), and that the selected kernel's Makefiles know the DTB.
- Check that the append that sets it targets the selected kernel recipe.
- Build and inspect deploy output.

## Validation

```bash
bitbake-getvar -r virtual/kernel KERNEL_DEVICETREE
bitbake virtual/kernel
ls -l tmp/deploy/images/<machine>/ | grep -i dtb
```
