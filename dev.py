# ruff: noqa: S607,S603,S404,FBT001,D401,D103

import re
import shutil
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, TypeAlias

import click
from ruamel.yaml import YAML
from ruamel.yaml.compat import BytesIO

FILE = Path(__file__)
HERE = FILE.parent
ANSWERS_DIR = HERE / "answers"
SAMPLES_DIR = HERE / "samples"

yaml = YAML()

GITHUB_WORKSPACE_PATTERN = re.compile(r"\$\{\{ *github\.workspace *\}\}")


@click.group()
def main():
    """A collection of dev utilities."""


@main.command("gen")
@click.option("--check", is_flag=True, help="Check sample projects.")
@click.option("--fresh", is_flag=True, help="Delete existing sample projects.")
@click.option("--diff", is_flag=True, help="Check if there's a diff.")
def gen(check: bool, fresh: bool, diff: bool):
    """Generate sample projects."""
    for answers_file in ANSWERS_DIR.glob("*.yml"):
        output_dir = SAMPLES_DIR / answers_file.stem
        shutil.rmtree(output_dir, ignore_errors=True)
        output_dir.mkdir(parents=True, exist_ok=True)
        run(
            [
                "copier",
                "copy",
                f"--data-file={answers_file}",
                "--overwrite",
                "--vcs-ref=HEAD",
                HERE,
                output_dir,
            ]
        )

        run(["uv", "run", FILE.name, "lint"], cwd=output_dir)
        run(["uv", "run", FILE.name, "cov"], cwd=output_dir)

        # copy workflow files to .github/workflows
        sample_check_workflow_yml = output_dir / ".github" / "workflows" / "check.yml"
        root_check_yml = (
            HERE / ".github" / "workflows" / f"check-{output_dir.name}-sample.yml"
        )
        doc = add_work_dir_to_workflow(output_dir, yaml.load(sample_check_workflow_yml))
        buffer = BytesIO()
        yaml.dump(doc, buffer)
        root_check_yml.write_bytes(buffer.getvalue())

        # Require .copier-answers.yml to exist, but delete it since it contains
        # the commit used to generate the sample which always creates a diff.
        (output_dir / ".copier-answers.yml").unlink(missing_ok=False)
    if diff:
        run(["git", "diff", "--exit-code", "--", "samples"])


def add_work_dir_to_workflow(work_dir: Path, doc: Any) -> Any:
    cwd_str = str(work_dir.relative_to(HERE))
    doc["name"] = f"{doc['name']}-{work_dir.name}-sample"
    for job in doc["jobs"].values():
        for step in job["steps"]:
            if "run" in step:
                step["working-directory"] = cwd_str

    def replace_github_workspace(value: Any, recurse: Recurse) -> Any:
        if isinstance(value, str):
            with_wd = "${{ github.workspace }}/" + cwd_str
            return GITHUB_WORKSPACE_PATTERN.sub(with_wd, value)
        return recurse(value, replace_github_workspace)

    return recurse_doc(doc, replace_github_workspace)


Recurse: TypeAlias = "Callable[[Any, Recurse], Any]"


def recurse_doc(doc: Any, visit: Recurse) -> Any:
    def drill(item: Any, visit: Recurse) -> Any:
        if isinstance(item, Mapping):
            return {k: visit(v, drill) for k, v in item.items()}
        elif isinstance(item, Sequence):
            return [visit(v, drill) for v in item]
        else:
            return item

    return visit(doc, drill)


if TYPE_CHECKING:
    run = subprocess.run
else:

    def run(*args, **kwargs):
        cmd, *args = args
        cmd = tuple(map(str, cmd))
        kwargs.setdefault("check", True)
        click.echo(click.style(" ".join(cmd), bold=True))
        try:
            return subprocess.run(cmd, *args, **kwargs)
        except subprocess.CalledProcessError as e:
            raise click.ClickException(e) from None
        except FileNotFoundError as e:
            msg = f"File not found {e}"
            raise click.ClickException(msg) from None


if __name__ == "__main__":
    main()
