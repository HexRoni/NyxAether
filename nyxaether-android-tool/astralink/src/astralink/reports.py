import json
from datetime import datetime, timezone
from pathlib import Path

def save_report(payload: dict, path: str = "reports/diagnostic-report.json") -> str:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    document = {"generated_at": datetime.now(timezone.utc).isoformat(), **payload}
    target.write_text(json.dumps(document, indent=2, ensure_ascii=False), encoding="utf-8")
    return str(target)
