from typing import Protocol

from PIL import Image


class Widget(Protocol):
    """An abstract protocol to be implemented by widgets.

    Widgets can be updated and provide an image and a position.
    """

    def update(self, value: str) -> None:
        """Update the widget's value.

        Args:
            value (str): The value to update the widget with.

        Returns:
            None
        """
        ...

    def get_image(self) -> Image.Image | None:
        """Get the widget's image or return None if no image is available.

        Returns:
            Optional[Image.Image]: The widget's image or None.
        """
        ...

    def get_position(self) -> tuple[int, int]:
        """Get the widget's position as a tuple (x, y).

        Returns:
            tuple[int, int]: The widget's position.
        """
        ...
