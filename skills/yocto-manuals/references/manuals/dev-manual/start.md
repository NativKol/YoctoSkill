<!-- Source: https://docs.yoctoproject.org/scarthgap/dev-manual/start.html (converted from singleindex.html). License: see LICENSE-docs.md in this folder. -->

#### 2 Setting Up to Use the Yocto Project

This chapter provides guidance on how to prepare to use the Yocto Project. You can learn about creating a team environment to develop using the Yocto Project, how to set up a build host, how to locate Yocto Project source repositories, and how to create local Git repositories.

##### 2.1 Creating a Team Development Environment

It might not be immediately clear how you can use the Yocto Project in a team development environment, or how to scale it for a large team of developers. You can adapt the Yocto Project to many different use cases and scenarios; however, this flexibility could cause difficulties if you are trying to create a working setup that scales effectively.

To help you understand how to set up this type of environment, this section presents a procedure that gives you information that can help you get the results you want. The procedure is high-level and presents some of the project’s most successful experiences, practices, solutions, and available technologies that have proved to work well in the past; however, keep in mind, the procedure here is simply a starting point. You can build off these steps and customize the procedure to fit any particular working environment and set of practices.

- *Determine Who is Going to be Developing:* You first need to understand who is going to be doing anything related to the Yocto Project and determine their roles. Making this determination is essential to completing subsequent steps, which are to get your equipment together and set up your development environment’s hardware topology.

Possible roles are:

  - *Application Developer:* This type of developer does application level work on top of an existing software stack.

  - *Core System Developer:* This type of developer works on the contents of the operating system image itself.

  - *Build Engineer:* This type of developer manages Autobuilders and releases. Depending on the specifics of the environment, not all situations might need a Build Engineer.

  - *Test Engineer:* This type of developer creates and manages automated tests that are used to ensure all application and core system development meets desired quality standards.

- *Gather the Hardware:* Based on the size and make-up of the team, get the hardware together. Ideally, any development, build, or test engineer uses a system that runs a supported Linux distribution. These systems, in general, should be high performance (e.g. dual, six-core Xeons with 24 Gbytes of RAM and plenty of disk space). You can help ensure efficiency by having any machines used for testing or that run Autobuilders be as high performance as possible.

Note

Given sufficient processing power, you might also consider building Yocto Project development containers to be run under Docker, which is described later.

- *Understand the Hardware Topology of the Environment:* Once you understand the hardware involved and the make-up of the team, you can understand the hardware topology of the development environment. You can get a visual idea of the machines and their roles across the development environment.

- *Use Git as Your Source Control Manager (SCM):* Keeping your Metadata (i.e. recipes, configuration files, classes, and so forth) and any software you are developing under the control of an SCM system that is compatible with the OpenEmbedded build system is advisable. Of all of the SCMs supported by BitBake, the Yocto Project team strongly recommends using Git. Git is a distributed system that is easy to back up, allows you to work remotely, and then connects back to the infrastructure.

Note

For information about BitBake, see the BitBake User Manual.

It is relatively easy to set up Git services and create infrastructure like https://git.yoctoproject.org/, which is based on server software called Gitolite with cgit being used to generate the web interface that lets you view the repositories. `gitolite` identifies users using SSH keys and allows branch-based access controls to repositories that you can control as little or as much as necessary.

- *Set up the Application Development Machines:* As mentioned earlier, application developers are creating applications on top of existing software stacks. Here are some best practices for setting up machines used for application development:

  - Use a pre-built toolchain that contains the software stack itself. Then, develop the application code on top of the stack. This method works well for small numbers of relatively isolated applications.

  - Keep your cross-development toolchains updated. You can do this through provisioning either as new toolchain downloads or as updates through a package update mechanism using `opkg` to provide updates to an existing toolchain. The exact mechanics of how and when to do this depend on local policy.

  - Use multiple toolchains installed locally into different locations to allow development across versions.

