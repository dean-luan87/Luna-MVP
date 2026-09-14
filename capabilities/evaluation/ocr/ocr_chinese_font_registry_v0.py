# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-002 — Chinese font registry v0 (Evaluation Tools).

Scan common macOS font directories, load via Pillow, and validate CJK visibility
using a conservative tofu detection heuristic.
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple


DEFAULT_FONT_DIRS = [
    "/System/Library/Fonts",
    "/System/Library/Fonts/Supplemental",
    "/Library/Fonts",
    str(Path.home() / "Library" / "Fonts"),
]


PROBE_TEXT = "上海地铁9号线防范电信网络诈骗"
PROBE_A = "中"
PROBE_B = "海"
PROBE_CHAR_SET = ["上", "海", "地", "铁", "防", "范", "电", "信", "网", "络", "诈", "骗"]


def _sha256_path(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _is_font_file(p: Path) -> bool:
    return p.is_file() and p.suffix.lower() in {".ttf", ".otf", ".ttc"}


def _render_text_mask(font_path: str, text: str, *, size: int = 36) -> "Any":
    from PIL import Image, ImageDraw, ImageFont

    font = ImageFont.truetype(font_path, size=size)
    img = Image.new("L", (520, 96), 255)
    d = ImageDraw.Draw(img)
    d.text((8, 20), text, font=font, fill=0)
    return img


def _ink_ratio(img_l: "Any") -> float:
    # img is L mode: 0=ink, 255=background
    data = img_l.getdata()
    total = len(data) or 1
    ink = sum(1 for v in data if v < 245)
    return float(ink) / float(total)


def _mask_signature(img_l: "Any") -> str:
    # coarse signature by hashing bytes
    b = img_l.tobytes()
    return hashlib.sha256(b).hexdigest()


def validate_cjk_font_visibility_v0(font_path: str) -> Dict[str, Any]:
    """
    Conservative tofu detection:
    - Render two different CJK chars. If resulting masks are identical -> tofu suspected.
    - Ensure ink ratio above a small threshold.
    - Extended probe: ensure a small CJK char set does not collapse into identical fallback glyphs.
    """
    out: Dict[str, Any] = {
        "font_path": font_path,
        "probe_text": PROBE_TEXT,
        "rendered_non_tofu": False,
        "tofu_suspected": None,
        "ink_ratio": None,
        "glyph_diversity_score": None,
        "probe_char_set_unique_ratio": None,
        "probe_char_set_duplicate_count": None,
        "error": None,
        "validation_result": "NO_GO",
    }
    try:
        m_a = _render_text_mask(font_path, PROBE_A)
        m_b = _render_text_mask(font_path, PROBE_B)
        sig_a = _mask_signature(m_a)
        sig_b = _mask_signature(m_b)
        same = sig_a == sig_b
        ink = _ink_ratio(_render_text_mask(font_path, PROBE_TEXT, size=30))
        # diversity: 1 if different, else 0
        div = 1.0 if not same else 0.0

        char_sigs: List[str] = []
        for ch in PROBE_CHAR_SET:
            try:
                mm = _render_text_mask(font_path, ch, size=40)
                char_sigs.append(_mask_signature(mm))
            except Exception:
                char_sigs.append("render_error")
        uniq = len(set(char_sigs))
        total = len(char_sigs)
        dup = total - uniq
        unique_ratio = float(uniq) / float(max(1, total))
        out["probe_char_set_unique_ratio"] = float(unique_ratio)
        out["probe_char_set_duplicate_count"] = int(dup)

        out["tofu_suspected"] = bool(same)
        out["ink_ratio"] = float(ink)
        out["glyph_diversity_score"] = float(div)
        passed = (not same) and (ink >= 0.002) and (unique_ratio >= 0.80)
        out["rendered_non_tofu"] = bool(passed)
        out["validation_result"] = "GO" if passed else "NO_GO"
        return out
    except Exception as e:
        out["error"] = repr(e)
        out["validation_result"] = "NO_GO"
        return out


def scan_chinese_fonts_v0(*, font_dirs: Optional[Sequence[str]] = None) -> Dict[str, Any]:
    dirs = list(font_dirs or DEFAULT_FONT_DIRS)
    found: List[Dict[str, Any]] = []
    for d in dirs:
        p = Path(d).expanduser()
        if not p.is_dir():
            continue
        for fp in sorted(p.iterdir(), key=lambda x: x.name):
            if not _is_font_file(fp):
                continue
            rec: Dict[str, Any] = {
                "font_id": f"font_{fp.stem}",
                "font_path": str(fp.resolve()),
                "exists": True,
                "can_load_with_pillow": False,
                "supports_cjk_probe": False,
                "supports_cjk_probe_report": None,
                "sha256": None,
                "selected_for_generation": False,
            }
            try:
                rec["sha256"] = _sha256_path(fp)
            except Exception:
                rec["sha256"] = None
            rep = validate_cjk_font_visibility_v0(str(fp.resolve()))
            rec["supports_cjk_probe_report"] = rep
            rec["can_load_with_pillow"] = rep.get("error") is None
            rec["supports_cjk_probe"] = bool(rep.get("validation_result") == "GO")
            found.append(rec)
    return {"font_dirs": dirs, "count": len(found), "fonts": found}


def select_best_cjk_font_v0(registry: Dict[str, Any]) -> Dict[str, Any]:
    fonts = registry.get("fonts") if isinstance(registry.get("fonts"), list) else []
    candidates = []
    for f in fonts:
        if not isinstance(f, dict):
            continue
        rep = f.get("supports_cjk_probe_report") or {}
        if rep.get("validation_result") != "GO":
            continue
        ink = float(rep.get("ink_ratio") or 0.0)
        candidates.append((ink, f))
    candidates.sort(key=lambda t: t[0], reverse=True)
    if not candidates:
        return {"ok": False, "selected": None, "reason": "no_cjk_visible_font_found"}
    selected = candidates[0][1]
    selected["selected_for_generation"] = True
    return {"ok": True, "selected": selected, "reason": "max_ink_ratio"}

