from __future__ import annotations

try:
    import pyarrow
    from packaging.version import Version

    def check_minimal_arrow_version() -> None:
        """Check if the installed pyarrow version meets the minimum requirements."""
        min_version = Version("14.0.1")
        current_version = Version(pyarrow.__version__)
        if current_version < min_version:
            raise ImportError(
                f"pyarrow {min_version} or greater is required, but {current_version} is installed."
            )
except ImportError:
    def check_minimal_arrow_version() -> None:
        """Check if pyarrow is installed."""
        try:
            import pyarrow
        except ImportError:
            raise ImportError("pyarrow is required but not installed.")

__all__ = [
    "check_minimal_arrow_version",
]
