# BitBake and Yocto Tasks Reference

Release: Yocto Project 5.0 "scarthgap" / BitBake 2.8. Sources: ref-manual "Tasks" (chapter 6), BitBake manual "Tasks" (3.6) and "Dependencies" (3.10), dev-manual "Running Specific Tasks" (32.9). The `yocto-manuals` skill has every task entry verbatim under `references/tasks/`.

## 1. The Normal Task Chain

`bitbake <recipe>` runs `do_build`, the default task, which depends on every normal task the recipe needs (6.1.1). For a typical target recipe the order is:

```text
do_fetch -> do_unpack -> do_patch -> do_prepare_recipe_sysroot -> do_configure -> do_compile -> do_install
do_install -> do_populate_sysroot                (staged for other recipes' DEPENDS)
do_install -> do_package -> do_packagedata       (pkgdata for oe-pkgdata-util and other recipes)
do_package -> do_package_qa                      (insane class QA)
do_package -> do_package_write_{ipk,rpm,deb}     (feeds in DEPLOY_DIR_*)
do_populate_lic                                  (license text collected for manifests)
do_deploy (only if the recipe inherits deploy and calls addtask)
do_build
```

Cross-recipe edges come from flags, not the order above (BitBake manual 3.10):

- `do_configure[deptask] = "do_populate_sysroot"` (via `DEPENDS`): every `DEPENDS` item must be staged before configure. This is why a missing `DEPENDS` shows up as a configure or compile failure, not a fetch failure.
- `do_package_qa[rdeptask] = "do_packagedata"`: runtime dependencies must have pkgdata before QA.
- `do_rootfs[recrdeptask] += "do_packagedata"` in `image.bbclass`: the image waits for pkgdata of everything reachable.
- `do_build[recrdeptask] += "do_deploy"` in `base.bbclass`: so `addtask deploy after do_compile` is enough.

Shared state (sstate) tasks such as `do_populate_sysroot`, `do_packagedata`, `do_package_write_*`, `do_deploy` and `do_populate_lic` can be restored from `SSTATE_DIR` or `SSTATE_MIRRORS` instead of run; when that happens the earlier tasks are skipped entirely. A recipe you never built locally can therefore have no `tmp/work/.../temp/log.do_compile`. If you need logs, force the task (`bitbake -f -c compile <recipe>`).

## 2. Normal Recipe Build Tasks (6.1)

| Task | What it does | Notes for debugging |
| --- | --- | --- |
| `do_fetch` | Downloads `SRC_URI` into `DL_DIR` using the fetcher chosen by the URI scheme. | Only task with network access by default (`[network]` flag). |
| `do_unpack` | Unpacks into `WORKDIR`; source must end up at `S`. | Git: `${WORKDIR}/git` on scarthgap. |
| `do_patch` | Applies `*.patch`/`*.diff` from `SRC_URI` (`apply=yes/no` overrides); searches `FILESPATH`. | `patch-fuzz`, `patch-status` QA run here. |
| `do_prepare_recipe_sysroot` | Builds `recipe-sysroot` and `recipe-sysroot-native` from `DEPENDS`. | Inspect these dirs for a missing header or tool. |
| `do_configure` | Runs in `${B}`; class-defined (autotools runs `autoreconf` + configure, cmake, meson). Default: `oe_runmake clean` if a Makefile exists. | `LIC_FILES_CHKSUM` is verified at the end of configure. |
| `do_compile` | Runs in `${B}`; default `oe_runmake`. | `compile-host-path` QA reads its log. |
| `do_install` | Copies files to `${D}`, in `${B}`, under fakeroot. Use `install`, `cp --no-preserve=ownership`, or `tar --no-same-owner`. | `host-user-contaminated`, `install-host-path` QA. |
| `do_populate_sysroot` | Stages a subset of `${D}` (`SYSROOT_DIRS`) for other recipes. `/etc` etc. not staged by default. | sstate task. |
| `do_package` | Splits `${D}` into `PACKAGES` using `FILES`; writes `packages-split/`. | Leftmost package wins. |
| `do_packagedata` | Saves package metadata to `PKGDATA_DIR`. | What `oe-pkgdata-util` reads. |
| `do_package_qa` | Runs insane-class QA on the packages. | See `qa-errors.md`. |
| `do_package_write_ipk/rpm/deb` | Writes packages to `DEPLOY_DIR_IPK/RPM/DEB`. | Backends from `PACKAGE_CLASSES`. |
| `do_populate_lic` | Writes license info used for image manifests. | |
| `do_deploy` | Writes to `${DEPLOYDIR}`; the deploy class copies it to `DEPLOY_DIR_IMAGE` through sstate. Not added by default: `inherit deploy` + `addtask deploy after do_compile`. Never write to `DEPLOY_DIR_IMAGE` directly. Previous output is cleaned on rerun. | Kernel, U-Boot, firmware recipes. |
| `do_populate_sdk` / `do_populate_sdk_ext` | Build an installable SDK / eSDK for an image (`bitbake -c populate_sdk <image>`). | |
| `do_rm_work` | Deletes the work dir after use when `rm_work` is inherited. | Disable it (or `RM_WORK_EXCLUDE`) while debugging. |
| `do_compile_ptest_base`, `do_configure_ptest_base`, `do_install_ptest_base` | Build and install the upstream test suite into `${PN}-ptest` (ptest class, active only with `ptest` in `DISTRO_FEATURES`). | |
| `do_build` | Default aggregate task. | |

