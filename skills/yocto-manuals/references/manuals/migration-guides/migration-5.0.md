<!-- Source: https://docs.yoctoproject.org/scarthgap/migration-guides/migration-5.0.html (converted from singleindex.html). License: see LICENSE-docs.md in this folder. -->

##### Release 5.0 LTS (scarthgap)

###### Migration notes for 5.0 (scarthgap)

This section provides migration information for moving to the Yocto Project 5.0 Release (codename “scarthgap”) from the prior release.

To migrate from an earlier LTS release, you **also** need to check all the previous migration notes from your release to this new one:

- Release 4.3 (nanbield)

- Release 4.2 (mickledore)

- Release 4.1 (langdale)

- Release 4.0 (kirkstone)

- Migration notes for 3.4 (honister)

- Release 3.3 (hardknott)

- Release 3.2 (gatesgarth)

###### Supported kernel versions

The OLDEST_KERNEL setting is still “5.15” in this release, meaning that out the box, older kernels are not supported. See 4.3 migration notes for details.

###### Supported distributions

Compared to the previous releases, running BitBake is supported on new GNU/Linux distributions:

- Rocky 9

On the other hand, some earlier distributions are no longer supported:

- Fedora 37

- Ubuntu 22.10

- OpenSUSE Leap 15.3

See all supported distributions.

###### Go language changes

The `linkmode` flag was dropped from `GO_LDFLAGS` for `nativesdk` and `cross-canadian`. Also, dynamic linking was disabled for the whole set of (previously) supported architectures in the `goarch` class.

###### systemd changes

Systemd’s nss-resolve plugin is now supported and can be added via the `nss-resolve` PACKAGECONFIG option , which is from now on required (along with `resolved`) by the `systemd-resolved` feature. Related to that (i.e., Systemd’s network name resolution), an option to use `stub-resolv.conf` was added as well.

###### Recipe changes

- Runtime testing of ptest now fails if no test results are returned by any given ptest.

###### Deprecated variables

- `CVE_CHECK_IGNORE` should be replaced with CVE_STATUS

###### Removed variables

The following variables have been removed:

- `DEPLOY_DIR_TAR`: no longer needed since the package_tar class was removed in 4.2.

- `PYTHON_PN`: Python 2 has previously been removed, leaving Python 3 as the sole major version. Therefore, this abstraction to differentiate both versions is no longer needed.

- `oldincludedir`

- `USE_L10N`: previously deprecated, and now removed.

- `CVE_SOCKET_TIMEOUT`

- `SERIAL_CONSOLES_CHECK` - use SERIAL_CONSOLES instead as all consoles specified in the latter are checked for their existence before a `getty` is started.

###### Removed recipes

The following recipes have been removed in this release:

- `libcroco`: deprecated and archived by the Gnome Project.

- `liberror-perl`: unmaintained and no longer needed - moved to meta-perl.

- `linux-yocto`: version 6.1 (version 6.6 provided instead).

- `systemtap-uprobes`: obsolete.

- `zvariant`: fails to build with newer Rust.

###### Removed classes

No classes have been removed in this release.

###### QEMU changes

In `tune-core2`, the cpu models `n270` and `core2duo` are no longer passed to QEMU, since its documentation recommends not using them with `-cpu` option. Therefore, from now on, `Nehalem` model is used instead.

###### ipk packaging changes

ipk packaging (using `opkg`) now uses `zstd` compression instead of `xz` for better compression and performance. This does mean that `.ipk` packages built using the 5.0 release requires Opkg built with zstd enabled — naturally this is the case in 5.0, but at least by default these packages will not be usable on older systems where Opkg does not have zstd enabled at build time.

Additionally, the internal dependency solver in Opkg is now deprecated — it is still available in this release but will trigger a warning if selected. The default has been the external `libsolv` solver for some time, but if you have explicitly removed that from PACKAGECONFIG for Opkg to select the internal solver, you should plan to switch to `libsolv` in the near future (by including `libsolv` your custom PACKAGECONFIG value for Opkg, or reverting to the default value).

###### motd message when using `DISTRO = "poky"`

The default `poky` DISTRO is explicitly a *reference* distribution for testing and development purposes. It enables most hardware and software features so that they can be tested, but this also means that from a security point of view the attack surface is very large.

We encourage anyone using the Yocto Project for production use to create their own distribution and not use Poky. To encourage this behaviour further, in 5.0 a warning has been added to `/etc/motd` when Poky is used so that the developer will see it when they log in. If you are creating your own distribution this message will not show up.

For information on how to create your own distribution, see “Creating Your Own Distribution”.

###### Miscellaneous changes

- `bitbake-whatchanged` script was removed as it was broken and unmaintained.

- `scripts/sstate-cache-management.sh` has been replaced by `scripts/sstate-cache-management.py`, a more performant Python-based version.

- The `bmap-tools` recipe has been renamed to `bmaptool`.

- `gpgme` has had Python binding support disabled since upstream does not support Python 3.12 yet. This will be fixed in future once it is fixed upstream.)

- A warning will now be shown if the `virtual/` prefix is used in runtime contexts (RDEPENDS / RPROVIDES) — See virtual-slash for details.

- `recipetool` now prefixes the names of recipes created for Python modules with `python3-`.

- The cve-check class no longer produces a warning for remote patches — it only logs a note and does not try to fetch the patch in order to scan it for issues or CVE numbers. However, CVE number references in remote patch file names will now be picked up.

- The values of PE and PR have been dropped from `-f{file,macro,debug}-prefix-map`, in order to avoid unnecessary churn in debugging symbol paths when the version is bumped. This is unlikely to cause issues, but if you are paying attention to the debugging source path (e.g. in recipes that need to manipulate these files during packaging) then you will notice the difference. A new TARGET_DBGSRC_DIR variable is provided to make this easier.

- `ccache` no longer supports FORTRAN.
