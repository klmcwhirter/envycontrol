# Envycontrol V4 Roadmap

> Issues to be created for unnumbered items below.

## Goals

* General technology refresh
* Automated CI/CD pipeline
  * including test bed with up to 50% coverage
* Redesign for ease of customization, system stability assurance
  * simple enough design for maintainability
* Address enhancements / bugs from backlog as appropriate

## Items to Consider

### Project Enhancements

* Adopt [pdm]() usage for testing, packaging and publishing
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
  * customized versions will be in "/etc/envycontrol/templates/" or "~/.config/envycontrol/templates/" directory
  * this should address issues like [#34](https://github.com/bayasdev/envycontrol/issues/34) and maybe [#142](https://github.com/bayasdev/envycontrol/issues/142) to the extent that the user can put in place guidance they receive from the community
* Add customizable envycontrol rules for state transitions between Optimus modes
  * this should allow users to add / remove files to change / delete instead of them being hard coded
  * allow for elegant per-display-manager customizations via separate dir per display-manager
  * envycontrol rules files to use paths to templates - allows to easily remap for other display-manager
  * [#145 - Runit?](https://github.com/bayasdev/envycontrol/issues/145) - eliminates the need for [ToneyFoxxy's](https://github.com/ToneyFoxxy/ToneyFoxxy-EnvyControl-Without-SystemD) cusomizations
  * [#141 - Please make it init agnostic](https://github.com/bayasdev/envycontrol/issues/141)
* [#113 - nvidia only mode by integrating with NVX](https://github.com/bayasdev/envycontrol/issues/113)
* [#147 - Can't use NVENC in hybrid mode, can use just in resetted mode](https://github.com/bayasdev/envycontrol/issues/147)
* WHAT ELSE?

### Envycontrol Issues

* [#116 - Switched to Nvidia mode then the host is unable to boot normally](https://github.com/bayasdev/envycontrol/issues/116)
* WHAT ELSE?

## Timeline

TBD
