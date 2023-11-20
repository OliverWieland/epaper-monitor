from dataclasses import dataclass
import json
from time import sleep
from typing import Any, Callable, Protocol
import requests

import paho.mqtt.client as mqtt

subscr_data = list[tuple[str, str]]
Callback = Callable[subscr_data, None] | None


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

    def subscribe_topics(self) -> None:
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


class MqttProvider:
    """A class for providing data through MQTT (Message Queuing Telemetry Transport).

    This class allows connecting to an MQTT broker, subscribing to topics, and
    providing data through registered callback functions.

    Attributes:
        host (str): The MQTT broker host address.
        port (int): The MQTT broker port number (default is 1883).
        topics (list[str]): A list of MQTT topics to subscribe to (default is an empty list).
        on_data (Callback): The callback function to handle received data (default is None).

    Methods:
        __init__(host: str, port: int = 1883, id: str = "", subscriptions: list[str] = []):
        Initialize an MqttProvider instance.
        connect(): Connect to the MQTT broker.
        run(): Start the MQTT data provider.
        on_message(client: mqtt.Client, userdata: Any, message: mqtt.MQTTMessage): Handle incoming MQTT messages.
        subscribe_topics(): Subscribe to predefined MQTT topics.
        get_subscriptions(): Get a list of subscribed MQTT topics.
        register_callback(callback: Callback): Register a callback function to handle received MQTT data.

    """

    def __init__(
        self, host: str, port: int = 1883, id: str = "", subscriptions: list[str] = []
    ) -> None:
        """Initialize an MqttProvider instance.

        Args:
            host (str): The MQTT broker host address.
            port (int, optional): The MQTT broker port number (default is 1883).
            id (str, optional): The client ID for the MQTT connection.
            subscriptions (list[str], optional): A list of MQTT topics to subscribe to (default is an empty list).

        Returns:
            None
        """
        self.host = host
        self.port = port
        self.topics: list[str] = subscriptions
        self.on_data: Callback = None

        self.client = mqtt.Client(client_id=id, clean_session=True)
        self.client.on_message = self.on_message

    def connect(self) -> None:
        """Connect to the MQTT broker.

        This method establishes a connection to the MQTT broker using the provided
        host and port.

        Returns:
            None
        """
        self.client.connect(self.host, self.port)

    def run(self) -> None:
        """Start the MQTT data provider.

        This method starts the MQTT data provider, which includes subscribing to
        topics and handling incoming MQTT messages.

        Returns:
            None
        """
        self.client.loop_start()
        self.subscribe_topics()

    def on_message(
        self, client: mqtt.Client, userdata: Any, message: mqtt.MQTTMessage
    ) -> None:
        """Handle incoming MQTT messages.

        This method is called when an MQTT message is received. It prints the message
        and, if a callback function is registered, passes the message's topic and payload
        to the callback.

        Args:
            client (mqtt.Client): The MQTT client.
            userdata (Any): User data.
            message (mqtt.MQTTMessage): The received MQTT message.

        Returns:
            None
        """
        print(message)
        if self.on_data is not None:
            self.on_data([(message.topic, message.payload.decode("utf-8"))])

    def subscribe_topics(self) -> None:
        """Subscribe to predefined MQTT topics.

        This method subscribes to the MQTT topics defined in the 'topics' attribute.

        Returns:
            None
        """
        for topic in self.topics:
            if topic:
                self.client.subscribe(topic)

    def get_subscriptions(self) -> list[str]:
        """Get a list of subscribed MQTT topics.

        Returns:
            list[str]: A list of MQTT topics to which the MQTT data provider is subscribed.
        """
        return self.topics

    def register_callback(self, callback: Callback) -> None:
        """Register a callback function to handle received MQTT data.

        Args:
            callback (Callback): The callback function to be registered.

        Returns:
            None
        """
        self.on_data = callback


@dataclass
class Data:
    topic: str
    value: any


class SignalKProvider:
    def __init__(
        self,
        url: str,
        subscriptions: list[str] = [],
        request_cycle_time: float = 10,
    ) -> None:
        self.url = url
        self.topics: list[str] = subscriptions
        self.on_data: Callback = None
        self.request_cycle_time = request_cycle_time

        self.data = {}

        for topic in subscriptions:
            self.data[topic] = 0

    def connect(self) -> None:
        self.client.connect(self.host, self.port)

    def subscribe_topics(self) -> None:
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
        self.on_data = callback

    def get_subscriptions(self) -> list[str]:
        """Get a list of subscribed topics.

        Returns:
            list[str]: A list of topics to which the data provider is subscribed.
        """
        ...

    def run(self) -> None:
        """Start running the data provider.

        This method should start the data provider's main loop or execution.

        Returns:
            None
        """
        while True:
            response = requests.get(self.url)
            if response.status_code == 200:
                obj = json.loads(response.text)

                data = self.eval_response(obj)
                if self.on_data is not None:
                    self.on_data(data)

            sleep(self.request_cycle_time)

    def eval_response(self, response: dict[str, Any]) -> list:
        data = []

        for topic in self.topics:
            path = topic.split("/")

            value = response
            for element in path:
                value = value.get(element, "")

            if self.data[topic] != value:
                data.append((topic, value))
                self.data[topic] = value

        return data
