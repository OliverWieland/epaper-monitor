from typing import Any

import paho.mqtt.client as mqtt

from provider.provider import Callback


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
        self.on_data: Callback | None = None

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
        for topic in self.topics:
            self.subscribe_topic(topic)

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
            self.on_data(message.topic, message.payload.decode("utf-8"))

    def subscribe_topic(self, topic: str) -> None:
        """Subscribe to predefined MQTT topics.

        This method subscribes to the MQTT topics defined in the 'topics' attribute.

        Returns:
            None
        """
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
