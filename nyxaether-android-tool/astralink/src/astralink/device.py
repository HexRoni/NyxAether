from __future__ import annotations
from .adb_client import ADBClient, ADBError

class Device:
    def __init__(self, adb: ADBClient, serial: str | None = None):
        self.adb = adb
        self.serial = serial

    def choose_authorized(self) -> str:
        rows = self.adb.devices()
        ready = [r for r in rows if r["state"] == "device"]
        if self.serial:
            if any(r["serial"] == self.serial for r in ready):
                return self.serial
            raise ADBError(f"Selected device {self.serial!r} is not authorized/connected.")
        if len(ready) == 1:
            self.serial = ready[0]["serial"]
            return self.serial
        if not ready:
            raise ADBError("No authorized ADB device. Approve the debugging prompt on the phone.")
        raise ADBError("Multiple authorized devices found. Select one with --serial SERIAL.")

    def prop(self, name: str) -> str:
        serial = self.choose_authorized()
        return self.adb.shell(serial, ["getprop", name]).strip()

    def info(self) -> dict[str, str]:
        return {
            "serial": self.choose_authorized(),
            "manufacturer": self.prop("ro.product.manufacturer"),
            "model": self.prop("ro.product.model"),
            "android_release": self.prop("ro.build.version.release"),
            "sdk": self.prop("ro.build.version.sdk"),
            "build_fingerprint": self.prop("ro.build.fingerprint"),
        }

    def battery(self) -> str:
        return self.adb.shell(self.choose_authorized(), ["dumpsys", "battery"]).strip()

    def storage(self) -> str:
        return self.adb.shell(self.choose_authorized(), ["df", "-h", "/data"]).strip()

    def apps(self) -> list[str]:
        output = self.adb.shell(self.choose_authorized(), ["pm", "list", "packages", "-3"])
        return sorted(line.removeprefix("package:").strip()
                      for line in output.splitlines() if line.strip())

    def screenshot(self, path: str = "screenshots/astralink.png") -> str:
        from pathlib import Path
        import subprocess
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        data = self.adb.exec_out_bytes(self.choose_authorized(), ["screencap", "-p"])
        if not data.startswith(b"\x89PNG\r\n\x1a\n"):
            raise ADBError("Device did not return a valid PNG screenshot.")
        target.write_bytes(data)
        return str(target)

    def logcat(self, lines: int = 500) -> str:
        if not 1 <= lines <= 10000:
            raise ValueError("lines must be between 1 and 10000")
        return self.adb.run(["-s", self.choose_authorized(), "logcat", "-d", "-t", str(lines)])

    def pull(self, remote: str, local: str) -> str:
        return self.adb.run(["-s", self.choose_authorized(), "pull", remote, local]).strip()

    def push(self, local: str, remote: str) -> str:
        return self.adb.run(["-s", self.choose_authorized(), "push", local, remote]).strip()
