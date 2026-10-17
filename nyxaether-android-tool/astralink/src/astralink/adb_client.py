from __future__ import annotations
import ipaddress
import shutil
import subprocess
from typing import Sequence

class ADBError(RuntimeError):
    pass

def validate_ip(value: str) -> str:
    try:
        return str(ipaddress.ip_address(value))
    except ValueError as exc:
        raise ValueError("Enter a valid IPv4 or IPv6 address.") from exc

def validate_port(value: int | str) -> int:
    try:
        port = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("Port must be an integer from 1 to 65535.") from exc
    if not 1 <= port <= 65535:
        raise ValueError("Port must be from 1 to 65535.")
    return port

class ADBClient:
    def __init__(self, adb_path: str | None = None, timeout: int = 15):
        self.adb_path = adb_path or shutil.which("adb") or "adb"
        self.timeout = timeout

    def run(self, args: Sequence[str], *, timeout: int | None = None, binary: bool = False):
        command = [self.adb_path, *map(str, args)]
        try:
            result = subprocess.run(
                command, capture_output=True, text=not binary,
                timeout=timeout or self.timeout, check=False, shell=False
            )
        except FileNotFoundError as exc:
            raise ADBError("ADB not found. Install Android Platform Tools first.") from exc
        except subprocess.TimeoutExpired as exc:
            raise ADBError("ADB command timed out.") from exc
        if result.returncode != 0:
            stderr = result.stderr if isinstance(result.stderr, str) else "ADB command failed"
            raise ADBError(stderr.strip() or f"ADB exited with status {result.returncode}")
        return result.stdout

    def devices(self) -> list[dict[str, str]]:
        output = self.run(["devices", "-l"])
        rows = []
        for line in output.splitlines()[1:]:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            rows.append({"serial": parts[0], "state": parts[1],
                         "details": " ".join(parts[2:])})
        return rows

    def connect(self, ip: str, port: int) -> str:
        ip = validate_ip(ip)
        port = validate_port(port)
        return self.run(["connect", f"{ip}:{port}"]).strip()

    def disconnect(self, serial: str | None = None) -> str:
        args = ["disconnect"]
        if serial:
            args.append(serial)
        return self.run(args).strip()

    def shell(self, serial: str, args: Sequence[str]) -> str:
        # Only internal, fixed ADB subcommands call this helper; arbitrary shell
        # input is never exposed by the CLI.
        return self.run(["-s", serial, "shell", *args])

    def exec_out_bytes(self, serial: str, args: Sequence[str]) -> bytes:
        return self.run(["-s", serial, "exec-out", *args], binary=True)
