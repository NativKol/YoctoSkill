<!-- Source: https://docs.yoctoproject.org/scarthgap/ref-manual/tasks.html (converted from singleindex.html). License: see LICENSE-docs.md in this folder. -->

#### 6 Tasks

Tasks are units of execution for BitBake. Recipes (`.bb` files) use tasks to complete configuring, compiling, and packaging software. This chapter provides a reference of the tasks defined in the OpenEmbedded build system.

##### 6.1 Normal Recipe Build Tasks

The following sections describe normal tasks associated with building a recipe. For more information on tasks and dependencies, see the “Tasks” and “Dependencies” sections in the BitBake User Manual.

###### 6.1.1 `do_build`

The default task for all recipes. This task depends on all other normal tasks required to build a recipe.

###### 6.1.2 `do_compile`

Compiles the source code. This task runs with the current working directory set to `${`B`}`.

The default behavior of this task is to run the `oe_runmake` function if a makefile (`Makefile`, `makefile`, or `GNUmakefile`) is found. If no such file is found, the do_compile task does nothing.

###### 6.1.3 `do_compile_ptest_base`

Compiles the runtime test suite included in the software being built.

###### 6.1.4 `do_configure`

Configures the source by enabling and disabling any build-time and configuration options for the software being built. The task runs with the current working directory set to `${`B`}`.

The default behavior of this task is to run `oe_runmake clean` if a makefile (`Makefile`, `makefile`, or `GNUmakefile`) is found and CLEANBROKEN is not set to “1”. If no such file is found or the CLEANBROKEN variable is set to “1”, the do_configure task does nothing.

###### 6.1.5 `do_configure_ptest_base`

Configures the runtime test suite included in the software being built.

###### 6.1.6 `do_deploy`

Writes output files that are to be deployed to `${`DEPLOY_DIR_IMAGE`}`. The task runs with the current working directory set to `${`B`}`.

Recipes implementing this task should inherit the deploy class and should write the output to `${`DEPLOYDIR`}`, which is not to be confused with `${DEPLOY_DIR}`. The deploy class sets up do_deploy as a shared state (sstate) task that can be accelerated through sstate use. The sstate mechanism takes care of copying the output from `${DEPLOYDIR}` to `${DEPLOY_DIR_IMAGE}`.

Note

Do not write the output directly to `${DEPLOY_DIR_IMAGE}`, as this causes the sstate mechanism to malfunction.

The do_deploy task is not added as a task by default and consequently needs to be added manually. If you want the task to run after do_compile, you can add it by doing the following:

```
addtask deploy after do_compile

```

Adding do_deploy after other tasks works the same way.

Note

You do not need to add `before do_build` to the `addtask` command (though it is harmless), because the base class contains the following:

```
do_build[recrdeptask] += "do_deploy"

```

See the “Dependencies” section in the BitBake User Manual for more information.

If the do_deploy task re-executes, any previous output is removed (i.e. “cleaned”).

###### 6.1.7 `do_fetch`

Fetches the source code. This task uses the SRC_URI variable and the argument’s prefix to determine the correct fetcher module.

###### 6.1.8 `do_image`

Starts the image generation process. The do_image task runs after the OpenEmbedded build system has run the do_rootfs task during which packages are identified for installation into the image and the root filesystem is created, complete with post-processing.

The do_image task performs pre-processing on the image through the IMAGE_PREPROCESS_COMMAND and dynamically generates supporting do_image_* tasks as needed.

For more information on image creation, see the “Image Generation” section in the Yocto Project Overview and Concepts Manual.

###### 6.1.9 `do_image_complete`

Completes the image generation process. The do_image_complete task runs after the OpenEmbedded build system has run the do_image task during which image pre-processing occurs and through dynamically generated do_image_* tasks the image is constructed.

The do_image_complete task performs post-processing on the image through the IMAGE_POSTPROCESS_COMMAND.

