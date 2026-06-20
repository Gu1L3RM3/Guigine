# Guigine

Guigine is a lightweight 2D runtime built on top of `pygame-ce`.

It is designed for small and medium 2D games, gameplay prototypes, menu-heavy applications, and projects that benefit from scenes, ECS, resource loading, and simple rendering without carrying a large engine framework.

## Install

If you want the library and CLI together:

```bash
pip install guigine
```

If you mainly want the CLI in an isolated environment:

```bash
pipx install guigine
```

Both installation modes expose the `guigine` command on Windows, Linux, and macOS.

## CLI Quick Start

Create a new starter project:

```bash
guigine new my_game
```

Backward-compatible shorthand:

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
- a Python-focused `.gitignore`
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

## ECS Basics

Guigine uses a small ECS architecture:

- An `Entity` is an ID plus a bag of components.
- A `Component` stores data.
- A `System` reads entities that have a specific set of components and updates them every frame.

This model keeps behavior composable. Instead of creating a deep inheritance tree like `PlayerWithPhysicsAndHealthAndSprite`, you build an entity from small parts and let systems operate on those parts.

### Entity

An entity is just a container for components.

```python
from guigine.ecs.entity_manager import EntityManager
from guigine.components.base import Position, Velocity
from guigine.components.collider import Collider


entity_manager = EntityManager()

player = entity_manager.create(
    Position(100, 100),
    Velocity(180, 0),
    Collider(16, 16),
)
```

In this example, the entity itself does not know how to move or collide. It only owns the data required by other systems.

### Component

Components are focused data objects. A good component should answer "what data does this entity have?" rather than "what complex behavior does this entity execute?"

## Basic Components

### `Position`

`Position` stores world coordinates.

```python
from guigine.components.base import Position

position = Position(120, 64)
print(position.xy)  # (120.0, 64.0)
```

Use it for anything that exists in world space.

### `Velocity`

`Velocity` stores movement speed and direction.

```python
from guigine.components.base import Velocity

velocity = Velocity(150, -40)
print(velocity.vx, velocity.vy)
```

When an entity has both `Position` and `Velocity`, systems such as `PhysicsSystem` can move it every frame.

### `Collider`

`Collider` defines a collision rectangle and optional offsets relative to the entity position.

```python
from guigine.components.collider import Collider

collider = Collider(width=16, height=16, offset_x=0, offset_y=0)
```

This is the basic piece used by physics and collision logic.

### `Freeze`

`Freeze` is a small control component that allows systems to temporarily stop movement or logic.

```python
from guigine.components.base import Freeze

freeze = Freeze(active=True)
```

This is useful for pause states, cutscenes, hit-stop, and scripted interactions.

### `Sprite`

`Sprite` is the visual component used by rendering systems. It stores the image/surface and drawing rectangle for an entity.

Typical pattern:

```python
from guigine.components.base import Position
from guigine.components.sprite import Sprite


enemy = self.entity_manager.create(
    Position(200, 120),
    Sprite(self.resources.load_image("actors/enemy.png")),
)
```

### `Health`

`Health` is a simple gameplay-friendly component that stores hit points.

```python
from guigine.components.base import Health

health = Health(max_hp=100)
health.take_damage(20)
print(health.current_hp)  # 80.0
```

This is a good example of a component that still stays small and data-focused.

## Basic Systems

Systems are where frame-by-frame behavior happens.

### `PhysicsSystem`

`PhysicsSystem` looks for entities with `Position` and `Velocity` and moves them using `dt`. If an entity also has `Collider`, the system resolves collisions against static and dynamic colliders.

```python
from guigine.systems.physics import PhysicsSystem


class GameplayScene(BaseScene):
    def __init__(self, context):
        super().__init__(context, world_width=2000, world_height=1200)
        self.physics = PhysicsSystem()
        self.add_system(self.physics)

    def update(self, dt):
        self.physics.cache_static_colliders(self.entity_manager)
        self.update_systems(dt)
```

This is the most common system to start with when building actors that move.

### `RenderSystem`

`RenderSystem` is responsible for drawing sprite-based entities visible to the camera.

It mainly works with entities that have:

- `Position`
- `Sprite`
- optionally `Collider`, `RenderLayer`, `DepthAnchor`, or `AlwaysOnTop`

Example:

```python
from guigine.systems.render import RenderSystem


self.render_system = RenderSystem(
    screen=self.screen,
    camera=self.camera,
    entity_manager=self.entity_manager,
)
```

The render system sorts visible entities and draws them in a stable order, which helps a lot in top-down and layered scenes.

### `AnimationSystem`

`AnimationSystem` updates animation state over time for entities that expose animation-related components.

Use it when your scene has animated actors, props, or effects and you want that timing logic separated from scene orchestration.

### `AreaTriggerSystem`

`AreaTriggerSystem` is useful when regions in the world should react to entities entering them.

Common uses:

- dialogue triggers
- zone transitions
- interaction hotspots
- scripted events

### `PathFollowingSystem`

`PathFollowingSystem` is useful for moving entities along a computed route.

This becomes especially helpful when combined with navigation/pathfinding helpers from `guigine.utils.navigation`.

## ECS Example In A Scene

This example shows a small ECS-driven scene with a moving player.

```python
from guigine.components.base import Position, Velocity
from guigine.components.collider import Collider
from guigine.scene.base_scene import BaseScene
from guigine.systems.physics import PhysicsSystem


class GameplayScene(BaseScene):
    def __init__(self, context):
        super().__init__(context, world_width=2000, world_height=1200)
        self.physics = PhysicsSystem()
        self.add_system(self.physics)

        self.player = self.entity_manager.create(
            Position(100, 100),
            Velocity(120, 0),
            Collider(16, 16),
        )

    def update(self, dt):
        self.physics.cache_static_colliders(self.entity_manager)
        self.update_systems(dt)
```

The entity contains state. The scene owns the orchestration. The system owns the frame update logic.

## Resource Loading Example

```python
button_image = self.resources.load_image("ui/button.png")
font = self.resources.load_font("fonts/MyFont.ttf", 16)
click_sound = self.resources.load_sound("audio/click.wav")
```

## Widget Example

```python
from guigine.widgets.button import Button


button = Button(
    init_surface=self.resources.load_image("ui/button.png"),
    surface_pressed=self.resources.load_image("ui/button_pressed.png"),
    pos_center=(640, 360),
    action=lambda: self.scene_manager.start_fade("gameplay"),
    text="Start",
    font_size=16,
    font="fonts/MyFont.ttf",
    resource_manager=self.resources,
)

self.context.ui.clear()
self.context.ui.add(button)
```

## TMX Example

```python
from guigine.map.tile_map_loader import TileMapLoader


loader = TileMapLoader(self.resources, walk_layer_name="ground2")
tilemap = loader.load("maps/level_01.tmx")
```

## Practical Guidance

When building with Guigine, a good default approach is:

1. Keep scenes responsible for flow and orchestration.
2. Keep components small and data-oriented.
3. Keep systems narrow and reusable.
4. Move project-specific game rules outside the engine package whenever possible.

That keeps the runtime easy to reason about and easier to reuse across multiple projects.

## Notes For Publishing

- The PyPI package exposes the `guigine` command through a Python entry point.
- The local `bash/` wrappers are not part of the published package.
- The repository examples are documentation/reference material and are not installed as part of the runtime package.

## Current Status

Guigine is currently best treated as an early reusable runtime for experimentation, tooling, and game prototypes. The public API is intentionally small and should evolve carefully as more real projects adopt it.
