import time

from display.display import Display
from provider.provider import Provider


class Service:
    def __init__(self, provider: Provider, display: Display) -> None:
        """Initialize a Service instance.

        Args:
            provider (Provider): The data provider to connect to.
            display (BaseDisplay): The display to update with data.

        Returns:
            None
        """
        self.provider = provider
        self.display = display
        self.provider.register_callback(self.callback)

    def quit(self):
        """Terminate and clean up the service.

        This method terminates and cleans up the service and its components.

        Returns:
            None
        """
        self.display.terminate()

    def callback(self, topic: str, value: str) -> None:
        """Callback function to handle data updates.

        This method is called when the data provider receives new data. It updates the display with the data.

        Args:
            id (str): The unique identifier of the data.
            value (str): The value of the data.

        Returns:
            None
        """

        self.display.update_widget(topic, value, False)
        self.display.refresh()

    def run(self):
        """Start the service, connect the data provider, and run the main loop.

        This method starts the service, establishes a connection to the data provider, and runs the main service loop.

        Returns:
            None
        """
        try:
            self.provider.connect()
            self.provider.run()

            while True:
                time.sleep(0.1)
                pass

        except KeyboardInterrupt:
            self.quit()
