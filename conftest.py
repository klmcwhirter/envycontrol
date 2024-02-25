# Detect the mode amd set default as appropriate


import os

import pytest

from envycontrol import (BLACKLIST_PATH, EXTRA_XORG_PATH, LIGHTDM_CONFIG_PATH,
                         LIGHTDM_SCRIPT_PATH, MODESET_PATH,
                         UDEV_INTEGRATED_PATH, UDEV_PM_PATH, XORG_PATH,
                         get_current_mode)

SUPPORTED_OPTIMUS_MODES = [
    'hybrid',
    'integrated',
    'nvidia'
]
ROOT = 'root'

curr_mode = get_current_mode()


def is_root() -> bool:
    return os.geteuid() == 0


def pytest_configure(config):
    config.addinivalue_line('markers', f'{ROOT}: mark test as needing root privileges')

    for mode in SUPPORTED_OPTIMUS_MODES:
        config.addinivalue_line('markers', f'{mode}: mark test as applicable to {mode}')


def pytest_collection_modifyitems(session, config, items):
    print()
    print(f'pytest.mark.{curr_mode} in force')
    if is_root():
        print('pytest.mark.root in force')

    for item in items:
        try_skip(item)


def try_skip(item):
    own_markers = [mark for mark in item.own_markers]
    if own_markers:
        modes = [mark.name for mark in own_markers if mark.name in SUPPORTED_OPTIMUS_MODES]
        if curr_mode in modes:
            # {mode} in force: do not skip mode tests
            pass
        else:
            skip_mode = pytest.mark.skip(reason=f'needs one of "Optimus mode"={modes} to run; current_mode={curr_mode}')
            item.add_marker(skip_mode)

    if not is_root():
        marks = [mark for mark in item.own_markers if mark.name == ROOT]
        for mark in marks:
            skip_mode = pytest.mark.skip(reason=f'needs root privileges to run')
            item.add_marker(skip_mode)


@pytest.fixture
def files_to_remove() -> list[str]:
    return [
        BLACKLIST_PATH,
        UDEV_INTEGRATED_PATH,
        UDEV_PM_PATH,
        XORG_PATH,
        EXTRA_XORG_PATH,
        '/etc/X11/xorg.conf.d/90-nvidia.conf',
        MODESET_PATH,
        LIGHTDM_SCRIPT_PATH,
        LIGHTDM_CONFIG_PATH,
    ]
