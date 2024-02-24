# NOTES.md

## TODO
* more tests!
* set version # - 3.4.0 ?
* validate cached value when switch to nvidia mode
  * fallback to detection if no longer valid (did the user get a new card and is installed in a new spot on the bus?)

## cmd snippets
* lspci | grep 'VGA compatible controller'
* glxinfo | grep renderer

## conftest.py

Add marker for each Optimus mode:
* hybrid
* intel
* nvidia

```python

# Detect the mode amd set default as appropriate

def pytest_addoption(parser):
    parser.addoption(
        "--run-slow", action="store_true", default=False, help="run slow tests"
    )
def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-slow"):
        # --run-slow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --run-slow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
```

## Tests
cleanup() files removed - each mode switch calls cleanup() and then creates files

```python
    # define list of files to remove
    to_remove = [
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
```

## Tests for hybrid

These are created:
if rtd3_value:
MODESET_PATH - MODESET_CURRENT_RTD3.format(rtd3_value)
else:
MODESET_PATH - MODESET_CONTENT

UDEV_PM_PATH - UDEV_PM_CONTENT

CACHE_FILE_PATH = '/var/cache/envycontrol/cache.json'

## Tests for intel

These are created.
BLACKLIST_PATH - BLACKLIST_CONTENT
UDEV_INTEGRATED_PATH - UDEV_INTEGRATED

## Tests for nvidia
