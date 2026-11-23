# Strictness, Severity, Tone and Confidence

How hard to be on the author, how to rank what you found, how to say it, and how to avoid
reporting things that are not true. Read this before writing any review.

## Contents

1. Severity scale
2. Strictness levels
3. Choosing the level
4. Context modifiers: upstream vs product layers
5. Tone rules
6. Confidence labels
7. False-positive guards
8. Verdict
9. Practices borrowed from other review guides

## 1. Severity scale

Severity is a property of the finding, decided by its effect. Strictness only decides
which severities are shown.

| Severity | Meaning | Typical Yocto examples |
|---|---|---|
| **blocker** | The change breaks the build, ships wrong or unsafe output, violates license or security policy, or silently changes other machines/distros/recipes in a way the author did not intend. Must be fixed before merge. | `:append` without leading space that fuses two tokens; `DEPENDS = "foo"` in a bbappend that wipes the recipe's dependencies; QA check in `ERROR_QA` that the change will trigger (e.g. `dev-so`, `installed-vs-shipped`); wrong `LIC_FILES_CHKSUM`; `debug-tweaks` or an empty root password in a production image or distro; hard-coded password hash or private key in the layer; old `_append` override syntax in a scarthgap layer; unconditional global configuration in `layer.conf`. |
| **major** | Builds and may even work today, but is wrong in a way that will cost someone: incorrect effect in some configurations, upgrade/feed breakage, maintenance trap, rebuild blast radius out of proportion to the change, QA warning that will become an error. | `IMAGE_INSTALL +=` in `local.conf`; `${AUTOREV}` in a released layer; `PV` decreased without `PE` bump; new patch without `Upstream-Status` in a layer where `patch-status` only warns; runtime dependency put in `DEPENDS`; `PACKAGE_ARCH` missing for machine-specific output; a variable added to a globally inherited class without `vardepsexclude` where it should not affect signatures; machine-specific `SRC_URI` file placed where it applies to every machine. |
| **minor** | A real convention or clarity problem with small practical cost. | Missing `HOMEPAGE`/`SUMMARY`; commit shortlog without the `recipe:` prefix; commit body that does not say why; `PR` left behind after a `PV` bump; `${PN}` where `${BPN}` is the convention in a path; `LICENSE` without `License-Update:` explanation in the commit. |
| **nit** | Pure style with no behavioral effect. | Variable order differs from the style guide; single quotes instead of double; no spaces around `=`; continuation lines not aligned; tabs vs spaces in Python; trailing whitespace. |

Rules:

- Raise severity when the change lands in a widely shared place (a distro conf, a class
  in `INHERIT`, `layer.conf`, an `.inc` used by many recipes): the same mistake affects
  more builds.
- Lower severity only on evidence (for example, the value is overridden later in a file
  you read), never on hope.
- Security and license findings are never below **major** unless the context proves they
  are harmless (e.g. `debug-tweaks` in a file named and documented as a development
  template; still mention it).

## 2. Strictness levels

### gentle

For newcomers, first contributions, internal teams that asked for encouragement, or a
quick sanity pass.

- Report: all **blocker** and **major** findings. Then at most three **minor** findings,
  under a heading "Worth knowing (not blocking)". No nits at all, not even a count, unless
  the user asks.
- Every finding carries a complete, paste-ready fix and one sentence of "why" in plain
  language. Avoid jargon without a two-word gloss (e.g. "sstate (the shared build
  cache)").
- Phrase uncertain items as questions ("Is the `-dev` split intentional here?").
- Start with one specific, true thing the change does well, if there is one. Do not
  invent praise.
- Do not apply upstream-submission rules (mailing-list subject prefixes, cover letters,
  patch version changelogs) unless the user said the change is going upstream.

### standard (default)

For ordinary team review.

- Report: **blocker**, **major**, **minor**. Nits as a single line: "Nits: 4 style
  nits (variable order, quoting); ask for strict to list them." If there are three or
  fewer nits you may list them inline in that line.
- Tone: direct and courteous; explain why; one fix per finding.
- Apply commit-message conventions (shortlog prefix, body says why, Signed-off-by if the
  repository uses it). Apply upstream submission rules only if the target is upstream.

