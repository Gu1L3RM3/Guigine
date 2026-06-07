# Guigine

Guigine is a lightweight 2D runtime built on top of `pygame-ce`.

It is designed for:

- small and medium 2D games
- gameplay prototypes
- UI-heavy tools and menus
- experiments that benefit from scenes, ECS, resource loading, and simple rendering

This repository is intentionally structured so the reusable runtime lives in `guigine/`, while runnable example projects live in `examples/`.

You do not need any prior project-specific context to reuse Guigine.

## Goals

The engine is optimized for:

- clear architecture
- low cognitive overhead
- easy extension
- practical reuse across multiple projects

It does not try to be a fully general-purpose AAA framework.

Instead, it aims to provide a clean base with:

- a runtime loop
- scene management
- a compact ECS
- input, audio, and UI managers
- optional TMX map support
- example consumers outside the engine package

## Current Capabilities

The engine currently includes:

- reusable `EngineApp` runtime
- scene management with fade transitions
- shared `SceneContext`
- lightweight ECS
- 2D camera
- basic physics and collision
- base rendering support
- resource loading for images, fonts, and sounds
- audio and music managers
- reusable widgets
- optional TMX map loading
- generic TMX spawners
- example scenes with and without maps
- automated tests for core systems

## Repository Layout

- `guigine/`: reusable engine package
- `examples/`: example projects that consume the engine
- `examples/assets/`: self-contained assets for the examples
- `examples/recipes/`: small notes about example scenarios
- `tests/`: automated engine test suite
- `docs/`: planning and technical notes

## Quick Start

Run the example showcase:

```bash
python main.py
```

or:

```bash
python -m examples.run_examples
```

Run the test suite:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

Install dependencies from:

```bash
pip install -r requirements.txt
```

## Core Architecture

The engine is built around a few simple layers.

### `guigine.app`

This is the runtime bootstrap layer.

It is responsible for:

- initializing `pygame`
- creating the screen
- constructing managers
- creating the shared `SceneContext`
- running the frame loop
- shutting down cleanly

Primary file:

- [guigine/app/app.py](/abs/path/c:/Users/cavaz/OneDrive/Documentos/Projetos/Projetos_Python/IC/Alexandria/Alexandria_Engine/guigine/app/app.py)

### `guigine.scene`

Scenes are the main orchestration units of a project.

A scene owns:

- its own entities
- its own systems
- its input handling
- its update flow
- its rendering flow

Primary file:

- [guigine/scene/base_scene.py](/abs/path/c:/Users/cavaz/OneDrive/Documentos/Projetos/Projetos_Python/IC/Alexandria/Alexandria_Engine/guigine/scene/base_scene.py)

### `guigine.ecs`

The ECS layer provides:

- `Component`
- `Entity`
- `System`
- `EntityManager`

It is intentionally small.

The goal is to make composition easy without forcing a large framework around it.

### `guigine.components`

Components are mostly data carriers.

Examples include:

- `Position`
- `Velocity`
- `Collider`
- `Sprite`
- `Freeze`
- `AreaTrigger`
- `RenderLayer`
- `PathFollower`

As a rule, components should contain state, not large orchestration logic.

### `guigine.systems`

Systems operate on ECS state each frame.

Examples:

- `PhysicsSystem`
- `RenderSystem`
- `AnimationSystem`
- `AreaTriggerSystem`
- `PathFollowingSystem`
- `LightSystem`

The recommended approach is to keep each system narrow and reusable.

### `guigine.managers`

Managers provide small runtime services.

Examples:

- `InputManager`
- `UIManager`
- `AudioManager`
- `MusicManager`
- `EventManager`
- `TimeManager`

These help keep low-level runtime concerns out of scene code.

### `guigine.render`

Rendering helpers currently include:

- `Camera`
- `RectangleRenderer`

This layer is intentionally modest today and is a good candidate for future expansion.

### `guigine.map`

Map support is optional.

Use it when you need:

- TMX loading
- tiled surfaces
- tile-based colliders
- spawn points
- TMX object layer spawning

If your project is UI-only or does not use tilemaps, you can ignore this module entirely.

Primary files:

- [guigine/map/tile_map_loader.py](/abs/path/c:/Users/cavaz/OneDrive/Documentos/Projetos/Projetos_Python/IC/Alexandria/Alexandria_Engine/guigine/map/tile_map_loader.py)
- [guigine/map/map_entity_spawner.py](/abs/path/c:/Users/cavaz/OneDrive/Documentos/Projetos/Projetos_Python/IC/Alexandria/Alexandria_Engine/guigine/map/map_entity_spawner.py)

### `guigine.widgets`

Widgets provide a simple UI foundation.

Current examples include:

- `Text`
- `Button`
- `TypewriterEffect`
- `FPSWidget`
- `ClockWidget`

This is enough to support menus, overlays, and fully UI-driven scenes.

### `guigine.utils`

Shared lower-level helpers live here.

Examples:

- `spatial_hash.py`
- `navigation.py`

## Runtime Flow

At a high level, the engine runs like this:

1. `EngineApp` initializes `pygame`, the screen, managers, and `SceneManager`
2. the initial scene is activated
3. every frame:
   - events are collected
   - input state is updated
   - the active scene receives input
   - the scene updates
   - the scene renders
   - fade transitions are updated and drawn
   - the display is flipped
4. on shutdown, the active scene ends and `pygame.quit()` is called

## Reusable Project Structure

A good external consumer project should treat `guigine/` as infrastructure and keep game-specific code elsewhere.

A recommended layout looks like this:

```text
MyProject/
  guigine/
  game/
    scenes/
    entities/
    ui/
    assets/
  main.py
```

Another valid variant:

```text
MyProject/
  guigine/
  project/
    scenes/
    gameplay/
    content/
    assets/
  main.py
```

The important part is the separation:

- reusable engine code stays in `guigine/`
- project-specific code stays outside `guigine/`

## Recommended Architectural Practices

### 1. Use scenes as context boundaries

Typical scene boundaries include:

- main menu
- gameplay
- pause menu
- credits
- editor
- debug sandbox

If two flows have different lifecycle, input, rendering, or systems, they usually deserve separate scenes.

### 2. Keep engine systems generic

Good engine systems:

- movement
- physics
- rendering
- path following
- animation

Bad engine systems:

- quest-specific logic
- boss-specific behavior
- story event sequencing tied to one game

That kind of code belongs in the consumer project.

### 3. Treat components as state, not service objects

Good:

```python
from guigine.components.base import Position, Velocity
from guigine.components.collider import Collider

player = entity_manager.create(
    Position(120, 80),
    Velocity(),
    Collider(16, 16),
)
```

Avoid:

- components that perform file I/O
- components that load scene-specific content
- components that encode large business rules

### 4. Treat `engine.map` as optional

TMX support is a feature, not a foundation.

You can build:

- a UI application with no maps
- a freeform game with manual layout
- a tilemap game using `engine.map`

The engine should support all three.

### 5. Keep asset policy in the consumer project

The engine accepts an `asset_root`.

That means your project should decide:

- where assets live
- how folders are named
- which fonts and sounds are canonical

### 6. Keep `SceneContext` focused

`SceneContext` exists to expose runtime dependencies:

- `screen`
- `resources`
- `scene_manager`
- `input`
- `ui`
- `audio`
- `music`

It should not become an uncontrolled global state bucket.

### 7. Add to `guigine/` only when it is truly reusable

A good rule:

if a module only makes sense in one project, it should not live in `guigine/`.

## Code Examples

### Minimal App Bootstrap

This is the simplest way to create and run an app:

```python
from pathlib import Path

from guigine.app.app import EngineApp
from guigine.app.config import EngineConfig
from game.scenes.menu_scene import MenuScene


def main() -> None:
    app = EngineApp(
        EngineConfig(
            title="My Game",
            width=1280,
            height=720,
            asset_root=Path("game/assets"),
        )
    )
    app.register_scene("menu", lambda context: MenuScene(context))
    app.start("menu")
    app.run()


if __name__ == "__main__":
    main()
```

