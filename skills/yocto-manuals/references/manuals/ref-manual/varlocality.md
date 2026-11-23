<!-- Source: https://docs.yoctoproject.org/scarthgap/ref-manual/varlocality.html (converted from singleindex.html). License: see LICENSE-docs.md in this folder. -->

#### 13 Variable Context

While you can use most variables in almost any context such as `.conf`, `.bbclass`, `.inc`, and `.bb` files, some variables are often associated with a particular locality or context. This chapter describes some common associations.

##### 13.1 Configuration

The following subsections provide lists of variables whose context is configuration: distribution, machine, and local.

###### 13.1.1 Distribution (Distro)

This section lists variables whose configuration context is the distribution, or distro.

- DISTRO

- DISTRO_NAME

- DISTRO_VERSION

- MAINTAINER

- PACKAGE_CLASSES

- TARGET_OS

- TARGET_FPU

- TCMODE

- TCLIBC

###### 13.1.2 Machine

This section lists variables whose configuration context is the machine.

- TARGET_ARCH

- SERIAL_CONSOLES

- PACKAGE_EXTRA_ARCHS

- IMAGE_FSTYPES

- MACHINE_FEATURES

- MACHINE_EXTRA_RDEPENDS

- MACHINE_EXTRA_RRECOMMENDS

- MACHINE_ESSENTIAL_EXTRA_RDEPENDS

- MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS

###### 13.1.3 Local

This section lists variables whose configuration context is the local configuration through the `local.conf` file.

- DISTRO

- MACHINE

- DL_DIR

- EXTRA_IMAGE_FEATURES

- PACKAGE_CLASSES

- BB_NUMBER_THREADS

- BBINCLUDELOGS

- ENABLE_BINARY_LOCALE_GENERATION

##### 13.2 Recipes

The following subsections provide lists of variables whose context is recipes: required, dependencies, path, and extra build information.

###### 13.2.1 Required

This section lists variables that are required for recipes.

- LICENSE

- LIC_FILES_CHKSUM

- SRC_URI — used in recipes that fetch local or remote files.

###### 13.2.2 Dependencies

This section lists variables that define recipe dependencies.

- DEPENDS

- RDEPENDS

- RRECOMMENDS

- RCONFLICTS

- RREPLACES

###### 13.2.3 Paths

This section lists variables that define recipe paths.

- WORKDIR

- S

- FILES

###### 13.2.4 Extra Build Information

This section lists variables that define extra build information for recipes.

- DEFAULT_PREFERENCE

- EXTRA_OECMAKE

- EXTRA_OECONF

- EXTRA_OEMAKE

- PACKAGECONFIG_CONFARGS

- PACKAGES
