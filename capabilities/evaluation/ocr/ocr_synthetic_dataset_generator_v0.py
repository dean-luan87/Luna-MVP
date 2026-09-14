# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-001 — OCR Synthetic Test Generator v0 (Evaluation Tools).

Hard boundaries:
- Must NOT integrate into Luna runtime / mainline.
- Must NOT write to RequestTrace runtime pipelines.
- Must NOT invoke MidPlatform/SceneDelta/WorldContext/Qwen/TTS.
- Dataset generation must NOT invoke OCR providers.

TRDG is optional. If TRDG is unavailable, fall back to Pillow-only rendering.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import random
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


ALLOWED_EXT = ".png"


@dataclasses.dataclass(frozen=True)
class SyntheticSampleSpecV0:
    sample_id: str
    language: str  # zh | en | mixed
    category: str
    text: str


def check_trdg_available_v0() -> Dict[str, Any]:
    try:
        import importlib.util

        ok = importlib.util.find_spec("trdg") is not None
        return {"trdg_importable": bool(ok), "error": None}
    except Exception as e:
        return {"trdg_importable": False, "error": repr(e)}


def compute_file_sha256_v0(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _pillow_render_text_image_v0(
    text: str,
    *,
    width: int,
    height: int,
    rng: random.Random,
    font_path: Optional[str] = None,
    font_size: Optional[int] = None,
) -> Any:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont

    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Use specified font when provided; fall back to default.
    font = None
    if font_path:
        try:
            font = ImageFont.truetype(str(font_path), size=int(font_size or max(18, int(height * 0.22))))
        except Exception:
            font = None
    if font is None:
        try:
            font = ImageFont.load_default()
        except Exception:
            font = None

    # Layout: multi-line allowed
    lines = (text or "").splitlines() or [text]
    x = int(width * 0.06)
    y = int(height * 0.10)
    lh = int(height * 0.10)
    for ln in lines:
        draw.text((x, y), ln, fill=(0, 0, 0), font=font)
        y += lh

    # Optional mild blur/noise
    if rng.random() < 0.25:
        img = img.filter(ImageFilter.GaussianBlur(radius=0.6))
    if rng.random() < 0.25:
        # low contrast
        overlay = Image.new("RGB", (width, height), (240, 240, 240))
        img = Image.blend(img, overlay, alpha=0.25)
    return img


def _trdg_render_text_image_v0(text: str, *, width: int, height: int, rng: random.Random) -> Any:
    """
    Best-effort TRDG rendering; if TRDG internals change, callers should fall back.
    """
    from PIL import Image

    try:
        from trdg.generators import GeneratorFromStrings  # type: ignore
    except Exception as e:
        raise RuntimeError(f"trdg_import_failed:{e!r}")

    # TRDG returns (img, text) pairs. We request 1 image.
    gen = GeneratorFromStrings(
        strings=[text],
        count=1,
        size=max(24, int(min(width, height) * 0.12)),
        skewing_angle=int(rng.choice([0, 1, 2, 3])),
        random_skew=True,
        blur=int(rng.choice([0, 0, 1])),
        random_blur=True,
        background_type=int(rng.choice([1, 2])),
        distorsion_type=int(rng.choice([0, 1])),
        distorsion_orientation=int(rng.choice([0, 1, 2])),
        is_handwritten=False,
    )
    img, _ = next(iter(gen))
    if not isinstance(img, Image.Image):
        raise RuntimeError("trdg_return_not_pil_image")
    # Ensure fixed canvas size to keep manifest consistent
    img = img.convert("RGB")
    img = img.resize((width, height))
    return img


def _build_specs_v0(*, count: int, seed: int) -> List[SyntheticSampleSpecV0]:
    rng = random.Random(int(seed))

    zh_pool = [
        "今天天气不错",
        "心若没有栖息的地方，到哪里都是流浪。",
        "上海地铁 9 号线",
        "候车层\n卫生间\n饮用水\n检票口",
        "当心落物\n禁止抛物\n禁止攀登",
        "防范电信网络诈骗",
        "特别提醒：谨防诈骗！",
    ]
    en_pool = [
        "LUNA OCR STAGE 2 TEST",
        "Waiting Floor",
        "Restrooms",
        "Drinking Water",
        "CAUTION WET FLOOR",
        "SERVICE IN PROGRESS",
    ]
    sym_pool = [
        "0 1 9",
        "Line 9",
        "A/B test",
        "No. 12345",
        "C/J/y/0/1",
        "().,!?;:/\\-",
    ]

    # Category allocation (v0)
    plan = [
        ("zh_plain_text", "zh", 50, zh_pool),
        ("en_plain_text", "en", 30, en_pool),
        ("digits_and_symbols", "mixed", 30, sym_pool),
        ("mixed_zh_en_digit", "mixed", 40, zh_pool + en_pool + sym_pool),
        ("low_contrast_or_blur", "mixed", 30, zh_pool + en_pool),
        ("multi_line_text", "mixed", 20, [x for x in zh_pool + en_pool if "\n" in x] or zh_pool),
    ]

    specs: List[SyntheticSampleSpecV0] = []
    i = 1
    for cat, lang, n, pool in plan:
        for _ in range(n):
            if len(specs) >= count:
                break
            t = rng.choice(pool)
            # ensure multiline for multi_line_text
            if cat == "multi_line_text" and "\n" not in t:
                t = t + "\n" + rng.choice(pool)
            specs.append(
                SyntheticSampleSpecV0(
                    sample_id=f"sample_{i:06d}",
                    language=lang,
                    category=cat,
                    text=t,
                )
            )
            i += 1
    # If count is smaller than plan total, above truncates; if larger, pad
    while len(specs) < count:
        t = rng.choice(zh_pool + en_pool + sym_pool)
        specs.append(SyntheticSampleSpecV0(sample_id=f"sample_{i:06d}", language="mixed", category="pad", text=t))
        i += 1
    return specs[:count]


def generate_ocr_synthetic_samples_v0(
    *,
    output_root: Path,
    count: int,
    seed: int,
    prefer_trdg: bool = True,
) -> Dict[str, Any]:
    """
    Generate images + ground truth + manifest.jsonl under output_root.
    """
    t0 = time.perf_counter()
    output_root = output_root.expanduser().resolve()
    images_dir = output_root / "images"
    gt_dir = output_root / "ground_truth"
    images_dir.mkdir(parents=True, exist_ok=True)
    gt_dir.mkdir(parents=True, exist_ok=True)

    rng = random.Random(int(seed))
    specs = _build_specs_v0(count=count, seed=seed)

    trdg_status = check_trdg_available_v0()
    use_trdg = bool(prefer_trdg and trdg_status.get("trdg_importable"))
    generator = "trdg" if use_trdg else "pillow_fallback"

    # Fixed canvas size (v0)
    width, height = 640, 160

    manifest_path = output_root / "manifest.jsonl"
    manifest_f = manifest_path.open("w", encoding="utf-8")

    created: List[Dict[str, Any]] = []
    for spec in specs:
        img_path = images_dir / f"{spec.sample_id}{ALLOWED_EXT}"
        gt_path = gt_dir / f"{spec.sample_id}.txt"

        # Render image
        try:
            if use_trdg:
                img = _trdg_render_text_image_v0(spec.text, width=width, height=height, rng=rng)
            else:
                img = _pillow_render_text_image_v0(spec.text, width=width, height=height, rng=rng)
        except Exception:
            # fallback hard
            img = _pillow_render_text_image_v0(spec.text, width=width, height=height, rng=rng)
            generator = "pillow_fallback"
            use_trdg = False

        img.save(str(img_path), format="PNG")
        gt_path.write_text(spec.text + "\n", encoding="utf-8")

        sha = compute_file_sha256_v0(img_path)
        row = {
            "sample_id": spec.sample_id,
            "image_path": str(img_path),
            "ground_truth_path": str(gt_path),
            "ground_truth_text": spec.text,
            "language": spec.language,
            "category": spec.category,
            "generator": generator,
            "generator_config": {"width": width, "height": height, "seed": seed, "prefer_trdg": prefer_trdg},
            "sha256": sha,
            "width": width,
            "height": height,
        }
        manifest_f.write(json.dumps(row, ensure_ascii=False) + "\n")
        created.append(row)

    manifest_f.close()

    summary = {
        "phase": "Phase-EvaluationTools-OCR-001",
        "tool": "ocr_synthetic_dataset_generator_v0",
        "output_root": str(output_root),
        "count": len(created),
        "seed": int(seed),
        "prefer_trdg": bool(prefer_trdg),
        "trdg_status": trdg_status,
        "generator_used": generator,
        "categories": {c["category"]: 0 for c in created},
        "hard_audit": {
            "ocr_provider_invoked": False,
            "network_request_invoked": False,
            "semantic_interpretation_enabled": False,
            "midplatform_invoked": False,
            "scene_delta_invoked": False,
            "world_context_invoked": False,
        },
        "elapsed_ms": round((time.perf_counter() - t0) * 1000.0, 3),
    }
    for r in created:
        summary["categories"][r["category"]] = int(summary["categories"].get(r["category"], 0)) + 1
    return summary


def validate_synthetic_dataset_v0(*, dataset_root: Path, expected_count: int) -> Dict[str, Any]:
    dataset_root = dataset_root.expanduser().resolve()
    manifest = dataset_root / "manifest.jsonl"
    images_dir = dataset_root / "images"
    gt_dir = dataset_root / "ground_truth"

    blockers: List[str] = []
    if not manifest.is_file():
        blockers.append("manifest_missing")
    if not images_dir.is_dir():
        blockers.append("images_dir_missing")
    if not gt_dir.is_dir():
        blockers.append("ground_truth_dir_missing")

    rows: List[Dict[str, Any]] = []
    if manifest.is_file():
        for line in manifest.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                blockers.append("manifest_parse_failed")
                break

    if rows and len(rows) != int(expected_count):
        blockers.append("sample_count_mismatch")

    # Per-sample checks
    missing_img = 0
    missing_gt = 0
    missing_sha = 0
    for r in rows:
        ip = Path(str(r.get("image_path") or ""))
        gp = Path(str(r.get("ground_truth_path") or ""))
        if not ip.is_file():
            missing_img += 1
        if not gp.is_file():
            missing_gt += 1
        if not (r.get("sha256") and isinstance(r.get("sha256"), str) and len(r.get("sha256")) >= 16):
            missing_sha += 1

    if missing_img:
        blockers.append(f"missing_images:{missing_img}")
    if missing_gt:
        blockers.append(f"missing_ground_truth:{missing_gt}")
    if missing_sha:
        blockers.append(f"missing_sha256:{missing_sha}")

    ok = not blockers
    return {
        "ok": ok,
        "dataset_root": str(dataset_root),
        "expected_count": int(expected_count),
        "actual_count": len(rows),
        "blockers": blockers,
    }

