import json
from time import sleep
from typing import Any

import requests

from provider.provider import Callback

json_data = dict[str, Any]


class SignalKSubscription:
    def __init__(self, topic: str, callback: Callback = None) -> None:
        """Initialize a SignalKSubscription instance.

        Args:
            topic (str): The Signal K topic to subscribe to.
            callback (Callback, optional): The callback function to handle received data (default is None).

        Returns:
            None
        """
        self.topic = topic
        self.path = self.topic.split("/")
        self.callback = callback
        self.value = ""

    def update(self, data: json_data) -> None:
        """Update the subscription data.

        This method updates the subscription data based on the provided data.

        Args:
            data (json_data): The data received from the Signal K server.

        Returns:
            None
        """
        val = data
        for element in self.path:
            val = val.get(element, "")

        str_val = str(val)

        if self.value != str_val:
            self.value = str_val

            if not self.callback:
                return

            self.callback(self.topic, self.value)


class SignalKProvider:
    """A class for providing data through Signal K.

    This class allows connecting to a Signal K server, subscribing to topics, and
    providing data through registered callback functions.

    Attributes:
        url (str): The URL of the Signal K server.
        topics (list[str]): A list of Signal K topics to subscribe to.
        on_data (Callback): The callback function to handle received data.
        request_cycle_time (float): The time interval between consecutive requests to the Signal K server.

    Methods:
        __init__(url: str, subscriptions: list[str] = [], request_cycle_time: float = 10):
        Initialize a SignalKProvider instance.
        connect(): Connect to the Signal K server.
        run(): Start the Signal K data provider.
        eval_response(response: dict[str, Any]) -> list: Evaluate the response from the Signal K server
        and extract relevant data.
        subscribe_topics(): Subscribe to predefined Signal K topics.
        register_callback(callback: Callback): Register a callback function to handle received Signal K data.
        get_subscriptions() -> list[str]: Get a list of subscribed Signal K topics.

    """

    def __init__(
        self,
        url: str,
        subscriptions: list[str] = [],
        request_cycle_time: float = 10,
    ) -> None:
        """Initialize a SignalKProvider instance.

        Args:
            url (str): The URL of the Signal K server.
            subscriptions (list[str], optional): A list of Signal K topics to subscribe to (default is an empty list).
            request_cycle_time (float, optional): The time interval between consecutive requests to the Signal K server
            (default is 10 seconds).

        Returns:
            None
        """
        self.url = url
        self.topics: list[str] = subscriptions
        self.callback: Callback | None = None
        self.request_cycle_time = request_cycle_time
        self.subscriptions: list[SignalKSubscription] = []

        self.data: dict[str, Any] = {topic: 0 for topic in subscriptions}

    def connect(self) -> None:
        """Connect to the Signal K server.

        This method establishes a connection to the Signal K server using the provided URL.

        Returns:
            None
        """
        ...

    def subscribe_topic(self, topic: str) -> None:
        """Subscribe to a Signal K topic.

        This method subscribes to the specified Signal K topic.

        Args:
            topic (str): The Signal K topic to subscribe to.

        Returns:
            None
        """
        self.subscriptions.append(SignalKSubscription(topic, self.callback))

    def register_callback(self, callback: Callback) -> None:
        """Register a callback function to handle received Signal K data.

        Args:
            callback (Callback): The callback function to be registered.

        Returns:
            None
        """
        self.callback = callback

        for topic in self.topics:
            self.subscribe_topic(topic)

    def get_subscriptions(self) -> list[str]:
        """Get a list of subscribed Signal K topics.

        Returns:
            list[str]: A list of Signal K topics to which the Signal K data provider is subscribed.
        """
        ...

    def run(self) -> None:
        """Start the Signal K data provider.

        This method starts the Signal K data provider, which includes subscribing to
        topics and handling incoming Signal K data.

        Returns:
            None
        """
        while True:
            try:
                response = requests.get(self.url, json=True)
                response.raise_for_status()  # Raise an exception for bad responses

                self.eval_response(response.text)
            except requests.exceptions.RequestException as e:
                print(f"Error in HTTP request: {e}")

            sleep(self.request_cycle_time)

    def eval_response(self, response: str) -> None:
        """Evaluate the response from the Signal K server and extract relevant data.

        This method processes the response from the Signal K server and extracts
        data for the subscribed topics.

        Args:
            response (str): The response from the Signal K server.

        Returns:
            None
        """

        json_data = json.loads(response)

        for subscription in self.subscriptions:
            subscription.update(json_data)
