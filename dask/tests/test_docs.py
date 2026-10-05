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

    path = root_dir / filename
    if not path.exists():
        pytest.skip(f"{filename} is not present in this checkout")

    latest_env = "environment-3.12.yaml"
    with open(path, encoding="utf8") as f:
        assert latest_env in f.read()