For more information on image creation, see the “Image Generation” section in the Yocto Project Overview and Concepts Manual.

###### 6.1.10 `do_install`

Copies files that are to be packaged into the holding area `${`D`}`. This task runs with the current working directory set to `${`B`}`, which is the compilation directory. The do_install task, as well as other tasks that either directly or indirectly depend on the installed files (e.g. do_package, do_package_write_*, and do_rootfs), run under fakeroot.

Note

When installing files, be careful not to set the owner and group IDs of the installed files to unintended values. Some methods of copying files, notably when using the recursive `cp` command, can preserve the UID and/or GID of the original file, which is usually not what you want. The `host-user-contaminated` QA check checks for files that probably have the wrong ownership.

Safe methods for installing files include the following:

- The `install` utility. This utility is the preferred method.

- The `cp` command with the `--no-preserve=ownership` option.

- The `tar` command with the `--no-same-owner` option. See the `bin_package.bbclass` file in the `meta/classes-recipe` subdirectory of the Source Directory for an example.

###### 6.1.11 `do_install_ptest_base`

Copies the runtime test suite files from the compilation directory to a holding area.

###### 6.1.12 `do_package`

Analyzes the content of the holding area `${`D`}` and splits the content into subsets based on available packages and files. This task makes use of the PACKAGES and FILES variables.

The do_package task, in conjunction with the do_packagedata task, also saves some important package metadata. For additional information, see the PKGDESTWORK variable and the “Automatically Added Runtime Dependencies” section in the Yocto Project Overview and Concepts Manual.

###### 6.1.13 `do_package_qa`

Runs QA checks on packaged files. For more information on these checks, see the insane class.

###### 6.1.14 `do_package_write_deb`

Creates Debian packages (i.e. `*.deb` files) and places them in the `${`DEPLOY_DIR_DEB`}` directory in the package feeds area. For more information, see the “Package Feeds” section in the Yocto Project Overview and Concepts Manual.

###### 6.1.15 `do_package_write_ipk`

Creates IPK packages (i.e. `*.ipk` files) and places them in the `${`DEPLOY_DIR_IPK`}` directory in the package feeds area. For more information, see the “Package Feeds” section in the Yocto Project Overview and Concepts Manual.

###### 6.1.16 `do_package_write_rpm`

Creates RPM packages (i.e. `*.rpm` files) and places them in the `${`DEPLOY_DIR_RPM`}` directory in the package feeds area. For more information, see the “Package Feeds” section in the Yocto Project Overview and Concepts Manual.

###### 6.1.17 `do_packagedata`

Saves package metadata generated by the do_package task in PKGDATA_DIR to make it available globally.

###### 6.1.18 `do_patch`

Locates patch files and applies them to the source code.

After fetching and unpacking source files, the build system uses the recipe’s SRC_URI statements to locate and apply patch files to the source code.

Note

The build system uses the FILESPATH variable to determine the default set of directories when searching for patches.

Patch files, by default, are `*.patch` and `*.diff` files created and kept in a subdirectory of the directory holding the recipe file. For example, consider the bluez5 recipe from the OE-Core layer (i.e. `poky/meta`):

```
poky/meta/recipes-connectivity/bluez5

```

This recipe has two patch files located here:

```
poky/meta/recipes-connectivity/bluez5/bluez5

```

In the `bluez5` recipe, the SRC_URI statements point to the source and patch files needed to build the package.

Note

In the case for the `bluez5_5.48.bb` recipe, the SRC_URI statements are from an include file `bluez5.inc`.

As mentioned earlier, the build system treats files whose file types are `.patch` and `.diff` as patch files. However, you can use the “apply=yes” parameter with the SRC_URI statement to indicate any file as a patch file:

```
SRC_URI = " \
    git://path_to_repo/some_package \
    file://file;apply=yes \
    "

```