### strict

For upstream OE-Core / meta-openembedded submissions, release branches, or when the user
asks for the maintainer bar or "nitpick everything".

- Report everything, including every **nit**, each with file:line.
- Apply every rule in `commit-and-patch-rules.md`: shortlog format, body, trailers,
  one logical change per commit, upgrade removes the old recipe in the same commit,
  `License-Update:` tag, `Upstream-Status` with a valid value and reason, `CVE:` tag,
  `[PATCH vN]` and a changelog after `---` for a reroll, correct mailing list and subject
  prefix, `patchtest`-clean.
- Apply the recipe style guide in full (variable order, quoting, indentation,
  continuation alignment, required metadata).
- Tone: concise and neutral. No padding, no praise unless something is notably good,
  still never about the person.

## 3. Choosing the level

Order of precedence:

1. The user's explicit words in this conversation. Map synonyms:
   - gentle: "be gentle", "be easy on them", "newcomer", "first PR", "junior",
     "encouraging", "only what matters".
   - standard: "normal review", "regular", no qualifier.
   - strict: "strict", "hard", "maintainer bar", "upstream quality", "OE-Core standard",
     "nitpick", "pedantic", "everything".
   - Explicit forms such as `strictness: gentle` or `--strict`.
2. A review policy written in the repository (README, CONTRIBUTING, MAINTAINERS or a
   review guide). Quote where you found it.
3. Otherwise `standard`.

Do not infer the level from who the author seems to be. If the user's wording mixes
signals ("be gentle but it is going to OE-Core"), use gentle tone and filtering but still
report every upstream-blocking rule as at least **minor**, and say that strict review is
advisable before sending.

Always print the chosen level, and the reason if it came from the repository.

## 4. Context modifiers: upstream vs product layers

The same change is judged against different rules depending on where it goes:

| Target | Rules that apply in full | Rules that relax |
|---|---|---|
| OE-Core, BitBake, meta-poky, meta-yocto-bsp | everything in commit-and-patch-rules.md, style guide, patchtest | none |
| meta-openembedded and other community layers | same, plus the layer README's own rules (subject prefix such as `meta-oe][PATCH`) | none |
| Stable branch (e.g. `scarthgap`) | stable-branch policy: bug or CVE fixes only, already in master where possible, small and isolated | feature or upgrade changes are out of scope: blocker for the branch |
| Product / company layer | correctness, effects, security, license, reproducibility, the repo's own commit rules | mailing-list mechanics; `Upstream-Status` still matters for maintainability (the `patch-status` QA check applies wherever it is in `ERROR_QA`/`WARN_QA`) |

## 5. Tone rules

Apply at every level:

1. **Comment on the code, not the developer.** "This `:append` has no leading space, so
   ..." not "You forgot the space".
