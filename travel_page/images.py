from __future__ import annotations

import json
import urllib.parse
from pathlib import Path
from typing import Any, Iterable

APPROVED_SOURCE_HOSTS = (
    "commons.wikimedia.org",
    "wikimedia.org",
    "unsplash.com",
)


def _iter_image_uses(data: dict[str, Any]) -> Iterable[tuple[str, str]]:
    for image in data.get("gallery", []):
        if isinstance(image, dict) and image.get("src"):
            yield str(image["src"]), str(image.get("alt") or "Фото подорожі")
    for item in data.get("highlights", []):
        if isinstance(item, dict) and item.get("image"):
            yield str(item["image"]), str(item.get("title") or "Місце подорожі")
    for group in ("stays", "activities"):
        for item in data.get(group, []):
            if isinstance(item, dict) and item.get("image"):
                yield str(item["image"]), str(item.get("title") or item.get("name") or "Картка подорожі")
    for window in data.get("dateWindows", []):
        for day in window.get("itinerary", []):
            if isinstance(day, dict) and day.get("image"):
                yield str(day["image"]), str(day.get("title") or "День подорожі")


def _metadata_list(raw: Any) -> list[dict[str, Any]]:
    if raw is None:
        return []
    if isinstance(raw, dict):
        raw = list(raw.values())
    if not isinstance(raw, list):
        raise ValueError("image_source_metadata_invalid")
    result = []
    for item in raw:
        if not isinstance(item, dict):
            raise ValueError("image_source_metadata_item_invalid")
        result.append(dict(item))
    return result


def prepare_image_metadata(data: dict[str, Any], raw_metadata: Any) -> list[dict[str, Any]]:
    metadata = _metadata_list(raw_metadata)
    by_asset = {str(item.get("asset_url")): item for item in metadata if item.get("asset_url")}
    used: list[dict[str, Any]] = []
    seen: set[str] = set()
    for url, fallback_alt in _iter_image_uses(data):
        if url in seen:
            continue
        seen.add(url)
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError("image_asset_not_https")
        item = by_asset.get(url)
        if item is None:
            raise ValueError("image_metadata_missing")
        required = {"source_url", "author", "license", "retrieval_date"}
        if missing := sorted(required - set(item)):
            raise ValueError(f"image_metadata_missing_{missing[0]}")
        source = urllib.parse.urlparse(str(item["source_url"]))
        host = source.hostname or ""
        approved = any(host == allowed or host.endswith("." + allowed) for allowed in APPROVED_SOURCE_HOSTS)
        if not approved and not item.get("operator_approved"):
            raise ValueError("image_source_not_approved")
        normalized = {
            "subject": str(item.get("subject") or fallback_alt),
            "asset_url": url,
            "source_url": str(item["source_url"]),
            "author": str(item["author"]),
            "license": str(item["license"]),
            "retrieval_date": str(item["retrieval_date"]),
            "alt_text": str(item.get("alt_text") or fallback_alt),
        }
        used.append(normalized)
    return used


def write_asset_manifest(path: Path, assets: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"assets": assets}, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    path.chmod(0o600)
