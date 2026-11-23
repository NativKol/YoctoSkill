# Grader: rebuild blast radius and reproducibility of a distro-wide change

The intent is a one-recipe compiler flag, but the diff changes every target recipe's
signatures and makes output non-reproducible. A general model tends to approve the
`TARGET_CFLAGS` line as harmless and not notice what the class change does to every
recipe.

## Required to pass

1. Explains that `TARGET_CFLAGS` in the distro conf applies to every target recipe, so
   it changes the task signatures of essentially all target recipes and triggers a
   near-world rebuild, far beyond the stated intent. Recommends scoping it to the one
   recipe, e.g. `TARGET_CFLAGS:append:pn-perf-helper = " -fno-omit-frame-pointer"` or a
   `.bbappend` for perf-helper.
2. Explains that the class is inherited globally, so the `do_install:append` runs in
   every recipe and writes `/etc/mydistro-version` into every recipe's `${D}`,
   which is a problem on its own (file conflicts or `installed-vs-shipped`) and is made
   worse by the change; at minimum it should be in one recipe (e.g. base-files or an
   os-release bbappend).
3. Explains that embedding `${DATETIME}` makes the output non-reproducible, and that
   `[vardepsexclude]` only hides it from the signature, so sstate reuse will ship stale
   timestamps while fresh builds differ; recommends removing the timestamp or using
   `SOURCE_DATE_EPOCH`-based values.
4. Gives a verdict of request changes, with severities, file:line, and a fix per finding.
5. Recommends a way to verify the blast radius, such as `bitbake -S printdiff <image>` or
   `bitbake-diffsigs`, and labels findings as reasoned (no build available).

## Automatic fail

- Approves the change as-is.
- Says the `TARGET_CFLAGS` change only rebuilds perf-helper.
- Recommends deleting `sstate-cache/` or `tmp/`.

## Improves the score

- Notes that `+=` in a distro conf is fragile versus `:append` if something later
  assigns `TARGET_CFLAGS` with `=`.
- Mentions hash equivalence will not save the rebuild because the compiled output
  actually changes.
- Notes that editing the global class's `do_install:append` itself changes the
  `do_install` signature of every recipe, so the class change alone is also a world
  rebuild.
- Mentions reproducibility testing with
  `oe-selftest -r reproducible.ReproducibleTests.test_reproducible_builds`.
