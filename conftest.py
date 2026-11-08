from __future__ import annotations

import os
import pytest

pytest.register_assert_rewrite(
    "dask.array.utils", "dask.dataframe.utils", "dask.bag.utils"
)

# The doctests in these files fail due to either:
# - Non-required dependencies not being installed
# - Imported doctests due to pulling the docstrings from other packages
#   (e.g. `numpy`). No need to run these doctests.
collect_ignore = [
    "dask/bytes/hdfs3.py",
    "dask/bytes/pyarrow.py",
    "dask/bytes/s3.py",
    "dask/array/ghost.py",
    "dask/array/fft.py",
    "dask/dataframe/io/io.py",
    "dask/dataframe/io/parquet/arrow.py",
    "dask/dot.py",
    "dask/ml.py",
]

collect_ignore_glob = []
try:
    import numpy  # noqa: F401
except ImportError:
    collect_ignore_glob.append("dask/array/*")

try:
    import pandas  # noqa: F401
except ImportError:
    collect_ignore_glob.append("dask/dataframe/*")

try:
    import scipy  # noqa: F401
except ImportError:
    collect_ignore.append("dask/array/stats.py")

try:
    import pyarrow  # noqa: F401
except ImportError:
    collect_ignore.append("dask/dataframe/io/orc/arrow.py")

try:
    import tiledb  # noqa: F401
except ImportError:
    collect_ignore.append("dask/array/tiledb_io.py")

try:
    import sqlalchemy  # noqa: F401
except ImportError:
    collect_ignore.append("dask/dataframe/io/sql.py")


def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true", help="run slow tests")
    parser.addoption("--runarrayexpr", action="store_true", help="run array-expr tests")
    parser.addoption("--run-network", action="store_true", help="run network tests")


def pytest_runtest_setup(item):
    if "slow" in item.keywords and not item.config.getoption("--runslow"):
        pytest.skip("need --runslow option to run")
    if "array_expr" in item.keywords and not item.config.getoption("--runarrayexpr"):
        pytest.skip("need --runarrayexpr option to run")
    elif "array_expr" not in item.keywords and item.config.getoption("--runarrayexpr"):
        if "normal_and_array_expr" not in item.keywords:
            pytest.skip("only array-expr tests are being run")
    # Skip network tests if offline mode is enforced via HF_HUB_OFFLINE or TRANSFORMERS_OFFLINE
    # This takes precedence over --run-network or RUN_NETWORK_TESTS
    if "network" in item.keywords:
        # Check for offline mode environment variables first
        if os.environ.get("HF_HUB_OFFLINE") == "1" or os.environ.get("TRANSFORMERS_OFFLINE") == "1":
            pytest.skip("Offline mode is enforced (HF_HUB_OFFLINE=1 or TRANSFORMERS_OFFLINE=1)")
        # Skip network tests unless --run-network is passed or RUN_NETWORK_TESTS env var is set
        if not item.config.getoption("--run-network"):
            if not os.environ.get("RUN_NETWORK_TESTS"):
                pytest.skip("need --run-network option or RUN_NETWORK_TESTS env var to run")


def pytest_assertrepr_compare(op, left, right):
    import difflib

    from dask._task_spec import Task

    if isinstance(left, Task) and isinstance(right, Task):

        def _get_attrs(node):
            return (
                [
                    str(node.func),
                ]
                + sorted([str(a) for a in node.args])
                + sorted([f"{k}: {v}" for k, v in node.kwargs.items()])
            )

        diff = list(
            difflib.ndiff(
                _get_attrs(left),
                _get_attrs(right),
            )
        )
        return [
            "Comparing two dask graph nodes:",
            f" left: {left.key} right: {right.key}",
            " Diff:",
        ] + diff


@pytest.fixture(autouse=True, scope="session")
def allow_distributed_async_clients():
    import dask

    with dask.config.set({"admin.async-client-fallback": "sync"}):
        yield
