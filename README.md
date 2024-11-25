# Python Project Template

A template for Python projects built using [Copier](https://github.com/copier-org/copier).

# Generate a Project

Generate a project from this template using Copier:

```bash
# with pipx
pipx copier copy https://github.com/rmorshea/python-copier-template path/to/project

# with uvx
uvx copier copy https://github.com/rmorshea/python-copier-template path/to/project
```

## What's in the Box?


### Project Management

Projects generated from this template use [`uv`](https://github.com/astral-sh/uv) as a
package and project manager. Common developer commands are located in a `project.py`
file at project's root. To see a full list of commands run:

```bash
uv run project.py
```

### Continuous Integration

This template supplies a set of GitHub workflows for running tests, linting, deploying
documentation and making releases. These workflows are located in the `.github/workflows`.
Each pull request will trigger the `check.yml` workflow, which runs the test suite
(with coverage), linting, and checks for documentation build errors. Versioning is
not automated - you will still need to bump the version found in `pyproject.toml` -
however releases are whenever using
[GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository#creating-a-release).

# Contributing

This project uses [`uv`](https://github.com/astral-sh/uv) in combination with dev
scripts contained in `project.py`. To see available commands, run `uv run project.py`.

Make some changes to the `template/` and then run `uv run project.py gen` to update the
generated sample project(s). Sample projects are generated based on the answers files
found under the `answers/` directory.

Checks in CI work by taking the `.github/workflows/check.yml` file in each sample
project and "running" them. This is a bit hacky because there's no easy way to
[run workflows in subdirectories](https://github.com/orgs/community/discussions/18055).
As a result, what we actually do is generate a facsimile of the original workflow file
by modifying it and injecting `working-directory: path/to/sample` in each step of each
job and replacing any instance of `${{ github.workspace }}` with the path to the sample
project.
