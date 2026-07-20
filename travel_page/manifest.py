from __future__ import annotations

import copy
import json
import re
from pathlib import Path
from typing import Any

import yaml

TRIP_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{2,63}$")
EVIDENCE = {
    "CONFIRMED_LIVE_PRICE", "CURRENT_LISTED_PRICE", "INDICATIVE_PRICE",
    "HISTORICAL_PATTERN", "MODEL_PRIOR", "ESTIMATE", "UNKNOWN",
}


def _load(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text) if path.suffix.lower() in {".yaml", ".yml"} else json.loads(text)


def _resolve(base: Path, value: Any) -> str:
    path = Path(str(value)).expanduser()
    return str(path if path.is_absolute() else (base / path).resolve(strict=False))


def load_travel_manifest(path: str | Path) -> dict[str, Any]:
    manifest_path = Path(path).expanduser().resolve(strict=True)
    raw = _load(manifest_path)
    if not isinstance(raw, dict):
        raise ValueError("travel_manifest_not_object")
    manifest = copy.deepcopy(raw)
    manifest["_manifest_path"] = str(manifest_path)
    if manifest.get("trip_data_ref"):
        manifest["trip_data_ref"] = _resolve(manifest_path.parent, manifest["trip_data_ref"])
    options = manifest.get("backend_options")
    if isinstance(options, dict):
        for key in ("repository_path", "root", "fragment_key_file"):
            if options.get(key):
                options[key] = _resolve(manifest_path.parent, options[key])
    validate_travel_manifest(manifest)
    return manifest


def validate_travel_manifest(manifest: dict[str, Any]) -> None:
    required = {"schema_version", "trip_id", "title", "locale", "publication_profile_id", "publication_mode"}
    if missing := sorted(required - set(manifest)):
        raise ValueError(f"travel_manifest_missing_{missing[0]}")
    if manifest["schema_version"] not in {1, "1", "1.0"}:
        raise ValueError("travel_manifest_version_unsupported")
    if TRIP_ID_RE.fullmatch(str(manifest["trip_id"])) is None:
        raise ValueError("travel_trip_id_invalid")
    if manifest["publication_mode"] not in {"create", "update_owned"}:
        raise ValueError("travel_publication_mode_invalid")
    if not str(manifest["title"]).strip() or not str(manifest["locale"]).strip():
        raise ValueError("travel_manifest_empty_identity")
    if not any(key in manifest for key in ("trip_data", "trip_data_ref", "date_windows", "itinerary")):
        raise ValueError("travel_manifest_missing_trip_content")
    if manifest.get("calendar_event_refs") is not None and not isinstance(manifest["calendar_event_refs"], list):
        raise ValueError("calendar_event_refs_invalid")
    if manifest.get("image_source_metadata") is not None and not isinstance(manifest["image_source_metadata"], (list, dict)):
        raise ValueError("image_source_metadata_invalid")


