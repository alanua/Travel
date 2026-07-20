from __future__ import annotations

import json
from pathlib import Path

import pytest

from travel_page.calendar_actions import calendar_link_action
from travel_page.cli import prepare_skeleton_manifest
from travel_page.images import prepare_image_metadata
from travel_page.manifest import normalize_trip_data
from travel_page.renderer import render_trip_page


def _manifest(image_url: str = "https://upload.wikimedia.org/demo.jpg"):
    return {
        "schema_version": 1,
        "trip_id": "demo-trip",
        "title": "Демонстраційна поїздка",
        "locale": "uk",
        "publication_profile_id": "github_pages_encrypted_v1",
        "publication_mode": "create",
        "route": [{"title": "Центр", "text": "Піша прогулянка"}],
        "practical": [{"title": "Документи", "text": "Перевірити перед виїздом"}],
        "itinerary": [{"title": "День 1", "meta": "Прибуття", "text": "Спокійний початок", "image": image_url, "actions": []}],
        "cost_for_two": 300,
        "evidence": "ESTIMATE",
        "gallery": [{"src": image_url, "alt": "Міський центр"}],
        "image_source_metadata": [{
            "subject": "Місто", "asset_url": image_url,
            "source_url": "https://commons.wikimedia.org/wiki/File:Demo.jpg",
            "author": "Author", "license": "CC BY-SA 4.0",
            "retrieval_date": "2026-07-20", "alt_text": "Міський центр"
        }],
    }


def _template(root: Path):
    root.mkdir()
    (root / "index.html").write_text('<!doctype html><html><head><title>Trip</title><link rel="manifest" href="manifest.webmanifest"><link rel="stylesheet" href="styles.css"></head><body><section class="hero"><div id="heroGallery"></div></section><section class="intro-block"></section><script src="app.js" defer></script></body></html>', encoding="utf-8")
    (root / "styles.css").write_text(".hero-gallery{}", encoding="utf-8")
    (root / "manifest.webmanifest").write_text("{}", encoding="utf-8")
    app = '''(()=>{"use strict";const state={trip:null};const node=(t,c,v)=>{const e=document.createElement(t);e.className=c||"";if(v!==undefined)e.textContent=v;return e};function renderGallery(){state.trip.gallery.slice(0,3)}async function start(){const dataUrl=new URLSearchParams(location.search).get("data")||"fixtures/synthetic-trip.json";const response=await fetch(dataUrl,{cache:"no-store"});if(!response.ok)throw new Error(`data_load_failed_${response.status}`);state.trip=await response.json();if("serviceWorker"in navigator&&location.protocol==="https:")navigator.serviceWorker.register("service-worker.js").catch(()=>{})}start().catch(error=>{console.error(error)})})();'''
    (root / "app.js").write_text(app, encoding="utf-8")


def test_compact_manifest_normalizes_to_trip_schema():
    data = normalize_trip_data(_manifest())
    assert data["schemaVersion"] == "1.1"
    assert data["dateWindows"][0]["totalForTwo"] == 300
    assert data["dateWindows"][0]["itinerary"][0]["image"].startswith("https://")


def test_renderer_embeds_private_data_and_adds_gallery(tmp_path: Path):
    data = normalize_trip_data(_manifest())
    content = tmp_path / "trip.json"
    content.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    template = tmp_path / "template"
    _template(template)
    output = tmp_path / "out"
    render_trip_page({"content_ref": str(content), "template_options": {"template_root": str(template)}}, output)
    index = (output / "index.html").read_text(encoding="utf-8")
    app = (output / "app.js").read_text(encoding="utf-8")
    styles = (output / "styles.css").read_text(encoding="utf-8")
    assert "__TRAVEL_TRIP_DATA__" in index
    assert 'rel="manifest"' not in index
    assert "fetch(dataUrl" not in app
    assert "slice(0,5)" in app
    assert "renderTravelPhotoGallery" in app
    assert "travel-photo-grid" in styles


def test_image_metadata_is_required_and_source_bounded():
    data = normalize_trip_data(_manifest())
    with pytest.raises(ValueError, match="image_metadata_missing"):
        prepare_image_metadata(data, [])
    assert len(prepare_image_metadata(data, _manifest()["image_source_metadata"])) == 1
    bad = _manifest()["image_source_metadata"]
    bad[0]["source_url"] = "https://unknown.example/photo"
    with pytest.raises(ValueError, match="image_source_not_approved"):
        prepare_image_metadata(data, bad)


def test_skeleton_manifest_contains_renderer_and_calendar_action(tmp_path: Path):
    manifest = _manifest()
    manifest["calendar_event_refs"] = ["event-1", "event-2"]
    skeleton = prepare_skeleton_manifest(manifest, tmp_path / "private")
    assert skeleton["owner_module"] == "travel"
    assert skeleton["template_id"] == "travel_trip_v1"
    assert skeleton["downstream_actions"][0]["action_id"] == "travel_calendar_v1"
    assert Path(skeleton["content_ref"]).stat().st_mode & 0o077 == 0
    assert Path(skeleton["asset_manifest_ref"]).stat().st_mode & 0o077 == 0


def test_calendar_action_is_private_and_idempotent(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("TRAVEL_CALENDAR_OUTBOX", str(tmp_path / "outbox"))
    receipt = {"private_url": "https://example.test/demo/#k=secret", "revision": "abc123"}
    config = {"event_refs": ["event-1", "event-1", {"event_id": "event-2"}]}
    first = calendar_link_action(receipt, config)
    second = calendar_link_action(receipt, config)
    assert first == second
    assert first["calendar_status"] == "QUEUED"
    assert first["event_count"] == 2
    files = list((tmp_path / "outbox").glob("*.json"))
    assert len(files) == 1
    assert files[0].stat().st_mode & 0o077 == 0
    payload = json.loads(files[0].read_text(encoding="utf-8"))
    assert payload["forbid"] == ["create_event", "duplicate_event", "add_google_meet", "change_dates"]