- *Set up the Core Development Machines:* As mentioned earlier, core developers work on the contents of the operating system itself. Here are some best practices for setting up machines used for developing images:

  - Have the OpenEmbedded Build System available on the developer workstations so developers can run their own builds and directly rebuild the software stack.

  - Keep the core system unchanged as much as possible and do your work in layers on top of the core system. Doing so gives you a greater level of portability when upgrading to new versions of the core system or Board Support Packages (BSPs).

  - Share layers amongst the developers of a particular project and contain the policy configuration that defines the project.

- *Set up an Autobuilder:* Autobuilders are often the core of the development environment. It is here that changes from individual developers are brought together and centrally tested. Based on this automated build and test environment, subsequent decisions about releases can be made. Autobuilders also allow for “continuous integration” style testing of software components and regression identification and tracking.

See “Yocto Project Autobuilder” for more information and links to buildbot. The Yocto Project team has found this implementation works well in this role. A public example of this is the Yocto Project Autobuilders, which the Yocto Project team uses to test the overall health of the project.

The features of this system are:

  - Highlights when commits break the build.

  - Populates an sstate cache from which developers can pull rather than requiring local builds.

  - Allows commit hook triggers, which trigger builds when commits are made.

  - Allows triggering of automated image booting and testing under the QuickEMUlator (QEMU).

  - Supports incremental build testing and from-scratch builds.

  - Shares output that allows developer testing and historical regression investigation.

  - Creates output that can be used for releases.

  - Allows scheduling of builds so that resources can be used efficiently.

- *Set up Test Machines:* Use a small number of shared, high performance systems for testing purposes. Developers can use these systems for wider, more extensive testing while they continue to develop locally using their primary development system.

- *Document Policies and Change Flow:* The Yocto Project uses a hierarchical structure and a pull model. There are scripts to create and send pull requests (i.e. `create-pull-request` and `send-pull-request`). This model is in line with other open source projects where maintainers are responsible for specific areas of the project and a single maintainer handles the final “top-of-tree” merges.

Note

You can also use a more collective push model. The `gitolite` software supports both the push and pull models quite easily.

As with any development environment, it is important to document the policy used as well as any main project guidelines so they are understood by everyone. It is also a good idea to have well-structured commit messages, which are usually a part of a project’s guidelines. Good commit messages are essential when looking back in time and trying to understand why changes were made.

If you discover that changes are needed to the core layer of the project, it is worth sharing those with the community as soon as possible. Chances are if you have discovered the need for changes, someone else in the community needs them also.

- *Development Environment Summary:* Aside from the previous steps, here are best practices within the Yocto Project development environment:

  - Use Git as the source control system.

  - Maintain your Metadata in layers that make sense for your situation. See the “The Yocto Project Layer Model” section in the Yocto Project Overview and Concepts Manual and the “Understanding and Creating Layers” section for more information on layers.

  - Separate the project’s Metadata and code by using separate Git repositories. See the “Yocto Project Source Repositories” section in the Yocto Project Overview and Concepts Manual for information on these repositories. See the “Locating Yocto Project Source Files” section for information on how to set up local Git repositories for related upstream Yocto Project Git repositories.

  - Set up the directory for the shared state cache (SSTATE_DIR) where it makes sense. For example, set up the sstate cache on a system used by developers in the same organization and share the same source directories on their machines.

  - Set up an Autobuilder and have it populate the sstate cache and source directories.

  - The Yocto Project community encourages you to send patches to the project to fix bugs or add features. If you do submit patches, follow the project commit guidelines for writing good commit messages. See the “Contributing Changes to a Component” section in the Yocto Project and OpenEmbedded Contributor Guide.

  - Send changes to the core sooner than later as others are likely to run into the same issues. For some guidance on mailing lists to use, see the lists in the “Finding a Suitable Mailing List” section. For a description of the available mailing lists, see the “Mailing lists” section in the Yocto Project Reference Manual.

##### 2.2 Preparing the Build Host

This section provides procedures to set up a system to be used as your Build Host for development using the Yocto Project. Your build host can be a native Linux machine (recommended), it can be an OCI container (such as Docker or Podman), or it can be a Windows machine capable of running version 2 of Windows Subsystem For Linux (WSL 2).

