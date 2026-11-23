<!-- Source: https://docs.yoctoproject.org/bitbake/2.8/bitbake-user-manual/bitbake-user-manual-ref-variables-context.html (converted from singleindex.html). License: see LICENSE-docs.md in this folder. -->

## 4 Variable Context

Variables might only have an impact or can be used in certain contexts. Some should only be used in global files like `.conf`, while others are intended only for local files like `.bb`. This chapter aims to describe some important variable contexts.

### 4.1 BitBake’s own configuration

Variables starting with `BB_` usually configure the behaviour of BitBake itself. For example, one could configure:

- System resources, like disk space to be used (BB_DISKMON_DIRS), or the number of tasks to be run in parallel by BitBake (BB_NUMBER_THREADS).

- How the fetchers shall behave, e.g., BB_FETCH_PREMIRRORONLY is used by BitBake to determine if BitBake’s fetcher shall search only PREMIRRORS for files.

Those variables are usually configured globally.

### 4.2 BitBake configuration

There are variables:

- Like B or T, that are used to specify directories used by BitBake during the build of a particular recipe. Those variables are specified in `bitbake.conf`. Some, like B, are quite often overwritten in recipes.

- Starting with `FAKEROOT`, to configure how the `fakeroot` command is handled. Those are usually set by `bitbake.conf` and might get adapted in a `bbclass`.

- Detailing where BitBake will store and fetch information from, for data reuse between build runs like CACHE, DL_DIR or PERSISTENT_DIR. Those are usually global.

### 4.3 Layers and files

Variables starting with `LAYER` configure how BitBake handles layers. Additionally, variables starting with `BB` configure how layers and files are handled. For example:

- LAYERDEPENDS is used to configure on which layers a given layer depends.

- The configured layers are contained in BBLAYERS and files in BBFILES.

Those variables are often used in the files `layer.conf` and `bblayers.conf`.

### 4.4 Recipes and packages

Variables handling recipes and packages can be split into:

- PN, PV or PF for example, contain information about the name or revision of a recipe or package. Usually, the default set in `bitbake.conf` is used, but those are from time to time overwritten in recipes.

- SUMMARY, DESCRIPTION, LICENSE or HOMEPAGE contain the expected information and should be set specifically for every recipe.

- In recipes, variables are also used to control build and runtime dependencies between recipes/packages with other recipes/packages. The most common should be: PROVIDES, RPROVIDES, DEPENDS, and RDEPENDS.

- There are further variables starting with `SRC` that specify the sources in a recipe like SRC_URI or SRCDATE. Those are also usually set in recipes.

- Which version or provider of a recipe should be given preference when multiple recipes would provide the same item, is controlled by variables starting with `PREFERRED_`. Those are normally set in the configuration files of a `MACHINE` or `DISTRO`.
