import sys
from enum import Enum

from PIL import ImageFont

from display.display import BaseDisplay
from provider import MqttProvider, SignalKProvider
from service import Service
from widgets.icon import Icon
from widgets.text import HAlign, Text

Display_height: int = 128
Display_width: int = 296

Border: int = 10
Host = "desktop"
Port = 1883
Id = "battmon"

Url = (
    "http://sunjapi:3000/signalk/v1/api/vessels/urn:mrn:imo:mmsi:211868040/electrical/"
)


Fonts = dict[str, ImageFont.FreeTypeFont]


class Target(Enum):
    Screen = 1
    Epaper = 2


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

    fonts = add_fonts()
    define_widgets(display, fonts)

    display.update_all_widgets()
    subscriptions = [id for id in display.widgets if not id.startswith("__")]

    #    provider = MqttProvider(Host, Port, Id, subscriptions)
    provider = SignalKProvider(Url, subscriptions)
    service = Service(provider, display)
    service.run()


def add_fonts():
    """Add fonts for text widgets.

    Returns:
        Fonts: A dictionary of fonts for text widgets.
    """
    fonts: Fonts = {}
    fonts["font16"] = ImageFont.truetype("FreeSans", 16)
    fonts["font24"] = ImageFont.truetype("FreeSans", 24)
    return fonts


def create_display(target: Target) -> BaseDisplay:
    """Create a display based on the target.

    Args:
        target (Target): The target display type (Screen or Epaper).

    Returns:
        BaseDisplay: An instance of the selected display type.
    """
    if target == Target.Epaper:
        from display.epaper import EPaper

        display = EPaper()
    else:
        from display.screen import Screen

        display = Screen(Display_width, Display_height)
    return display


def define_widgets(display: BaseDisplay, fonts: Fonts = {}):
    """Define and add widgets for the display.

    Args:
        display (BaseDisplay): The display to which widgets will be added.
        fonts (Fonts, optional): A dictionary of fonts for text widgets (default is an empty dictionary).

    Returns:
        None
    """
    # ---------------------------------------
    # Battery image
    position = (Border, Border)
    widget = Icon(position=position, filename="icons/battery.bmp")
    display.add_widget("", widget)

    # ---------------------------------------
    # Battery load
    position = (Border + 36, Border + 4)
    size = (80, 24)
    widget = Text(
        position=position,
        size=size,
        font=fonts["font24"],
        halign=HAlign.right,
        suffix="%",
        is_numeric=True,
        decimal=0,
        scale=100,
    )
    display.add_widget(
        id="batteries/SHUNT/capacity/stateOfCharge/value",
        widget=widget,
    )

    # ---------------------------------------
    # Battery voltage
    position = (Border + 116, Border + 4)
    size = (80, 24)
    widget = Text(
        position=position,
        size=size,
        font=fonts["font24"],
        halign=HAlign.right,
        suffix="V",
        is_numeric=True,
        decimal=1,
    )
    display.add_widget(
        "batteries/SHUNT/voltage/value",
        widget,
    )

    # ---------------------------------------
    # Battery current
    position = (Border + 196, Border + 4)
    size = (80, 24)
    widget = Text(
        position=position,
        size=size,
        font=fonts["font24"],
        halign=HAlign.right,
        suffix="A",
        is_numeric=True,
        decimal=1,
    )
    display.add_widget(
        "batteries/SHUNT/current/value",
        widget,
    )

    # ---------------------------------------
    # Solar image
    position = (Border, Border + 40)
    widget = Icon(position=position, filename="icons/solar.bmp")
    display.add_widget("", widget)

    # ---------------------------------------
    # Solar power
    position = (Border + 36, Border + 44)
    size = (80, 24)
    widget = Text(
        position=position,
        size=size,
        font=fonts["font24"],
        halign=HAlign.right,
        suffix="W",
        is_numeric=True,
        decimal=0,
    )
    display.add_widget(
        "solar/MPPT/panelPower/value",
        widget,
    )

    # ---------------------------------------
    # Solar voltage
    position = (Border + 116, Border + 44)
    size = (80, 24)
    widget = Text(
        position=position,
        size=size,
        font=fonts["font24"],
        halign=HAlign.right,
        suffix="V",
        is_numeric=True,
        decimal=1,
    )
    display.add_widget(
        "solar/MPPT/voltage/value",
        widget,
    )

    # ---------------------------------------
    # Solar current
    position = (Border + 196, Border + 44)
    size = (80, 24)
    widget = Text(
        position=position,
        size=size,
        font=fonts["font24"],
        halign=HAlign.right,
        suffix="A",
        is_numeric=True,
        decimal=1,
    )
    display.add_widget(
        "solar/MPPT/current/value",
        widget,
    )


if __name__ == "__main__":
    main(sys.argv)
