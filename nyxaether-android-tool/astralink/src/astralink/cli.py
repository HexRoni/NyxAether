from __future__ import annotations
import argparse
import getpass
import json
import sys
from . import APP_NAME, NETWORK_PASSPHRASE
from .adb_client import ADBClient, ADBError, validate_ip, validate_port
from .audit import record
from .device import Device
from .reports import save_report

PURPLE = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"

def startup_gate() -> bool:
    attempt = getpass.getpass(f"{APP_NAME} passphrase: ")
    if attempt != APP_NAME:
        print("Access denied.")
        record("startup_auth_failed")
        return False
    record("startup_auth_ok")
    return True

def network_gate() -> bool:
    attempt = getpass.getpass("Network-mode passphrase: ")
    if attempt != NETWORK_PASSPHRASE:
        print("Access denied.")
        record("network_auth_failed")
        return False
    record("network_auth_ok")
    return True

def menu(adb: ADBClient, serial: str | None = None) -> None:
    print(f"\n{PURPLE}╔══════════════════════════════════════╗{RESET}")
    print(f"{PURPLE}║  {APP_NAME}  •  DARK TERMINAL SUITE     ║{RESET}")
    print(f"{PURPLE}╚══════════════════════════════════════╝{RESET}")
    print(f"{CYAN}Android Network & Device Diagnostics{RESET}")
    print("USB mode requires the device to approve ADB authorization.")
    actions = {
        "1": "devices", "2": "connect", "3": "info", "4": "battery",
        "5": "storage", "6": "apps", "7": "screenshot", "8": "monitor",
        "9": "logcat", "10": "report", "11": "disconnect", "0": "exit"
    }
    while True:
        print("\n1 Devices   2 Quick IP Connect   3 Device info   4 Battery")
        print("5 Storage   6 Third-party apps  7 Screenshot    8 Live monitor")
        print("9 Logcat    10 JSON report     11 Disconnect    0 Exit")
        choice = input("AstraLink> ").strip()
        try:
            if choice == "0":
                return
            if choice == "1":
                print(json.dumps(adb.devices(), indent=2))
            elif choice == "2":
                if not network_gate():
                    continue
                ip = validate_ip(input("Device IP: ").strip())
                port_text = input("ADB port [5555]: ").strip() or "5555"
                port = validate_port(port_text)
                print(adb.connect(ip, port))
                record("network_connect_attempt", f"{ip}:{port}")
                print("If this fails, enable Wireless debugging and use its displayed ADB port; pairing/authorization cannot be bypassed.")
            elif choice == "11":
                print(adb.disconnect())
                record("disconnect")
            elif choice in {"3", "4", "5", "6", "7", "8", "9", "10"}:
                dev = Device(adb, serial)
                if choice == "3":
                    result = dev.info()
                    print(json.dumps(result, indent=2))
                    record("device_info", result.get("serial", ""))
                elif choice == "4":
                    print(dev.battery())
                    record("battery")
                elif choice == "5":
                    print(dev.storage())
                    record("storage")
                elif choice == "6":
                    print("\n".join(dev.apps()))
                    record("list_apps")
                elif choice == "7":
                    path = dev.screenshot()
                    print(f"Saved screenshot: {path}")
                    record("screenshot", path)
                elif choice == "8":
                    from .monitor import monitor_screen
                    monitor_screen(adb, serial)
                    record("screen_monitor")
                elif choice == "9":
                    lines = int(input("Number of log lines (1–10000) [500]: ").strip() or "500")
                    print(dev.logcat(lines))
                    record("logcat", f"lines={lines}")
                elif choice == "10":
                    payload = {"device": dev.info(), "battery": dev.battery(),
                               "storage": dev.storage(), "third_party_apps": dev.apps()}
                    path = save_report(payload)
                    print(f"Saved report: {path}")
                    record("report", path)
            else:
                print("Unknown option.")
        except (ADBError, ValueError, OSError) as exc:
            print(f"Error: {exc}")

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="nyxaether", description="NyxAether Android ADB Utility")
    parser.add_argument("--serial", help="Explicit ADB serial when multiple devices are connected")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("devices")
    connect = sub.add_parser("connect")
    connect.add_argument("ip")
    connect.add_argument("port", type=int)
    sub.add_parser("disconnect")
    for name in ("info", "battery", "storage", "apps", "screenshot", "monitor", "report"):
        sub.add_parser(name)
    logcat = sub.add_parser("logcat")
    logcat.add_argument("--lines", type=int, default=500)
    args = parser.parse_args(argv)
    adb = ADBClient()
    try:
        if not startup_gate():
            raise SystemExit(1)
        if args.command is None:
            menu(adb, args.serial)
        elif args.command == "devices":
            print(json.dumps(adb.devices(), indent=2))
        elif args.command == "connect":
            if network_gate():
                print(adb.connect(validate_ip(args.ip), validate_port(args.port)))
                print("If connection fails, confirm Wireless debugging is enabled and use the port shown on the phone. Pairing/authorization cannot be bypassed.")
                record("network_connect_attempt", f"{args.ip}:{args.port}")
        elif args.command == "disconnect":
            print(adb.disconnect())
            record("disconnect")
        else:
            dev = Device(adb, args.serial)
            if args.command == "info":
                result = dev.info()
                print(json.dumps(result, indent=2))
            elif args.command == "battery":
                print(dev.battery())
            elif args.command == "storage":
                print(dev.storage())
            elif args.command == "apps":
                print("\n".join(dev.apps()))
            elif args.command == "screenshot":
                print(f"Saved screenshot: {dev.screenshot()}")
            elif args.command == "monitor":
                from .monitor import monitor_screen
                monitor_screen(adb, args.serial)
            elif args.command == "logcat":
                print(dev.logcat(args.lines))
            elif args.command == "report":
                path = save_report({"device": dev.info(), "battery": dev.battery(),
                                    "storage": dev.storage(), "third_party_apps": dev.apps()})
                print(f"Saved report: {path}")
            record(args.command)
    except (ADBError, ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)

if __name__ == "__main__":
    main()
