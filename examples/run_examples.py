import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from guigine.app.app import EngineApp
from guigine.app.config import EngineConfig
from examples.basic_scene import BasicScene
from examples.shared_assets import get_examples_asset_root
from examples.splash_scene import SplashScene
from examples.tmx_scene import TmxScene
from examples.widgets_only_scene import WidgetsOnlyScene


def main() -> None:
    app = EngineApp(
        EngineConfig(
            title="Guigine Examples",
            asset_root=get_examples_asset_root(),
        )
    )
    app.register_scene("splash", lambda context: SplashScene(context))
    app.register_scene("basic", lambda context: BasicScene(context))
    app.register_scene("tmx_demo", lambda context: TmxScene(context))
    app.register_scene("widgets_only", lambda context: WidgetsOnlyScene(context))
    app.start("splash")
    app.run()


if __name__ == "__main__":
    main()
