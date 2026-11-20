"""Resolve contained build paths before creating directories or publishing outputs."""

from __future__ import annotations

import os
from pathlib import Path


def contained_path(root: Path, value: str) -> Path:
    """Reject ambiguous, injected, or escaping workspace-relative paths."""
    if (
        not value
        or Path(value).is_absolute()
        or any(part in {"", ".", ".."} for part in value.split("/"))
        or "\\" in value
        or any(ord(char) < 32 or ord(char) == 127 for char in value)
    ):
        raise ValueError("Expected a nonempty workspace-relative path without traversal")
    candidate = (root / value).resolve()
    if any(ord(char) < 32 or ord(char) == 127 for char in str(candidate)):
        raise ValueError("Resolved path contains control characters")
    if candidate == root or not candidate.is_relative_to(root):
        raise ValueError("Path escapes workspace")
    return candidate


def setup(root: Path, source_value: str, build_value: str) -> tuple[Path, Path]:
    """Validate both paths before creating the build directory."""
    root = root.resolve(strict=True)
    source = contained_path(root, source_value)
    build = contained_path(root, build_value)
    if source.is_relative_to(build) or build.is_relative_to(source):
        raise ValueError("Source and build directories must not overlap")
    build.mkdir(parents=True, exist_ok=True)
    if build.resolve() != build:
        raise ValueError("Build path changed during directory creation")
    return source, build


def main() -> None:
    """Write only validated absolute paths to the GitHub output file."""
    source, build = setup(
        Path(os.environ["GITHUB_WORKSPACE"]), os.environ["SOURCE_PATH"], os.environ["BUILD_PATH"]
    )
    with Path(os.environ["GITHUB_OUTPUT"]).open("a", encoding="utf-8") as output:
        output.write(f"source-dir={source}\nbuild-dir={build}\n")


if __name__ == "__main__":
    main()
