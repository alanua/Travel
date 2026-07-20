from __future__ import annotations

import argparse
import json
import shutil
import tempfile
import time
from pathlib import Path
from typing import Any, Iterable

from travel_page.calendar_actions import calendar_link_action
from travel_page.images import prepare_image_metadata, write_asset_manifest
from travel_page.manifest import load_travel_manifest, normalize_trip_data
from travel_page.renderer import render_trip_page


def _skeleton_imports():
    try:
        from core.page_pipeline import build_manifest, publish_manifest, register_downstream_action
        from core.page_renderer_registry import register_renderer
    except ImportError as exc:
        raise RuntimeError("skeleton_page_pipeline_not_available") from exc
    return build_manifest, publish_manifest, register_downstream_action, register_renderer


def prepare_skeleton_manifest(travel_manifest: dict[str, Any], workspace: Path) -> dict[str, Any]:
    data = normalize_trip_data(travel_manifest)
    assets = prepare_image_metadata(data, travel_manifest.get("image_source_metadata"))
    workspace.mkdir(parents=True, exist_ok=True)
    try:
        workspace.chmod(0o700)
    except OSError:
        pass
    data_path = workspace / "trip-data.json"
    assets_path = workspace / "assets.json"
    data_path.write_text(json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")), encoding="utf-8")
    data_path.chmod(0o600)
    write_asset_manifest(assets_path, assets)
    skeleton_manifest: dict[str, Any] = {
        "schema_version": 1,
        "owner_module": "travel",
        "publication_profile_id": str(travel_manifest["publication_profile_id"]),
        "page_id": str(travel_manifest["trip_id"]),
        "template_id": "travel_trip_v1",
        "content_ref": str(data_path),
        "asset_manifest_ref": str(assets_path),
        "publication_mode": str(travel_manifest["publication_mode"]),
        "operator_approval": str(travel_manifest.get("operator_approval") or "publish_page_v1"),
        "locale": str(travel_manifest["locale"]),
        "selected_variant": travel_manifest.get("selected_default_window"),
        "stable_url": travel_manifest.get("stable_url"),
        "backend_options": dict(travel_manifest.get("backend_options") or {}),
        "evidence_metadata": dict(travel_manifest.get("evidence_metadata") or {}),
        "template_options": {
            "template_root": str(travel_manifest.get("template_root") or (Path(__file__).resolve().parents[1] / "web" / "trip-page")),
            "theme_id": str(travel_manifest.get("theme_id") or "travel-white-teal-v1"),
        },
    }
    events = travel_manifest.get("calendar_event_refs") or []
    if events:
        skeleton_manifest["downstream_actions"] = [{
            "action_id": "travel_calendar_v1",
            "config": {
                "event_refs": events,
                "date_selectors": travel_manifest.get("calendar_date_selectors") or {},
            },
        }]
    return {key: value for key, value in skeleton_manifest.items() if value is not None}


def run(command: str, manifest_path: str | Path, *, mode_override: str | None = None, pipeline_root: Path | None = None) -> dict[str, Any]:
    started = time.monotonic()
    manifest = load_travel_manifest(manifest_path)
    if mode_override:
        if mode_override not in {"create", "update_owned"}:
            raise ValueError("travel_publication_mode_invalid")
        manifest["publication_mode"] = mode_override
    build_manifest, publish_manifest, register_downstream_action, register_renderer = _skeleton_imports()
    register_renderer("travel_trip_v1", render_trip_page, replace=True)
    register_downstream_action("travel_calendar_v1", calendar_link_action, replace=True)
    private_parent = Path(manifest.get("private_workspace_root") or Path.home() / ".local" / "share" / "travel" / "page-builds").expanduser().resolve(strict=False)
    private_parent.mkdir(parents=True, exist_ok=True)
    try:
        private_parent.chmod(0o700)
    except OSError:
        pass
    workspace = Path(tempfile.mkdtemp(prefix=f"{manifest['trip_id']}-", dir=private_parent))
    try:
        skeleton_manifest = prepare_skeleton_manifest(manifest, workspace)
        if command == "build":
            receipt, artifact = build_manifest(skeleton_manifest, root=pipeline_root)
            shutil.rmtree(artifact.rendered_dir, ignore_errors=True)
        elif command == "publish":
            receipt = publish_manifest(skeleton_manifest, root=pipeline_root)
        else:
            raise ValueError("travel_command_invalid")
        receipt = dict(receipt)
        receipt["travel_trip_id"] = manifest["trip_id"]
        receipt["travel_total_seconds"] = round(time.monotonic() - started, 4)
        return receipt
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m travel_page")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("build", "publish"):
        item = subparsers.add_parser(name)
        item.add_argument("--manifest", required=True)
        item.add_argument("--mode", choices=("create", "update_owned"))
        item.add_argument("--pipeline-root")
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        receipt = run(args.command, args.manifest, mode_override=args.mode, pipeline_root=Path(args.pipeline_root).expanduser() if args.pipeline_root else None)
    except Exception as exc:
        reason = str(exc) if str(exc).replace("_", "").isalnum() else type(exc).__name__.lower()
        receipt = {"status": "BLOCKED", "reason": reason}
    print(json.dumps(receipt, sort_keys=True, ensure_ascii=False))
    return 0 if receipt.get("status") in {"BUILT", "PUBLISHED", "NO_CHANGE", "PUBLISHED_WITH_ACTION_ERRORS"} else 2
