<!-- Source: https://docs.yoctoproject.org/scarthgap/dev-manual/temporary-source-code.html (converted from singleindex.html). License: see LICENSE-docs.md in this folder. -->

#### 8 Finding Temporary Source Code

You might find it helpful during development to modify the temporary source code used by recipes to build packages. For example, suppose you are developing a patch and you need to experiment a bit to figure out your solution. After you have initially built the package, you can iteratively tweak the source code, which is located in the Build Directory, and then you can force a re-compile and quickly test your altered code. Once you settle on a solution, you can then preserve your changes in the form of patches.

During a build, the unpacked temporary source code used by recipes to build packages is available in the Build Directory as defined by the S variable. Below is the default value for the S variable as defined in the `meta/conf/bitbake.conf` configuration file in the Source Directory:

```
S = "${WORKDIR}/${BP}"

```

You should be aware that many recipes override the S variable. For example, recipes that fetch their source from Git usually set S to `${WORKDIR}/git`.

Note

The BP represents the base recipe name, which consists of the name and version:

```
BP = "${BPN}-${PV}"

```

The path to the work directory for the recipe (WORKDIR) is defined as follows:

```
${BASE_WORKDIR}/${MULTIMACH_TARGET_SYS}/${PN}/${PV}

```

The actual directory depends on several things:

- BASE_WORKDIR: The top-level build output directory.

- MULTIMACH_TARGET_SYS: The target system identifier.

- PN: The recipe name.

- PV: The recipe version.

As an example, assume a Source Directory top-level folder named `project`, a default Build Directory at `project/build`, and a `qemux86-poky-linux` machine target system. Furthermore, suppose your recipe is named `foo_1.3.0.bb`. In this case, the work directory the build system uses to build the package would be as follows:

```
project/build/tmp/work/qemux86-poky-linux/foo/1.3.0

```
