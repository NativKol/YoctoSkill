<!-- Source: https://docs.yoctoproject.org/scarthgap/ref-manual/system-requirements.html (converted from singleindex.html). License: see LICENSE-docs.md in this folder. -->

#### 1 System Requirements

Welcome to the Yocto Project Reference Manual. This manual provides reference information for the current release of the Yocto Project, and is most effectively used after you have an understanding of the basics of the Yocto Project. The manual is neither meant to be read as a starting point to the Yocto Project, nor read from start to finish. Rather, use this manual to find variable definitions, class descriptions, and so forth as needed during the course of using the Yocto Project.

For introductory information on the Yocto Project, see the Yocto Project Website and the “The Yocto Project Development Environment” chapter in the Yocto Project Overview and Concepts Manual.

If you want to use the Yocto Project to quickly build an image without having to understand concepts, work through the Yocto Project Quick Build document. You can find “how-to” information in the Yocto Project Development Tasks Manual. You can find Yocto Project overview and conceptual information in the Yocto Project Overview and Concepts Manual.

Note

For more information about the Yocto Project Documentation set, see the Links and Related Documentation section.

##### 1.1 Minimum Free Disk Space

To build an image such as `core-image-sato` for the `qemux86-64` machine, you need a system with at least 90 Gbytes of free disk space. However, much more disk space will be necessary to build more complex images, to run multiple builds and to cache build artifacts, improving build efficiency.

If you have a shortage of disk space, see the “Conserving Disk Space” section of the Development Tasks Manual.

##### 1.2 Minimum System RAM

You will manage to build an image such as `core-image-sato` for the `qemux86-64` machine with as little as 8 Gbytes of RAM on an old system with 4 CPU cores, but your builds will be much faster on a system with as much RAM and as many CPU cores as possible.

##### 1.3 Supported Linux Distributions

Currently, the 5.0.21 release (“Scarthgap”) of the Yocto Project is supported on the following distributions:

- AlmaLinux 8

- AlmaLinux 9

- CentOS Stream 9

- Debian 11

- Debian 12

- Fedora 39

- Fedora 40

- Fedora 41

- Rocky Linux 8

- Rocky Linux 9

- Ubuntu 22.04 (LTS)

- Ubuntu 24.04 (LTS)

The following distribution versions are still tested, even though the organizations publishing them no longer make updates publicly available:

- Fedora 39

- Fedora 40

- Fedora 41

Note that the Yocto Project doesn’t have access to private updates that some of these versions may have. Therefore, our testing has limited value if you have access to such updates.

Finally, here are the distribution versions which were previously tested on former revisions of “Scarthgap”, but no longer are:

- CentOS Stream 8

- Fedora 38

- OpenSUSE Leap 15.4

- Ubuntu 18.04

- Ubuntu 20.04

- Ubuntu 23.04

- Ubuntu 24.10

Note

- While the Yocto Project Team attempts to ensure all Yocto Project releases are one hundred percent compatible with each officially supported Linux distribution, you may still encounter problems that happen only with a specific distribution.

- Yocto Project releases are tested against the stable Linux distributions in the above list. The Yocto Project should work on other distributions but validation is not performed against them.

- In particular, the Yocto Project does not support and currently has no plans to support rolling-releases or development distributions due to their constantly changing nature. We welcome patches and bug reports, but keep in mind that our priority is on the supported platforms listed above.

- If your Linux distribution is not in the above list, we recommend to get the buildtools or buildtools-extended tarballs containing the host tools required by your Yocto Project release, typically by running `scripts/install-buildtools` as explained in the “Required Git, tar, Python, make and gcc Versions” section.

- You may use Windows Subsystem For Linux v2 to set up a build host using Windows 10 or later, or Windows Server 2019 or later, but validation is not performed against build hosts using WSL 2.

See the Setting Up to Use Windows Subsystem For Linux (WSL 2) section in the Yocto Project Development Tasks Manual for more information.

- If you encounter problems, please go to Yocto Project Bugzilla and submit a bug. We are interested in hearing about your experience. For information on how to submit a bug, see the Yocto Project Bugzilla wiki page and the “Reporting a Defect Against the Yocto Project and OpenEmbedded” section in the Yocto Project and OpenEmbedded Contributor Guide.

