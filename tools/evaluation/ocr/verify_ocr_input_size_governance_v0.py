#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-OCR-Input-Size-Governance-001 — Static verifier for OCR input size / ROI / tiling governance docs + example config.

Does not run OCR, does not touch routing or runtime.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _doc_must_contain(text: str, needles: Tuple[str, ...], label: str, blockers: List[str]) -> None:
    low = text.lower()
    for n in needles:
        if n.lower() not in low:
            blockers.append(f"doc_missing_reference:{label}:{n}")


def _doc_must_not_allow_full_bleed(text: str, path: Path, blockers: List[str]) -> None:
    bad_patterns = (
        r"允许\s*超大图\s*直接\s*实时",
        r"允许\s*整图\s*原分辨率\s*直送\s*实时",
        r"tile\s*结果\s*可\s*丢弃\s*坐标",
        r"无需\s*坐标\s*回填",
    )
    for pat in bad_patterns:
        if re.search(pat, text, re.IGNORECASE):
            blockers.append(f"doc_forbidden_language:{path.name}:{pat}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace-root", required=True)
    ap.add_argument("--failed-sample-isolation-root", required=True)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    ws = _require_abs(args.workspace_root, "--workspace-root")
    iso = _require_abs(args.failed_sample_isolation_root, "--failed-sample-isolation-root")
    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    blockers: List[str] = []

    if not iso.is_dir():
        blockers.append("failed_sample_isolation_root_not_dir")

    docs = {
        "image_input_gate": ws / "docs/architecture/ocr/LUNA_OCR_IMAGE_INPUT_GATE_V0.md",
        "size_pixel_budget": ws / "docs/architecture/ocr/LUNA_OCR_IMAGE_SIZE_AND_PIXEL_BUDGET_POLICY_V0.md",
        "roi_first": ws / "docs/architecture/ocr/LUNA_OCR_ROI_FIRST_INPUT_POLICY_V0.md",
        "downscale_tiling": ws / "docs/architecture/ocr/LUNA_OCR_DOWNSCALE_AND_TILING_POLICY_V0.md",
        "coordinate_reconstruction": ws / "docs/architecture/ocr/LUNA_OCR_TILE_COORDINATE_RECONSTRUCTION_POLICY_V0.md",
        "evaluation_governance": ws / "docs/architecture/evaluation/LUNA_EVALUATION_OCR_INPUT_SIZE_GOVERNANCE_V0.md",
        "evaluation_go_pack": ws / "docs/architecture/evaluation/LUNA_EVALUATION_OCR_INPUT_SIZE_GOVERNANCE_GO_NO_GO_PACK_V0.md",
    }
    readme_ocr = ws / "docs/architecture/ocr/README.md"
    readme_eval = ws / "docs/architecture/evaluation/README.md"
    cfg = ws / "configs/ocr/ocr_image_input_governance_v0.example.json"

    for label, p in list(docs.items()) + [("readme_ocr", readme_ocr), ("readme_eval", readme_eval)]:
        if not p.is_file():
            blockers.append(f"missing_doc:{label}:{p}")

    if not cfg.is_file():
        blockers.append(f"missing_config:{cfg}")

    iso_needles = ("paddleocr_failed_sample_isolation", "size_sensitive")
    for label, p in docs.items():
        if not p.is_file():
            continue
        t = _read_text(p)
        _doc_must_contain(t, iso_needles, label, blockers)
        _doc_must_not_allow_full_bleed(t, p, blockers)

    for rm, label in ((readme_ocr, "readme_ocr"), (readme_eval, "readme_eval")):
        if rm.is_file():
            t = _read_text(rm)
            if "paddleocr_failed_sample_isolation" not in t.lower():
                blockers.append(f"readme_missing_isolation_ref:{label}")

    cfg_obj: Dict[str, Any] = {}
    if cfg.is_file():
        cfg_obj = _read_json(cfg)
        if str(cfg_obj.get("schema_version") or "") != "ocr_image_input_governance_v0":
            blockers.append("config_schema_version_mismatch")
        gate = cfg_obj.get("image_input_gate") if isinstance(cfg_obj.get("image_input_gate"), dict) else {}
        if gate.get("full_image_realtime_allowed") is not False:
            blockers.append("full_image_realtime_allowed_must_be_false")
        if gate.get("roi_first_required") is not True:
            blockers.append("roi_first_required_must_be_true")
        if not isinstance(cfg_obj.get("downscale_policy"), dict):
            blockers.append("missing_downscale_policy")
        if not isinstance(cfg_obj.get("tiling_policy"), dict):
            blockers.append("missing_tiling_policy")
        tp = cfg_obj.get("tiling_policy") if isinstance(cfg_obj.get("tiling_policy"), dict) else {}
        if tp.get("requires_coordinate_reconstruction") is not True:
            blockers.append("tiling_requires_coordinate_reconstruction_must_be_true")
        sc = cfg_obj.get("source_chain_policy") if isinstance(cfg_obj.get("source_chain_policy"), dict) else {}
        for k in ("record_original_image_ref", "record_transformed_image_ref", "record_tile_ref", "record_coordinate_transform"):
            if sc.get(k) is not True:
                blockers.append(f"source_chain_missing_true:{k}")
        st = cfg_obj.get("stcm_policy") if isinstance(cfg_obj.get("stcm_policy"), dict) else {}
        for k in ("large_image_default_async", "expired_tile_result_cannot_drive_action", "timeout_must_notify_orchestrator"):
            if st.get(k) is not True:
                blockers.append(f"stcm_policy_missing_true:{k}")
        fb = cfg_obj.get("forbidden_actions") if isinstance(cfg_obj.get("forbidden_actions"), dict) else {}
        for k in (
            "send_oversized_full_image_to_realtime_ocr",
            "drop_coordinate_mapping",
            "force_reading_order_without_confidence",
            "direct_midplatform_write",
            "direct_world_model_write",
        ):
            if fb.get(k) is not True:
                blockers.append(f"forbidden_actions_must_be_true:{k}")

    verdict = "GO" if not blockers else "NO_GO"

    size_matrix = {
        "schema": "ocr_input_size_policy_matrix_v0",
        "phase": "Phase-OCR-Input-Size-Governance-001",
        "rows": [
            {"policy": "image_input_gate", "doc": str(docs["image_input_gate"]), "required": True},
            {"policy": "size_pixel_budget", "doc": str(docs["size_pixel_budget"]), "required": True},
            {"policy": "roi_first", "doc": str(docs["roi_first"]), "required": True},
            {"policy": "downscale_tiling", "doc": str(docs["downscale_tiling"]), "required": True},
            {"policy": "coordinate_reconstruction", "doc": str(docs["coordinate_reconstruction"]), "required": True},
            {"policy": "evaluation_alignment", "doc": str(docs["evaluation_governance"]), "required": True},
            {"policy": "evaluation_go_pack", "doc": str(docs["evaluation_go_pack"]), "required": True},
        ],
    }

    sc_keys = list((cfg_obj.get("source_chain_policy") or {}).keys()) if cfg_obj else []
    st_keys = list((cfg_obj.get("stcm_policy") or {}).keys()) if cfg_obj else []
    transform_matrix = {
        "schema": "ocr_input_transform_policy_matrix_v0",
        "phase": "Phase-OCR-Input-Size-Governance-001",
        "rows": [
            {"transform": "downscale", "config_key": "downscale_policy", "required_fields": ["enabled", "preferred_max_side", "fallback_max_side"]},
            {"transform": "tiling", "config_key": "tiling_policy", "required_fields": ["tile_max_side", "tile_overlap_ratio", "requires_coordinate_reconstruction"]},
            {"transform": "coordinate_reconstruction", "config_key": "tiling_policy", "required_fields": ["requires_duplicate_text_merge"]},
            {"transform": "source_chain", "config_key": "source_chain_policy", "required_fields": sc_keys},
            {"transform": "stcm_coordination", "config_key": "stcm_policy", "required_fields": st_keys},
        ],
    }

    summary = {
        "schema": "ocr_input_size_governance_summary_v0",
        "phase": "Phase-OCR-Input-Size-Governance-001",
        "governance_verdict": verdict,
        "input_failed_sample_isolation_root": str(iso),
        "workspace_root": str(ws),
        "config_example_path": str(cfg),
        "documentation_paths": {k: str(v) for k, v in docs.items()},
        "readme_paths": {"ocr": str(readme_ocr), "evaluation": str(readme_eval)},
        "interpretation": "governance_docs_and_static_config_only_not_runtime_go",
        "paddleocr_size_sensitive_trace": {
            "reference_dir": str(iso),
            "documented_samples": ["labeled_007", "labeled_010", "labeled_019"],
            "note": "Written into policy docs as empirical justification for ImageInputGate and pixel budgets.",
        },
    }

    _write_json(out / "ocr_input_size_policy_matrix.json", size_matrix)
    _write_json(out / "ocr_input_transform_policy_matrix.json", transform_matrix)
    _write_json(out / "ocr_input_size_governance_summary.json", summary)
    rep = {
        "schema": "ocr_input_size_governance_verifier_report_v0",
        "phase": "Phase-OCR-Input-Size-Governance-001",
        "output_root": str(out),
        "verdict": verdict,
        "blockers": blockers,
    }
    _write_json(out / "ocr_input_size_governance_verifier_report.json", rep)

    print(json.dumps({"output_root": str(out), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