def _action(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("trip_action_invalid")
    return {
        "label": str(value.get("label") or "Відкрити"),
        "url": str(value.get("url") or "#"),
        **({"kind": value["kind"]} if value.get("kind") else {}),
    }


def _day(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("trip_day_invalid")
    return {
        "title": str(value.get("title") or value.get("name") or "День"),
        "meta": str(value.get("meta") or value.get("time") or ""),
        "text": str(value.get("text") or value.get("description") or ""),
        **({"image": str(value["image"])} if value.get("image") else {}),
        "actions": [_action(item) for item in value.get("actions", [])],
    }


def _window(value: Any, *, fallback_itinerary: list[Any] | None = None, fallback_cost: float = 0, fallback_evidence: str = "UNKNOWN") -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("date_window_invalid")
    days = int(value.get("days") or max(1, len(value.get("itinerary") or fallback_itinerary or [])))
    nights = int(value.get("nights") if value.get("nights") is not None else max(0, days - 1))
    evidence = str(value.get("priceEvidence") or value.get("price_evidence") or fallback_evidence or "UNKNOWN")
    if evidence not in EVIDENCE:
        raise ValueError("price_evidence_invalid")
    itinerary = value.get("itinerary") or fallback_itinerary or []
    return {
        "id": str(value.get("id") or "primary"),
        "shortLabel": str(value.get("shortLabel") or value.get("short_label") or value.get("label") or "Основний"),
        "label": str(value.get("label") or value.get("shortLabel") or value.get("short_label") or "Основний варіант"),
        "dateRangeLong": str(value.get("dateRangeLong") or value.get("date_range_long") or value.get("dates") or "Дати уточнюються"),
        "days": days,
        "nights": nights,
        "workdays": int(value.get("workdays") or value.get("work_days") or 0),
        "format": str(value.get("format") or "Самостійна поїздка"),
        "status": str(value.get("status") or "Кандидат"),
        "totalForTwo": float(value.get("totalForTwo") if value.get("totalForTwo") is not None else value.get("total_for_two", fallback_cost)),
        "priceEvidence": evidence,
        "checkedAt": str(value.get("checkedAt") or value.get("checked_at") or "UNKNOWN"),
        "actions": [_action(item) for item in value.get("actions", [])],
        "budget": [
            {"label": str(item.get("label") or "Витрати"), "amount": float(item.get("amount") or 0)}
            for item in value.get("budget", []) if isinstance(item, dict)
        ],
        "itinerary": [_day(item) for item in itinerary],
    }


def _load_trip_data(manifest: dict[str, Any]) -> dict[str, Any] | None:
    if isinstance(manifest.get("trip_data"), dict):
        return copy.deepcopy(manifest["trip_data"])
    if manifest.get("trip_data_ref"):
        value = _load(Path(str(manifest["trip_data_ref"])))
        if not isinstance(value, dict):
            raise ValueError("trip_data_not_object")
        return value
    return None


def normalize_trip_data(manifest: dict[str, Any]) -> dict[str, Any]:
    existing = _load_trip_data(manifest)
    if existing is not None:
        existing.setdefault("schemaVersion", "1.1")
        existing.setdefault("locale", manifest["locale"])
        existing.setdefault("title", manifest["title"])
        validate_trip_data(existing)
        return existing

    metadata = manifest.get("image_source_metadata") or []
    if isinstance(metadata, dict):
        metadata = list(metadata.values())
    gallery = copy.deepcopy(manifest.get("gallery") or [])
    if not gallery:
        for item in metadata:
            if isinstance(item, dict) and item.get("asset_url"):
                gallery.append({"src": str(item["asset_url"]), "alt": str(item.get("alt_text") or item.get("subject") or "Фото подорожі")})
    fallback_evidence = str(manifest.get("evidence") or "UNKNOWN")
    fallback_cost = float(manifest.get("cost_for_two") or 0)
    windows_raw = manifest.get("date_windows") or [{
        "id": str(manifest.get("selected_default_window") or "primary"),
        "itinerary": manifest.get("itinerary") or [],
        "total_for_two": fallback_cost,
        "price_evidence": fallback_evidence,
    }]
    windows = [
        _window(item, fallback_itinerary=manifest.get("itinerary"), fallback_cost=fallback_cost, fallback_evidence=fallback_evidence)
        for item in windows_raw
    ]
    first = windows[0]
    data = {
        "schemaVersion": "1.1",
        "locale": str(manifest["locale"]),
        "currency": str(manifest.get("currency") or "EUR"),
        "mode": str(manifest.get("mode") or "candidate"),
        "modeLabel": str(manifest.get("mode_label") or "Кандидат"),
        "metaTitle": str(manifest.get("meta_title") or manifest["title"]),
        "eyebrow": str(manifest.get("eyebrow") or "Мініплан подорожі"),
        "title": str(manifest["title"]),
        "subtitle": str(manifest.get("subtitle") or "Практичний маршрут, бюджет і перевірки"),
        "gallery": gallery,
        "heroFacts": list(manifest.get("hero_facts") or [
            f"{first['days']} днів / {first['nights']} ночі",
            f"{first['workdays']} робочі дні",
            first["format"],
        ]),
        "why": str(manifest.get("why") or "Стислий практичний план без припущення про бронювання."),
        "highlights": copy.deepcopy(manifest.get("highlights") or []),
        "route": copy.deepcopy(manifest.get("route") or []),
        "stays": copy.deepcopy(manifest.get("stays") or []),
        "activities": copy.deepcopy(manifest.get("activities") or []),
        "included": list(manifest.get("included") or []),
        "excluded": list(manifest.get("excluded") or []),
        "practical": copy.deepcopy(manifest.get("practical") or []),
        "sources": copy.deepcopy(manifest.get("sources") or []),
        "dateWindows": windows,
    }
    validate_trip_data(data)
    return data


def validate_trip_data(data: dict[str, Any]) -> None:
    required = {
        "schemaVersion", "locale", "currency", "mode", "modeLabel", "title", "subtitle",
        "gallery", "heroFacts", "why", "highlights", "route", "stays", "included", "excluded",
        "practical", "sources", "dateWindows",
    }
    if missing := sorted(required - set(data)):
        raise ValueError(f"trip_data_missing_{missing[0]}")
    if data["schemaVersion"] != "1.1":
        raise ValueError("trip_data_schema_version")
    if not data["gallery"]:
        raise ValueError("trip_gallery_empty")
    if not data["dateWindows"]:
        raise ValueError("trip_windows_empty")
    for window in data["dateWindows"]:
        if not window.get("itinerary"):
            raise ValueError("trip_itinerary_empty")
        if str(window.get("priceEvidence")) not in EVIDENCE:
            raise ValueError("trip_price_evidence_invalid")
    try:
        import jsonschema
    except ImportError:
        return
    schema_path = Path(__file__).resolve().parents[1] / "web" / "trip-page" / "schema" / "trip-page.schema.json"
    if schema_path.is_file():
        try:
            jsonschema.validate(data, json.loads(schema_path.read_text(encoding="utf-8")))
        except jsonschema.ValidationError as exc:
            raise ValueError("trip_data_schema_invalid") from exc
