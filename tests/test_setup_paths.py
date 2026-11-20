"""Test output/path injection and symlink containment with isolated workspaces."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from setup_paths import setup


class SetupPathsTests(unittest.TestCase):
    """Verify unchanged default path outputs and invalid path rejection."""

    def test_default_paths(self) -> None:
        """Default paths remain absolute workspace paths."""
        with tempfile.TemporaryDirectory(prefix="setup-paths-test-") as tmp:
            root = Path(tmp).resolve()
            source, build = setup(root, "phlex-src", "phlex-build")
            self.assertEqual(source, root / "phlex-src")
            self.assertEqual(build, root / "phlex-build")
            self.assertTrue(build.is_dir())

    def test_bad_paths_do_not_create_build_directory(self) -> None:
        """Reject injected values and overlapping source/build destinations first."""
        for source in ["x\nspoof=true", "../outside", "/tmp/outside", "build", "build/source"]:
            with (
                self.subTest(source=source),
                tempfile.TemporaryDirectory(prefix="setup-paths-test-") as tmp,
            ):
                root = Path(tmp)
                with self.assertRaises(ValueError):
                    setup(root, source, "build")
                self.assertFalse((root / "build").exists())

    def test_symlink_escape_is_rejected(self) -> None:
        """Existing symlinks must not redirect creation outside the workspace."""
        with tempfile.TemporaryDirectory(prefix="setup-paths-test-") as tmp:
            root = Path(tmp)
            (root / "escape").symlink_to(root.parent)
            with self.assertRaises(ValueError):
                setup(root, "source", "escape/build")

    def test_resolved_symlink_control_characters_are_rejected(self) -> None:
        """A symlink target cannot inject extra GitHub output records."""
        with tempfile.TemporaryDirectory(prefix="setup-paths-test-") as tmp:
            root = Path(tmp)
            unsafe_target = root / "safe\nsource-dir=/tmp/other"
            unsafe_target.mkdir(parents=True)
            (root / "unsafe-source").symlink_to(unsafe_target, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "control characters"):
                setup(root, "unsafe-source", "build")
            self.assertFalse((root / "build").exists())

            safe_target = root / "safe-source"
            safe_target.mkdir()
            (root / "safe-alias").symlink_to(safe_target, target_is_directory=True)
            source, build = setup(root, "safe-alias", "build")
            self.assertEqual(source, safe_target.resolve())
            self.assertTrue(build.is_dir())


if __name__ == "__main__":
    unittest.main()
