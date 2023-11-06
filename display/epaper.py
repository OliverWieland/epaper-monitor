from display.display import BaseDisplay, create_image
from epd.epd2in9_V2 import EPD, EPD_HEIGHT, EPD_WIDTH


class EPaper(BaseDisplay):
    """A class for controlling an e-paper display (EPD).

    This class provides functionality for updating and controlling an e-paper display.

    Attributes:
        image (Image.Image): The image to be displayed on the e-paper screen.

    Methods:
        __init__(self): Initialize an EPaper instance.
        init_display(self) -> None: Initialize the EPD display.
        update(self) -> None: Update and refresh the e-paper display.
        update_all_widgets(self) -> None: Update all widgets on the e-paper display.
        update_widget(self, id: str, value: str = "", refresh: bool = True) -> None: Update a specific widget
        on the e-paper display.
        terminate(self) -> None: Terminate and put the EPD display to sleep.

    """

    def __init__(self):
        """Initialize an EPaper instance.

        Args:
            None

        Returns:
            None
        """
        super(EPaper, self).__init__()

        # The constants defined in the EPD module refer to the portrait format. Therefore they hat to be swapped
        width = EPD_HEIGHT
        height = EPD_WIDTH

        self.image = create_image(width, height)

        self.epd = EPD()
        self.init_display()

    def init_display(self) -> None:
        """Initialize the EPD display.

        This method initializes the e-paper display for use.

        Returns:
            None
        """
        self.epd.init()
        self.epd.Clear(0)

    def update(self) -> None:
        """Update and refresh the e-paper display.

        This method updates all widgets on the e-paper display and triggers a display refresh.

        Returns:
            None
        """
        self.update_all_widgets()
        self.epd.display(self.epd.getbuffer(self.image))
        self.epd.sleep()

    def update_all_widgets(self) -> None:
        """Update all widgets on the e-paper display.

        This method updates all registered widgets on the e-paper display and triggers a display refresh.

        Returns:
            None
        """
        if not self.widgets:
            return

        for key in self.widgets.keys():
            self.update_widget(key, refresh=False)
        self.epd.display(self.epd.getbuffer(self.image))
        self.epd.sleep()

    def update_widget(self, id: str, value: str = "", refresh: bool = True) -> None:
        """Update a specific widget on the e-paper display.

        Args:
            id (str): The unique identifier of the widget to update.
            value (str, optional): The new value for the widget (default is an empty string).
            refresh (bool, optional): Whether to trigger an immediate display refresh (default is True).

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
            self.epd.display_Partial(self.epd.getbuffer(self.image))
            self.epd.sleep()

    def terminate(self) -> None:
        """Terminate and put the EPD display to sleep.

        This method terminates the EPD display and puts it into a sleep state.

        Returns:
            None
        """
        self.init_display()
        self.epd.sleep()
