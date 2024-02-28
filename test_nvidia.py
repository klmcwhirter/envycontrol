
import os

import pytest

from envycontrol import (CACHE_FILE_PATH, EXTRA_XORG_PATH, LIGHTDM_CONFIG_PATH,
                         LIGHTDM_SCRIPT_PATH, MODESET_PATH, SDDM_XSETUP_PATH,
                         XORG_PATH, get_current_mode)


@pytest.mark.nvidia
def test_mode_is_nvidia() -> None:
    curr_mode = get_current_mode()
    assert 'nvidia' == curr_mode


@pytest.fixture
def nvidia_files():
    def wrapper(dm: str) -> list[str]:
        rc = [
            EXTRA_XORG_PATH,
            MODESET_PATH,
            XORG_PATH,
            CACHE_FILE_PATH,
        ]
        if dm == 'sddm':
            rc.append(SDDM_XSETUP_PATH)
        elif dm == 'lightdm':
            rc.append(LIGHTDM_SCRIPT_PATH)
            rc.append(LIGHTDM_CONFIG_PATH)
        return rc
    return wrapper


@pytest.mark.nvidia
def test_nvidia_should_remove_expected(files_to_remove: list[str], nvidia_files, display_manager) -> None:
    expected_to_remove = [f for f in files_to_remove if f not in nvidia_files(display_manager)]

    for f in expected_to_remove:
        assert not os.path.exists(f)


@pytest.mark.nvidia
def test_nvidia_should_create_expected(nvidia_files, display_manager) -> None:

    rc = [*map(lambda f: (os.path.exists(f), f), nvidia_files(display_manager))]

    should_assert = False
    for r in rc:
        if not r[0]:
            print(f'ERROR: {r[1]} expected to exist')
            should_assert = True

    if should_assert:
        assert False, 'missing files'
