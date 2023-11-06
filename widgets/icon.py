from PIL import Image


class Icon:
    """A class for representing an icon.

    This class allows displaying an icon at a specific position.
    """

    def __init__(self, position: tuple[int, int], filename: str) -> None:
        """Initialize an Icon instance.

        Args:
            position (tuple[int, int]): The position of the icon as a tuple (x, y).
            filename (str): The filename of the icon.

        Returns:
            None
        """
        self.position = position

        self.image = Image.open(filename, mode="r")

    def update(self, value: str) -> None:
        """Update the icon (not used).

        Args:
            value (str): The value (not used).

        Returns:
            None
        """
        pass

    def get_image(self) -> Image.Image | None:
        """Get the image of the icon or return None if no image is available.

        Returns:
            Optional[Image.Image]: The image of the icon or None.
        """
        return self.image

    def get_position(self) -> tuple[int, int]:
        """Get the position of the icon as a tuple (x, y).

        Returns:
            tuple[int, int]: The position of the icon.
        """
        return self.position
