
import os

import pytest

from envycontrol import (CACHE_FILE_PATH, MODESET_PATH, UDEV_PM_PATH,
                         get_current_mode)


@pytest.mark.hybrid
def test_mode_is_hybrid():
    curr_mode = get_current_mode()
    assert 'hybrid' == curr_mode


@pytest.fixture
def hybrid_files() -> list[str]:
    return [
        MODESET_PATH,
        UDEV_PM_PATH,
        CACHE_FILE_PATH,
    ]


@pytest.mark.hybrid
def test_hybrid_should_remove_expected(files_to_remove: list[str], hybrid_files: list[str]) -> None:
    expected_to_remove = [f for f in files_to_remove if f not in hybrid_files]

    for f in expected_to_remove:
        assert not os.path.exists(f)


@pytest.mark.hybrid
def test_hybrid_should_create_expected(hybrid_files: list[str]) -> None:

    rc = [*map(lambda f: (os.path.exists(f), f), hybrid_files)]

    should_assert = False
    for r in rc:
        if not r[0]:
            print(f'ERROR: {r[1]} expected to exist')
            should_assert = True

    if should_assert:
        assert False, 'missing files'
