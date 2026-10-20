from __future__ import annotations

import warnings

import pytest

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from dask.dataframe.utils import pyarrow_strings_enabled

        convert_string = pyarrow_strings_enabled()
except (ImportError, RuntimeError, DeprecationWarning):
    convert_string = False

skip_with_pyarrow_strings = pytest.mark.skipif(
    convert_string,
    reason="No need to run with pyarrow strings",
)

xfail_with_pyarrow_strings = pytest.mark.xfail(
    convert_string,
    reason="Known failure with pyarrow strings",
)


def pytest_collection_modifyitems(config, items):
    for item in items:
        if "skip_with_pyarrow_strings" in item.keywords:
            item.add_marker(skip_with_pyarrow_strings)
        if "xfail_with_pyarrow_strings" in item.keywords:
            item.add_marker(xfail_with_pyarrow_strings)


@pytest.fixture(params=["disk", "tasks"])
def shuffle_method(request):
    import dask

    with dask.config.set({"dataframe.shuffle.method": request.param}):
        yield request.param
