from __future__ import annotations

from pathlib import Path

import pytest


@pytest.mark.parametrize(
    "filename",
    [
        "docs/source/develop.rst",
        ".github/workflows/additional.yml",
        ".github/workflows/upstream.yml",
    ],
)
def test_development_guidelines_matches_ci(filename):
    """When the environment.yaml changes in CI, make sure to change it in the docs as well"""
    root_dir = Path(__file__).parent.parent.parent

    if not (root_dir / ".github" / "workflows").exists():
        pytest.skip("Test can only be run on an editable install")

    # Check if the file exists before trying to open it
    file_path = root_dir / filename
    if not file_path.exists():
        pytest.skip(f"File {filename} does not exist in this environment")

    latest_env = "environment-3.12.yaml"
    with open(file_path, encoding="utf8") as f:
        assert latest_env in f.read()
