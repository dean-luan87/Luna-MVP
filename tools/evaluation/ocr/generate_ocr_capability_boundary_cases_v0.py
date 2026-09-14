#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-006 — Generate OCR capability boundary cases v0 (Evaluation Tools).

Generates a small boundary dataset with:
- content type taxonomy coverage
- quality perturbation coverage (selective)
- ground truth + expected routing labels

This generator is evaluation-only and does NOT invoke OCR providers.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import dataclasses
import json
import os
import random
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.evaluation.ocr.ocr_capability_boundary_router_policy_v0 import build_routing_policy_draft_v0  # noqa: E402
from capabilities.evaluation.ocr.ocr_capability_boundary_taxonomy_v0 import (  # noqa: E402
    OcrBoundaryTestCaseV0,
    OcrExpectedRouting,
    OcrQualityPerturbationV0,
    build_default_expected_metrics_v0,
    testcase_to_dict_v0,
)
from capabilities.evaluation.ocr.ocr_chinese_font_registry_v0 import select_best_cjk_font_v0, scan_chinese_fonts_v0  # noqa: E402


def _now_iso() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, row: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _render_text_image(
    *,
    text: str,
    width: int,
    height: int,
    font_path: Optional[str],
    font_size: int,
    background: str,
    rng: random.Random,
) -> "Any":
    from PIL import Image, ImageDraw, ImageFilter, ImageFont

    if background == "white":
        img = Image.new("RGB", (width, height), (255, 255, 255))
    elif background == "gradient":
        img = Image.new("RGB", (width, height), (255, 255, 255))
        px = img.load()
        for y in range(height):
            v = int(245 - 30 * (y / max(1, height - 1)))
            for x in range(width):
                px[x, y] = (v, v, v)
    else:
        # textured/noisy/photo_background (synthetic approximation)
        img = Image.new("RGB", (width, height), (245, 245, 245))
        d = ImageDraw.Draw(img)
        for _ in range(180):
            x1 = rng.randint(0, width - 1)
            y1 = rng.randint(0, height - 1)
            x2 = min(width - 1, x1 + rng.randint(8, 80))
            y2 = min(height - 1, y1 + rng.randint(3, 30))
            c = rng.randint(220, 252)
            d.rectangle([x1, y1, x2, y2], fill=(c, c, c))

    draw = ImageDraw.Draw(img)
    font = None
    if font_path:
        try:
            font = ImageFont.truetype(font_path, size=int(font_size))
        except Exception:
            font = None
    if font is None:
        try:
            font = ImageFont.load_default()
        except Exception:
            font = None

    # simple layout: multi-line supported
    lines = (text or "").splitlines() or [text]
    x = int(width * 0.06)
    y = int(height * 0.18)
    lh = int(font_size * 1.15)
    for ln in lines:
        draw.text((x, y), ln, fill=(0, 0, 0), font=font)
        y += lh

    # subtle paper noise
    if rng.random() < 0.15:
        img = img.filter(ImageFilter.GaussianBlur(radius=0.3))
    return img


def _apply_perturbations(
    *,
    img: "Any",
    blur: str,
    contrast: str,
    brightness: str,
    skew_angle: int,
    compression: str,
    rng: random.Random,
) -> Tuple["Any", Optional[str]]:
    from PIL import Image, ImageEnhance, ImageFilter

    out = img
    if skew_angle:
        out = out.rotate(int(skew_angle), resample=Image.BICUBIC, expand=True, fillcolor=(255, 255, 255))

    if brightness == "underexposed":
        out = ImageEnhance.Brightness(out).enhance(0.55)
    elif brightness == "overexposed":
        out = ImageEnhance.Brightness(out).enhance(1.35)

    if contrast == "high":
        out = ImageEnhance.Contrast(out).enhance(1.35)
    elif contrast == "low":
        out = ImageEnhance.Contrast(out).enhance(0.72)
    elif contrast == "very_low":
        out = ImageEnhance.Contrast(out).enhance(0.55)

    if blur == "mild":
        out = out.filter(ImageFilter.GaussianBlur(radius=0.8))
    elif blur == "medium":
        out = out.filter(ImageFilter.GaussianBlur(radius=1.6))
    elif blur == "heavy":
        out = out.filter(ImageFilter.GaussianBlur(radius=2.8))

    # compression: return desired format
    fmt = None
    if compression == "mild_jpeg":
        fmt = "jpeg_mild"
    elif compression == "heavy_jpeg":
        fmt = "jpeg_heavy"
    return out, fmt