Conversely, if you have a file whose file type is `.patch` or `.diff` and you want to exclude it so that the do_patch task does not apply it during the patch phase, you can use the “apply=no” parameter with the SRC_URI statement:

```
SRC_URI = " \
    git://path_to_repo/some_package \
    file://file1.patch \
    file://file2.patch;apply=no \
    "

```

In the previous example `file1.patch` would be applied as a patch by default while `file2.patch` would not be applied.

You can find out more about the patching process in the “Patching” section in the Yocto Project Overview and Concepts Manual and the “Patching Code” section in the Yocto Project Development Tasks Manual.

###### 6.1.19 `do_populate_lic`

Writes license information for the recipe that is collected later when the image is constructed.

###### 6.1.20 `do_populate_sdk`

Creates the file and directory structure for an installable SDK. See the “SDK Generation” section in the Yocto Project Overview and Concepts Manual for more information.

###### 6.1.21 `do_populate_sdk_ext`

Creates the file and directory structure for an installable extensible SDK (eSDK). See the “SDK Generation” section in the Yocto Project Overview and Concepts Manual for more information.

###### 6.1.22 `do_populate_sysroot`

Stages (copies) a subset of the files installed by the do_install task into the appropriate sysroot. For information on how to access these files from other recipes, see the STAGING_DIR* variables. Directories that would typically not be needed by other recipes at build time (e.g. `/etc`) are not copied by default.

For information on what directories are copied by default, see the SYSROOT_DIRS* variables. You can change these variables inside your recipe if you need to make additional (or fewer) directories available to other recipes at build time.

The do_populate_sysroot task is a shared state (sstate) task, which means that the task can be accelerated through sstate use. Realize also that if the task is re-executed, any previous output is removed (i.e. “cleaned”).

###### 6.1.23 `do_prepare_recipe_sysroot`

Installs the files into the individual recipe specific sysroots (i.e. `recipe-sysroot` and `recipe-sysroot-native` under `${`WORKDIR`}` based upon the dependencies specified by DEPENDS). See the “staging” class for more information.

###### 6.1.24 `do_rm_work`

Removes work files after the OpenEmbedded build system has finished with them. You can learn more by looking at the “rm_work” section.

###### 6.1.25 `do_unpack`

Unpacks the source code into a working directory pointed to by `${`WORKDIR`}`. The S variable also plays a role in where unpacked source files ultimately reside. For more information on how source files are unpacked, see the “Source Fetching” section in the Yocto Project Overview and Concepts Manual and also see the WORKDIR and S variable descriptions.

##### 6.2 Manually Called Tasks

These tasks are typically manually triggered (e.g. by using the `bitbake -c` command-line option):

###### 6.2.1 `do_checkuri`

Validates the SRC_URI value.

###### 6.2.2 `do_clean`

Removes all output files for a target from the do_unpack task forward (i.e. do_unpack, do_configure, do_compile, do_install, and do_package).

You can run this task using BitBake as follows:

```
$ bitbake -c clean recipe

```

Running this task does not remove the sstate cache files. Consequently, if no changes have been made and the recipe is rebuilt after cleaning, output files are simply restored from the sstate cache. If you want to remove the sstate cache files for the recipe, you need to use the do_cleansstate task instead (i.e. `bitbake -c cleansstate` recipe).

###### 6.2.3 `do_cleanall`

Removes all output files, shared state (sstate) cache, and downloaded source files for a target (i.e. the contents of DL_DIR). Essentially, the do_cleanall task is identical to the do_cleansstate task with the added removal of downloaded source files.

You can run this task using BitBake as follows:

```
$ bitbake -c cleanall recipe

```

You should never use the do_cleanall task in a normal scenario. If you want to start fresh with the do_fetch task, use instead:

```
$ bitbake -f -c fetch recipe

```

Note

The reason to prefer `bitbake -f -c fetch` is that the do_cleanall task would break in some cases, such as:

