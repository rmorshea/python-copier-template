# Python Project Template

A template for Python projects built using [Copier](https://github.com/copier-org/copier).

# Getting Started

Generate a project from this template using Copier:

```bash
# with pipx
pipx copier copy https://github.com/rmorshea/python-copier-template path/to/project

# with uvx
uvx copier copy https://github.com/rmorshea/python-copier-template path/to/project
```

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
job.
