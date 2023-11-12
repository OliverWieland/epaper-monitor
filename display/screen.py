from PIL import ImageDraw

from display.display import BaseDisplay, create_image


class Screen(BaseDisplay):
    """A class for managing a virtual screen for display testing.

    This class provides functionality for managing a virtual screen used for testing and development purposes.

    Attributes:
        image (Image.Image): The image representing the virtual screen.
        width (int): The width of the virtual screen.
        height (int): The height of the virtual screen.

    Methods:
        __init__(self, width: int, height: int) -> None: Initialize a Screen instance.
        init_display(self) -> None: Initialize the virtual screen.
        update(self) -> None: Update the virtual screen and its widgets.
        update_all_widgets(self) -> None: Update all widgets on the virtual screen.
        update_widget(self, id: str, value: str = "", refresh: bool = True) -> None: Update a specific widget on the
            virtual screen.
        terminate(self) -> None: Terminate and clean up the virtual screen.

    """

    def __init__(self, width: int, height: int) -> None:
        """Initialize a Screen instance.

        Args:
            width (int): The width of the virtual screen.
            height (int): The height of the virtual screen.

        Returns:
            None
        """
        super(Screen, self).__init__()

        self.width: int = width
        self.height: int = height

        self.image = create_image(width, height)
        self.init_display()

    def init_display(self) -> None:
        """Initialize the virtual screen.

        This method sets up the virtual screen by drawing a rectangle on the image to represent the screen outline.

        Returns:
            None
        """
        self.draw = ImageDraw.Draw(self.image)
        self.draw.rectangle((0, 0, self.width - 1, self.height - 1), outline=1)
        self.update()

    def update(self) -> None:
        """Update the virtual screen.

        This method triggers an update of all widgets on the virtual screen.

        Returns:
            None
        """
        self.update_all_widgets()

    def update_all_widgets(self) -> None:
        """Update all widgets on the virtual screen.

        This method updates all registered widgets on the virtual screen and displays the image.

        Returns:
            None
        """
        if not self.widgets:
            return

        for key in self.widgets.keys():
            self.update_widget(key, refresh=False)
        self.image.show()

    def update_widget(self, id: str, value: str = "", refresh: bool = True) -> None:
        """Update a specific widget on the virtual screen.

        Args:
            id (str): The unique identifier of the widget to update.
            value (str, optional): The new value for the widget (default is an empty string).
            refresh (bool, optional): Whether to trigger an immediate display update (default is True).

        Returns:
            None
        """
        for widget in self.widgets[id]:
            widget.update(value)
            position = widget.get_position()
            image = widget.get_image()
            if image is not None:
                self.image.paste(image, position)

        if refresh:
            self.image.show()

    def terminate(self) -> None:
        """Terminate and clean up the virtual screen.

        This method performs any necessary cleanup when terminating the virtual screen.

        Returns:
            None
        """
        pass

    def refresh(self):
        self.image.show()
