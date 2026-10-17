import json
from datetime import datetime, timezone
from pathlib import Path

def record(action: str, detail: str = "", path: str = "astralink_audit.jsonl") -> None:
    row = {"timestamp": datetime.now(timezone.utc).isoformat(),
           "action": action, "detail": detail[:500]}
    with Path(path).open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(row, ensure_ascii=False) + "\n")