##### 1.4 Required Packages for the Build Host

The list of packages you need on the host development system can be large when covering all build scenarios using the Yocto Project. This section describes required packages according to Linux distribution and function.

###### 1.4.1 Ubuntu and Debian

Here are the packages needed to build an image on a headless system with a supported Ubuntu or Debian Linux distribution:

```
$ sudo apt install build-essential chrpath cpio debianutils diffstat file gawk gcc git iputils-ping libacl1 liblz4-tool locales python3 python3-git python3-jinja2 python3-pexpect python3-pip python3-subunit socat texinfo unzip wget xz-utils zstd

```

You also need to ensure you have the `en_US.UTF-8` locale enabled:

```
$ locale --all-locales | grep en_US.utf8

```

If this is not the case, you can reconfigure the `locales` package to add it (requires an interactive shell):

```
$ sudo dpkg-reconfigure locales

```

Note

- If you are not in an interactive shell, `dpkg-reconfigure` will not work as expected. To add the locale you will need to edit `/etc/locale.gen` file to add/uncomment the `en_US.UTF-8` locale. A naive way to do this as root is:

```
$ echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
$ locale-gen

```

- If your build system has the `oss4-dev` package installed, you might experience QEMU build failures due to the package installing its own custom `/usr/include/linux/soundcard.h` on the Debian system. If you run into this situation, try either of these solutions:

```
$ sudo apt build-dep qemu
$ sudo apt remove oss4-dev

```

Here are the packages needed to build Project documentation manuals:

```
$ sudo apt install git librsvg2-bin locales make python3-saneyaml python3-sphinx-rtd-theme sphinx

```

In addition to the previous packages, here are the packages needed to build the documentation in PDF format:

```
$ sudo apt install fonts-freefont-otf latexmk tex-gyre texlive-fonts-extra texlive-fonts-recommended texlive-lang-all texlive-latex-extra texlive-latex-recommended texlive-xetex

```

###### 1.4.2 Fedora Packages

Here are the packages needed to build an image on a headless system with a supported Fedora Linux distribution:

```
$ sudo dnf install bzip2 ccache chrpath cpio cpp diffstat diffutils file findutils gawk gcc gcc-c++ git glibc-devel glibc-langpack-en gzip hostname libacl lz4 make patch perl perl-Data-Dumper perl-File-Compare perl-File-Copy perl-FindBin perl-Text-ParseWords perl-Thread-Queue perl-bignum perl-locale python python3 python3-GitPython python3-jinja2 python3-pexpect python3-pip rpcgen socat tar texinfo unzip wget which xz zstd

```

Here are the packages needed to build Project documentation manuals:

```
$ sudo dnf install git glibc-locale-source librsvg2-tools make python3-pip which
$ sudo pip3 install sphinx sphinx_rtd_theme pyyaml

```

In addition to the previous packages, here are the packages needed to build the documentation in PDF format:

```
$ sudo dnf install 'texlive-collection-lang*' latexmk texlive-collection-fontsextra texlive-collection-fontsrecommended texlive-collection-latex texlive-collection-latexextra texlive-collection-latexrecommended texlive-collection-xetex texlive-fncychap texlive-gnu-freefont texlive-tex-gyre texlive-xetex

```

###### 1.4.3 openSUSE Packages

Here are the packages needed to build an image on a headless system with a supported openSUSE distribution:

```
$ sudo zypper install bzip2 chrpath diffstat gcc gcc-c++ git gzip hostname libacl1 lz4 make makeinfo patch python python-curses python-xml python3 python3-Jinja2 python3-curses python3-pexpect python3-pip rpcgen socat tar wget which xz zstd
$ sudo pip3 install GitPython

```

Here are the packages needed to build Project documentation manuals:

```
$ sudo zypper install git glibc-i18ndata make python3-pip rsvg-convert which
$ sudo pip3 install sphinx sphinx_rtd_theme pyyaml

```

In addition to the previous packages, here are the packages needed to build the documentation in PDF format:

