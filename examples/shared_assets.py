from __future__ import annotations

from pathlib import Path


def get_examples_asset_root() -> Path:
    return Path(__file__).resolve().parent / "assets"

FONT_PRIMARY = "fonts/PressStart2P-Regular.ttf"

BUTTON_WIDE = "images/buttons/wide.png"
BUTTON_WIDE_PRESSED = "images/buttons/wide_pressed.png"
BUTTON_SHORT = "images/buttons/short.png"
BUTTON_SHORT_PRESSED = "images/buttons/short_pressed.png"

MUSIC_MENU = "sounds/music/main_menu.wav"
MUSIC_WORLD = "sounds/music/home.ogg"
MUSIC_MAP = "sounds/music/home_after.ogg"

SFX_UI_CLICK = "sounds/sfx/ui_click.wav"
SFX_UI_HOVER = "sounds/sfx/ui_hover.wav"
SFX_UI_BACK = "sounds/sfx/ui_back.wav"
SFX_CONFIRM = "sounds/sfx/interact_confirm.wav"
SFX_TYPE = "sounds/sfx/dialogue_type.wav"