## 3. Manually Called Tasks (6.2)

| Task | Use | Safety |
| --- | --- | --- |
| `do_listtasks` | `bitbake -c listtasks <recipe>`: every task the recipe defines (proves whether, e.g., `kernel_configme` exists). | read-only |
| `do_checkuri` | Validates `SRC_URI` reachability. | read-only, needs network |
| `do_clean` | Removes work output from `do_unpack` on; sstate is kept, so a rebuild may just restore from sstate. | destructive to `WORKDIR` only |
| `do_cleansstate` | `do_clean` plus the recipe's sstate objects. Not recommended with a shared `SSTATE_DIR`; cannot clean remote mirrors. The manual prefers `bitbake -f` to force a rebuild. | destructive, ask first |
| `do_cleanall` | `do_cleansstate` plus the downloads in `DL_DIR`. "You should never use the do_cleanall task in a normal scenario"; use `bitbake -f -c fetch <recipe>` to refetch. | destructive, ask first |
| `do_devshell` | Opens an interactive shell with the task environment. | interactive: for a human only |
| `do_pydevshell` | Interactive Python shell on the datastore. | interactive: for a human only |
| `do_package_index` | Regenerates feed indexes. Not run with `-c`: run `bitbake package-index`. | |

## 4. Image Tasks (6.3, 6.1.8-6.1.9)

- `do_rootfs`: installs the image's packages with the package manager from the first `PACKAGE_CLASSES` entry and runs `pkg_postinst` scriptlets offline; then `ROOTFS_POSTPROCESS_COMMAND`.
- `do_image`: pre-processing (`IMAGE_PREPROCESS_COMMAND`) and creation of one dynamic `do_image_<type>` task per `IMAGE_FSTYPES` entry (for example `do_image_ext4`, `do_image_wic`, `do_image_tar`).
- `do_image_complete`: post-processing (`IMAGE_POSTPROCESS_COMMAND`) and deploy to `DEPLOY_DIR_IMAGE`.
- `do_bootimg`: creates a bootable live image (`live`, `iso`, `hddimg` in `IMAGE_FSTYPES`, image-live class).
- `do_bundle_initramfs`: combines an initramfs image and the kernel into one image (`INITRAMFS_IMAGE_BUNDLE = "1"`).
- `do_testimage`: boots the image and runs runtime tests (`bitbake -c testimage <image>`). `do_testimage_auto`: same, right after build, when `TESTIMAGE_AUTO = "1"`.
- `do_populate_sdk`, `do_populate_sdk_ext`: SDK outputs for the image.

