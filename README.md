# Guigine

Guigine is a lightweight 2D runtime built on top of `pygame-ce`.

It is meant for small and medium 2D games, gameplay prototypes, menu-heavy applications, and projects that benefit from scenes, ECS, resource loading, and simple rendering without carrying a large engine framework.

## Install

If you want the library:

```bash
pip install guigine
```

If you mainly want the project generator CLI:

```bash
pipx install guigine
```

Both installation modes expose the `guigine` command on Windows, Linux, and macOS.

## CLI Quick Start

Create a new starter project:

```bash
guigine new my_game
```

Or, for backward compatibility with the original command shape:

```bash
guigine my_game
```

Remove a generated project:

```bash
guigine remove my_game
```

The generated project includes:

- a local `guigine/` engine copy
- an `assets/` folder
- a `src/<project_name>/main.py` entry point
- a starter `README.md`
- `Poetry` and `taskipy` commands for running and testing

## Contributor Setup

Clone the repository and install dependencies with Poetry:

```bash
poetry install
```

Run the full test suite:

```bash
poetry run task test
```

Run only the CLI-focused tests:

```bash
poetry run task test-cli
```

Run the example showcase from the repository:

```bash
poetry run task run-examples
```

## What Guigine Includes

- `EngineApp` runtime bootstrap
- scene management with fade transitions
- shared `SceneContext`
- lightweight ECS primitives
- 2D camera support
- physics and collision helpers
- resource loading for images, fonts, and sounds
- audio and music managers
- reusable widgets
- optional TMX map loading
- TMX entity spawning helpers
- automated tests for core runtime systems

## Package Layout

Repository structure:

```text
Guigine/
|- guigine/
|- examples/
|- tests/
|- pyproject.toml
\- README.md
```

- `guigine/` contains the reusable runtime package published to PyPI.
- `examples/` contains repository-only examples and assets.
- `tests/` contains the automated suite used during development.

The `bash/` folder is kept only for local compatibility wrappers and is excluded from published package artifacts.

## Minimal Example

```python
from pathlib import Path

from guigine.app.app import EngineApp
from guigine.app.config import EngineConfig
from guigine.scene.base_scene import BaseScene


class DemoScene(BaseScene):
    def __init__(self, context):
        super().__init__(context, world_width=1280, world_height=720)

    def process_input(self, events):
        _ = events

    def update(self, dt):
        _ = dt

    def render(self):
        self.screen.fill((20, 24, 30))


def main() -> None:
    app = EngineApp(
        EngineConfig(
            title="My Game",
            width=1280,
            height=720,
            asset_root=Path("assets"),
        )
    )
    app.register_scene("demo", lambda context: DemoScene(context))
    app.start("demo")
    app.run()


if __name__ == "__main__":
    main()
```

## ECS Example

```python
from guigine.components.base import Position, Velocity
from guigine.components.collider import Collider


player = self.entity_manager.create(
    Position(100, 100),
    Velocity(),
    Collider(16, 16),
)
```

## TMX Example

```python
from guigine.map.tile_map_loader import TileMapLoader


loader = TileMapLoader(self.resources, walk_layer_name="ground2")
tilemap = loader.load("maps/level_01.tmx")
```

## Notes For Publishing

- The PyPI package exposes the `guigine` command through a Python entry point.
- The local `bash/` wrappers are not part of the published package.
- The repository examples are documentation/reference material and are not installed as part of the runtime package.

## Current Status

Guigine is currently best treated as an early reusable runtime for experimentation, tooling, and game prototypes. The public API is small on purpose and should evolve carefully as more real projects adopt it.