Note

The Yocto Project is not compatible with version 1 of Windows Subsystem for Linux. It is compatible but neither officially supported nor validated with WSL 2. If you still decide to use WSL please upgrade to WSL 2.

Once your build host is set up to use the Yocto Project, further steps are necessary depending on what you want to accomplish. See the following references for information on how to prepare for Board Support Package (BSP) development and kernel development:

- *BSP Development:* See the “Preparing Your Build Host to Work With BSP Layers” section in the Yocto Project Board Support Package (BSP) Developer’s Guide.

- *Kernel Development:* See the “Preparing the Build Host to Work on the Kernel” section in the Yocto Project Linux Kernel Development Manual.

###### 2.2.1 Setting Up a Native Linux Host

Follow these steps to prepare a native Linux machine as your Yocto Project Build Host:

- *Use a Supported Linux Distribution:* You should have a reasonably current Linux-based host system. You will have the best results with a recent release of Fedora, openSUSE, Debian, Ubuntu, RHEL or CentOS as these releases are frequently tested against the Yocto Project and officially supported. For a list of the distributions under validation and their status, see the “Supported Linux Distributions” section in the Yocto Project Reference Manual.

- *Have Enough Free Memory:* Your system should have at least 50 Gbytes of free disk space for building images.

- *Meet Minimal Version Requirements:* The OpenEmbedded build system should be able to run on any modern distribution that has the following versions for Git, tar, Python, gcc and make.

  - Git 1.8.3.1 or greater

  - tar 1.28 or greater

  - Python 3.8.0 or greater.

  - gcc 8.0 or greater.

  - GNU make 4.0 or greater

If your build host does not meet any of these listed version requirements, you can take steps to prepare the system so that you can still use the Yocto Project. See the “Required Git, tar, Python, make and gcc Versions” section in the Yocto Project Reference Manual for information.

- *Install Development Host Packages:* Required development host packages vary depending on your build host and what you want to do with the Yocto Project. Collectively, the number of required packages is large if you want to be able to cover all cases.

For lists of required packages for all scenarios, see the “Required Packages for the Build Host” section in the Yocto Project Reference Manual.

Once you have completed the previous steps, you are ready to continue using a given development path on your native Linux machine. If you are going to use BitBake, see the “Cloning the poky Repository” section. If you are going to use the Extensible SDK, see the “Using the Extensible SDK” Chapter in the Yocto Project Application Development and the Extensible Software Development Kit (eSDK) manual. If you want to work on the kernel, see the Yocto Project Linux Kernel Development Manual. If you are going to use Toaster, see the “Setting Up and Using Toaster” section in the Toaster User Manual. If you are a VSCode user, you can configure the Yocto Project BitBake extension accordingly.

###### 2.2.2 Setting Up to Use Windows Subsystem For Linux (WSL 2)

With Windows Subsystem for Linux (WSL 2), you can create a Yocto Project development environment that allows you to build on Windows. You can set up a Linux distribution inside Windows in which you can develop using the Yocto Project.

Follow these general steps to prepare a Windows machine using WSL 2 as your Yocto Project build host:

- *Make sure your Windows machine is capable of running WSL 2:*

While all Windows 11 and Windows Server 2022 builds support WSL 2, the first versions of Windows 10 and Windows Server 2019 didn’t. Check the minimum build numbers for Windows 10 and for Windows Server 2019.

To check which build version you are running, you may open a command prompt on Windows and execute the command “ver”:

```
C:\Users\user> ver

Microsoft Windows [Version 10.0.19041.153]

```

- *Install the Linux distribution of your choice inside WSL 2:* Once you know your version of Windows supports WSL 2, you can install the distribution of your choice from the Microsoft Store. Open the Microsoft Store and search for Linux. While there are several Linux distributions available, the assumption is that your pick will be one of the distributions supported by the Yocto Project as stated on the instructions for using a native Linux host. After making your selection, simply click “Get” to download and install the distribution.

