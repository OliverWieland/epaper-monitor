import random
import string
from abc import ABC, abstractmethod

from PIL import Image

from widgets.widget import Widget


def generate_id(length: int = 8) -> str:
    """Generate a random widget ID.

    Args:
        length (int, optional): The length of the generated ID (default is 8).

    Returns:
        str: A randomly generated widget ID.
    """
    return "".join(random.choices(string.ascii_uppercase, k=length))


def create_image(width: int, height: int) -> Image.Image:
    """
    Create a blank PIL (Python Imaging Library) image with the specified dimensions.

    Args:
        width (int): The width of the image.
        height (int): The height of the image.

    Returns:
        Image.Image: A new PIL image with the specified dimensions and an initial
                     background color of black (0). The image is in 1-bit mode (monochrome).

    Example:
        To create a blank image with a width of 200 pixels and a height of 100 pixels:

        >>> image = create_image(200, 100)
    """
    return Image.new("1", (width, height), 0)


class Display(ABC):
    """Base class for managing a display.

    This abstract base class defines the interface and common functionality for managing a display.

    Attributes:
        widgets (dict[str, list[Widget]]): A dictionary of widgets associated with their IDs.

    Methods:
        __init__(self) -> None: Initialize a BaseDisplay instance.
        add_widget(self, id: str, widget: Widget) -> None: Add a widget to the display.
        update(self) -> None: Abstract method to update the display.
        update_all_widgets(self) -> None: Abstract method to update all widgets on the display.
        terminate(self) -> Abstract method to terminate the display.
        update_widget(self, id: str, value: str = "") -> None: Abstract method to update a specific widget
        on the display.

    """

    def __init__(self) -> None:
        """Initialize a BaseDisplay instance.

        Args:
            None

        Returns:
            None
        """
        self.widgets: dict[str, list[Widget]] = {}

    def add_widget(self, id: str, widget: Widget) -> None:
        """Add a widget to the display.

        Args:
            id (str): The ID of the widget to be added.
            widget (Widget): The widget to add to the display.

        Returns:
            None
        """
        if not id:
            id = f"__{generate_id()}"
        if self.widgets.get(id, []) == []:
            self.widgets[id] = []
        self.widgets[id].append(widget)

    @abstractmethod
    def update(self) -> None:
        """Abstract method to update the display.

        This method should be implemented in derived classes to update the display's content.

        Returns:
            None
        """
        pass

    @abstractmethod
    def update_all_widgets(self) -> None:
        """Abstract method to update all widgets on the display.

        This method should be implemented in derived classes to update all widgets on the display.

        Returns:
            None
        """
        pass

    @abstractmethod
    def terminate(self) -> None:
        """Abstract method to terminate the display.

        This method should be implemented in derived classes to terminate the display and perform any necessary cleanup.

        Returns:
            None
        """
        pass

    @abstractmethod
    def update_widget(self, id: str, value: str = "", refresh: bool = True) -> None:
        """Abstract method to update a specific widget on the display.

        This method should be implemented in derived classes to update a specific widget on the display.

        Args:
            id (str): The ID of the widget to update.
            value (str, optional): The new value for the widget (default is an empty string).

        Returns:
            None
        """
        pass

    @abstractmethod
    def refresh(self) -> None:
        pass
