#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WEB = ROOT / "web" / "trip-page"
FIXTURE = WEB / "fixtures" / "synthetic-trip.json"


def main() -> int:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    required = {"title", "dateWindows", "gallery", "route"}
    missing = sorted(required - set(data))
    if missing:
        raise SystemExit(f"missing fields: {missing}")
    if not all(window.get("itinerary") for window in data["dateWindows"]):
        raise SystemExit("missing itinerary")
    if not (WEB / "index.html").is_file():
        raise SystemExit("missing index.html")
    print(json.dumps({"status": "ok", "date_windows": len(data["dateWindows"]), "title": data["title"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