- *Check which Linux distribution WSL 2 is using:* Open a Windows PowerShell and run:

```
C:\WINDOWS\system32> wsl -l -v
NAME    STATE   VERSION
*Ubuntu Running 2

```

Note that WSL 2 supports running as many different Linux distributions as you want to install.

- *Optionally Get Familiar with WSL:* You can learn more on https://docs.microsoft.com/en-us/windows/wsl/wsl2-about.

- *Launch your WSL Distibution:* From the Windows start menu simply launch your WSL distribution just like any other application.

- *Optimize your WSL 2 storage often:* Due to the way storage is handled on WSL 2, the storage space used by the underlying Linux distribution is not reflected immediately, and since BitBake heavily uses storage, after several builds, you may be unaware you are running out of space. As WSL 2 uses a VHDX file for storage, this issue can be easily avoided by regularly optimizing this file in a manual way:

  - *Find the location of your VHDX file:*

First you need to find the distro app package directory, to achieve this open a Windows Powershell as Administrator and run:

```
C:\WINDOWS\system32> Get-AppxPackage -Name "*Ubuntu*" | Select PackageFamilyName
PackageFamilyName
-----------------
CanonicalGroupLimited.UbuntuonWindows_79abcdefgh

```

You should now replace the PackageFamilyName and your user on the following path to find your VHDX file:

```
ls C:\Users\user\AppData\Local\Packages\CanonicalGroupLimited.UbuntuonWindows_79abcdefgh\LocalState\
Mode                 LastWriteTime         Length Name
-a----         3/14/2020   9:52 PM    57418973184 ext4.vhdx

```

Your VHDX file path is: `C:\Users\user\AppData\Local\Packages\CanonicalGroupLimited.UbuntuonWindows_79abcdefgh\LocalState\ext4.vhdx`

2a. *Optimize your VHDX file using Windows Powershell:*

To use the `optimize-vhd` cmdlet below, first install the Hyper-V option on Windows. Then, open a Windows Powershell as Administrator to optimize your VHDX file, shutting down WSL first:

```
C:\WINDOWS\system32> wsl --shutdown
C:\WINDOWS\system32> optimize-vhd -Path C:\Users\user\AppData\Local\Packages\CanonicalGroupLimited.UbuntuonWindows_79abcdefgh\LocalState\ext4.vhdx -Mode full

```

A progress bar should be shown while optimizing the VHDX file, and storage should now be reflected correctly on the Windows Explorer.

2b. *Optimize your VHDX file using DiskPart:*

The `optimize-vhd` cmdlet noted in step 2a above is provided by Hyper-V. Not all SKUs of Windows can install Hyper-V. As an alternative, use the DiskPart tool. To start, open a Windows command prompt as Administrator to optimize your VHDX file, shutting down WSL first:

```
C:\WINDOWS\system32> wsl --shutdown
C:\WINDOWS\system32> diskpart

DISKPART> select vdisk file="<path_to_VHDX_file>"
DISKPART> attach vdisk readonly
DISKPART> compact vdisk
DISKPART> detach
DISKPART> exit

```

Note

The current implementation of WSL 2 does not have out-of-the-box access to external devices such as those connected through a USB port, but it automatically mounts your `C:` drive on `/mnt/c/` (and others), which you can use to share deploy artifacts to be later flashed on hardware through Windows, but your Build Directory should not reside inside this mountpoint.

Once you have WSL 2 set up, everything is in place to develop just as if you were running on a native Linux machine. If you are going to use the Extensible SDK container, see the “Using the Extensible SDK” Chapter in the Yocto Project Application Development and the Extensible Software Development Kit (eSDK) manual. If you are going to use the Toaster container, see the “Setting Up and Using Toaster” section in the Toaster User Manual. If you are a VSCode user, you can configure the Yocto Project BitBake extension accordingly.

##### 2.3 Locating Yocto Project Source Files

This section shows you how to locate, fetch and configure the source files you’ll need to work with the Yocto Project.

Note

- For concepts and introductory information about Git as it is used in the Yocto Project, see the “Git” section in the Yocto Project Overview and Concepts Manual.

