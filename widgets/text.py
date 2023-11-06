from enum import Enum
from typing import Optional

from PIL import Image, ImageDraw, ImageFont


class HAlign(Enum):
    """An enumeration representing the horizontal alignment of text.

    Possible values are 'left', 'center', and 'right'.
    """

    left = 0
    center = 1
    right = 2


class Text:
    """A class for creating text visualizations.

    The Text class allows creating text representations with various options
    such as font, alignment, and numeric formatting.
    """

    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        font: ImageFont.ImageFont | ImageFont.FreeTypeFont,
        halign: HAlign = HAlign.left,
        is_numeric: bool = False,
        decimal: int = 0,
        text: str = "",
        suffix: str = "",
    ) -> None:
        """Initialize a Text instance.

        Args:
            position (tuple[int, int]): The position of the text as a tuple (x, y).
            size (tuple[int, int]): The size of the text area as a tuple (width, height).
            font (ImageFont.ImageFont | ImageFont.FreeTypeFont): The font for the text.
            halign (HAlign, optional): The horizontal alignment of the text. Default is left.
            is_numeric (bool, optional): Indicates whether the text is numerically formatted. Default is False.
            decimal (int, optional): The number of decimal places (only relevant for numeric formatting). Default is 0.
            text (str, optional): The initial text content. Default is empty.
            suffix (str, optional): A suffix to be added to the text. Default is empty.

        Returns:
            None
        """
        self.position = position
        self.size = size
        self.font = font
        self.halign = halign
        self.text = text
        self.is_numeric: bool = is_numeric
        self.decimal: int = decimal
        self.suffix = suffix
        self.image: Image.Image = Image.new("1", self.size, 0)

    def update(self, value: str) -> None:
        """Update the text content based on the provided value.

        Args:
            value (str): The value to be displayed.

        Returns:
            None
        """
        draw = ImageDraw.Draw(self.image)
        draw.rectangle(((0, 0), self.size), fill=0)

        value = self.format_text(value)

        width, height = self.get_size(value)

        if width == 0 or height == 0:
            return

        new_image = Image.new("1", (width, height), 0)
        new_draw = ImageDraw.Draw(new_image)
        new_draw.text((0, 0), value, font=self.font, fill=1)

        x = self.align_text(width)

        self.image.paste(new_image, (x, 0))

    def align_text(self, width: int) -> int:
        """Align the text horizontally within the widget's boundaries.

        Args:
            width (int): The width of the text.

        Returns:
            int: The horizontal position (x-coordinate) for aligning the text.
        """
        if self.halign == HAlign.left:
            x = 0
        elif self.halign == HAlign.center:
            x = (self.size[0] - width) // 2
        elif self.halign == HAlign.right:
            x = self.size[0] - width
        else:
            raise ValueError
        return x

    def format_text(self, value: str):
        """Format the text content based on the specified options.

        Args:
            value (str): The value to be formatted.

        Returns:
            str: The formatted text content.
        """
        if not value:
            value = self.text if not self.is_numeric else "0"

        if self.is_numeric:
            if self.decimal > 0:
                value = f"{float(value):.{self.decimal}f}"
            else:
                value = f"{int(round(float(value), self.decimal))}"

        if self.suffix:
            value = " ".join((value, self.suffix))
        return value

    def get_image(self) -> Optional[Image.Image]:
        """Get the image of the text or return None if no image is available.

        Returns:
            Optional[Image.Image]: The image of the text or None.
        """
        return self.image

    def get_position(self) -> tuple[int, int]:
        """Get the position of the text as a tuple (x, y).

        Returns:
            tuple[int, int]: The position of the text.
        """
        return self.position

    def get_size(self, value: str) -> tuple[int, int]:
        """Get the size of the text based on the displayed value.

        Args:
            value (str): The value being displayed.

        Returns:
            tuple[int, int]: The size of the text as a tuple (width, height).
        """
        # https://stackoverflow.com/a/46220683/9263761
        _, descent = self.font.getmetrics()

        mask = self.font.getmask(value)
        bbox = mask.getbbox()
        text_width = bbox[2]
        text_height = bbox[3] + descent

        return text_width, text_height