def _pick_font_for_language(*, lang: str, cjk_font_path: Optional[str]) -> Optional[str]:
    if lang in ("zh", "mixed"):
        return cjk_font_path
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--per-type", type=int, default=5, help="base cases per content type")
    args = ap.parse_args()

    out_root = _require_abs(args.output_root, "--output-root")
    out_root.mkdir(parents=True, exist_ok=True)
    images_dir = out_root / "images"
    gt_dir = out_root / "ground_truth"
    exp_dir = out_root / "expected_routing"
    images_dir.mkdir(parents=True, exist_ok=True)
    gt_dir.mkdir(parents=True, exist_ok=True)
    exp_dir.mkdir(parents=True, exist_ok=True)

    rng = random.Random(int(args.seed))

    # choose a CJK font (best-effort) for rendering
    reg = scan_chinese_fonts_v0()
    sel = select_best_cjk_font_v0(reg)
    cjk_font_path = None
    if sel.get("ok") and isinstance(sel.get("selected"), dict):
        cjk_font_path = str((sel["selected"] or {}).get("font_path") or "") or None

    routing_policy = build_routing_policy_draft_v0()
    _write_json(exp_dir / "ocr_recommended_routing_policy_draft.json", routing_policy)

    content_specs: List[Tuple[str, str, str]] = [
        ("zh_plain_text", "zh", "上海地铁9号线"),
        ("zh_traditional_text", "zh", "臺北捷運文湖線"),
        ("en_plain_text", "en", "CAUTION KEEP CLEAR"),
        ("digits", "en", "2026 11 100"),
        ("symbols_and_punctuation", "en", "()/:-→•"),
        ("mixed_zh_en_digit", "mixed", "上海 Metro Line 9"),
        ("multi_line_text", "zh", "防范电信网络诈骗\n文明乘车"),
        ("document_text", "zh", "说明：本品请置于阴凉处保存。\n成分：水、盐、糖。"),
        ("product_label", "zh", "配料表：水、白砂糖、食用盐\n净含量：500ml"),
        ("signboard", "mixed", "EXIT 2 出口"),
        ("vertical_text", "zh", "上\n海\n地\n铁"),
        ("handwritten_style", "zh", "手写风格示例"),
        ("low_quality_text", "zh", "低清反光倾斜样例"),
        ("multi_panel_layout", "zh", "（九宫格占位：需人工样本）"),
        ("icon_text_mix", "zh", "（图标+文字占位：需人工样本）"),
        ("artistic_text", "zh", "（艺术字占位：需人工样本）"),
        ("stylized_digits", "en", "（异形数字占位：需人工样本）"),
        ("decorative_graphic_non_text", "en", "（装饰图形占位：非文本）"),
    ]

    # base perturbation profile
    base_profile = OcrQualityPerturbationV0(
        size_scale="normal_text",
        blur="none",
        contrast="normal",
        brightness="normal",
        compression="none_png",
        skew_angle=0,
        background="white",
        layout_complexity="single_line",
    )

    def expected_route_for(ct: str) -> OcrExpectedRouting:
        if ct in ("zh_plain_text", "en_plain_text", "digits", "mixed_zh_en_digit", "multi_line_text"):
            return "rapidocr_primary"
        if ct in ("document_text", "product_label", "multi_panel_layout", "icon_text_mix"):
            return "layout_branch"
        if ct in ("artistic_text", "stylized_digits", "handwritten_style", "vertical_text"):
            return "visual_glyph_branch"
        if ct in ("symbols_and_punctuation", "decorative_graphic_non_text"):
            return "visual_symbol_branch"
        if ct in ("low_quality_text", "signboard", "zh_traditional_text"):
            return "manual_review"
        return "manual_review"

    cases_path = out_root / "boundary_case_manifest.jsonl"
    if cases_path.exists():
        cases_path.unlink()

    total = 0
    generated = 0
    manual_required = 0

    # Generate base cases per type (small)
    for ct, lang, text in content_specs:
        for i in range(int(args.per_type)):
            total += 1
            cid = f"ocr_boundary_{ct}_base_{i+1:03d}"
            prof = base_profile
            # per type tweak
            layout = "single_line"
            if ct in ("multi_line_text", "document_text", "product_label"):
                layout = "multi_line"
                prof = dataclasses.replace(prof, layout_complexity="multi_line")  # type: ignore
            if ct in ("vertical_text",):
                prof = dataclasses.replace(prof, layout_complexity="multi_line")  # type: ignore

            route = expected_route_for(ct)
            metrics = build_default_expected_metrics_v0(content_type=ct)  # type: ignore[arg-type]
            gen_status = "generated"
            if "占位" in text or "非文本" in text:
                gen_status = "manual_sample_required"
            tc = OcrBoundaryTestCaseV0(
                case_id=cid,
                content_type=ct,  # type: ignore[arg-type]
                language=lang,
                text=text,
                quality_profile=prof,
                expected_ocr_route=route,
                expected_metrics=metrics,
                expected_failure_mode=None,
                ground_truth_text="" if gen_status != "generated" else text,
                should_enter_mainline_ocr=route in ("rapidocr_primary", "layout_branch"),
                should_enter_layout_branch=route == "layout_branch",
                should_enter_symbol_branch=route == "visual_symbol_branch",
                should_enter_glyph_branch=route == "visual_glyph_branch",
                generation_status=gen_status,
            )

            rec = testcase_to_dict_v0(tc)
            img_path = images_dir / f"{cid}.png"
            gt_path = gt_dir / f"{cid}.txt"
            rec["image_path"] = str(img_path)
            rec["ground_truth_path"] = str(gt_path)

            if gen_status == "generated":
                font_path = _pick_font_for_language(lang=lang, cjk_font_path=cjk_font_path)
                font_size = 46 if prof.size_scale in ("normal_text", "large_text") else 34
                w, h = 900, 260
                if prof.size_scale == "tiny_text":
                    font_size = 18
                elif prof.size_scale == "small_text":
                    font_size = 26
                elif prof.size_scale == "large_text":
                    font_size = 62
                img = _render_text_image(text=text, width=w, height=h, font_path=font_path, font_size=font_size, background=prof.background, rng=rng)
                img.save(str(img_path))
                gt_path.write_text(text, encoding="utf-8")
                generated += 1
            else:
                # placeholder: create a small stub image + empty GT
                from PIL import Image

                Image.new("RGB", (640, 240), (250, 250, 250)).save(str(img_path))
                gt_path.write_text("", encoding="utf-8")
                manual_required += 1

            _append_jsonl(cases_path, rec)

    # Add targeted perturbations for key types (limited)
    perturb_targets = [
        ("zh_plain_text", "zh", "上海地铁9号线"),
        ("digits", "en", "9 11 100 2026"),
        ("mixed_zh_en_digit", "mixed", "上海 Metro Line 9"),
        ("low_quality_text", "zh", "低清反光倾斜样例"),
    ]
    perturb_profiles: List[OcrQualityPerturbationV0] = []
    for size_scale in ("tiny_text", "small_text", "normal_text", "oversized_image_small_text"):
        perturb_profiles.append(
            OcrQualityPerturbationV0(
                size_scale=size_scale, blur="none", contrast="normal", brightness="normal",
                compression="none_png", skew_angle=0, background="white", layout_complexity="single_line"
            )
        )
    for blur in ("mild", "medium", "heavy"):
        perturb_profiles.append(
            OcrQualityPerturbationV0(
                size_scale="normal_text", blur=blur, contrast="normal", brightness="normal",
                compression="none_png", skew_angle=0, background="white", layout_complexity="single_line"
            )
        )
    for contrast in ("low", "very_low"):
        perturb_profiles.append(
            OcrQualityPerturbationV0(
                size_scale="normal_text", blur="none", contrast=contrast, brightness="normal",
                compression="none_png", skew_angle=0, background="white", layout_complexity="single_line"
            )
        )
    for b in ("underexposed", "overexposed"):
        perturb_profiles.append(
            OcrQualityPerturbationV0(
                size_scale="normal_text", blur="none", contrast="normal", brightness=b,
                compression="none_png", skew_angle=0, background="white", layout_complexity="single_line"
            )
        )
    for comp in ("mild_jpeg", "heavy_jpeg"):
        perturb_profiles.append(
            OcrQualityPerturbationV0(
                size_scale="normal_text", blur="none", contrast="normal", brightness="normal",
                compression=comp, skew_angle=0, background="white", layout_complexity="single_line"
            )
        )
    for ang in (5, 15, 30):
        perturb_profiles.append(
            OcrQualityPerturbationV0(
                size_scale="normal_text", blur="none", contrast="normal", brightness="normal",
                compression="none_png", skew_angle=ang, background="white", layout_complexity="single_line"
            )
        )
    for bg in ("textured", "noisy"):
        perturb_profiles.append(
            OcrQualityPerturbationV0(
                size_scale="normal_text", blur="none", contrast="normal", brightness="normal",
                compression="none_png", skew_angle=0, background=bg, layout_complexity="single_line"
            )
        )

    for ct, lang, text in perturb_targets:
        for j, prof in enumerate(perturb_profiles[:20]):  # cap for v0
            total += 1
            cid = f"ocr_boundary_{ct}_pert_{j+1:03d}"
            route = expected_route_for(ct)
            metrics = build_default_expected_metrics_v0(content_type=ct)  # type: ignore[arg-type]
            tc = OcrBoundaryTestCaseV0(
                case_id=cid,
                content_type=ct,  # type: ignore[arg-type]
                language=lang,
                text=text,
                quality_profile=prof,
                expected_ocr_route=route,
                expected_metrics=metrics,
                expected_failure_mode=None,
                ground_truth_text=text,
                should_enter_mainline_ocr=route in ("rapidocr_primary", "layout_branch"),
                should_enter_layout_branch=route == "layout_branch",
                should_enter_symbol_branch=route == "visual_symbol_branch",
                should_enter_glyph_branch=route == "visual_glyph_branch",
                generation_status="generated",
            )
            rec = testcase_to_dict_v0(tc)
            img_path = images_dir / f"{cid}.png"
            gt_path = gt_dir / f"{cid}.txt"
            rec["image_path"] = str(img_path)
            rec["ground_truth_path"] = str(gt_path)

            font_path = _pick_font_for_language(lang=lang, cjk_font_path=cjk_font_path)
            # size scale controls
            w, h = 900, 260
            font_size = 46
            if prof.size_scale == "tiny_text":
                font_size = 18
            elif prof.size_scale == "small_text":
                font_size = 26
            elif prof.size_scale == "large_text":
                font_size = 62
            elif prof.size_scale == "oversized_image_small_text":
                w, h = 2400, 1400
                font_size = 26
            img = _render_text_image(text=text, width=w, height=h, font_path=font_path, font_size=font_size, background=prof.background, rng=rng)
            img2, fmt = _apply_perturbations(img=img, blur=prof.blur, contrast=prof.contrast, brightness=prof.brightness, skew_angle=prof.skew_angle, compression=prof.compression, rng=rng)

            if fmt is None:
                img2.save(str(img_path))
            else:
                # save jpeg then convert to png path for uniformity (keep artifact)
                tmp_j = images_dir / f"{cid}.jpg"
                q = 70 if fmt == "jpeg_mild" else 25
                img2.save(str(tmp_j), quality=q, optimize=True)
                # re-open and save as png to keep manifest stable but retain artifacts from jpeg decode
                from PIL import Image

                Image.open(str(tmp_j)).convert("RGB").save(str(img_path))
                try:
                    tmp_j.unlink()
                except Exception:
                    pass
            gt_path.write_text(text, encoding="utf-8")
            generated += 1
            _append_jsonl(cases_path, rec)

    summary = {
        "phase": "Phase-EvaluationTools-OCR-006",
        "tool": "generate_ocr_capability_boundary_cases_v0",
        "ts": _now_iso(),
        "output_root": str(out_root),
        "seed": int(args.seed),
        "base_per_type": int(args.per_type),
        "total_cases": int(total),
        "generated_cases": int(generated),
        "manual_sample_required_cases": int(manual_required),
        "cjk_font_selected": cjk_font_path,
        "hard_audit": {
            "ocr_provider_invoked": False,
            "runtime_integration": False,
            "whitebox_integration": False,
            "mainline_side_effect": False,
        },
    }
    _write_json(out_root / "boundary_case_summary.json", summary)
    (out_root / "generation_notes.md").write_text(
        "\n".join(
            [
                "# OCR capability boundary cases (Evaluation Tools) v0",
                "",
                f"- **output_root:** `{summary['output_root']}`",
                f"- **total_cases:** `{summary['total_cases']}`",
                f"- **generated_cases:** `{summary['generated_cases']}`",
                f"- **manual_sample_required_cases:** `{summary['manual_sample_required_cases']}`",
                "",
                "## Notes",
                "",
                "- Some complex types are placeholders requiring manual real-world samples (v0).",
                "- Generator does not invoke OCR providers.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"ok": True, "output_root": str(out_root), "total_cases": total, "generated": generated, "manual_required": manual_required}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

