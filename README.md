# E-Ink Display Demo

The **E-Ink Display Demo** is a Python application that provides a graphical user interface for monitoring data on an e-ink (e-paper) display on a Raspberry Pi. This README provides an overview of the application and instructions for running it.

## Features

- As for now, the application displays data provided by MQTT or SignalK, other providers can easily be integrated
- Supports [Waveshare 2.9 inch e-paper module](https://www.waveshare.com/wiki/2.9inch_e-Paper_Module) on a Raspberry Pi, other compatible Waveshare modules should work out of the box with the appropriate python module (https://github.com/waveshare/e-Paper.git)
- For development, you can also output the image on your screen

## Prerequisites

Before running the application, you need to ensure you have the following dependencies installed:

- Python 3.x
- [Pillow](https://pillow.readthedocs.io/en/stable/index.html) (PIL Fork) for image processing.
- [Paho-MQTT](https://pypi.org/project/paho-mqtt/) Eclipse Paho MQTT Python client library.
- Display drivers compatible with e-paper displays for your hardware (driver code for [Waveshare 2.9 inch e-paper module](https://www.waveshare.com/wiki/2.9inch_e-Paper_Module) is included, other compatible Waveshare modules can integrated easily with the appropriate python module)

## Installation

1. Clone or download the repository to your local machine.

2. Install the required Python packages using `pip`:

   ```shell
   pip install pillow paho-mqtt
   ```

3. Ensure you have the appropriate display driver installed for your e-paper display hardware.

## Configuration

The application allows you to configure various settings. You can modify the following parameters in the `main` function of the `app.py` script:

- `Display_height` and `Display_width`: Set the dimensions of your e-paper display (only used for testing purposes, when you want to output the image on your development system).
- `Border`: Define the border size for the graphics.
- `Host`, `Port`, and `Id`: Configure MQTT broker connection details.

## Usage

Run the application by executing the `epaper_demo.py` script:

```shell
python epaper_demo.py
```
or, for output on your development system,
```shell
python epaper_demo.py -s
```

## Widgets

The application includes various widgets:
- Text
- Progress bar
- Icon

You can customize and extend these widgets as needed.

## Support

For issues and questions related to the e-paper display demo, please create a GitHub issue on the project's repository.

## License

This application is distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

- [Pillow (PIL Fork)](https://pillow.readthedocs.io/en/stable/index.html) for image processing.

Thank you for using the E-Ink Display Demo! This application provides a demonstration of how to display on an e-ink display, and it is designed for learning and development purposes.

For detailed information on how to use the application and customize it to your requirements, please refer to the source code and documentation within this repository.

**Happy E-Ink Display Development!**