### Minimal Scene

```python
import pygame

from guigine.scene.base_scene import BaseScene


class MenuScene(BaseScene):
    def __init__(self, context):
        super().__init__(context, world_width=1280, world_height=720)

    def process_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.scene_manager.start_fade("gameplay", duration=0.25)

    def update(self, dt):
        _ = dt

    def render(self):
        self.screen.fill((20, 24, 30))
```

### ECS Entity Creation

```python
from guigine.components.base import Position, Velocity
from guigine.components.collider import Collider


player = self.entity_manager.create(
    Position(100, 100),
    Velocity(),
    Collider(16, 16),
)
```

### Adding a System to a Scene

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
        self.camera.update(dt)
```

### Loading Resources

```python
button_image = self.resources.load_image("ui/button.png")
font = self.resources.load_font("fonts/MyFont.ttf", 16)
click_sound = self.resources.load_sound("audio/click.wav")
```

### Using Widgets

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

### Loading a TMX Map

```python
from guigine.map.tile_map_loader import TileMapLoader


loader = TileMapLoader(self.resources, walk_layer_name="ground2")
tilemap = loader.load("maps/level_01.tmx")
```

### Spawning Entities from TMX Object Layers

```python
from guigine.ecs.core import Entity
from guigine.components.base import Position
from guigine.components.collider import Collider
from guigine.map.map_entity_spawner import MapEntitySpawner


def crate_factory(obj, entity_manager, tilemap):
    entity = Entity()
    entity.add(
        Position(obj.x, obj.y),
        Collider(int(obj.width), int(obj.height)),
    )
    return entity


spawner = MapEntitySpawner(spawn_tile_layer_entities=True)
spawner.register_factory("props", crate_factory)
spawner.spawn_entities(tilemap, self.entity_manager)
```

## What to Avoid

Avoid these patterns if you want the engine to stay reusable:

- putting game rules inside `guigine/`
- storing project-specific entities in `guigine/`
- hardcoding one story flow into widgets or managers
- making `SceneContext` the global state of the game
- forcing every app to use TMX
- turning managers into oversized god objects

## Examples Included

The `examples/` folder demonstrates three important usage modes:

- no-map gameplay
- TMX-based gameplay
- widget-only UI

Primary entry points:

- [main.py](/abs/path/c:/Users/cavaz/OneDrive/Documentos/Projetos/Projetos_Python/IC/Alexandria/Alexandria_Engine/main.py)
- [examples/run_examples.py](/abs/path/c:/Users/cavaz/OneDrive/Documentos/Projetos/Projetos_Python/IC/Alexandria/Alexandria_Engine/examples/run_examples.py)

## Testing

The automated suite currently covers:

- ECS basics
- `SceneManager`
- `PhysicsSystem`
- `ResourceManager`
- `TileMapLoader`
- `MapEntitySpawner`
- base widgets

Run it with:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Public API Mindset

When deciding whether something belongs in `guigine/`, ask:

- can this be reused across multiple projects?
- does it avoid project-specific semantics?
- does it reduce real structural duplication?
- is the API still small and understandable?

If the answer is "no" for most of those, it probably belongs in the consumer project instead.

## Suggested Next Steps for Consumers

If you want to build on top of this engine, the healthiest next move is:

1. create a separate project folder outside `examples/`
2. keep your assets and scenes there
3. import only `guigine`
4. use `examples/` as reference, not as a dependency

## Summary

Guigine works best when used as:

- a small reusable runtime
- a scene-driven application framework
- a lightweight ECS-based game foundation
- an optional TMX-capable engine, not a TMX-only engine

The separation between `guigine/` and `examples/` is deliberate.

That separation is what makes the engine reusable without requiring any context from the original game it was extracted from.
