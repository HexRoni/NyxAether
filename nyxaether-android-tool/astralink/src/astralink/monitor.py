from __future__ import annotations
import base64
import tkinter as tk
from tkinter import messagebox
from .adb_client import ADBClient, ADBError
from .device import Device

def monitor_screen(adb: ADBClient, serial: str | None = None, interval_ms: int = 1000) -> None:
    """Visible Tk window; periodically fetches a screenshot from an authorized device."""
    device = Device(adb, serial)
    device.choose_authorized()
    root = tk.Tk()
    root.title("AstraLink — Live Screen Monitor")
    root.geometry("520x850")
    heading = tk.Label(root, text=f"AstraLink • Visible monitor • {device.serial}",
                       font=("TkDefaultFont", 10, "bold"))
    heading.pack(padx=8, pady=8)
    image_label = tk.Label(root, text="Waiting for screenshot…")
    image_label.pack(expand=True, fill="both", padx=8, pady=8)
    status = tk.Label(root, text="Close this window to stop monitoring.")
    status.pack(padx=8, pady=8)
    state = {"running": True, "image": None}

    def update_frame():
        if not state["running"]:
            return
        try:
            png = adb.exec_out_bytes(device.serial, ["screencap", "-p"])
            state["image"] = tk.PhotoImage(data=base64.b64encode(png))
            image_label.configure(image=state["image"], text="")
            status.configure(text="Monitoring active • close window to stop")
        except Exception as exc:
            status.configure(text=f"Monitor paused: {str(exc)[:140]}")
        root.after(interval_ms, update_frame)

    def close():
        state["running"] = False
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", close)
    root.after(100, update_frame)
    root.mainloop()
