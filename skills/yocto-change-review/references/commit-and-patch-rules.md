# Commit Message, Patch Header and Series Rules

Rules for the *history* of a change: commit messages, patch files carried in `SRC_URI`,
patch series, stable-branch submissions, and the Yocto Project AI-assisted contribution
policy. Sources: contributor-guide/submit-changes.md, contributor-guide/recipe-style-guide.md
3.5.3.1 and 3.6-3.7, contributor-guide/ai-assisted-contribution-policy.md,
dev-manual/vulnerabilities.md.

These rules are written for OE-Core and Yocto Project layers. Product layers often adopt
them; apply them in full at `strict`, or when the change is going upstream, and apply the
repository's own documented rules otherwise (strictness-levels.md section 4).

## Contents

1. Commit structure
2. Commit message format
3. Trailers and tags
4. Patch files in SRC_URI (Upstream-Status, CVE, Signed-off-by)
5. Series hygiene and rerolls
6. Stable branches
7. AI-assisted contribution policy
8. Mechanical checks

## 1. Commit structure

- "Create *one Git commit per change*." Small, isolated changes "aid review, makes
  merging/rebasing easier and keeps the change history clean".
- "When you intend to add multiple new recipes, each recipe should be added in a separate
  commit." (minor at standard, major at strict for upstream)
- "For upgrades to existing recipes, the previous version should usually be deleted as
  part of the same commit to add the upgraded version." Upgrade commits that leave the
  old `.bb` behind create two providers.
- Review feedback is addressed by reworking the series: "never fix reported issues by
  fixing them in new commits on the tip of your branch." A "fix review comments" commit
  on top is a strict-level finding.

## 2. Commit message format

- **Shortlog (subject):** "a single-line summary of the change ... You should prefix this
  short description with the recipe name (if changing a recipe), or else with the short
  form path to the file being changed." Examples: `curl: upgrade 8.6.0 -> 8.7.1`,
  `conf/distro/mydistro: switch to systemd`. Find the usual prefix with
  `git log --oneline <paths>`. The manual sets no character limit; keep it short enough
  to read in a shortlog.
- **Body:** "describes what you changed, why you made the change, and the approach you
  used. It might also be helpful if you mention how you tested the change." It "can be
  left empty" when the shortlog says everything. A body that restates the diff without
  the why is a minor.
- **Bug references:** Yocto Bugzilla form `Fixes [YOCTO #<id>]` in the body.
- **License changes:** a commit that changes `LICENSE` or `LIC_FILES_CHKSUM` because
  upstream changed the license files needs `License-Update: <reason>` (recipe-style-guide
  3.5.3.1). Not needed when correcting wrong metadata.
- **CVE fixes:** mention the CVE ID in the shortlog/body; the patch file carries the
  `CVE:` tag (section 4).

## 3. Trailers and tags

- `Signed-off-by:` - added by `git commit -s`; it certifies the Developer's Certificate
  of Origin 1.1 (rights to submit under the project license, and that the contribution
  and the sign-off are public and kept indefinitely). Missing in an OE-Core-bound commit
  is a **blocker** at strict. The reviewer must not add it on the author's behalf, and an
  AI agent must never add it (section 7). Suggest `git commit --amend -s` *to the
  human*.
- `Reported-by:`, `Suggested-by:`, `Tested-by:`, `Reviewed-by:`, `Cc:` credit others;
  `Tested-by`/`Reviewed-by` are usually added by maintainers or carried unchanged into a
  reroll.
- `AI-Generated: <tool>, <model>` - required where AI-generated code or commit messages
  are contributed (section 7).
- Placeholders only in examples: `Signed-off-by: Full Name <email>`.

## 4. Patch files in SRC_URI

Each `.patch` the change adds or modifies is reviewed for its header, not for upstream's
code style.

- **Description:** "detailed information about the bug that it addresses, such as the URL
  in a bug tracking system and links to relevant mailing list archives."
- **`Upstream-Status:`** one of:
  - `Pending` - not yet submitted; "should only be used in exceptional cases if there are
    genuine obstacles to submitting a patch upstream; the reason for that should be
    included in the patch."
  - `Submitted [where]`
  - `Backport [version or commit URL]`
  - `Denied` - include the reason.
  - `Inactive-Upstream [lastcommit: when (and/or) lastrelease: when]`
  - `Inappropriate [reason]` - the only accepted reasons now are `oe specific` and
    `upstream ticket <link>`. Other reasons (`configuration`, `embedded specific`, ...)
    are a minor at standard and a major at strict.
