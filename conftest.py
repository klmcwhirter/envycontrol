# Detect the mode amd set default as appropriate


import os
from argparse import Namespace

import pytest

from envycontrol import (BLACKLIST_PATH, EXTRA_XORG_PATH, LIGHTDM_CONFIG_PATH,
                         LIGHTDM_SCRIPT_PATH, MODESET_PATH,
                         UDEV_INTEGRATED_PATH, UDEV_PM_PATH, XORG_PATH,
                         CachedConfig, get_current_mode)

SUPPORTED_OPTIMUS_MODES = [
    'hybrid',
    'integrated',
    'nvidia'
]
ROOT_MARK = 'root'
SLOW_MARK = 'slow'
CUSTOM_PYTEST_MARKS = [ROOT_MARK, SLOW_MARK]
SUPPORTED_PYTEST_MARKS = [*SUPPORTED_OPTIMUS_MODES, *CUSTOM_PYTEST_MARKS]

curr_mode = None


def is_root() -> bool:
    return os.geteuid() == 0


def pytest_configure(config):
    config.addinivalue_line('markers', f'{ROOT_MARK}: mark test as needing root privileges')
    config.addinivalue_line('markers', f'{SLOW_MARK}: mark test as slow integration test; filter with pytest -m "not slow"')

    for mode in SUPPORTED_OPTIMUS_MODES:
        config.addinivalue_line('markers', f'{mode}: mark test as applicable to {mode}')


def pytest_collection_modifyitems(session, config, items):
    global curr_mode
    if not curr_mode:
        curr_mode = get_current_mode()

    print()
    print(f'pytest.mark.{curr_mode} in force')
    if is_root():
        print(f'pytest.mark.{ROOT_MARK} in force')

    for item in items:
        try_skip(item)


def try_skip(item):
    own_markers = [mark for mark in item.own_markers if mark.name != 'parametrize']

    if own_markers:
        marks = [mark.name for mark in own_markers if mark.name in SUPPORTED_PYTEST_MARKS]
        if curr_mode not in marks:
            modes = [mark for mark in marks if mark in SUPPORTED_OPTIMUS_MODES]
            if modes:
                skip_mode = pytest.mark.skip(reason=f'needs one of "Optimus mode"={modes} to run; current_mode={curr_mode}')
                item.add_marker(skip_mode)

    if not is_root():
        marks = [mark for mark in item.own_markers if mark.name == ROOT_MARK]
        if marks:
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


cache_file_obj = None


def read_cache():
    global cache_file_obj
    cache = CachedConfig(Namespace())
    cache.read_cache_file()
    cache_file_obj = cache.obj


@pytest.fixture
def is_rtd3():
    if cache_file_obj is None:
        read_cache()
    rtd3 = cache_file_obj['metadata']['args']['rtd3'] is not None
    return rtd3


@pytest.fixture
def display_manager():
    if cache_file_obj is None:
        read_cache()
    dm = cache_file_obj['metadata']['display_manager']
    return dm
