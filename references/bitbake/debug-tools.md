# BitBake Inspection, Signature, and devtool Reference

Release: Yocto Project 5.0 "scarthgap" / BitBake 2.8. Sources: dev-manual "Debugging Tools and Techniques" (32.1-32.12), ref-manual "devtool Quick Reference" (7), overview-manual "Shared State Cache", BitBake manual "Task Checksums and Setscene" (3.12), dev-manual "Maintaining Build Output Quality" (31), ref-manual variables `SSTATE_DIR`, `SSTATE_MIRRORS`, `BB_HASHSERVE`.

Each command is marked: **read-only** (safe to run without asking), **builds** (runs tasks, may take long), **destructive** (deletes state; ask first), **interactive** (needs a human at a terminal; an agent cannot drive it).

## 1. Values, Logs, Graphs

| Command | Class | Use |
| --- | --- | --- |
| `bitbake-getvar VAR` / `bitbake-getvar -r <recipe> VAR` | read-only | Final value plus the history of how it was set (file, line, operator); `--value` prints only the value; `-f FLAG` for a flag. Works for shell functions and tasks (`do_install`). (32.2) |
| `bitbake -e <recipe> \| grep ...` | read-only | Full environment including Python functions and the list of included/inherited files at the top. Always filter with `grep`; never page with `less`. |
| `bitbake-layers show-layers` / `show-recipes <pn>` / `show-appends` / `show-overlayed` | read-only | Which layers, which recipe file wins, which appends apply. |
| `bitbake -c listtasks <recipe>` | read-only (runs a trivial task) | Every task defined for the recipe. |
| `bitbake -g <target>` | read-only | Writes `pn-buildlist` and `task-depends.dot` to the current directory; grep the dot file (`grep '"foo.do_configure" ->' task-depends.dot`). `-u taskexp` is a GUI (interactive). (32.4) |
| `bitbake -DDD -v <target>` | builds | Verbose decisions: why this provider or version was chosen. (32.10) |
| `bitbake -n <target>` | read-only | Dry run: shows what would run. |
| `oe-pkgdata-util list-pkgs [pattern]`, `list-pkg-files -p <pkg>`, `find-path <path>`, `lookup-recipe <pkg>` | read-only | Package data in `PKGDATA_DIR`; only for packages that have already been built. (32.3) |
| logs: `${WORKDIR}/temp/log.do_<task>` and `run.do_<task>` | read-only | Symlinks to the latest `log.do_<task>.<pid>` / script. Read the first error, not the summary. (32.1) |
| `tmp/log/cooker/<machine>/console-latest.log` | read-only | The full console output of the last build. |
| `bitbake -c devshell <recipe>`, `-c pydevshell`, `-c menuconfig` | interactive | For a human. An agent reproduces a step by reading `run.do_<task>` and rerunning the task with `bitbake -f -c <task> <recipe>`. |

## 2. Why Did This Rebuild (or Not)?

BitBake computes a signature (hash) for each task from the variables and functions it uses plus the hashes of the tasks it depends on (BitBake manual 3.12). If the signature matches an object in `SSTATE_DIR` or `SSTATE_MIRRORS`, the task is restored ("setscene") instead of run. With hash equivalence (`BB_HASHSERVE`, commonly `auto`), tasks whose inputs changed but whose output is identical are also treated as unchanged, so a change may stop propagating downstream.

```bash
# What would rerun and why, compared with the closest earlier signature (no build):
bitbake -S printdiff <target>                                # (32.6)
# Inspect what went into one task's signature:
ls tmp/stamps/*/<recipe>/*.do_compile.sigdata.*
bitbake-dumpsig tmp/stamps/<arch>/<recipe>/<ver>.do_compile.sigdata.<hash>   # (32.5)
# Compare two signatures (e.g. before/after a change, or a local stamp vs a siginfo in SSTATE_DIR):
bitbake-diffsigs <old.sigdata.X> <new.sigdata.Y>              # (32.6)
bitbake-diffsigs -t <recipe> do_compile                       # last two signatures of a task
```

Tool name note: the dev-manual uses `bitbake-dumpsig`, which is the script BitBake ships; BitBake manual 3.12 spells it `bitbake-dumpsigs`.

`bitbake-dumpsig` prints the task's variable dependencies (`Task dependencies: [...]`), their values, and `BB_BASEHASH_IGNORE_VARS`. Typical findings:

