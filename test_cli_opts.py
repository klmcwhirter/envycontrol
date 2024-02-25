
import json
import sys
from argparse import Namespace
from typing import Any

import pytest

from envycontrol import CACHE_FILE_PATH, CachedConfig, main


def test_create_cache_obj__constructs_structure() -> None:
    # for vars() support -- mimic envycontrol parse_args ouytput
    args = Namespace(**{
        "query": False,
        "switch": "nvidia",
        "dm": None,
        "force_comp": True,
        "coolbits": None,
        "rtd3": None,
        "use_nvidia_current": True,
        "reset_sddm": False,
        "reset": False,
        "cache_create": False,
        "cache_delete": False,
        "cache_query": False,
        "verbose": False
    })
    cache = CachedConfig(args)
    cache_dict = cache.create_cache_obj('PCI:3:3:3')
    validate_cache_dict_structure(cache_dict)


@pytest.mark.parametrize([], [pytest.param(marks=[pytest.mark.integrated, pytest.mark.root])])
def test_cache_create_throws_when_integrated():
    with pytest.raises(ValueError):
        sys.argv = [sys.argv[0], '--cache-create']
        main()


@pytest.mark.parametrize([], [pytest.param(marks=[pytest.mark.nvidia, pytest.mark.root])])
def test_cache_create_throws_when_nvidia():
    with pytest.raises(ValueError):
        sys.argv = [sys.argv[0], '--cache-create']
        main()


@pytest.mark.parametrize([], [pytest.param(marks=[pytest.mark.integrated, pytest.mark.nvidia])])
def test_cache_create__does_create_file():
    '''After switch from hybrid'''
    content = ''
    with open(CACHE_FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    cache_dict = json.loads(content)

    validate_cache_dict_structure(cache_dict)

    assert 'hybrid' == cache_dict['metadata']['current_mode']


def validate_cache_dict_structure(cache_dict: dict[str, Any]) -> None:
    # region switch

    assert 'switch' in cache_dict
    assert 'nvidia_gpu_pci_bus' in cache_dict['switch']

    # endregion

    # region metadata

    assert 'metadata' in cache_dict

    expected_metadata = [
        'audit_iso_tmstmp',
        'args',
        'amd_igpu_name',
        'current_mode',
        'display_manager',
        'igpu_pci_bus',
        'igpu_vendor'
    ]

    results = [(metadata in cache_dict['metadata'], metadata) for metadata in expected_metadata]
    for result in results:
        exists, metadata = result
        if not exists:
            print(f'ERROR: {metadata} is missing')
    assert all(exists for exists, _ in results), 'missing metadata'

    # endregion

    # region args

    expected_args = [
        'query',
        'switch',
        'dm',
        'force_comp',
        'coolbits',
        'rtd3',
        'use_nvidia_current',
        'reset_sddm',
        'reset',
        'cache_create',
        'cache_delete',
        'cache_query',
        'verbose',
    ]

    results = [(arg in cache_dict['metadata']['args'], arg) for arg in expected_args]
    for result in results:
        exists, metadata = result
        if not exists:
            print(f'ERROR: {metadata} is missing')
    assert all(exists for exists, _ in results), 'missing arg(s)'

    # endregion
