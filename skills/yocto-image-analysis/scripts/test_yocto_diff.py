#!/usr/bin/env python3
"""Tests for yocto_diff.py. Run: python3 -m unittest test_yocto_diff (from this folder)."""

from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yocto_diff  # noqa: E402

# Shaped like real `bitbake -e core-image-minimal` output (BitBake 2.8), trimmed.
ENV_OLD = '''# $DISTRO_FEATURES [3 operations]
#   set? /home/user/poky/meta-poky/conf/distro/poky.conf:21
#     "${DISTRO_FEATURES_DEFAULT} ${POKY_DEFAULT_DISTRO_FEATURES}"
#   set? /home/user/poky/meta/conf/bitbake.conf:950
#     ""
#   append base.bbclass:414 [features_backfill]
#     " pulseaudio sysvinit gobject-introspection-data ldconfig"
# pre-expansion value:
#   "${DISTRO_FEATURES_DEFAULT} ${POKY_DEFAULT_DISTRO_FEATURES} pulseaudio sysvinit gobject-introspection-data ldconfig"
DISTRO_FEATURES="acl alsa x11 opengl pulseaudio sysvinit gobject-introspection-data ldconfig"
#
# $IMAGE_INSTALL
#   set /home/user/poky/meta/recipes-core/images/core-image-minimal.bb:3
#     "packagegroup-core-boot ${CORE_IMAGE_EXTRA_INSTALL}"
IMAGE_INSTALL="packagegroup-core-boot "
#
# $DATETIME
DATETIME="20240101120000"
export CC="gcc \\$FOO"
MULTI="line one \\
line two"
do_something() {
    FAKE="not a variable"
}
python do_other () {
    X="also not a variable"
}
'''

ENV_NEW = '''# $DISTRO_FEATURES [4 operations]
#   set? /home/user/poky/meta-poky/conf/distro/poky.conf:21
#     "${DISTRO_FEATURES_DEFAULT} ${POKY_DEFAULT_DISTRO_FEATURES}"
#   :remove /home/user/meta-company/conf/distro/company.conf:7
#     "x11"
#   set? /home/user/poky/meta/conf/bitbake.conf:950
#     ""
#   append base.bbclass:414 [features_backfill]
#     " pulseaudio sysvinit gobject-introspection-data ldconfig"
# pre-expansion value:
#   "${DISTRO_FEATURES_DEFAULT} ${POKY_DEFAULT_DISTRO_FEATURES} pulseaudio sysvinit gobject-introspection-data ldconfig"
DISTRO_FEATURES="acl alsa opengl pulseaudio sysvinit gobject-introspection-data ldconfig"
#
# $IMAGE_INSTALL [2 operations]
#   set /home/user/poky/meta/recipes-core/images/core-image-minimal.bb:3
#     "packagegroup-core-boot ${CORE_IMAGE_EXTRA_INSTALL}"
#   :append /home/user/build/conf/local.conf:300
#     " htop"
# pre-expansion value:
#   "packagegroup-core-boot ${CORE_IMAGE_EXTRA_INSTALL}"
IMAGE_INSTALL="packagegroup-core-boot  htop"
#
# $DATETIME
DATETIME="20240202120000"
export CC="gcc \\$FOO"
MULTI="line one \\
line three"
NEWVAR="hello \\"world\\""
'''

MANIFEST_OLD = """busybox core2_64 1.36.1
base-files qemux86_64 3.0.14
libc6 core2_64 2.39+git0+abc
"""

MANIFEST_NEW = """busybox core2_64 1.36.1
base-files qemux86_64 3.0.14
libc6 core2_64 2.39+git0+def
htop core2_64 3.3.0
"""

DOT = '''digraph depends {
    node [shape=plaintext]
"busybox" -> "libc6"
"htop" -> "libc6"
"htop" -> "ncurses-libtinfo"
"htop" -> "ncurses-terminfo-base" [style=dotted]
"ncurses-libtinfo" -> "libc6"
"packagegroup-core-boot" -> "busybox"
"packagegroup-core-boot" -> "base-files"
"packagegroup-core-boot" -> "libc6" [label=">= 2.39"]
"run-postinsts" -> "libc6" [style=dashed]
}
'''


