from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from guigine import cli


class CliHelpersTestCase(unittest.TestCase):
    def test_get_package_name_normalizes_input(self) -> None:
        self.assertEqual(cli.get_package_name("My Cool-Game"), "my_cool_game")

    def test_build_readme_mentions_assets_and_commands(self) -> None:
        content = cli.build_readme("MyGame", "mygame")
        self.assertIn("# MyGame", content)
        self.assertIn("|- assets/", content)
        self.assertIn("poetry run task run", content)
        self.assertIn("poetry run task test", content)
        self.assertIn("src/mygame/main.py", content)


class CreateProjectTestCase(unittest.TestCase):
    def test_create_project_bootstraps_expected_files(self) -> None:
        commands: list[tuple[str, Path]] = []

        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            engine_source = workspace / "engine_source" / "guigine"
            engine_source.mkdir(parents=True)
            (engine_source / "__init__.py").write_text(
                '"""Guigine reusable runtime package."""\n',
                encoding="utf-8",
            )

            def fake_runner(args: list[str], cwd: Path) -> None:
                commands.append((" ".join(args), cwd))
                if args[:2] == ["poetry", "new"]:
                    project_dir = cwd / args[2]
                    (project_dir / "src" / args[2]).mkdir(parents=True)
                    (project_dir / "README.md").write_text("# Placeholder\n", encoding="utf-8")
                    (project_dir / "pyproject.toml").write_text(
                        (
                            "[project]\n"
                            f'name = "{args[2]}"\n'
                            'version = "0.1.0"\n'
                            'requires-python = ">=3.12"\n'
                        ),
                        encoding="utf-8",
                    )
                elif args[:3] == ["poetry", "add", "--group"]:
                    return
                elif args[:2] == ["poetry", "add"]:
                    return
                else:
                    raise AssertionError(f"Unexpected command: {args}")

            cli.create_project(
                project_name="sample_game",
                workspace=workspace,
                engine_source=engine_source,
                runner=fake_runner,
                open_editor=False,
            )

            project_dir = workspace / "sample_game"
            self.assertTrue((project_dir / "assets").is_dir())
            self.assertTrue((project_dir / "guigine").is_dir())
            self.assertTrue((project_dir / "src" / "sample_game" / "__init__.py").is_file())
            self.assertTrue((project_dir / "src" / "sample_game" / "main.py").is_file())

            readme = (project_dir / "README.md").read_text(encoding="utf-8")
            self.assertIn("Project created with `Guigine` + `Poetry`.", readme)
            self.assertIn("|- assets/", readme)

            pyproject = (project_dir / "pyproject.toml").read_text(encoding="utf-8")
            self.assertIn('requires-python = ">=3.12,<4.0"', pyproject)
            self.assertIn('[tool.taskipy.tasks]', pyproject)
            self.assertEqual(
                [command for command, _cwd in commands],
                [
                    "poetry new sample_game",
                    "poetry add pygame-ce numpy pytmx pathfinding",
                    "poetry add --group dev taskipy pytest",
                ],
            )

    def test_create_project_rejects_existing_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            engine_source = workspace / "engine_source" / "guigine"
            engine_source.mkdir(parents=True)
            (workspace / "taken").mkdir()

            with self.assertRaisesRegex(FileExistsError, "already exists"):
                cli.create_project(
                    project_name="taken",
                    workspace=workspace,
                    engine_source=engine_source,
                    runner=lambda args, cwd: None,
                    open_editor=False,
                )


class RemoveProjectTestCase(unittest.TestCase):
    def test_remove_project_deletes_directory_and_attempts_env_removal(self) -> None:
        commands: list[list[str]] = []

        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            project_dir = workspace / "demo"
            project_dir.mkdir()
            (project_dir / "pyproject.toml").write_text("[project]\nname = 'demo'\n", encoding="utf-8")

            def fake_runner(args: list[str], cwd: Path, capture_output: bool = False) -> str:
                commands.append(args)
                if args == ["poetry", "env", "info", "--path"]:
                    return str(project_dir / ".venv")
                if args[:3] == ["poetry", "env", "remove"]:
                    return ""
                raise AssertionError(f"Unexpected command: {args}")

            cli.remove_project("demo", workspace=workspace, runner=fake_runner)

            self.assertFalse(project_dir.exists())
            self.assertEqual(
                commands,
                [
                    ["poetry", "env", "info", "--path"],
                    ["poetry", "env", "remove", str(project_dir / ".venv" / "Scripts" / "python.exe")],
                ],
            )
