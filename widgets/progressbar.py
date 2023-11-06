from PIL import Image, ImageDraw


class ProgressBar:
    """A class for representing a progress bar.

    This class creates a progress bar that can be updated to display progress.
    """

    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        min: float = 0,
        max: float = 100,
    ) -> None:
        """Initialize a ProgressBar instance.

        Args:
            position (tuple[int, int]): The position of the progress bar as a tuple (x, y).
            size (tuple[int, int]): The size of the progress bar as a tuple (width, height).
            min (float, optional): The minimum progress value. Default is 0.
            max (float, optional): The maximum progress value. Default is 100.

        Returns:
            None
        """
        self.position = position
        self.size = size
        self.min = min
        self.max = max

        self.image = Image.new("1", self.position, 0)
        self.draw = ImageDraw.Draw(self.image)

        self.update(f"{min}")

    def update(self, value: str) -> None:
        """Update the progress bar based on the provided value.

        Args:
            value (str): The progress value to be displayed.

        Returns:
            None
        """
        try:
            val = float(value)
        except ValueError:
            val = self.min
        val = min(max(val, self.min), self.max)
        width = int((val - self.min) / (self.max - self.min) * self.size[0])
        end = (width, self.size[1] - 1)
        frame_end = (self.size[0] - 1, self.size[1] - 1)
        self.draw.rectangle(((0, 0), frame_end), outline=1, fill=0)
        self.draw.rectangle(((0, 0), end), 1)

    def get_image(self) -> Image.Image | None:
        """Get the image of the progress bar or return None if no image is available.

        Returns:
            Optional[Image.Image]: The image of the progress bar or None.
        """
        return self.image

    def get_position(self) -> tuple[int, int]:
        """Get the position of the progress bar as a tuple (x, y).

        Returns:
            tuple[int, int]: The position of the progress bar.
        """
        return self.position
