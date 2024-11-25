# ruff: noqa: S607,S603,S404,FBT001,D401,D103

import shutil
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING, Any

import click
from ruamel.yaml import YAML
from ruamel.yaml.compat import BytesIO

HERE = Path(__file__).parent
TEMPLATE_DIR = HERE / "template"
ANSWERS_DIR = HERE / "answers"
SAMPLES_DIR = HERE / "samples"

yaml = YAML()


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
        run(
            [
                "copier",
                "copy",
                f"--data-file={answers_file}",
                "--overwrite",
                TEMPLATE_DIR,
                output_dir,
            ]
        )
        if check:
            run(["uv", "run", "project.py", "lint"], cwd=output_dir)
            run(["uv", "run", "project.py", "test"], cwd=output_dir)

        # copy workflow files to .github/workflows
        sample_check_workflow_yml = output_dir / ".github" / "workflows" / "check.yml"
        root_check_yml = (
            HERE / ".github" / "workflows" / f"check-{output_dir.name}-sample.yml"
        )
        check_workflow_doc = yaml.load(sample_check_workflow_yml)
        update_check_workflow(output_dir, check_workflow_doc)
        buffer = BytesIO()
        yaml.dump(check_workflow_doc, buffer)
        root_check_yml.write_bytes(buffer.getvalue())
    if diff:
        run(["git", "diff", "--exit-code", "--", "samples"])


def update_check_workflow(work_dir: Path, doc: Any) -> None:
    doc["name"] = f"{doc['name']}-{work_dir.name}-sample"
    for job in doc["jobs"].values():
        for step in job["steps"]:
            if "run" in step:
                step["working-directory"] = str(work_dir.relative_to(HERE))


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
