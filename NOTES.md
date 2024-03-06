# NOTES.md

## Simply disable dGPU

### References
* [Linux on the ASUS ROG Zephyrus G14 2021](https://blog.nil.im/?7b)
  - [Optional: Actually secure boot on Fedora](https://blog.nil.im/?7a)
  - [Optional - Actually secure boot on Fedora 39](https://blog.nil.im/?80)
* [tmpfiles.d man page](https://www.freedesktop.org/software/systemd/man/latest/tmpfiles.d.html)
* [Configuration of Temporary Files with systemd-tmpfiles](https://www.baeldung.com/linux/systemd-tmpfiles-configure-temporary-files)

### New supported mode - no-nvidia

```python
SUPPORTED_MODES = ['integrated', 'hybrid', 'nvidia', 'no-nvidia']
```

### New CLI Logic
```python
        with CachedConfig(args).adapter() as adapter:
            if args.switch == 'no-nvidia':
                assert_root()
                cleanup()
                adapter.write_no_nvidia()
                CachedConfig.delete_cache_file()
                rebuild_initramfs()
                print('Operation completed successfully')
            elif args.switch:
                assert_root()
                graphics_mode_switcher(**vars(adapter.app_args))
        ...
```

### New adapter method

```python
    def write_no_nvidia(self):
        acer_tmpfile = '/etc/tmpfiles.d/acer_no_gpu.conf'
        tmpfile_content = [
            'w /sys/devices/pci0000:00/0000:00:01.0/0000:01:00.0/remove - - - - 1',
            'w /sys/devices/pci0000:00/0000:00:01.0/0000:01:00.1/remove - - - - 1',
            ''
        ]
        with open(acer_tmpfile, 'w') as f:
            f.writelines(acer_tmpfile)
```
