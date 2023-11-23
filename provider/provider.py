from typing import Callable, Protocol, TypeAlias

subscription_data = str | int | float
subscription: TypeAlias = tuple[str, subscription_data]
Callback: TypeAlias = Callable[[str, str], None] | None


class Provider(Protocol):
    """An abstract protocol for data provider classes.

    This protocol defines the common interface for data provider classes
    that can subscribe to topics, register callbacks, connect, and run.

    Attributes:
        None

    Methods:
        subscribe_topics(): Subscribe to predefined topics.
        register_callback(callback: Callback): Register a callback function to handle received data.
        get_subscriptions(): Get a list of subscribed topics.
        connect(): Connect to the data source.
        run(): Start running the data provider.

    """

    def subscribe_topic(self, topic: str) -> None:
        """Subscribe to predefined topics.

        This method should implement the logic to subscribe to specific topics
        relevant to the data provider.

        Returns:
            None
        """
        ...

    def register_callback(self, callback: Callback) -> None:
        """Register a callback function to handle received data.

        Args:
            callback (Callback): The callback function to be registered.

        Returns:
            None
        """
        ...

    def get_subscriptions(self) -> list[str]:
        """Get a list of subscribed topics.

        Returns:
            list[str]: A list of topics to which the data provider is subscribed.
        """
        ...

    def connect(self) -> None:
        """Connect to the data source.

        This method should implement the logic to establish a connection to
        the data source.

        Returns:
            None
        """
        ...

    def run(self) -> None:
        """Start running the data provider.

        This method should start the data provider's main loop or execution.

        Returns:
            None
        """
        ...