- Missing or malformed `Upstream-Status` triggers the `patch-status` QA check
  ("Missing Upstream-Status in patch ..." / "Malformed Upstream-Status ...").
  Whether it errors depends on `ERROR_QA`; since nanbield the check can be made
  layer-specific, e.g. `ERROR_QA:layer-core:append = " patch-status"`
  (release-notes-4.3.md) *[release-specific: named `patch-status-core` /
  `patch-status-noncore` in 4.2]*.
- **`CVE:`** "patches that fix CVEs must contain a `CVE:` tag. This tag should list all
  CVEs fixed by the patch", space-separated. `cve-check` also treats a CVE ID in the
  patch file name as patched ("if multiple CVE IDs are found in the filename, only the
  last one is considered"), so a filename alone is fragile: ask for the tag.
- **`Signed-off-by:`** of the person who added the patch to the layer, and an extra
  `Signed-off-by:` by whoever later takes over upstreaming.
- The patch must apply without fuzz (`patch-fuzz`); refresh with `devtool modify` then
  `devtool finish --force-patch-refresh` and review the refreshed hunks.

Example header (from the style guide, contact details replaced):

```text
include missing sys/file.h for LOCK_EX

Upstream-Status: Backport [https://github.com/systemd/systemd/commit/ac8db36cbc26694ee94beecc8dca208ec4b5fd45]
Signed-off-by: Full Name <email>
```

## 5. Series hygiene and rerolls

- More than one commit: a cover letter describing the series is recommended
  (`git branch --edit-description`, `git format-patch --cover-letter --cover-from-description=auto`).
- Rerolls are `[PATCH v2]`, `[PATCH v3]` (`git format-patch -v2`), with a per-version
  changelog *after the `---` marker* so it does not enter history.
- Layer other than OE-Core on a shared list: subject prefix such as
  `--subject-prefix="meta-oe][PATCH"`.
- Where to send: OE-Core (`meta/`, `scripts/`) to openembedded-core; BitBake to
  bitbake-devel; meta-poky / meta-yocto-bsp to poky; docs to docs; other
  git.yoctoproject.org layers to yocto-patches; git.openembedded.org layers to
  openembedded-devel "unless specified otherwise in the layer's README".
- "Don't just edit the patch file written out by `git format-patch` and resend it" -
  retest revised changes.

## 6. Stable branches

"Changes to a stable branch must address identified bugs or CVEs"; fixes normally land in
master first and are requested as backports; direct stable patches are a "last resort"
with a subject prefix like `scarthgap][PATCH`. Large or complex changes are "unlikely to
be accepted"; EOL branches are not accepted. A feature or version-upgrade commit aimed at
a stable branch is a **blocker** for that target (unless the branch policy for that
recipe allows upgrades - ask).

## 7. AI-assisted contribution policy

Source: contributor-guide/ai-assisted-contribution-policy.md (included in the scarthgap
docs set). It covers patches, commit messages, *and review comments*.

- "**The Signed-off-by tag must never be added by an AI-agent.**" The reviewer agent
  must not add it, must not instruct another agent to add it, and must not draft a
  commit that contains it pre-filled for the human.
- Commits containing AI-generated code or AI-generated commit messages "must include the
  `AI-Generated` tag identifying the AI tool or framework and the specific AI model
  used". When reviewing a change that the author says was AI-assisted, a missing
  `AI-Generated:` tag is a finding (blocker at strict for upstream targets).
- Review comments sent to Yocto Project lists count as contributions: disclosure is
  required ("Where AI-generated output is used in emails ... disclosure is also
  required"), and "Do not act as a simple proxy between your AI-agent and the Yocto
  Project community." When the user intends to post this review upstream, end the
  report with a note that a human must validate it and that it must be marked as
  AI-generated.
- "The project will not accept automated contributions which rely completely on AI
  generation without any significant human involvement."
- Do not paste embargoed vulnerability details into third-party AI services.

## 8. Mechanical checks

- `patchtest` (OE-Core) checks formatting and required information such as
  `Signed-off-by`; it does no functional testing, supports only openembedded-core
  branches, and may report false "merge on head" failures for patches meant to apply on
  top of earlier ones in a series. Setup and use: verification.md.
- `git log --oneline <paths>` for shortlog prefixes; `git shortlog -- <file>` and
  `meta/conf/distro/include/maintainers.inc` for who maintains a recipe.

Derived from the Yocto Project scarthgap (5.0) documentation, CC BY-SA 2.0 UK.
