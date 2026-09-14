#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-010-Repeat — Prepare a readable OCR input fixture.

Modes:
- generate: create a deterministic PNG with fixed text (preferred, reproducible)
- download: (optional) download an image by URL/query is intentionally minimal; prefer generate

Hard boundaries:
- Does NOT invoke OCR providers/models.
- Does NOT enter MidPlatform / SceneDelta / WorldContext.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional


ALLOWED_EXT = {".png", ".jpg", ".jpeg", ".webp"}


def _now_iso() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _ensure_output_image_path(p: Path) -> None:
    if not p.is_absolute():
        raise SystemExit("ERROR: --output-image must be an absolute path")
    if p.suffix.lower() not in ALLOWED_EXT:
        raise SystemExit(f"ERROR: output image extension must be one of {sorted(ALLOWED_EXT)}")
    p.parent.mkdir(parents=True, exist_ok=True)


def _generate_png(output_path: Path, lines: List[str]) -> Dict[str, Any]:
    """
    Deterministic fixture: white background, black text.
    Avoids external fonts by using Pillow default bitmap font.
    """
    try:
        from PIL import Image, ImageDraw, ImageFont  # type: ignore
    except Exception as e:
        raise SystemExit(f"ERROR: pillow_not_available:{e!r}")

    width, height = 900, 420
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    y = 40
    for line in lines:
        d.text((40, y), line, fill=(0, 0, 0), font=font)
        y += 40

    # Add a simple border for stable edges
    d.rectangle([20, 20, width - 20, height - 20], outline=(0, 0, 0), width=2)

    img.save(str(output_path), format="PNG", optimize=False)
    return {"width": width, "height": height, "format": "PNG"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", required=True, choices=["generate", "download"])
    ap.add_argument("--output-image", required=True)
    ap.add_argument("--query", default=None, help="Only used for download mode (not recommended).")
    ap.add_argument("--source-url", default=None, help="Direct image URL for download mode (preferred over query).")
    ap.add_argument("--output-root", default=None, help="Optional: write summary/metadata JSONs into this directory (absolute).")
    args = ap.parse_args()

    out_img = Path(args.output_image).expanduser()
    _ensure_output_image_path(out_img)

    output_root: Optional[Path] = None
    if args.output_root:
        output_root = Path(args.output_root).expanduser()
        if not output_root.is_absolute():
            raise SystemExit("ERROR: --output-root must be an absolute path when provided")
        output_root.mkdir(parents=True, exist_ok=True)
    else:
        # default colocated with image
        output_root = out_img.parent

    expected_hint = ["LUNA OCR STAGE 2 TEST", "RAW TEXT CANDIDATE", "2026"]
    fixture_id = f"ocr_fixture_{hashlib.sha256(str(out_img).encode('utf-8')).hexdigest()[:12]}"

    source_url = None
    downloaded_at = None
    gen_meta: Dict[str, Any] = {}

    if args.mode == "generate":
        lines = [
            "LUNA OCR STAGE 2 TEST",
            "RAW TEXT CANDIDATE",
            "2026",
            "This is a reproducible local fixture.",
        ]
        gen_meta = _generate_png(out_img, lines)
    else:
        # Minimal guardrails: require explicit source-url; do not scrape the web.
        if not args.source_url:
            raise SystemExit("ERROR: download mode requires --source-url (explicit image URL). Prefer --mode generate.")
        source_url = str(args.source_url)
        downloaded_at = _now_iso()
        # Use curl via os.system is avoided; rely on urllib (no auth).
        import urllib.request

        req = urllib.request.Request(source_url, headers={"User-Agent": "LunaGuardedTrial/010-Repeat"})
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read()
        out_img.write_bytes(data)

    exists = out_img.is_file()
    size_bytes = int(out_img.stat().st_size) if exists else 0
    sha256 = _sha256_file(out_img) if exists else None

    summary = {
        "fixture_id": fixture_id,
        "mode": args.mode,
        "image_path": str(out_img.resolve()),
        "source_url": source_url,
        "downloaded_at": downloaded_at,
        "text_intent": "clear readable OCR test text",
        "exists": exists,
        "extension_allowed": out_img.suffix.lower() in ALLOWED_EXT,
        "sha256": sha256,
        "size_bytes": size_bytes,
        "expected_readable_text_hint": expected_hint,
        "will_invoke_ocr": False,
        "generated_image_metadata": gen_meta,
    }

    _write_json(output_root / "ocr_stage2_readable_input_fixture_summary.json", {"ok": True, "ts": _now_iso(), "fixture_id": fixture_id})
    _write_json(output_root / "ocr_stage2_readable_input_fixture_metadata.json", summary)

    print(json.dumps(summary, ensure_ascii=False))
    return 0 if exists and size_bytes > 0 and sha256 else 2


if __name__ == "__main__":
    raise SystemExit(main())

