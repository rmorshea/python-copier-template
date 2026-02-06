# Python Project Template

A template for Python projects built using [Copier](https://github.com/copier-org/copier).

# Generate a Project

Generate a project from this template using Copier:

```bash
# with pipx
pipx copier copy https://github.com/rmorshea/python-copier-template path/to/project
```

```bash
# with uvx
uvx copier copy https://github.com/rmorshea/python-copier-template path/to/project
```

## What's in the Box?

- [Mise](https://mise.jdx.dev/) for managing tool versions and project scripts.
- [UV](https://docs.astral.sh/uv/) for managing Python versions and dependencies.
- [MkDocs](https://www.mkdocs.org/) for documentation.
- [Pyright](https://github.com/microsoft/pyright) for Python type checking.
- [Ruff](https://docs.astral.sh/ruff/) for Python linting.
- [PyTest](https://docs.pytest.org/) for Python testing.

### Continuous Integration

This template supplies a set of GitHub workflows for running tests, linting, deploying documentation
and making releases. These workflows are located in the `.github/workflows`. Each pull request will
trigger the `check.yml` workflow, which runs the test suite (with coverage), linting, and checks for
documentation build errors. Versioning is not automated - you will still need to bump the version
found in `pyproject.toml` - however that the current version will be published whenever a
[GitHub Release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository#creating-a-release)
is created.

# Contributing

First install [Mise](https://mise.jdx.dev/), then make some changes to the `template/` and then run
`mise run gen` to update the generated sample project(s). Sample projects are generated based on the
answers files found under the `answers/` directory.

Checks in CI work by taking the `.github/workflows/check.yml` file in each sample project and
"running" them. This is a bit hacky because there's no easy way to
[run workflows in subdirectories](https://github.com/orgs/community/discussions/18055). As a result,
what we actually do is generate a facsimile of the original workflow file by modifying it and
injecting `working-directory: path/to/sample` in each step of each job and replacing any instance of
`${{ github.workspace }}` with the path to the sample project.
