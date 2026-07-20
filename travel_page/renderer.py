from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Any


def _default_template_root() -> Path:
    return Path(__file__).resolve().parents[1] / "web" / "trip-page"


def _json_for_script(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def render_trip_page(manifest: dict[str, Any], output_dir: Path) -> None:
    content_path = Path(str(manifest["content_ref"]))
    if not content_path.is_file():
        raise ValueError("travel_content_ref_missing")
    data = json.loads(content_path.read_text(encoding="utf-8"))
    options = manifest.get("template_options") or {}
    template_root = Path(str(options.get("template_root") or _default_template_root())).resolve(strict=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    for item in template_root.iterdir():
        if item.is_file() and item.suffix.lower() in {".html", ".css", ".js", ".json", ".webmanifest", ".txt"}:
            shutil.copy2(item, output_dir / item.name)
    index_path = output_dir / "index.html"
    app_path = output_dir / "app.js"
    styles_path = output_dir / "styles.css"
    if not all(path.is_file() for path in (index_path, app_path, styles_path)):
        raise ValueError("travel_template_incomplete")

    index = index_path.read_text(encoding="utf-8")
    index = re.sub(r'<link[^>]+rel="manifest"[^>]*>', '', index, flags=re.IGNORECASE)
    marker = '<script src="app.js" defer></script>'
    if marker not in index:
        raise ValueError("travel_template_script_marker_missing")
    data_script = f'<script>window.__TRAVEL_TRIP_DATA__={_json_for_script(data)};</script>'
    index = index.replace(marker, data_script + marker)
    index_path.write_text(index, encoding="utf-8")

    app = app_path.read_text(encoding="utf-8")
    original_fetch = 'const dataUrl=new URLSearchParams(location.search).get("data")||"fixtures/synthetic-trip.json";const response=await fetch(dataUrl,{cache:"no-store"});if(!response.ok)throw new Error(`data_load_failed_${response.status}`);state.trip=await response.json();'
    if original_fetch not in app:
        raise ValueError("travel_template_data_loader_changed")
    app = app.replace(original_fetch, 'state.trip=window.__TRAVEL_TRIP_DATA__;if(!state.trip)throw new Error("trip_data_missing");')
    app = app.replace('state.trip.gallery.slice(0,3)', 'state.trip.gallery.slice(0,5)')
    app = app.replace('if("serviceWorker"in navigator&&location.protocol==="https:")navigator.serviceWorker.register("service-worker.js").catch(()=>{})', '')
    gallery_function = '''function renderTravelPhotoGallery(){if(document.getElementById("travelPhotoGallery"))return;const images=(state.trip.gallery||[]).slice(0,8);if(!images.length)return;const anchor=document.querySelector(".intro-block")||document.querySelector(".route-section");if(!anchor)return;const section=node("section","section-block travel-photo-section");section.id="travelPhotoGallery";const heading=node("div","section-heading");const headingCopy=document.createElement("div");headingCopy.append(node("p","section-kicker","Фотогалерея"),node("h2","","Місця маршруту"));heading.append(headingCopy);const grid=node("div","travel-photo-grid");images.forEach((image,index)=>{const figure=node("figure","travel-photo-card");const img=document.createElement("img");img.src=image.src;img.alt=image.alt||"Фото подорожі";img.loading=index===0?"eager":"lazy";img.decoding="async";figure.append(img);grid.append(figure)});section.append(heading,grid);anchor.after(section)}'''
    if 'start().catch(error=>' not in app:
        raise ValueError("travel_template_start_marker_changed")
    app = app.replace('start().catch(error=>', gallery_function + 'start().then(renderTravelPhotoGallery).catch(error=>')
    app_path.write_text(app, encoding="utf-8")

    styles = styles_path.read_text(encoding="utf-8")
    styles += '''\n/* Travel generated image-led extension */\n:root{--travel-teal:#0b6e5b;--travel-teal-soft:#eaf4f1;--travel-orange:#e8590c}.button.primary{background:var(--travel-teal);border-color:var(--travel-teal);color:#fff;box-shadow:none}.eyebrow,.section-kicker{color:var(--travel-teal)}.status-pill,.label-chip{background:var(--travel-teal-soft);color:var(--travel-teal)}.hero-gallery{grid-template-columns:2fr 1fr 1fr;grid-template-rows:1fr 1fr}.hero-gallery .hero-photo:first-child{grid-column:1;grid-row:1/3}.travel-photo-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.travel-photo-card{margin:0;aspect-ratio:1;overflow:hidden;border-radius:12px;background:#f1f4f3}.travel-photo-card img{width:100%;height:100%;object-fit:cover;transition:transform .3s}.travel-photo-card:hover img{transform:scale(1.03)}@media(max-width:820px){.travel-photo-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.hero-gallery{height:580px;grid-template-columns:1fr 1fr;grid-template-rows:2fr 1fr 1fr}.hero-gallery .hero-photo:first-child{grid-column:1/3;grid-row:1}}@media(max-width:640px){.hero-gallery{height:420px}.travel-photo-grid{gap:6px}}\n'''
    styles_path.write_text(styles, encoding="utf-8")
