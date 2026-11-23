---
name: bitbake-debug
description: Diagnose failing or surprising Yocto/BitBake builds from evidence - parse errors, do_fetch/do_unpack/do_patch/do_configure/do_compile/do_install/do_package/do_package_qa failures, "Nothing PROVIDES", dangling bbappend errors, QA Issue messages seen while building, host contamination, and "why did this rebuild / why did my change do nothing" questions about sstate, task signatures and hash equivalence (bitbake-getvar, bitbake-dumpsig, bitbake-diffsigs, bitbake -S printdiff). Use it whenever someone pastes BitBake output, an ERROR line, a log.do_* or run.do_* file from tmp/work, or asks how to find out why a Yocto build broke, even if they do not say "debug". Targets Yocto 5.0 scarthgap / BitBake 2.8. Hand off do_rootfs and image content problems to yocto-image-rootfs, kernel config and devicetree problems to yocto-bsp-kernel, and license/CVE/SBOM failures to yocto-security-sbom; not for generic Linux, Buildroot or Debian packaging problems.
---

# BitBake Debug

Diagnose from evidence, not from memory. The first failing task and its first error decide everything; the final "Summary: 1 task failed" line does not.

## Workflow

1. **Find the first failure.** Get the failing recipe, task and the first `ERROR:` line. If only the summary was pasted, ask for `tmp/work/<arch>/<pn>/<pv>/temp/log.do_<task>` (or `tmp/log/cooker/<machine>/console-latest.log`).
2. **Classify it.** Parse error (before any task runs), fetch/unpack/patch, configure/compile (usually a missing `DEPENDS` or host contamination), install, package/QA, sstate/signature, or a hand-off (rootfs, kernel, license).
3. **Collect values, not guesses.** Use the agent-safe commands below; `bitbake-getvar` shows the final value and every assignment that produced it.
4. **Apply the playbook** for that task in [references/yocto-field-guide.md](references/yocto-field-guide.md) (section 4); for QA tags use [references/qa-errors.md](references/qa-errors.md).
5. **Propose the smallest metadata fix** in the right layer (bbappend or recipe), explain it in BitBake terms, and give the validation command.

```bash
bitbake-getvar -r <recipe> SRC_URI          # any variable, with history
bitbake-getvar -r <recipe> do_install       # final shell task body
bitbake-layers show-recipes <pn>
bitbake-layers show-appends
bitbake -c listtasks <recipe>
bitbake -n <target>                         # dry run
bitbake -k <target>                         # keep going, collect every failure (builds)
grep -n -E 'ERROR|error:|QA Issue' tmp/work/*/<pn>/*/temp/log.do_<task>
```

Do not run interactive commands (`bitbake -c devshell`, `menuconfig`, `bitbake -e | less`): read `run.do_<task>` and rerun the task with `bitbake -f -c <task> <recipe>` instead. Do not run destructive commands (`cleansstate`, `cleanall`, deleting `tmp/` or `sstate-cache/`) without asking; prefer `bitbake -f` (see the clean table in the field guide).

## Rebuild and Signature Questions

"It rebuilt everything", "my change is ignored", "sstate is not reused": compare task signatures with `bitbake -S printdiff <target>`, `bitbake-dumpsig <sigdata>`, `bitbake-diffsigs <old> <new>`, and check for a devtool workspace or an append shadowing the recipe. Details and the `vardeps`/`vardepsexclude` fixes are in [references/debug-tools.md](references/debug-tools.md).

## References

- [references/yocto-field-guide.md](references/yocto-field-guide.md): per-task playbook, parse errors, clean commands, red flags.
- [references/qa-errors.md](references/qa-errors.md): every scarthgap QA check with its message and fix.
- [references/tasks-reference.md](references/tasks-reference.md): task chain, dependency flags, where outputs live.
- [references/variables-core.md](references/variables-core.md): operators, override ordering, key variables.
- [references/debug-tools.md](references/debug-tools.md): inspection commands, sstate/signatures, devtool, buildhistory.
- [references/keywords.md](references/keywords.md): the official scarthgap manual entry for every keyword this skill names; grep for `` ## Variable `NAME` `` (or `Class`, `Task`, `QA check`). For anything else use the `yocto-manuals` skill.

## Output

1. most likely cause, with the log line that shows it
2. evidence still needed (if any) and the exact command to get it
3. the metadata change or command
4. why it is the Yocto fix (which variable, task or class behavior)
5. validation command (`bitbake -c <task> <recipe>`, then `bitbake <target>`)