```
$ bitbake -c fetch    recipe
$ bitbake -c cleanall recipe-native
$ bitbake -c unpack   recipe

```

because after step 1 there is a stamp file for the do_fetch task of `recipe`, and it won’t be removed at step 2 because step 2 uses a different work directory. So the unpack task at step 3 will try to extract the downloaded archive and fail as it has been deleted in step 2.

Note that this also applies to BitBake from concurrent processes when a shared download directory (DL_DIR) is setup.

###### 6.2.4 `do_cleansstate`

Removes all output files and shared state (sstate) cache for a target. Essentially, the do_cleansstate task is identical to the do_clean task with the added removal of shared state (sstate) cache.

You can run this task using BitBake as follows:

```
$ bitbake -c cleansstate recipe

```

When you run the do_cleansstate task, the OpenEmbedded build system no longer uses any sstate. Consequently, building the recipe from scratch is guaranteed.

Note

Using do_cleansstate with a shared SSTATE_DIR is not recommended because it could trigger an error during the build of a separate BitBake instance. This is because the builds check sstate “up front” but download the files later, so it if is deleted in the meantime, it will cause an error but not a total failure as it will rebuild it.

The reliable and preferred way to force a new build is to use `bitbake -f` instead.

Note

The do_cleansstate task cannot remove sstate from a remote sstate mirror. If you need to build a target from scratch using remote mirrors, use the “-f” option as follows:

```
$ bitbake -f -c do_cleansstate target

```

###### 6.2.5 `do_pydevshell`

Starts a shell in which an interactive Python interpreter allows you to interact with the BitBake build environment. From within this shell, you can directly examine and set bits from the data store and execute functions as if within the BitBake environment. See the “Using a Python Development Shell” section in the Yocto Project Development Tasks Manual for more information about using `pydevshell`.

###### 6.2.6 `do_devshell`

Starts a shell whose environment is set up for development, debugging, or both. See the “Using a Development Shell” section in the Yocto Project Development Tasks Manual for more information about using `devshell`.

###### 6.2.7 `do_listtasks`

Lists all defined tasks for a target.

###### 6.2.8 `do_package_index`

Creates or updates the index in the Package Feeds area.

Note

This task is not triggered with the `bitbake -c` command-line option as are the other tasks in this section. Because this task is specifically for the `package-index` recipe, you run it using `bitbake package-index`.

##### 6.3 Image-Related Tasks

The following tasks are applicable to image recipes.

###### 6.3.1 `do_bootimg`

Creates a bootable live image. See the IMAGE_FSTYPES variable for additional information on live image types.

###### 6.3.2 `do_bundle_initramfs`

Combines an Initramfs image and kernel together to form a single image.

###### 6.3.3 `do_rootfs`

Creates the root filesystem (file and directory structure) for an image. See the “Image Generation” section in the Yocto Project Overview and Concepts Manual for more information on how the root filesystem is created.

###### 6.3.4 `do_testimage`

Boots an image and performs runtime tests within the image. For information on automatically testing images, see the “Performing Automated Runtime Testing” section in the Yocto Project Test Environment Manual.

###### 6.3.5 `do_testimage_auto`

Boots an image and performs runtime tests within the image immediately after it has been built. This task is enabled when you set TESTIMAGE_AUTO equal to “1”.

For information on automatically testing images, see the “Performing Automated Runtime Testing” section in the Yocto Project Test Environment Manual.

##### 6.4 Kernel-Related Tasks

The following tasks are applicable to kernel recipes. Some of these tasks (e.g. the do_menuconfig task) are also applicable to recipes that use Linux kernel style configuration such as the BusyBox recipe.

###### 6.4.1 `do_compile_kernelmodules`

Runs the step that builds the kernel modules (if needed). Building a kernel consists of two steps: 1) the kernel (`vmlinux`) is built, and 2) the modules are built (i.e. `make modules`).

###### 6.4.2 `do_diffconfig`

