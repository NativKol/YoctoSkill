# YoctoSkill

Manual-grounded Yocto Project and BitBake skills for AI coding agents, targeting
**Yocto Project 5.0 "scarthgap" (LTS) with BitBake 2.8**.

This is a fork of [Higangssh/yocto-agent-skills](https://github.com/Higangssh/yocto-agent-skills)
(MIT, v0.3.0). It keeps the upstream history, tooling and skill split, and changes three
things:

1. **The official manuals are included.** The `yocto-manuals` skill carries the scarthgap
   manuals and the BitBake 2.8 User Manual as Markdown. Each variable, class, task,
   feature and QA check has its own file, and every other skill ships a generated
   `references/keywords.md` with the verbatim manual entry for each keyword it uses. An
   agent can look up the exact behavior of anything a skill mentions without leaving the
   skill folder.
2. **Fixes.** The upstream references had factual errors: the `+=` spacing rule, the
   `PREFERRED_VERSION:` form, a class name that doesn't exist, invented QA tags, and the
   "silently ignored" bbappend claim. They also had broken grep patterns, interactive or
   destructive commands offered as evidence gathering, and thin references. These were
   checked against the manuals and corrected.
3. **Two new skills:** `yocto-image-analysis`, for what an image or distro really contains
   and what a commit changed in it, and `yocto-change-review`, for automated review of
   Yocto changes with a strictness setting.

## Skills

- `skills/yocto-manuals`: offline scarthgap manuals split per keyword (880 variables, 166 classes, 50 tasks, 99 features, 46 QA checks) plus every manual page, with an index and a table of contents.
- `skills/yocto-image-analysis`: walks the evaluation order (layers, local/auto.conf, distro, machine, image recipe, bbappends, overrides) and the inclusion chain (`IMAGE_INSTALL`, `IMAGE_FEATURES`, packagegroups, `RDEPENDS`/`RRECOMMENDS`, exclusions, providers) to explain what ends up in an image and what a commit changed in it. Includes `scripts/yocto_diff.py` to diff manifests, `bitbake -e` dumps and buildhistory dependency chains.
- `skills/yocto-change-review`: automated review of diffs, commits, PRs and patch series. It covers effects (operators, overrides, dependencies, features, sstate blast radius, QA checks) and conventions (style guide, licensing, `Upstream-Status`, commit messages), and has `gentle`, `standard` and `strict` levels.
- `skills/yocto-doc-router`: release-aware routing to the right Yocto, OpenEmbedded and BitBake documentation.
- `skills/bitbake-debug`: debugging BitBake failures from task logs, rootfs, package and provider errors.
- `skills/yocto-recipe-review`: review of recipes, bbappends, bbclasses, dependencies, packaging, licensing and override syntax.
- `skills/yocto-layer-review`: review of `layer.conf`, compatibility, priority, dependencies, providers and bbappend matching.
- `skills/yocto-image-rootfs`: image recipes, package names, `IMAGE_INSTALL`, `IMAGE_FEATURES`, `do_rootfs`, pkgdata and package manager failures.
- `skills/yocto-bsp-kernel`: machine config, BSP layers, kernel providers, devicetree, defconfig, U-Boot and deploy artifacts.
- `skills/yocto-security-sbom`: license metadata, CVE handling, SPDX/SBOM, archiver and copyleft flows, and compliance artifacts.

The root `SKILL.md` is a compatibility router for hosts that install the whole repository
as one skill.

## Release

Everything is written for scarthgap (5.0). Each skill tells the agent to check the
project's release first (`LAYERSERIES_COMPAT_*`, the poky or openembedded-core branch,
`DISTRO_VERSION`) and to flag anything that may differ on another release. To move to
another release, regenerate the manuals (see Development) and review the facts marked as
release-specific.

## Installation

Every skill folder is self-contained, so a skill works when its folder is installed on
its own.

### Claude Code

The repository is a Claude Code plugin:

```bash
/plugin marketplace add NativKol/YoctoSkill
/plugin install yocto-skill@yoctoskill
```

Or try it without installing: `claude --plugin-dir /path/to/YoctoSkill`.

### Individual skill folders

```bash
mkdir -p ~/.claude/skills
for skill in skills/*/; do ln -s "$(pwd)/$skill" ~/.claude/skills/"$(basename "$skill")"; done
```

Use the same loop with `${CODEX_HOME:-$HOME/.codex}/skills` for Codex.

## Example prompts

```text
What does our image actually install, and why is busybox-syslog in it?
```

```text
This commit switched INIT_MANAGER to systemd. What changed in core-image-base?
```

```text
Review this patch series for meta-company. Be gentle, it's their first contribution.
```

```text
Review my diff to the distro conf at strict level.
```

```text
Why does do_rootfs fail with "nothing provides" for my package?
```

## Contents

- `skills/*/SKILL.md`: the skills
- `skills/*/keywords.txt`: the keywords each skill relies on, turned into `references/keywords.md`
- `skills/*/references/`: skill references (shared copies are generated; see below)
- `references/`: source of truth for the shared summary references
- `tools/convert_manuals.py`: converts the docs.yoctoproject.org `singleindex.html` pages to Markdown
- `tools/build_manual_refs.py`: splits the manuals per keyword and generates each skill's `keywords.md`
- `tools/sync_references.py`: copies shared references into the skills that link them
- `tools/validate_skills.py`: frontmatter, links, drift of both generators, README catalog, manifests and disclosure scan
- `examples/`, `evals/`: worked examples and eval cases with graders
- `.claude-plugin/`: Claude Code plugin and marketplace manifests

## Development

```bash
python tools/sync_references.py      # after editing references/
python tools/build_manual_refs.py    # after editing a keywords.txt or the manuals
python tools/validate_skills.py      # must pass before every commit
```

To refresh the manuals, download `https://docs.yoctoproject.org/<release>/singleindex.html`
and `https://docs.yoctoproject.org/bitbake/<bitbake-version>/singleindex.html`. Then
run `tools/convert_manuals.py` on each, writing into `skills/yocto-manuals/references/manuals`,
and then run `tools/build_manual_refs.py`.

## License

- Code, skills and the original references: MIT (see `LICENSE`). Upstream copyright
  Sanghee Son; fork changes by the YoctoSkill contributors.
- Manual text under `skills/yocto-manuals/references/` and the generated
  `skills/*/references/keywords.md` files come from the Yocto Project documentation
  (CC BY-SA 2.0 UK) and the BitBake User Manual (CC BY 2.5). See
  `skills/yocto-manuals/LICENSE-docs.md`. Skill references that paraphrase the manuals
  say so at the bottom of the file.
