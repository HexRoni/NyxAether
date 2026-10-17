# NyxAether — Dark Terminal Android ADB Suite

NyxAether is a Python-based Android diagnostics and screen-monitoring tool for Kali Linux and Termux. It uses Android Debug Bridge (ADB), and never bypasses Android pairing or authorization.

## Passphrase behavior

The requested hidden-input passphrase is `NyxAether`: `getpass` prevents the characters from being echoed while typing. The same value is used at startup and before network-mode connection attempts. **This is not strong security** because the name is public and is present in the source code. It is a simple access gate only; use a user-chosen secret for real protection.

## Quick IP connect

In the menu choose **2 Quick IP Connect**, enter the phone IP, and press Enter to use port `5555` by default. This makes one connection attempt to that exact IP and port; it does not scan ports. If your phone shows a different ADB port, enter it instead. Android Wireless debugging often uses a dynamic port. First-time pairing may require:

```bash
adb pair PHONE_IP:PAIRING_PORT
# enter the pairing code shown on the phone
adb connect PHONE_IP:ADB_PORT
```

IP alone cannot turn on debugging, bypass the phone's authorization, or connect when no ADB service is listening. The phone and computer generally need to be on the same network.

## Features

- Black/purple terminal branding and hidden passphrase input
- USB device listing and authorized ADB status
- Quick IP connect attempt (defaults to port 5555; no scanning)
- Device model, Android version, SDK, manufacturer and build fingerprint
- Battery and storage summaries; third-party package listing
- User-initiated screenshots and visible live screen monitor
- Bounded logcat snapshots, file transfer, JSON diagnostic reports, local JSONL audit log
- Safe subprocess argument lists (`shell=False`); no arbitrary shell runner, stealth, persistence, exploits, or authorization bypass

## Requirements

- Python 3.10+
- Android Platform Tools (`adb`)
- Tkinter for optional live monitor (Kali: `python3-tk`; availability varies on Termux)

### Kali Linux

```bash
sudo apt update
sudo apt install adb python3 python3-tk
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
nyxaether
```

Or run directly with `python cli.py`.

### Termux

```bash
pkg update
pkg install python android-tools
pip install -e .
nyxaether
```

Termux may not support Tkinter; use screenshots if the live monitor is unavailable.

## CLI examples

```bash
python cli.py devices
python cli.py connect 192.0.2.10 5555
python cli.py info
python cli.py battery
python cli.py storage
python cli.py apps
python cli.py screenshot
python cli.py monitor
python cli.py logcat --lines 500
python cli.py report
python cli.py disconnect
```

## Security and limitations

- Connect only to devices you own or are authorized to administer.
- The app cannot enable Wireless debugging remotely from an IP address alone.
- Use the ADB connection port displayed by the phone; the pairing port and connection port may differ.
- Logs/reports can contain device identifiers and app names; keep them private.
- Screen monitoring is visible and user-initiated.

## Tests

```bash
python -m unittest discover -s tests -v
```

This build has not been tested against a physical Android device.
