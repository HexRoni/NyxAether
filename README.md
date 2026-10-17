# NyxAether — Android Device Management Toolkit

**A lightweight ADB-based Android device management toolkit with a dark, modern interface and practical device diagnostics.**

NyxAether is a Python-based utility designed to help users manage and inspect Android devices through the Android Debug Bridge (ADB). It provides convenient access to common device-management and diagnostic operations, including device information, battery status, installed applications, screenshots, file transfers, and log monitoring.

The project is intended for personal device management, Android development, troubleshooting, and authorized security learning.

> **Important:** NyxAether does not bypass Android security, ADB authorization, device pairing, or USB debugging restrictions. Network connections require the appropriate Android debugging settings and authorization.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running NyxAether](#running-nyxaether)
- [Connecting an Android Device](#connecting-an-android-device)
- [Available Commands](#available-commands)
- [Troubleshooting](#troubleshooting)
- [Security and Privacy](#security-and-privacy)
- [Limitations](#limitations)
- [Disclaimer](#disclaimer)

## Overview

NyxAether provides a convenient interface for working with Android devices using ADB. Instead of manually entering every common diagnostic command, users can access supported device-management functions through the toolkit.

The project is suitable for:

- Android developers and testers.
- Users troubleshooting their own Android devices.
- Students learning about ADB and Android diagnostics.
- Authorized device-management and testing environments.

## Features

Depending on the installed version and available ADB capabilities, NyxAether may provide the following functionality:

- **Device Detection:** Detect Android devices recognized by ADB.
- **Device Information:** Retrieve basic device model, Android version, and related system information.
- **Battery Diagnostics:** Inspect reported battery information.
- **Storage Information:** View available device storage details.
- **Application Management:** List installed packages and inspect available application information.
- **Screenshot Capture:** Capture screenshots from an authorized, connected device.
- **Screen Monitoring:** Access supported screen-monitoring functionality.
- **File Transfer:** Transfer supported files between the computer and Android device.
- **Log Monitoring:** Read supported Android diagnostic logs for troubleshooting.
- **Reports:** Generate structured device information reports where supported.
- **USB and Network Connectivity:** Work with USB-connected devices or properly configured ADB-over-network connections.
- **Auditability:** Keep device-management operations transparent and under the user's control.

Feature availability depends on the project version, operating system, installed dependencies, Android version, and device authorization status.

## Requirements

Before running NyxAether, make sure you have:

- Python 3.10 or a compatible version supported by your project.
- Android Debug Bridge (ADB).
- An Android device that you own or are authorized to manage.
- USB debugging or an appropriately configured wireless debugging connection.
- A compatible terminal or desktop environment.

Some graphical features may require a desktop environment and a working display server.

## Installation

### 1. Kali Linux

Update the package lists and install the required system packages:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv adb git
```

If you have downloaded or cloned the NyxAether repository, navigate to its directory:

```bash
cd NyxAether
```

If the extracted project directory has a different name, replace `NyxAether` with the actual directory name.

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

If the project contains a `pyproject.toml` file and supports installation as a Python package, install it with:

```bash
python -m pip install -e .
```

If the repository instead contains a `requirements.txt` file, install the listed dependencies with:

```bash
python -m pip install -r requirements.txt
```

Use the installation method supported by the files included in your repository. Do not run both commands blindly if the project does not contain the corresponding files.

### 2. Ubuntu or Debian

Install Python, ADB, and the common development tools:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv adb git
```

Then follow the same virtual-environment and project-installation steps described in the Kali Linux section.

### 3. Downloading from GitHub

If the repository is publicly available, clone it with:

```bash
git clone https://github.com/YOUR_USERNAME/NyxAether.git
cd NyxAether
```

Replace `YOUR_USERNAME` with your GitHub username and `NyxAether` with the actual repository name.

If you downloaded a ZIP archive instead, extract it first, then open a terminal inside the extracted project folder.

### 4. Termux on Android

Install the required packages:

```bash
pkg update
pkg upgrade
pkg install python android-tools git
```

Navigate to the project directory and follow the installation instructions supported by the repository.

**Note:** Termux is a command-line environment. Desktop GUI features may not work without additional graphical-environment configuration. USB access and network connectivity also depend on Android and Termux permissions.

## Running NyxAether

The exact launch command depends on the entry-point files included in your repository.

### Option A: Run the Python entry point

If the project contains a `main.py` file:

```bash
python3 main.py
```

If you are using a virtual environment, activate it first:

```bash
source .venv/bin/activate
python main.py
```

### Option B: Run the CLI entry point

If the project contains a `nyxaether.py` script:

```bash
python3 nyxaether.py
```

Use the filename that actually exists in your downloaded project.

### Option C: Run an installed command

If `pyproject.toml` defines a console entry point named `nyxaether`, you may be able to run:

```bash
nyxaether --help
```

This command is applicable only if that entry point is defined by the installed package.

## Connecting an Android Device

### Method 1: USB Connection

1. Open Android Settings.
2. Open **About phone**.
3. Enable Developer Options by following the instructions for your device.
4. Open Developer Options and enable **USB debugging**.
5. Connect the device to your computer with a suitable USB cable.
6. Unlock the Android device.
7. Approve the ADB authorization prompt when it appears.
8. Confirm that ADB recognizes the device.

Check connected devices:

```bash
adb devices
```

A device marked `device` is generally ready for authorized ADB operations.

A device marked `unauthorized` requires approval on the Android device.

### Method 2: Wireless Debugging

On supported Android versions:

1. Connect the computer and Android device to a suitable network.
2. Open Developer Options on Android.
3. Enable **Wireless debugging**.
4. Follow Android's pairing instructions.
5. Use the pairing information displayed by Android.

Pair with the pairing endpoint shown on the Android device:

```bash
adb pair DEVICE_IP:PAIRING_PORT
```

Enter the pairing code when prompted.

After successful pairing, connect using the separate connection endpoint displayed by Android:

```bash
adb connect DEVICE_IP:ADB_PORT
```

Verify the connection:

```bash
adb devices
```

Replace `DEVICE_IP`, `PAIRING_PORT`, and `ADB_PORT` with the actual values shown in Android's Wireless debugging settings.

**Important:** The pairing port and connection port may be different. Do not assume they are interchangeable.

### Method 3: Connecting to an Already-Configured ADB Endpoint

If the Android device already has a supported ADB-over-network endpoint enabled and authorized, connect with:

```bash
adb connect DEVICE_IP:PORT
```

Verify the result:

```bash
adb devices
```

Replace the placeholders with the actual IP address and port.

An IP address alone is not sufficient to establish an authorized connection. The device must be configured to accept the connection.

## Available Commands

The commands below are standard ADB commands that can help verify connectivity and perform basic diagnostics independently of NyxAether.

### Check ADB Installation

```bash
adb version
```

### List Connected Devices

```bash
adb devices
```

Show additional device details:

```bash
adb devices -l
```

### Connect to an Authorized Network Endpoint

```bash
adb connect DEVICE_IP:PORT
```

### Disconnect from a Network Endpoint

```bash
adb disconnect DEVICE_IP:PORT
```

### View Android Device Information

```bash
adb shell getprop ro.product.model
adb shell getprop ro.build.version.release
adb shell getprop ro.build.version.sdk
```

### View Battery Information

```bash
adb shell dumpsys battery
```

### View Storage Information

```bash
adb shell df -h
```

### List Installed Application Packages

```bash
adb shell pm list packages
```

### Capture a Screenshot

```bash
adb shell screencap -p /sdcard/nyxaether-screenshot.png
adb pull /sdcard/nyxaether-screenshot.png .
```

### Read Recent Diagnostic Logs

```bash
adb logcat -d -t 300
```

### Display Connected Device Information

```bash
adb get-state
```

These commands are intended for authorized devices. The commands shown here do not necessarily correspond one-to-one with NyxAether's own command-line interface.

## Troubleshooting

### ADB is not installed

Check whether ADB is available:

```bash
adb version
```

On Kali Linux, Ubuntu, or Debian, install it with:

```bash
sudo apt update
sudo apt install adb
```

### Device shows as unauthorized

- Unlock the Android device.
- Approve the ADB authorization prompt.
- Disconnect and reconnect the USB cable if necessary.
- Check the Android Developer Options settings.

Do not attempt to bypass the device's authorization requirements.

### No devices are detected

Run:

```bash
adb kill-server
adb start-server
adb devices
```

Also check the USB cable, USB mode, debugging settings, and device permissions.

### Wireless connection fails

Check that:

- Wireless debugging is enabled where required.
- The computer and phone can communicate over the network.
- The IP address and port are correct.
- The required pairing process has been completed.
- The network or firewall is not blocking the connection.

### Python dependency errors

Activate the project's virtual environment and install the dependencies declared by the repository.

For a `requirements.txt`-based project:

```bash
python -m pip install -r requirements.txt
```

For a package that supports editable installation:

```bash
python -m pip install -e .
```

### GUI does not open

Check that your operating system has the graphical libraries required by the application and that a graphical desktop session is available.

A command-line environment such as a standard Termux session may not support desktop GUI functionality by default.

## Security and Privacy

NyxAether is designed for transparent and authorized device management.

- Use the toolkit only on devices you own or have explicit permission to manage.
- Keep Android debugging features disabled when they are not needed.
- Approve ADB authorization prompts only for trusted computers.
- Use wireless debugging on trusted networks.
- Avoid sharing logs, screenshots, or reports containing private information.
- Review files before transferring them between devices.
- Do not expose debugging ports to untrusted networks.

If the application uses a password prompt, remember that masking the characters on screen does not by itself provide secure authentication. A password that is identical to the public application name should not be considered a secret.

## Limitations

- NyxAether depends on ADB being installed and available.
- Device operations require the relevant Android permissions and authorization.
- Supported features may vary by Android version and device manufacturer.
- Some operations may be restricted by Android's security model.
- Network connectivity requires appropriate device-side configuration.
- GUI features may be unavailable in terminal-only environments.
- The commands and launch instructions must match the files and entry points included in the specific repository version.

## Disclaimer

NyxAether is provided for educational, diagnostic, development, and authorized device-management purposes.

The author and contributors do not authorize unauthorized access to devices, circumvention of security controls, or activities that violate applicable laws or another person's privacy.

Users are responsible for obtaining permission before accessing or managing any device.

## Author

**X**

## License

Choose and add an appropriate open-source license before redistributing this project. If you intend to use the MIT License, include a `LICENSE` file containing the complete MIT License text and the appropriate copyright notice.