- A variable you changed is not listed: the task reads it indirectly (constructed name, Python `d.getVar` in an odd place). Add `do_task[vardeps] += "VAR"`.
- A volatile variable (date, build host path) is listed and causes rebuilds every time: `do_task[vardepsexclude] += "VAR"` or fix the value.
- An external tool's output changed but no metadata did: the signature cannot see it (32.8). Force the task: `bitbake -f -c <task> <recipe>` (builds; taints the stamp) rather than deleting sstate.

Signature data for sstate objects lives next to them as `*.siginfo` in `SSTATE_DIR` (32.7).

## 3. Forcing Work Without Deleting Caches

Prefer, in this order:

1. `bitbake -f -c <task> <recipe>` or `bitbake -C <task> <recipe>`: rerun from that task (builds).
2. `bitbake -c clean <recipe>`: remove `WORKDIR` output; sstate is kept, so the next build may simply restore (destructive to work dir only).
3. `bitbake -c cleansstate <recipe>`: also remove the recipe's sstate; not recommended with a shared `SSTATE_DIR`, and it cannot touch remote mirrors (destructive, ask first).
4. `bitbake -c cleanall <recipe>`: also delete downloads; the manual says never in a normal scenario, use `bitbake -f -c fetch <recipe>` instead (destructive, ask first).

Never delete `tmp/`, `sstate-cache/` or `downloads/` wholesale as a fix. `scripts/sstate-cache-management.py` (5.0; replaced the `.sh`) prunes old sstate objects deliberately.

## 4. devtool (ref-manual chapter 7)

devtool works in a workspace layer (`<builddir>/workspace`, added to `bblayers.conf` automatically) and builds the recipe from an external source tree via the `externalsrc` class.

| Command | Effect |
| --- | --- |
| `devtool add <name> <url-or-path>` | New recipe from a source tree or URL (runs recipetool; in 5.0 Python module recipes get a `python3-` prefix). |
| `devtool modify <recipe>` | Extracts the source into `workspace/sources/<recipe>` as a git tree with each patch as a commit, and builds from it. |
| `devtool build <recipe>` / `devtool build-image <image>` | Build the workspace recipe / an image including workspace packages. |
| `devtool update-recipe <recipe> [-a <layer>]` | Writes commits back as patches into the original recipe (or a bbappend in `<layer>`). |
| `devtool finish <recipe> <layer>` | `update-recipe` plus remove from the workspace. `--force-patch-refresh` refreshes patch context (the documented fix for `patch-fuzz`). |
| `devtool upgrade <recipe> [-V <version>]`, `devtool latest-version`, `devtool check-upgrade-status` | Version upgrades. |
| `devtool reset <recipe>` | Remove from the workspace without writing back. |
| `devtool deploy-target <recipe> root@<ip>` / `undeploy-target` | Copy build output to a running target over SSH (development only). |
| `devtool status`, `devtool search`, `devtool edit-recipe`, `devtool configure-help`, `devtool menuconfig`, `devtool ide-sdk` | Workspace status, search, open recipe, configure options, kernel-style config, IDE setup. |

Review rule: a workspace recipe shadows the layer recipe until `devtool reset`/`finish`; a forgotten workspace entry explains "my layer change has no effect".

## 5. Build History and Statistics

- `INHERIT += "buildhistory"` and `BUILDHISTORY_COMMIT = "1"` record package lists, sizes, dependencies and image file lists into a git repository at `BUILDHISTORY_DIR` (default `${TOPDIR}/buildhistory`). `buildhistory-diff . HEAD^` (needs GitPython) prints only significant changes (31.2.5). Enables the `version-going-backwards` QA check.
- `buildstats` (on by default via `USER_CLASSES`) writes per-task time and resource use to `${TMPDIR}/buildstats/`; `scripts/pybootchartgui/pybootchartgui.py` charts it.

## 6. Logging From Metadata (32.12)

- Python: `bb.plain()`, `bb.note()`, `bb.warn()`, `bb.error()`, `bb.fatal()`, `bb.debug(level, msg)`.
- Shell: `bbplain`, `bbnote`, `bbwarn`, `bberror`, `bbfatal`, `bbdebug level msg`.

Derived from the Yocto Project scarthgap (5.0) documentation, CC BY-SA 2.0 UK.
