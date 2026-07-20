from __future__ import annotations

import hashlib
import json
import os
import shlex
import subprocess
import tempfile
from pathlib import Path
from typing import Any


def _private_root() -> Path:
    root = Path(os.environ.get("TRAVEL_CALENDAR_OUTBOX", Path.home() / ".local" / "share" / "travel" / "calendar-outbox")).expanduser().resolve(strict=False)
    root.mkdir(parents=True, exist_ok=True)
    try:
        root.chmod(0o700)
    except OSError:
        pass
    return root


def _event_ids(config: dict[str, Any]) -> list[str]:
    values = config.get("event_refs") or []
    result = []
    for item in values:
        value = item.get("event_id") if isinstance(item, dict) else item
        if value and str(value) not in result:
            result.append(str(value))
    return result


def calendar_link_action(receipt: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    private_url = str(receipt.get("private_url") or "")
    if not private_url.startswith("https://") or "#k=" not in private_url:
        raise ValueError("verified_private_url_missing")
    events = _event_ids(config)
    if not events:
        return {"calendar_status": "SKIPPED", "event_count": 0}
    payload = {
        "schema": "travel.calendar_link_action.v1",
        "event_refs": events,
        "private_url": private_url,
        "date_selectors": config.get("date_selectors") or {},
        "preserve": ["title", "start", "end", "transparency", "visibility", "attendees", "reminders"],
        "forbid": ["create_event", "duplicate_event", "add_google_meet", "change_dates"],
        "revision": receipt.get("revision"),
    }
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    payload["idempotency_key"] = digest
    root = _private_root()
    outbox = root / f"{digest}.json"
    if not outbox.exists():
        fd, temp_name = tempfile.mkstemp(prefix="calendar-", suffix=".tmp", dir=root)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, sort_keys=True, ensure_ascii=False)
                handle.write("\n")
            Path(temp_name).chmod(0o600)
            Path(temp_name).replace(outbox)
        finally:
            Path(temp_name).unlink(missing_ok=True)
    bridge = os.environ.get("TRAVEL_CALENDAR_BRIDGE_COMMAND", "").strip()
    if bridge:
        result = subprocess.run(shlex.split(bridge), input=json.dumps(payload), text=True, capture_output=True, timeout=60, check=False)
        if result.returncode != 0:
            raise RuntimeError("calendar_bridge_failed")
        try:
            bridge_result = json.loads(result.stdout or "{}")
        except json.JSONDecodeError as exc:
            raise RuntimeError("calendar_bridge_invalid_result") from exc
        if bridge_result.get("status") not in {"DONE", "NO_CHANGE"}:
            raise RuntimeError("calendar_bridge_not_completed")
        return {"calendar_status": bridge_result["status"], "event_count": len(events), "idempotency_key": digest}
    return {"calendar_status": "QUEUED", "event_count": len(events), "idempotency_key": digest}
