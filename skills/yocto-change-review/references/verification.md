# Build-Backed Verification

Commands that turn a `reasoned` finding into a `verified` one. Use them only when a
configured build directory exists (after `source oe-init-build-env <builddir>`), and
prefer the cheap ones. Do not start full image builds or `bitbake world` without the
user's agreement; say what you would run instead. Sources: dev-manual/debugging.md,
dev-manual/layers.md, dev-manual/build-quality.md, contributor-guide/submit-changes.md,
test-manual/reproducible-builds.md, ref-manual/tasks.md.

## Cost guide

| Cost | Commands |
|---|---|
| seconds to a minute (parse only) | `bitbake-getvar`, `bitbake -e`, `bitbake-layers show-*`, `bitbake -p` |
| minutes, no compilation | `bitbake -S none|printdiff <target>`, `bitbake-diffsigs`, `patchtest`, `oelint-adv` |
| one recipe build | `bitbake <recipe>`, `bitbake <recipe> -c patch`, `-c kernel_configcheck -f` |
| large | `bitbake <image>`, `yocto-check-layer` (includes world builds), reproducibility selftest |

## Applying the change

Check out the base and the change in the layer repository (or a worktree), so you can run
the same command before and after. Never modify the user's branch to test; use a
temporary worktree or ask.

## Variable values and history

```bash
bitbake-getvar -r <recipe> IMAGE_INSTALL          # value + how it got there
bitbake-getvar DISTRO_FEATURES                    # global (configuration) value
bitbake -e <recipe> | grep -E '^(DEPENDS|RDEPENDS|FILES|PACKAGECONFIG)'
```

"In the output of `bitbake-getvar`, the line containing the value of the variable is
preceded by a description of how the variable got its value, including temporary values
that were later overridden" (dev-manual/debugging.md). This is the proof for operator,
override and ordering findings: show the before/after value.

## Layers and appends

```bash
bitbake-layers show-layers        # priorities
bitbake-layers show-appends       # which bbappends apply to which recipe file
bitbake-layers show-overlayed     # recipes hidden by a higher-priority layer
bitbake-layers show-recipes <pn>
bitbake-layers show-cross-depends
```

## Signatures and blast radius

```bash
bitbake -S none <target>          # write sigdata for every task that would run
bitbake -S printdiff <target>     # compare with the most recent matching signatures
bitbake-diffsigs <old.sigdata> <new.sigdata>
bitbake-dumpsig <file.siginfo>
```

"printdiff will try to establish the most recent signature match (e.g. in the sstate
cache) and then compare the matched signatures to determine the stamps and delta where
these two stamp trees diverge" (dev-manual/debugging.md 32.6). Run on the base, then on
the change, and count the tasks whose hash changed; quote the variable that differs. The
`siginfo` files in `SSTATE_DIR` show which variables went into a signature (32.7).

## Build-level checks

```bash
bitbake <recipe> -c patch          # patches apply, patch-fuzz / patch-status QA
bitbake <recipe>                   # do_package_qa runs as part of the build
bitbake <kernel> -c kernel_configcheck -f
oe-pkgdata-util list-pkg-files -p <recipe>    # resulting package split
```

QA results come from `do_package_qa` with the check name in brackets. Whether it is an
error or warning: `bitbake-getvar -r <recipe> ERROR_QA` / `WARN_QA`.

## Output comparison

With `INHERIT += "buildhistory"` and `BUILDHISTORY_COMMIT = "1"` in `local.conf`, build
before and after and run `buildhistory-diff . HEAD^` from the build directory "that
queries the Git repository and prints just the differences that might be significant"
(package lists, sizes, dependencies, image contents) (dev-manual/build-quality.md).

## Layer compatibility

```bash
yocto-check-layer <layer-dir>
```

Tests listed in dev-manual/layers.md 3.3.2 (`common.test_signatures`,
`bsp.test_machine_signatures`, ...). Expensive; usually report "would run".

## Patch format (OE-Core)

```bash
pip install -r meta/lib/patchtest/requirements.txt
source oe-init-build-env
bitbake-layers add-layer ../meta-selftest
patchtest --patch <file.patch>          # or --directory <dir>
```

Only supports openembedded-core branches; use `--repodir`/`--testdir` for others
(contributor-guide/submit-changes.md 4.4). `bitbake-layers add-layer ../meta-selftest`
changes the build configuration: ask first, or use a throwaway build directory.

## Reproducibility

```bash
# local.conf: OEQA_REPRODUCIBLE_TEST_TARGET = "<recipe>"
oe-selftest -r reproducible.ReproducibleTests.test_reproducible_builds
```

## External linter (optional)

`oelint-adv` is a third-party linter for BitBake recipes (installed with
`pip install oelint_adv`, run as `oelint-adv <files>`). It is not part of the Yocto
Project and not described in the scarthgap manuals; the OE-Core `oelint` class is
described there as "an obsolete lint checking tool". Use its output as hints, verify
each one against the manual, and attribute it ("oelint-adv: ...").

## Reporting results

- Put each command and its relevant output line under "Verification run".
- Mark findings proven by output `verified`; everything else stays `reasoned`.
- If verification contradicts a reasoned finding, drop or correct the finding; do not
  keep it "just in case".
- If no build directory was available, write "none: no build directory available" and
  list the two or three commands that would settle the most important findings.

Derived from the Yocto Project scarthgap (5.0) documentation, CC BY-SA 2.0 UK.