- For concepts on Yocto Project source repositories, see the “Yocto Project Source Repositories” section in the Yocto Project Overview and Concepts Manual.”

###### 2.3.1 Accessing Source Repositories

Working from a copy of the upstream Accessing Source Repositories is the preferred method for obtaining and using a Yocto Project release. You can view the Yocto Project Source Repositories at https://git.yoctoproject.org/. In particular, you can find the `poky` repository at https://git.yoctoproject.org/poky.

Use the following procedure to locate the latest upstream copy of the `poky` Git repository:

- *Access Repositories:* Open a browser and go to https://git.yoctoproject.org/ to access the GUI-based interface into the Yocto Project source repositories.

- *Select the Repository:* Click on the repository in which you are interested (e.g. `poky`).

- *Find the URL Used to Clone the Repository:* At the bottom of the page, note the URL used to clone that repository (e.g. https://git.yoctoproject.org/poky).

Note

For information on cloning a repository, see the “Cloning the poky Repository” section.

###### 2.3.2 Accessing Source Archives

The Yocto Project also provides source archives of its releases, which are available on https://downloads.yoctoproject.org/releases/yocto/. Then, choose the subdirectory containing the release you wish to use, for example yocto-5.0.21.

You will find there source archives of individual components (if you wish to use them individually), and of the corresponding Poky release bundling a selection of these components.

Note

The recommended method for accessing Yocto Project components is to use Git to clone the upstream repository and work from within that locally cloned repository.

###### 2.3.3 Using the Downloads Page

The Yocto Project Website uses a “RELEASES” page from which you can locate and download tarballs of any Yocto Project release. Rather than Git repositories, these files represent snapshot tarballs similar to the tarballs located in the Index of Releases described in the “Accessing Source Archives” section.

- *Go to the Yocto Project Website:* Open The Yocto Project Website in your browser.

- *Get to the Downloads Area:* Select the “RELEASES” item from the pull-down “DEVELOPMENT” tab menu near the top of the page.

- *Select a Yocto Project Release:* On the top of the “RELEASE” page currently supported releases are displayed, further down past supported Yocto Project releases are visible. The “Download” links in the rows of the table there will lead to the download tarballs for the release.

Note

For a “map” of Yocto Project releases to version numbers, see the Releases page.

You can use the “RELEASE ARCHIVE” link to reveal a menu of all Yocto Project releases.

- *Download Tools or Board Support Packages (BSPs):* Next to the tarballs you will find download tools or BSPs as well. Just select a Yocto Project release and look for what you need.

##### 2.4 Cloning and Checking Out Branches

To use the Yocto Project for development, you need a release locally installed on your development system. This locally installed set of files is referred to as the Source Directory in the Yocto Project documentation.

The preferred method of creating your Source Directory is by using Git to clone a local copy of the upstream `poky` repository. Working from a cloned copy of the upstream repository allows you to contribute back into the Yocto Project or to simply work with the latest software on a development branch. Because Git maintains and creates an upstream repository with a complete history of changes and you are working with a local clone of that repository, you have access to all the Yocto Project development branches and tag names used in the upstream repository.

###### 2.4.1 Cloning the `poky` Repository

Follow these steps to create a local version of the upstream Poky Git repository.

- *Set Your Directory:* Change your working directory to where you want to create your local copy of `poky`.

- *Clone the Repository:* The following example command clones the `poky` repository and uses the default name “poky” for your local repository:

```
$ git clone git://git.yoctoproject.org/poky
Cloning into 'poky'...
remote: Counting objects: 432160, done.
remote: Compressing objects: 100% (102056/102056), done.
remote: Total 432160 (delta 323116), reused 432037 (delta 323000)
Receiving objects: 100% (432160/432160), 153.81 MiB | 8.54 MiB/s, done.
Resolving deltas: 100% (323116/323116), done.
Checking connectivity... done.

```

Unless you specify a specific development branch or tag name, Git clones the “master” branch, which results in a snapshot of the latest development changes for “master”. For information on how to check out a specific development branch or on how to check out a local branch based on a tag name, see the “Checking Out by Branch in Poky” and “Checking Out by Tag in Poky” sections, respectively.

Once the local repository is created, you can change to that directory and check its status. The `master` branch is checked out by default:

```
$ cd poky
$ git status
On branch master
Your branch is up-to-date with 'origin/master'.
nothing to commit, working directory clean
$ git branch
* master

```

Your local repository of poky is identical to the upstream poky repository at the time from which it was cloned. As you work with the local branch, you can periodically use the `git pull --rebase` command to be sure you are up-to-date with the upstream branch.

###### 2.4.2 Checking Out by Branch in Poky

When you clone the upstream poky repository, you have access to all its development branches. Each development branch in a repository is unique as it forks off the “master” branch. To see and use the files of a particular development branch locally, you need to know the branch name and then specifically check out that development branch.

Note

Checking out an active development branch by branch name gives you a snapshot of that particular branch at the time you check it out. Further development on top of the branch that occurs after check it out can occur.

- *Switch to the Poky Directory:* If you have a local poky Git repository, switch to that directory. If you do not have the local copy of poky, see the “Cloning the poky Repository” section.

- *Determine Existing Branch Names:*

```
$ git branch -a
* master
remotes/origin/1.1_M1
remotes/origin/1.1_M2
remotes/origin/1.1_M3
remotes/origin/1.1_M4
remotes/origin/1.2_M1
remotes/origin/1.2_M2
remotes/origin/1.2_M3
. . .
remotes/origin/thud
remotes/origin/thud-next
remotes/origin/warrior
remotes/origin/warrior-next
remotes/origin/zeus
remotes/origin/zeus-next
... and so on ...

```

- *Check out the Branch:* Check out the development branch in which you want to work. For example, to access the files for the Yocto Project 5.0.21 Release (Scarthgap), use the following command:

```
$ git checkout -b scarthgap origin/scarthgap
Branch scarthgap set up to track remote branch scarthgap from origin.
Switched to a new branch 'scarthgap'

```

The previous command checks out the “scarthgap” development branch and reports that the branch is tracking the upstream “origin/scarthgap” branch.

The following command displays the branches that are now part of your local poky repository. The asterisk character indicates the branch that is currently checked out for work:

```
$ git branch
  master
  * scarthgap

```

###### 2.4.3 Checking Out by Tag in Poky

Similar to branches, the upstream repository uses tags to mark specific commits associated with significant points in a development branch (i.e. a release point or stage of a release). You might want to set up a local branch based on one of those points in the repository. The process is similar to checking out by branch name except you use tag names.

Note

Checking out a branch based on a tag gives you a stable set of files not affected by development on the branch above the tag.

- *Switch to the Poky Directory:* If you have a local poky Git repository, switch to that directory. If you do not have the local copy of poky, see the “Cloning the poky Repository” section.

- *Fetch the Tag Names:* To checkout the branch based on a tag name, you need to fetch the upstream tags into your local repository:

```
$ git fetch --tags
$

```

- *List the Tag Names:* You can list the tag names now:

```
$ git tag
1.1_M1.final
1.1_M1.rc1
1.1_M1.rc2
1.1_M2.final
1.1_M2.rc1
   .
   .
   .
yocto-2.5
yocto-2.5.1
yocto-2.5.2
yocto-2.5.3
yocto-2.6
yocto-2.6.1
yocto-2.6.2
yocto-2.7
yocto_1.5_M5.rc8

```

- *Check out the Branch:*

```
$ git checkout tags/yocto-5.0.21 -b my_yocto_5.0.21
Switched to a new branch 'my_yocto_5.0.21'
$ git branch
  master
* my_yocto_5.0.21

```

The previous command creates and checks out a local branch named “my_yocto_5.0.21”, which is based on the commit in the upstream poky repository that has the same tag. In this example, the files you have available locally as a result of the `checkout` command are a snapshot of the “scarthgap” development branch at the point where Yocto Project 5.0.21 was released.
