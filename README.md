## Guest notification system - IoT project
This project uses Micropython, a Python implementation for microcontrollers, to build an Internet of Things (IoT) application. The purpose of this project is to fullfil college assignment.

## Prerequisites
- A device that runs Micropython (this project is configured to use ESP8266 stub)
- [Micropy-CLI](https://github.com/BradenM/micropy-cli), a command-line interface for managing Micropython projects. Install it using `pip install micropy-cli`
- [Visual Studio Code](https://code.visualstudio.com/) with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Pymakr - Preview extension](https://marketplace.visualstudio.com/items?itemName=pycom.pymakr-preview) installed

## Getting started
To run the application, first clone this repository to your local machine:

```bash
git clone https://github.com/arville27/iot-guest-notification-system
```
Next, navigate to the root directory of the repository and setup project using micropy.
```bash
cd iot-guest-notification-system
micropy
```
Use the Pymakr extension to upload your code to the device:
Open the command palette (Ctrl+Shift+P) and select "Pymakr > Upload".
Alternatively, use the "Upload" button in the Pymakr toolbar.

## Troubleshooting
If you encounter any issues while using Micropy-CLI or running your Micropython code, here are a few steps you can try:

#### **Outdated Micropy-CLI version**
Make sure that you are using the latest version of Micropy-CLI by running `pip install micropy-cli --upgrade`.
#### **Unknown issue with Micropy-CLI**
Check the Micropy-CLI documentation and see if there are any known issues or troubleshooting tips.
#### **Device-specific issue with Micropython**
Check the Micropython documentation for specific instructions on using Micropython on your device.
#### **Unrecognized builtin python function**
Tweak `.vscode/settings.json`, for my case removing `python.analysis.typeshedPaths` entry, solved the issue.
