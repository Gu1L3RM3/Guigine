from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Callable


PYTHON_CONSTRAINT = 'requires-python = ">=3.12,<4.0"'
RUNTIME_DEPENDENCIES = ["pygame-ce", "numpy", "pytmx", "pathfinding"]
DEV_DEPENDENCIES = ["taskipy", "pytest"]

CommandRunner = Callable[..., str | None]


def run_command(args: list[str], cwd: Path, capture_output: bool = False) -> str | None:
    completed = subprocess.run(
        args,
        cwd=str(cwd),
        check=True,
        text=True,
        capture_output=capture_output,
    )
    if capture_output:
        return completed.stdout.strip()
    return None


def get_package_name(source_name: str) -> str:
    return "".join(char.lower() if char.isalnum() or char == "_" else "_" for char in source_name).strip("_")


def resolve_engine_source() -> Path:
    return Path(__file__).resolve().parent


def build_readme(project_name: str, package_name: str) -> str:
    return f"""# {project_name}

Project created with `Guigine` + `Poetry`.

## Requirements

- Python 3.12
- Poetry installed on your machine

## How To Run

```powershell
poetry install
poetry run task run
```

## Basic Commands

```powershell
poetry run task run
poetry run task start
poetry run task test
poetry run task test-v
poetry run task test-cov
poetry run task shell
poetry run task update
poetry run task tree
poetry run task freeze
poetry run task clean
```

## Initial Structure

```text
{project_name}/
|- assets/
|- guigine/
|- src/
|  \\- {package_name}/
|     |- __init__.py
|     \\- main.py
\\- pyproject.toml
```

## Main Entry Point

The initial entry point is `src/{package_name}/main.py`.

## Next Steps

1. Adjust your project's `EngineConfig`.
2. Create your own scenes, entities, and assets.
3. Run the test suite whenever you evolve the codebase.
"""


def build_main_module() -> str:
    return """from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from guigine.app.app import EngineApp
from guigine.app.config import EngineConfig


def main() -> None:
    config = EngineConfig(asset_root=PROJECT_ROOT / "assets")
    app = EngineApp(config=config)

    print("Guigine project bootstrapped successfully.")
    print(f"Window size: {config.width}x{config.height}")
    print(f"App instance created: {app.__class__.__name__}")


if __name__ == "__main__":
    main()
"""


def build_taskipy_block(package_name: str) -> str:
    return f"""
[tool.taskipy.tasks]
run = "python src/{package_name}/main.py"
start = "python src/{package_name}/main.py"
test = "pytest"
test-v = "pytest -v"
test-cov = "pytest --cov"
shell = "python"
install = "poetry install"
update = "poetry update"
add-dev = "poetry add --group dev"
tree = "python -m pip list"
freeze = "python -m pip freeze"
clean = "python -c \\"import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]\\""
"""


def write_project_files(project_dir: Path, package_name: str, engine_source: Path) -> None:
    assets_dir = project_dir / "assets"
    package_dir = project_dir / "src" / package_name
    assets_dir.mkdir(parents=True, exist_ok=True)
    package_dir.mkdir(parents=True, exist_ok=True)

    shutil.copytree(engine_source, project_dir / "guigine", dirs_exist_ok=True)

    (package_dir / "__init__.py").write_text(
        '"""Starter package for the generated Guigine project."""\n',
        encoding="utf-8",
    )
    (package_dir / "main.py").write_text(build_main_module(), encoding="utf-8")


def update_generated_pyproject(pyproject_path: Path, package_name: str) -> None:
    pyproject_content = pyproject_path.read_text(encoding="utf-8")
    pyproject_content = pyproject_content.replace('requires-python = ">=3.12"', PYTHON_CONSTRAINT)
    pyproject_content += build_taskipy_block(package_name)
    pyproject_path.write_text(pyproject_content, encoding="utf-8")


def create_project(
    project_name: str,
    workspace: Path,
    engine_source: Path | None = None,
    runner: CommandRunner = run_command,
    open_editor: bool = True,
) -> Path:
    package_name = get_package_name(project_name)
    if not package_name:
        raise ValueError("Project name must contain at least one letter or number.")

    project_dir = workspace / project_name
    if project_dir.exists():
        raise FileExistsError(f"Path '{project_name}' already exists.")

    engine_dir = engine_source or resolve_engine_source()
    if not engine_dir.exists():
        raise FileNotFoundError(f"Guigine source folder was not found at '{engine_dir}'.")

    runner(["poetry", "new", project_name], workspace)
    runner(["poetry", "add", *RUNTIME_DEPENDENCIES], project_dir)
    runner(["poetry", "add", "--group", "dev", *DEV_DEPENDENCIES], project_dir)

    update_generated_pyproject(project_dir / "pyproject.toml", package_name)
    write_project_files(project_dir, package_name, engine_dir)
    (project_dir / "README.md").write_text(build_readme(project_name, package_name), encoding="utf-8")

    if open_editor:
        try:
            run_command(["code", "."], cwd=project_dir)
        except Exception:
            pass

    return project_dir


def resolve_virtualenv_python(venv_path: Path) -> Path:
    if os.name == "nt":
        return venv_path / "Scripts" / "python.exe"
    return venv_path / "bin" / "python"


def remove_project(project_name: str, workspace: Path, runner: CommandRunner = run_command) -> None:
    project_dir = workspace / project_name
    if not project_dir.exists():
        raise FileNotFoundError(f"Project path '{project_name}' was not found in the current directory.")

    pyproject_path = project_dir / "pyproject.toml"
    if pyproject_path.exists():
        poetry_env_path = runner(["poetry", "env", "info", "--path"], project_dir, capture_output=True)
        if poetry_env_path:
            env_python = resolve_virtualenv_python(Path(poetry_env_path))
            runner(["poetry", "env", "remove", str(env_python)], project_dir)

    shutil.rmtree(project_dir)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="guigine",
        description="Create and manage Guigine starter projects.",
    )
    subparsers = parser.add_subparsers(dest="command")

    create_parser = subparsers.add_parser("new", help="Create a new Poetry project with the Guigine engine.")
    create_parser.add_argument("project_name")

    remove_parser = subparsers.add_parser("remove", help="Remove a generated project and its Poetry environment.")
    remove_parser.add_argument("project_name")

    parser.add_argument("project_name", nargs="?", help=argparse.SUPPRESS)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    workspace = Path.cwd()

    if args.command == "new":
        create_project(args.project_name, workspace=workspace)
        return 0

    if args.command == "remove":
        remove_project(args.project_name, workspace=workspace)
        return 0

    if getattr(args, "project_name", None):
        create_project(args.project_name, workspace=workspace)
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
