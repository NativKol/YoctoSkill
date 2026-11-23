<!-- Source: https://docs.yoctoproject.org/scarthgap/dev-manual/wayland.html (converted from singleindex.html). License: see LICENSE-docs.md in this folder. -->

#### 37 Using Wayland and Weston

Wayland is a computer display server protocol that provides a method for compositing window managers to communicate directly with applications and video hardware and expects them to communicate with input hardware using other libraries. Using Wayland with supporting targets can result in better control over graphics frame rendering than an application might otherwise achieve.

The Yocto Project provides the Wayland protocol libraries and the reference Weston compositor as part of its release. You can find the integrated packages in the `meta` layer of the Source Directory. Specifically, you can find the recipes that build both Wayland and Weston at `meta/recipes-graphics/wayland`.

You can build both the Wayland and Weston packages for use only with targets that accept the Mesa 3D and Direct Rendering Infrastructure, which is also known as Mesa DRI. This implies that you cannot build and use the packages if your target uses, for example, the Intel Embedded Media and Graphics Driver (Intel EMGD) that overrides Mesa DRI.

Note

Due to lack of EGL support, Weston 1.0.3 will not run directly on the emulated QEMU hardware. However, this version of Weston will run under X emulation without issues.

This section describes what you need to do to implement Wayland and use the Weston compositor when building an image for a supporting target.

##### 37.1 Enabling Wayland in an Image

To enable Wayland, you need to enable it to be built and enable it to be included (installed) in the image.

###### 37.1.1 Building Wayland

To cause Mesa to build the `wayland-egl` platform and Weston to build Wayland with Kernel Mode Setting (KMS) support, include the “wayland” flag in the DISTRO_FEATURES statement in your `local.conf` file:

```
DISTRO_FEATURES:append = " wayland"

```

Note

If X11 has been enabled elsewhere, Weston will build Wayland with X11 support

###### 37.1.2 Installing Wayland and Weston

To install the Wayland feature into an image, you must include the following CORE_IMAGE_EXTRA_INSTALL statement in your `local.conf` file:

```
CORE_IMAGE_EXTRA_INSTALL += "wayland weston"

```

##### 37.2 Running Weston

To run Weston inside X11, enabling it as described earlier and building a Sato image is sufficient. If you are running your image under Sato, a Weston Launcher appears in the “Utility” category.

Alternatively, you can run Weston through the command-line interpretor (CLI), which is better suited for development work. To run Weston under the CLI, you need to do the following after your image is built:

- Run these commands to export `XDG_RUNTIME_DIR`:

```
mkdir -p /tmp/$USER-weston
chmod 0700 /tmp/$USER-weston
export XDG_RUNTIME_DIR=/tmp/$USER-weston

```

- Launch Weston in the shell:

```
weston

```
