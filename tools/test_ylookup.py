"""Tests for the offline lookup script, run against a generated skill copy.

    python -m unittest discover -s tools -p "test_*.py"
"""

import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "skills" / "yocto-image-rootfs" / "scripts" / "ylookup.py"


def run(*args):
    out = subprocess.run([sys.executable, "-I", str(SCRIPT), *args],
                         capture_output=True, text=True, timeout=60)
    return out.returncode, out.stdout


class LookupTest(unittest.TestCase):
    def test_variable_from_skill_glossary(self):
        code, out = run("IMAGE_INSTALL", "--max-lines", "0")
        self.assertEqual(code, 0)
        self.assertIn("## Variable `IMAGE_INSTALL`", out)
        self.assertIn("PACKAGE_INSTALL", out)
        self.assertIn("Offline source: yocto-manuals/references/manuals/ref-manual/variables.md", out)

    def test_keyword_outside_glossary_uses_full_manuals(self):
        code, out = run("BB_DANGLINGAPPENDS_WARNONLY", "--max-lines", "0")
        self.assertEqual(code, 0)
        self.assertIn("Variable `BB_DANGLINGAPPENDS_WARNONLY`", out)

    def test_kinds_and_clipping(self):
        code, out = run("do_rootfs", "image:read-only-rootfs", "installed-vs-shipped", "--max-lines", "2")
        self.assertEqual(code, 0)
        self.assertIn("Task `do_rootfs`", out)
        self.assertIn("Feature `image:read-only-rootfs`", out)
        self.assertIn("QA check `installed-vs-shipped`", out)
        self.assertIn("more lines", out)

    def test_unknown_keyword_fails(self):
        code, out = run("NO_SUCH_VARIABLE_XYZ")
        self.assertEqual(code, 1)
        self.assertIn("not found", out)

    def test_find_topic_section_grep(self):
        self.assertIn("BAD_RECOMMENDATIONS", run("--find", "recommended-only")[1])
        self.assertIn("dev-manual/read-only-rootfs.md", run("--topic", "read-only root")[1])
        code, out = run("--section", "dev-manual/read-only-rootfs.md", "Creating the Root Filesystem")
        self.assertEqual(code, 0)
        self.assertIn('IMAGE_FEATURES += "read-only-rootfs"', out)
        self.assertIn("ref-manual/variables.md", run("--grep", "BB_DANGLINGAPPENDS", "--in", "ref-manual")[1])


if __name__ == "__main__":
    unittest.main()
