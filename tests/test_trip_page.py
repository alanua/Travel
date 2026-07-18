import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web" / "trip-page"


def test_required_assets_exist():
    for name in ("index.html", "styles.css", "app.js", "manifest.webmanifest", "service-worker.js"):
        assert (WEB / name).is_file()


def test_fixture_is_public_safe_and_has_date_windows():
    data = json.loads((WEB / "fixtures" / "synthetic-trip.json").read_text(encoding="utf-8"))
    assert data["mode"] in {"candidate", "planned", "in_trip"}
    assert data["dateWindows"]
    blob = json.dumps(data).lower()
    for forbidden in ("calendar_id", "tailscale", "private_key", "milan", "людмила"):
        assert forbidden not in blob


def test_renderer_uses_safe_dom_apis():
    js = (WEB / "app.js").read_text(encoding="utf-8")
    assert "innerHTML" not in js
    assert "textContent" in js
    assert "noopener noreferrer" in js


def test_mobile_touch_target_and_no_embedded_map():
    css = (WEB / "styles.css").read_text(encoding="utf-8")
    html = (WEB / "index.html").read_text(encoding="utf-8")
    assert "min-height:44px" in css
    assert "<iframe" not in html.lower()