```
$ sudo zypper install 'texlive-collection-lang*' texlive-collection-fontsextra texlive-collection-fontsrecommended texlive-collection-latex texlive-collection-latexextra texlive-collection-latexrecommended texlive-collection-xetex texlive-fncychap texlive-gnu-freefont texlive-latexmk texlive-tex-gyre texlive-xetex

```

###### 1.4.4 AlmaLinux Packages

Here are the packages needed to build an image on a headless system with a supported AlmaLinux distribution:

```
$ sudo dnf install -y epel-release
$ sudo yum install dnf-plugins-core
$ sudo dnf config-manager --set-enabled crb
$ sudo dnf makecache
$ sudo dnf install bzip2 ccache chrpath cpio cpp diffstat diffutils gawk gcc gcc-c++ git glibc-devel glibc-langpack-en gzip libacl lz4 make patch perl perl-Data-Dumper perl-Text-ParseWords perl-Thread-Queue python3 python3-GitPython python3-jinja2 python3-pexpect python3-pip rpcgen socat tar texinfo unzip wget which xz zstd

```

Note

- Extra Packages for Enterprise Linux (i.e. `epel-release`) is a collection of packages from Fedora built on RHEL/CentOS for easy installation of packages not included in enterprise Linux by default. You need to install these packages separately.

- The `PowerTools/CRB` repo provides additional packages such as `rpcgen` and `texinfo`.

- The `makecache` command consumes additional Metadata from `epel-release`.

Here are the packages needed to build Project documentation manuals:

```
$ sudo dnf install git glibc-locale-source librsvg2-tools make python3-pip which
$ sudo pip3 install sphinx sphinx_rtd_theme pyyaml

```

In addition to the previous packages, here are the packages needed to build the documentation in PDF format:

```
$ sudo dnf install latexmk texlive-collection-fontsrecommended texlive-collection-latex texlive-collection-latexrecommended texlive-collection-xetex texlive-fncychap texlive-gnu-freefont texlive-tex-gyre texlive-xetex

```

Warning

Unlike Fedora or OpenSUSE, AlmaLinux does not provide the packages `texlive-collection-fontsextra`, `texlive-collection-lang*` and `texlive-collection-latexextra`, so you may run into issues. These may be installed using tlmgr.

##### 1.5 Required Git, tar, Python, make and gcc Versions

In order to use the build system, your host development system must meet the following version requirements for Git, tar, and Python:

- Git 1.8.3.1 or greater

- tar 1.28 or greater

- Python 3.8.0 or greater

- GNU make 4.0 or greater

If your host development system does not meet all these requirements, you can resolve this by installing a buildtools tarball that contains these tools. You can either download a pre-built tarball or use BitBake to build one.

In addition, your host development system must meet the following version requirement for gcc:

- gcc 8.0 or greater

If your host development system does not meet this requirement, you can resolve this by installing a buildtools-extended tarball that contains additional tools, the equivalent of the Debian/Ubuntu `build-essential` package.

For systems with a broken make version (e.g. make 4.2.1 without patches) but where the rest of the host tools are usable, you can use the buildtools-make tarball instead.

In the sections that follow, three different methods will be described for installing the buildtools, buildtools-extended or buildtools-make toolset.

###### 1.5.1 Installing a Pre-Built `buildtools` Tarball with `install-buildtools` script

The `install-buildtools` script is the easiest of the three methods by which you can get these tools. It downloads a pre-built buildtools installer and automatically installs the tools for you:

- Execute the `install-buildtools` script. Here is an example:

```
$ cd poky
$ scripts/install-buildtools \
  --without-extended-buildtools \
  --base-url https://downloads.yoctoproject.org/releases/yocto \
  --release yocto-5.0.21 \
  --installer-version 5.0.21

```

During execution, the buildtools tarball will be downloaded, the checksum of the download will be verified, the installer will be run for you, and some basic checks will be run to make sure the installation is functional.

To avoid the need of `sudo` privileges, the `install-buildtools` script will by default tell the installer to install in:

```
/path/to/poky/buildtools

```

If your host development system needs the additional tools provided in the buildtools-extended tarball, you can instead execute the `install-buildtools` script with the default parameters:

```
$ cd poky
$ scripts/install-buildtools

```

Alternatively if your host development system has a broken `make` version such that you only need a known good version of `make`, you can use the `--make-only` option:

```
$ cd poky
$ scripts/install-buildtools --make-only

```

- Source the tools environment setup script by using a command like the following:

```
$ source /path/to/poky/buildtools/environment-setup-x86_64-pokysdk-linux

```

After you have sourced the setup script, the tools are added to `PATH` and any other environment variables required to run the tools are initialized. The results are working versions versions of Git, tar, Python and `chrpath`. And in the case of the buildtools-extended tarball, additional working versions of tools including `gcc`, `make` and the other tools included in `packagegroup-core-buildessential`.

###### 1.5.2 Downloading a Pre-Built `buildtools` Tarball

If you would prefer not to use the `install-buildtools` script, you can instead download and run a pre-built buildtools installer yourself with the following steps:

- Go to https://downloads.yoctoproject.org/releases/yocto/yocto-5.0.21/buildtools/, locate and download the `.sh` file corresponding to your host architecture and to buildtools, buildtools-extended or buildtools-make.

- Execute the installation script. Here is an example for the traditional installer:

```
$ sh ~/Downloads/x86_64-buildtools-nativesdk-standalone-5.0.21.sh

```

Here is an example for the extended installer:

```
$ sh ~/Downloads/x86_64-buildtools-extended-nativesdk-standalone-5.0.21.sh

```

An example for the make-only installer:

```
$ sh ~/Downloads/x86_64-buildtools-make-nativesdk-standalone-5.0.21.sh

```

During execution, a prompt appears that allows you to choose the installation directory. For example, you could choose the following: `/home/user/buildtools`

- As instructed by the installer script, you will have to source the tools environment setup script:

```
$ source /home/user/buildtools/environment-setup-x86_64-pokysdk-linux

```

After you have sourced the setup script, the tools are added to `PATH` and any other environment variables required to run the tools are initialized. The results are working versions versions of Git, tar, Python and `chrpath`. And in the case of the buildtools-extended tarball, additional working versions of tools including `gcc`, `make` and the other tools included in `packagegroup-core-buildessential`.

###### 1.5.3 Building Your Own `buildtools` Tarball

Building and running your own buildtools installer applies only when you have a build host that can already run BitBake. In this case, you use that machine to build the `.sh` file and then take steps to transfer and run it on a machine that does not meet the minimal Git, tar, and Python (or gcc) requirements.

Here are the steps to take to build and run your own buildtools installer:

- On the machine that is able to run BitBake, be sure you have set up your build environment with the setup script (oe-init-build-env).

- Run the BitBake command to build the tarball:

```
$ bitbake buildtools-tarball

```

or to build the extended tarball:

```
$ bitbake buildtools-extended-tarball

```

or to build the make-only tarball:

```
$ bitbake buildtools-make-tarball

```

Note

The SDKMACHINE variable in your `local.conf` file determines whether you build tools for a 32-bit or 64-bit system.

Once the build completes, you can find the `.sh` file that installs the tools in the `tmp/deploy/sdk` subdirectory of the Build Directory. The installer file has the string “buildtools” or “buildtools-extended” in the name.

- Transfer the `.sh` file from the build host to the machine that does not meet the Git, tar, or Python (or gcc) requirements.

- On this machine, run the `.sh` file to install the tools. Here is an example for the traditional installer:

```
$ sh ~/Downloads/x86_64-buildtools-nativesdk-standalone-5.0.21.sh

```

For the extended installer:

```
$ sh ~/Downloads/x86_64-buildtools-extended-nativesdk-standalone-5.0.21.sh

```

And for the make-only installer:

```
$ sh ~/Downloads/x86_64-buildtools-make-nativesdk-standalone-5.0.21.sh

```

During execution, a prompt appears that allows you to choose the installation directory. For example, you could choose the following: `/home/user/buildtools`

- Source the tools environment setup script by using a command like the following:

```
$ source /home/user/buildtools/environment-setup-x86_64-poky-linux

```

After you have sourced the setup script, the tools are added to `PATH` and any other environment variables required to run the tools are initialized. The results are working versions versions of Git, tar, Python and `chrpath`. And in the case of the buildtools-extended tarball, additional working versions of tools including `gcc`, `make` and the other tools included in `packagegroup-core-buildessential`.