2. **Explain why.** State the concrete effect in the build ("`IMAGE_INSTALL` becomes
   `...packagegroup-basestrace`, and do_rootfs fails to find that package"), then cite
   the manual.
3. **Offer a fix.** Minimal replacement metadata, or a command to find the right value
   (e.g. build once to get the checksum the error reports).
4. **Separate must from may.** Severity labels do this; do not phrase a nit as a demand.
5. **Ask when intent is unclear.** Overriding a distro default, pinning an old version
   or skipping a QA check may be deliberate. Ask, and say what would make it acceptable
   (a comment, a narrow override, an upstream link).
6. **No sarcasm, no "obviously", "just", "simply", no rhetorical questions.**
7. **Acknowledge constraints.** If the author works on an old vendor BSP that pins a
   release, say what is release-specific.
8. **Be brief.** One finding per root cause; do not repeat the same issue for every
   line it appears on; give the count and the lines.

## 6. Confidence labels

Every finding carries one label:

- `verified` - shown by command output in this session (`bitbake-getvar`, `bitbake -e`,
  `bitbake -S printdiff`, a QA error from a build, `yocto-check-layer`, `patchtest`).
  Name the command in "Verification run".
- `reasoned` - follows from the diff, the surrounding files you read, and the manual.
  This is the normal label when no build directory is available.

Something you suspect but cannot support goes under "Questions for the author", not in
Findings. Do not use "probably" inside a finding; move it to a question instead.

## 7. False-positive guards

Before reporting, check each of these:

- **Is the "missing" thing set elsewhere?** Look in `require`/`include` files, inherited
  classes, the base recipe of a bbappend, other bbappends, distro and machine conf.
  Example: a bbappend need not repeat `LICENSE`.
- **Underscore names that are not overrides.** `BBFILE_PATTERN_<collection>`,
  `BBFILE_PRIORITY_<collection>`, `LAYERDEPENDS_<collection>`,
  `LAYERSERIES_COMPAT_<collection>`, `LAYERVERSION_<collection>`, `SRCREV_<name>`,
  `PREFERRED_VERSION_<recipe>`, `PREFERRED_PROVIDER_<target>` use `_` by design
  (migration-guides/migration-3.4.md, "Override syntax changes").
- **Classes set defaults.** `FILES:${PN}-dev`, `PACKAGES`, `S` for some fetchers, and
  `do_install` for build-system classes come from classes; absence in the recipe is not a
  bug.
- **`+=` is fine in the recipe that owns the variable** and in a bbappend for variables
  the recipe sets with `=`. The `+=` vs `:append` problem appears when a later `?=`/`=`
  or an earlier weak default is involved (see change-effects.md section 1).
- **Release.** Do not flag syntax or variables valid in the target release. scarthgap
  uses `S = "${WORKDIR}/git"` for git sources; `UNPACKDIR` does not exist there
  *[release-specific]*.
- **Generated or vendored content.** Patches copied verbatim from upstream keep
  upstream style; review only their header (Upstream-Status, CVE, Signed-off-by).
- **QA check names and defaults.** Confirm the check exists in the scarthgap list
  (ref-manual/qa-checks.md and the `insane` class section of ref-manual/classes.md)
  and whether it is in `ERROR_QA` or `WARN_QA` for the user's config before calling it a
  blocker; use `bitbake-getvar ERROR_QA` when you can.
- **Do not double-report** what a linter already reported unless you add the effect.

## 8. Verdict

- **request changes** - at least one blocker, or a major the author has not justified.
- **approve with suggestions** - only minors/nits, or majors explicitly justified.
- **approve** - nothing to report at the chosen level.

Following Google's "standard of code review": approve a change that clearly improves the
layer even if it is not perfect; do not block on personal preference that no
documented convention supports.

## 9. Practices borrowed from other review guides

- **yocto-recipe-review** (this repository): its "Findings to Prioritize" list (license,
  `AUTOREV`, `DEPENDS` vs `RDEPENDS`, `FILES`, `${D}`, host contamination,
  `INSANE_SKIP`, patch status, bbappend scope) seeds the recipe checks in
  file-type-checks.md. For a newly added recipe, run its checklist on the whole file.
- **yocto-layer-review** (this repository): "prove whether BitBake sees the metadata
  first" became the `bitbake-layers show-appends` / `show-overlayed` verification step,
  and its layer checklist is used for new or changed `layer.conf` files.
- **Google engineering practices, "How to write code review comments"**
  (https://google.github.io/eng-practices/review/reviewer/comments.html): comment on the
  code not the developer, explain why, label severity ("Nit:"), balance giving
  direction with letting the author decide. **"The Standard of Code Review"**
  (https://google.github.io/eng-practices/review/reviewer/standard.html): approve when
  code health improves; no perfection gate.
- **Conventional Comments** (https://conventionalcomments.org/): explicit labels and
  blocking/non-blocking decoration, adapted here as blocker/major/minor/nit plus
  "Questions for the author".
- **Yocto Project contributor guide** (contributor-guide/submit-changes.md): "review is
  made by many eyes" and the "Taking Patch Review into Account" section - feedback is
  addressed by reworking the series, not by fix-up commits on top.
- **General code-review discipline** (the `code-review` approach used by agent review
  tools): read the full file around a hunk, verify before reporting, one finding per
  root cause, rank by severity, and prefer few high-confidence findings over many
  speculative ones.

Derived from the Yocto Project scarthgap (5.0) documentation, CC BY-SA 2.0 UK.
