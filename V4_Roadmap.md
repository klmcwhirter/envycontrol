# Envycontrol V4 Roadmap

> Issues to be created for unnumbered items below.

## Goals

* General technology refresh
* Redesign for ease of customization, system stability assurance
  * simple enough design for maintainability
  * rely on stdlib only (e.g., json and not yaml)
* Address enhancements / bugs from backlog as appropriate
* Automated CI/CD pipeline
  * including test bed with up to 50% coverage

## Items to Consider

### Project Enhancements

* Adopt [pdm](https://pdm-project.org/latest/) usage for testing, packaging and publishing
* Adopt project structure as created by [`pdm init`](https://pdm-project.org/latest/usage/project/#new-project)
* Adopt guidance from the new [Python Packaging User Guide](https://packaging.python.org/en/latest/)
* Adopt [pytest](https://docs.pytest.org/en/stable/) for unit and integration testing
  * At least 50% test coverage (measured with pytest-cov) - enforced via [github action status check](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/about-status-checks)
  * See [klmcwhirter/envycontrol#tests](https://github.com/klmcwhirter/envycontrol/tree/tests) for potential starting point
* Support Python >= 3.10
* Distribute as a Python package with `envycontrol` wrapper shell script to maintain current interface
* Adopt github actions for CI/CD pipeline
  * [Using scripts to test your code on a runner](https://docs.github.com/en/actions/examples/using-scripts-to-test-your-code-on-a-runner)
  * [About packaging with GitHub Actions](https://docs.github.com/en/actions/publishing-packages/about-packaging-with-github-actions)
  * Not Python, but ... [Publishing Node.js packages](https://docs.github.com/en/actions/publishing-packages/publishing-nodejs-packages)
  * [marketplace/actions/pypi-publish](https://github.com/marketplace/actions/pypi-publish)
* [flake.nix version](https://github.com/bayasdev/envycontrol/pull/156) - make version dynamic from github action 
* WHAT ELSE?

### Envycontrol Enhancements

* Refactor to use modern Python features
  * f-strings instead of .format
  * type hints
  * use unpacking instead of positional parameters to simplifying calling functions
  * usage of "walrus operator" as appropriate - [3.8 assignment expressions](https://docs.python.org/3/whatsnew/3.8.html#assignment-expressions)
  * custom generic contextmanagers that ease the coding of file creation operations
* Refactor as a package (note can be bundled as a zip file to keep 'single file delivery')
* Refactor to construct "context" class that collects data prior to emitting file changes
  * provides mechanism to override values as analysis steps proceed.
  * output process simply emits stuff from context
* Move file content constants to "templates" that can be customized by users
  * note that delivered templates will be in "envycontrol/src/templates/" directory
  * customized versions will be in "/etc/envycontrol/templates/" directory
  * this should address issues like [#34](https://github.com/bayasdev/envycontrol/issues/34) and maybe [#142](https://github.com/bayasdev/envycontrol/issues/142) to the extent that the user can put in place guidance they receive from the community
* Add customizable envycontrol rules for state transitions between Optimus modes
  * these are envycontrol rules NOT udev rules - Python code modules
  * allow for elegant per-display-manager customizations via separate dir per display-manager
  * envycontrol rules files to use paths to template files - allows to easily remap for different display-managers
  * this should allow users to add / remove files to change / delete instead of them being hard coded
  * [#141 - Please make it init agnostic](https://github.com/bayasdev/envycontrol/issues/141)
  * [#145 - Runit?](https://github.com/bayasdev/envycontrol/issues/145) - eliminates the need for [ToneyFoxxy's](https://github.com/ToneyFoxxy/ToneyFoxxy-EnvyControl-Without-SystemD) customizations
* Add custom profiles to simplify command lines:
  * envycontrol --profile my_hybrid ==> `envycontrol --switch hybrid --rtd3 1`
  * envycontrol --profile my_nvidia ==> `envycontrol --switch nvidia --force-comp --coolbits 24 --dm sddm --use-nvidia-current`
* While researching which of the 3 methods to use to install the nvidia drivers on Fedora 39, I ran into this video.
  * [The Linux Experiment - NVIDIA on Linux is WAY BETTER than everyone says, but...](https://youtu.be/9f4B8uIPqcE)
  * Wayland support is MUCH better on modern Linux kernels and 30 series and up cards.
  * **Do we need a level of abstraction to model the different card families** so that different actions can be taken?
  * What would that look like?
* [#113 - nvidia only mode by integrating with NVX](https://github.com/bayasdev/envycontrol/issues/113)
* [#147 - Can't use NVENC in hybrid mode, can use just in resetted mode](https://github.com/bayasdev/envycontrol/issues/147)
* WHAT ELSE?

### Envycontrol Issues

* [#116 - Switched to Nvidia mode then the host is unable to boot normally](https://github.com/bayasdev/envycontrol/issues/116)
* WHAT ELSE?

## Timeline

TBD

## Deployment Model
```
/etc/envycontrol/
    profiles/*.json           # custom profiles with pre-filled command line options
    rules/**/*.py             # customized rules; deployment does not touch these
    templates/**/*            # customized template text files; deployment does not touch these

/var/cache/envycontrol/       # cache directory
    system/                   # location to backup original system files modified; put back upon `reset all` operation
                              # file names as full path with '/' chars replaced with '$' (some sentinel char TBD)
    cache.json

/usr/local/sbin/envycontrol   # wrapper sh script

/usr/local/share/envycontrol/ # ENVYCONTROL_HOME deployed Python package
    profiles/*.json           # deployed profiles with pre-filled command line options
    rules/**/*.py             # deployed rules; these are upgraded with each release
    templates/**/*            # deployed template text files; these are upgraded with each release
```

## Command Line Interface

```
envycontrol 4.x.x - switch between GPU modes on Nvidia Optimus systems

  [ORIG_OPTS]       Retain original options for backward compatibility


  Verb-based interface *NEW*
  --------------------------

  switch [MODE]     Where MODE is integrated, hybrid or nvidia; e.g., `envycontrol switch integrated`
    profile [NAME]  Perform switch based on values in ENVYCONTROL_ETC/profiles/NAME.json or ENVYCONTROL_HOME/profiles/NAME.json
                    E.g., `envycontrol switch profile my_nvidia`
    [OPTS]          Allow any available non-verb options; these override values in profile used if any
                    E.g., `envycontrol switch profile my_hybrid --rtd3 0`
                    E.g., `envycontrol switch hybrid --rtd3 1`

  profile [NAME]
    copy [TO_NAME]  Copy profile from ENVYCONTROL_HOME/profiles/NAME.json to ENVYCONTROL_ETC/profiles/TO_NAME.json

  cache
    create [OPTS]   Creates cache file with OPTS as args
    delete          Deletes cache file
    show            Dumps cache file to stdout

  reset
    all             Undo all system modifications and rebuild initramfs
    sddm            Redo sddm specific modifications
```