## 5. Kernel Tasks (6.4)

Present in recipes that inherit `kernel`; the `kernel_*` configuration tasks come from `kernel-yocto` (linux-yocto style recipes). A vendor kernel recipe that only inherits `kernel` may not have `kernel_configme`/`kernel_configcheck`/`kernel_metadata`; check with `bitbake -c listtasks virtual/kernel`.

| Task | What it does |
| --- | --- |
| `do_kernel_checkout` | Turns the unpacked tree into a clean git working copy with the right branches (kernel-yocto). |
| `do_validate_branches` | Checks that `SRCREV_machine`/`SRCREV_meta` exist on the configured branches (unless `AUTOREV`). |
| `do_kernel_metadata` | Collects features (`KERNEL_FEATURES`, `.scc`, `.cfg` in `SRC_URI`) into fragments and patches. |
| `do_kernel_configme` | Merges defconfig + fragments into the configuration (applies `KCONFIG_MODE`). |
| `do_kernel_configcheck` | Warns when a requested option is missing from the final `.config` (`bitbake -f -c kernel_configcheck virtual/kernel`). |
| `do_menuconfig` | Interactive `menuconfig` (human only). Changes live in the work dir and are lost on clean. |
| `do_diffconfig` | Writes `fragment.cfg` in `${WORKDIR}` with the difference from the `kernel_configme` result: turn it into a `.cfg` in your layer. |
| `do_savedefconfig` | Writes a minimal `defconfig` in `${B}`. |
| `do_compile_kernelmodules` | Builds modules after the image. |
| `do_shared_workdir` | Copies build outputs needed for out-of-tree modules. |
| `do_sizecheck` | Fails if no image in `KERNEL_IMAGETYPES` fits `KERNEL_IMAGE_MAXSIZE`. |
| `do_strip` | Strips `KERNEL_IMAGE_STRIP_EXTRA_SECTIONS` from `vmlinux`. |
| `do_deploy` | Kernel images, DTBs, modules tarball to `DEPLOY_DIR_IMAGE`. |

## 6. Running and Forcing Tasks (dev-manual 32.9)

```bash
bitbake -c listtasks <recipe>       # what exists
bitbake -c compile <recipe>         # runs compile and its dependencies, only if out of date
bitbake -f -c compile <recipe>      # force; marks the task "tainted" (warning until a clean rebuild)
bitbake -C compile <recipe>         # invalidate compile, then run do_build (rest of the chain)
bitbake -b path/to/recipe.bb        # no dependency handling; only when deps are already built
bitbake -k <target>                 # continue after errors to see every failure
bitbake -g <target>                 # pn-buildlist and task-depends.dot in the current directory
```

`-c` omits the `do_` prefix. `-f`/`-C` taint the input checksum; the "is tainted from a forced run" warning is expected afterwards.

## 7. Where Task Output Lives

```text
${WORKDIR}/temp/log.do_<task>      # symlink to the latest log.do_<task>.<pid>
${WORKDIR}/temp/run.do_<task>      # the exact script BitBake ran
${WORKDIR}/image/                  # ${D}, after do_install
${WORKDIR}/packages-split/<pkg>/   # after do_package (needs rm_work disabled)
${WORKDIR}/recipe-sysroot*/        # after do_prepare_recipe_sysroot
tmp/stamps/.../<task>.sigdata.*    # signature data for bitbake-dumpsig
tmp/deploy/images/${MACHINE}/      # do_deploy and image outputs
```

## 8. Which Skill Owns Which Failure

- fetch, unpack, patch, configure, compile, install, package, package_qa, sstate/rebuild questions: `bitbake-debug` (recipe fixes then go through `yocto-recipe-review`).
- rootfs, image, package selection, postinst: `yocto-image-rootfs`.
- kernel_*, deploy of kernel/U-Boot/DTB: `yocto-bsp-kernel`.
- populate_lic, license and CVE tasks: `yocto-security-sbom`.

Derived from the Yocto Project scarthgap (5.0) documentation, CC BY-SA 2.0 UK.
