# ruff: noqa: S607,S603,S404,FBT001,D401,D103

import shutil
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

import click

HERE = Path(__file__).parent
TEMPLATE_DIR = HERE / "template"
ANSWERS_DIR = HERE / "answers"
SAMPLES_DIR = HERE / "samples"


@click.group()
def main():
    """A collection of dev utilities."""


@main.command("samples")
@click.option("--check", is_flag=True, help="Check sample projects.")
@click.option("--fresh", is_flag=True, help="Delete existing sample projects.")
@click.option("--diff", is_flag=True, help="Check if there's a diff.")
def samples(check: bool, fresh: bool, diff: bool):
    """Commands related to sample projects."""
    for answers_file in ANSWERS_DIR.glob("*.yml"):
        output_dir = str(SAMPLES_DIR / answers_file.stem)
        shutil.rmtree(output_dir, ignore_errors=True)
        run(
            [
                "copier",
                "copy",
                f"--data-file={answers_file}",
                "--overwrite",
                str(TEMPLATE_DIR),
                output_dir,
            ]
        )
        if check:
            run(["uv", "run", "project.py", "lint"], cwd=output_dir)
            run(["uv", "run", "project.py", "test"], cwd=output_dir)
    if diff:
        run(["git", "diff", "--exit-code", "--", "samples"])


if TYPE_CHECKING:
    run = subprocess.run
else:

    def run(*args, **kwargs):
        kwargs.setdefault("check", True)
        click.echo(click.style(" ".join(args[0]), bold=True))
        try:
            return subprocess.run(*args, **kwargs)
        except subprocess.CalledProcessError as e:
            raise click.ClickException(e) from None
        except FileNotFoundError as e:
            msg = f"File not found {e}"
            raise click.ClickException(msg) from None


if __name__ == "__main__":
    main()