When invoked by the user, this task creates a file containing the differences between the original config as produced by do_kernel_configme task and the changes made by the user with other methods (i.e. using (do_menuconfig). Once the file of differences is created, it can be used to create a config fragment that only contains the differences. You can invoke this task from the command line as follows:

```
$ bitbake linux-yocto -c diffconfig

```

For more information, see the “Creating Configuration Fragments” section in the Yocto Project Linux Kernel Development Manual.

###### 6.4.3 `do_kernel_checkout`

Converts the newly unpacked kernel source into a form with which the OpenEmbedded build system can work. Because the kernel source can be fetched in several different ways, the do_kernel_checkout task makes sure that subsequent tasks are given a clean working tree copy of the kernel with the correct branches checked out.

###### 6.4.4 `do_kernel_configcheck`

Validates the configuration produced by the do_menuconfig task. The do_kernel_configcheck task produces warnings when a requested configuration does not appear in the final `.config` file or when you override a policy configuration in a hardware configuration fragment. You can run this task explicitly and view the output by using the following command:

```
$ bitbake linux-yocto -c kernel_configcheck -f

```

For more information, see the “Validating Configuration” section in the Yocto Project Linux Kernel Development Manual.

###### 6.4.5 `do_kernel_configme`

After the kernel is patched by the do_patch task, the do_kernel_configme task assembles and merges all the kernel config fragments into a merged configuration that can then be passed to the kernel configuration phase proper. This is also the time during which user-specified defconfigs are applied if present, and where configuration modes such as `--allnoconfig` are applied.

###### 6.4.6 `do_kernel_metadata`

Collects all the features required for a given kernel build, whether the features come from SRC_URI or from Git repositories. After collection, the do_kernel_metadata task processes the features into a series of config fragments and patches, which can then be applied by subsequent tasks such as do_patch and do_kernel_configme.

###### 6.4.7 `do_menuconfig`

Invoked by the user to manipulate the `.config` file used to build a linux-yocto recipe. This task starts the Linux kernel configuration tool, which you then use to modify the kernel configuration.

You can invoke this tool from the command line as follows:

```
$ bitbake linux-yocto -c menuconfig

```

See the “Using menuconfig” section in the Yocto Project Linux Kernel Development Manual for more information on this configuration tool.

###### 6.4.8 `do_savedefconfig`

When invoked by the user, creates a defconfig file that can be used instead of the default defconfig. The saved defconfig contains the differences between the default defconfig and the changes made by the user using other methods (i.e. the do_menuconfig task. You can invoke the task using the following command:

```
$ bitbake linux-yocto -c savedefconfig

```

###### 6.4.9 `do_shared_workdir`

After the kernel has been compiled but before the kernel modules have been compiled, this task copies files required for module builds and which are generated from the kernel build into the shared work directory. With these copies successfully copied, the do_compile_kernelmodules task can successfully build the kernel modules in the next step of the build.

###### 6.4.10 `do_sizecheck`

If the variable KERNEL_IMAGE_MAXSIZE is set, this task compares the size of all stripped kernel images listed in KERNEL_IMAGETYPES against that value. If more than one image type is listed there, warn on any that exceed that value, but fail only if none of them fit.

###### 6.4.11 `do_strip`

If KERNEL_IMAGE_STRIP_EXTRA_SECTIONS is defined, this task strips the sections named in that variable from `vmlinux`. This stripping is typically used to remove nonessential sections such as `.comment` sections from a size-sensitive configuration.

Common sections to strip:

- `.comment`: Holds compiler version strings and information

- `.note.*`: Extra notes often left by the compiler

- `.debug`: Debugging information

###### 6.4.12 `do_validate_branches`

After the kernel is unpacked but before it is patched, this task makes sure that the machine and metadata branches as specified by the SRCREV variables actually exist on the specified branches. Otherwise, if AUTOREV is not being used, the do_validate_branches task fails during the build.
