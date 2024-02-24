
import os

import pytest

from envycontrol import (BLACKLIST_PATH, CACHE_FILE_PATH, UDEV_INTEGRATED_PATH,
                         get_current_mode)


@pytest.mark.integrated
def test_mode_is_integrated():
    curr_mode = get_current_mode()
    assert 'integrated' == curr_mode


@pytest.fixture
def integrated_files() -> list[str]:
    return [
        BLACKLIST_PATH,
        UDEV_INTEGRATED_PATH,
        CACHE_FILE_PATH,
    ]


@pytest.mark.integrated
def test_integrated_should_remove_expected(files_to_remove: list[str], integrated_files: list[str]) -> None:
    expected_to_remove = [f for f in files_to_remove if f not in integrated_files]

    for f in expected_to_remove:
        assert not os.path.exists(f)


@pytest.mark.integrated
def test_integrated_should_create_expected(integrated_files: list[str]) -> None:

    rc = [*map(lambda f: (os.path.exists(f), f), integrated_files)]

    should_assert = False
    for r in rc:
        if not r[0]:
            print(f'ERROR: {r[1]} expected to exist')
            should_assert = True

    if should_assert:
        assert False, 'missing files'