class ManifestTests(unittest.TestCase):
    def test_diff(self):
        result = yocto_diff.diff_manifests(yocto_diff.parse_package_list(MANIFEST_OLD),
                                           yocto_diff.parse_package_list(MANIFEST_NEW))
        self.assertEqual([a["package"] for a in result["added"]], ["htop"])
        self.assertEqual(result["removed"], [])
        self.assertEqual(result["changed"][0]["package"], "libc6")
        self.assertEqual(result["changed"][0]["new_version"], "2.39+git0+def")

    def test_names_only_list(self):
        old = yocto_diff.parse_package_list("a\nb\n")
        new = yocto_diff.parse_package_list("b\nc\n")
        result = yocto_diff.diff_manifests(old, new)
        self.assertEqual([x["package"] for x in result["added"]], ["c"])
        self.assertEqual([x["package"] for x in result["removed"]], ["a"])


class EnvTests(unittest.TestCase):
    def test_parse_values(self):
        values, history = yocto_diff.parse_env(ENV_NEW)
        self.assertEqual(values["CC"], "gcc $FOO")
        self.assertEqual(values["MULTI"], "line one\nline three")
        self.assertEqual(values["NEWVAR"], 'hello "world"')
        self.assertNotIn("FAKE", values)
        self.assertNotIn("X", values)
        ops = [h["op"] for h in history["DISTRO_FEATURES"]]
        self.assertEqual(ops, ["set?", ":remove", "set?", "append"])
        self.assertEqual(history["DISTRO_FEATURES"][3]["func"], "features_backfill")

    def test_diff(self):
        result = yocto_diff.diff_env(ENV_OLD, ENV_NEW, None, None, 5)
        by_name = {c["variable"]: c for c in result["changes"]}
        self.assertNotIn("DATETIME", by_name)  # volatile, ignored by default
        self.assertNotIn("CC", by_name)
        self.assertEqual(by_name["DISTRO_FEATURES"]["words_removed"], ["x11"])
        self.assertEqual(by_name["IMAGE_INSTALL"]["words_added"], ["htop"])
        last = by_name["IMAGE_INSTALL"]["history"][-1]
        self.assertEqual((last["op"], last["file"].rsplit("/", 1)[-1], last["line"]),
                         (":append", "local.conf", "300"))
        self.assertIsNone(by_name["NEWVAR"]["old"])
        self.assertIn("MULTI", by_name)

    def test_only_filter(self):
        result = yocto_diff.diff_env(ENV_OLD, ENV_NEW, "^IMAGE_", None, 3)
        self.assertEqual([c["variable"] for c in result["changes"]], ["IMAGE_INSTALL"])


class WhyTests(unittest.TestCase):
    def test_chains(self):
        reverse = yocto_diff.parse_depends_dot(DOT)
        chains = yocto_diff.why_chains(reverse, "ncurses-terminfo-base", 5)
        self.assertEqual(yocto_diff.format_chain(chains[0]), "htop ~> ncurses-terminfo-base")
        libc = [yocto_diff.format_chain(c) for c in yocto_diff.why_chains(reverse, "libc6", 10)]
        self.assertIn("packagegroup-core-boot -> libc6", libc)
        self.assertIn("run-postinsts => libc6", libc)
        self.assertIn("htop -> ncurses-libtinfo -> libc6", libc)

    def test_missing(self):
        reverse = yocto_diff.parse_depends_dot(DOT)
        self.assertEqual(yocto_diff.why_chains(reverse, "openssh", 5), [])


class CliTests(unittest.TestCase):
    def run_cli(self, *args):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = yocto_diff.main(list(args))
        return code, buf.getvalue()

    def test_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            (t / "a.manifest").write_text(MANIFEST_OLD)
            (t / "b.manifest").write_text(MANIFEST_NEW)
            (t / "a.env").write_text(ENV_OLD)
            (t / "b.env").write_text(ENV_NEW)
            (t / "depends.dot").write_text(DOT)
            code, out = self.run_cli("manifest", str(t / "a.manifest"), str(t / "b.manifest"))
            self.assertEqual(code, 1)
            self.assertIn("+ htop", out)
            code, out = self.run_cli("manifest", str(t / "a.manifest"), str(t / "a.manifest"))
            self.assertEqual(code, 0)
            code, out = self.run_cli("env", str(t / "a.env"), str(t / "b.env"), "--json")
            self.assertEqual(code, 1)
            self.assertTrue(json.loads(out)["changes"])
            code, out = self.run_cli("why", str(t / "depends.dot"), "ncurses-libtinfo")
            self.assertEqual(code, 1)
            self.assertIn("htop -> ncurses-libtinfo", out)


if __name__ == "__main__":
    unittest.main()
