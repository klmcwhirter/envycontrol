
import sys

import pytest

from envycontrol import main


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


@pytest.mark.parametrize([], [pytest.param(marks=[pytest.mark.hybrid, pytest.mark.root])])
def test_cache_create_creates_file():
    raise NotImplementedError()
