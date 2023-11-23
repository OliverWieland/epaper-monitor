import sys
from enum import Enum
from typing import Any, Optional

import yaml
from PIL import ImageFont

from display.display import Display
from service import Service
from widgets.icon import Icon
from widgets.text import HAlign, Text

Display_height: int = 128
Display_width: int = 296

Border: int = 10
Host = "desktop"
Port = 1883
Id = "battmon"

# Url = (
#     "http://sunjapi:3000/signalk/v1/api/vessels/urn:mrn:imo:mmsi:211868040/electrical/"
# )

Provider_type = "signalk"

Fonts = dict[str, ImageFont.FreeTypeFont]


class Target(Enum):
    Screen = 1
    Epaper = 2


def add_fonts(config: dict[str, Any]) -> Fonts:
    """Add fonts for text widgets.

    Returns:
        Fonts: A dictionary of fonts for text widgets.
    """
    fonts: Fonts = {}

    for font in config:
        fonts[font] = ImageFont.truetype(config[font]["name"], config[font]["size"])
    return fonts


def create_display(target: Target) -> Display:
    """Create a display based on the target.

    Args:
        target (Target): The target display type (Screen or Epaper).

    Returns:
        Display: An instance of the selected display type.
    """
    if target == Target.Epaper:
        from display.epaper import EPaper

        display = EPaper()
    else:
        from display.screen import Screen

        display = Screen(Display_width, Display_height)
    return display


def define_widgets(display: Display, layout: dict[str, Any], fonts: Fonts = {}):
    """Define and add widgets for the display.

    Args:
        display (BaseDisplay): The display to which widgets will be added.
        fonts (Fonts, optional): A dictionary of fonts for text widgets (default is an empty dictionary).

    Returns:
        None
    """

    border = layout.get("border", 10)
    for _, widget in layout["widgets"].items():
        position = tuple[int, int](pos + border for pos in widget["position"])

        if widget["type"] == "icon":
            display.add_widget("", Icon(position, widget["filename"]))
        elif widget["type"] == "text":
            size = tuple[int, int](widget["size"])
            font = fonts[widget["font"]]
            id = widget.get("id", "")
            halign = HAlign[widget.get("halign", "left")]
            suffix = widget.get("suffix", "")
            numeric = widget.get("numeric", False)
            decimal = widget.get("decimal", 1)
            scale = widget.get("scale", 1)

            w = Text(
                position=position,
                size=size,
                font=font,
                halign=halign,
                suffix=suffix,
                is_numeric=numeric,
                decimal=decimal,
                scale=scale,
            )
            display.add_widget(id, w)


def read_yaml_config(file_path: str) -> Optional[dict[str, Any]]:
    try:
        with open(file_path, "r") as file:
            config_data: dict[str, Any] = yaml.safe_load(file)
            return config_data
    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error reading the YAML file: {e}")
        return None


def main(argv: list[str]):
    """Main entry point for the application.

    Args:
        argv (list[str]): Command-line arguments.

    Returns:
        None
    """
    target = Target.Epaper

    if "-s" in argv:
        target = Target.Screen
    display = create_display(target)

    config = read_yaml_config("config.yaml")

    if not config:
        print("No configuration")
        exit()

    fonts = add_fonts(config["config"]["fonts"])
    define_widgets(display, config["layout"], fonts)

    display.update_all_widgets()
    subscriptions = [id for id in display.widgets if not id.startswith("__")]

    if Provider_type == "mqtt":
        from provider.mqtt import MqttProvider

        data_provider = MqttProvider(Host, Port, Id, subscriptions)
    elif Provider_type == "signalk":
        from provider.signalk import SignalKProvider

        data_provider = SignalKProvider(config["config"]["url"], subscriptions)
    else:
        print("Unknown Provider type")
        exit()

    service = Service(data_provider, display)
    service.run()


if __name__ == "__main__":
    main(sys.argv)
