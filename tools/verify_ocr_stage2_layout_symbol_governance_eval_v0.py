#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify Phase-Mainline-GuardedTrial-012-Improve-B layout/symbol governance outputs.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _nonempty(path: Path) -> bool:
    try:
        return path.is_file() and bool(path.read_text(encoding="utf-8").strip())
    except Exception:
        return False


def _case(name: str, ok: bool, details: Dict[str, Any]) -> Dict[str, Any]:
    return {"case": name, "ok": bool(ok), "details": details}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--expected-count", type=int, default=12)
    ap.add_argument("--sample-regex", default=r"^ocr_(?:[1-9]|1[0-2])\.(?:png|jpg|jpeg|webp)$")
    args = ap.parse_args()

    outp = Path(args.output_root).expanduser()
    if not outp.is_absolute():
        raise SystemExit("ERROR: --output-root must be absolute")
    out_root = outp.resolve()

    required = [
        "ocr_stage2_layout_symbol_summary.json",
        "ocr_stage2_layout_symbol_sample_matrix.json",
        "ocr_stage2_visual_symbol_candidates.json",
        "ocr_stage2_visual_glyph_candidates.json",
        "ocr_stage2_layout_groups.json",
        "ocr_stage2_reading_order_candidates.json",
        "ocr_stage2_grouped_raw_text_report.json",
        "ocr_stage2_symbol_noise_filter_report.json",
        "ocr_stage2_layout_symbol_trace.jsonl",
        "ocr_stage2_layout_symbol_replay.jsonl",
        "ocr_stage2_layout_symbol_whitebox.jsonl",
        "layout_symbol_eval_notes.md",
    ]

    results: List[Dict[str, Any]] = []
    results.append(_case("A_output_root_exists", out_root.is_dir(), {"output_root": str(out_root)}))
    for fn in required:
        p = out_root / fn
        ok = p.is_file()
        if fn.endswith((".jsonl", ".md")):
            ok = ok and _nonempty(p)
        results.append(_case(f"file_{fn}", ok, {"path": str(p)}))

    summ = _read_json(out_root / "ocr_stage2_layout_symbol_summary.json")
    sc = int(summ.get("sample_count") or -1)
    results.append(_case("B_sample_count_matches", sc == int(args.expected_count), {"sample_count": sc, "expected": args.expected_count}))

    # Sample scope validation
    rx = re.compile(str(args.sample_regex), re.IGNORECASE)
    mat = _read_json(out_root / "ocr_stage2_layout_symbol_sample_matrix.json")
    if not isinstance(mat, list):
        mat = []
    sample_ids = [str(x.get("sample_id") or "") for x in mat if isinstance(x, dict)]
    # Note: sample_id is stem; enforce by checking original file basename pattern in sample_matrix image_path
    ok_scope = True
    for x in mat:
        if not isinstance(x, dict):
            continue
        ip = str(x.get("image_path") or "")
        bn = Path(ip).name
        if not rx.fullmatch(bn):
            ok_scope = False
    results.append(_case("C_sample_scope_regex", ok_scope and len(mat) == args.expected_count, {"count": len(mat)}))

    # Provider must be rapidocr and not macos vision
    ok_provider = True
    for x in mat:
        if not isinstance(x, dict):
            continue
        ps = str(x.get("provider_selected") or "")
        if "rapidocr" not in ps.lower():
            ok_provider = False
        if "macos_vision" in ps.lower():
            ok_provider = False
    results.append(_case("D_provider_rapidocr_only", ok_provider, {}))

    # Hard boundary from whitebox
    wb_line = (out_root / "ocr_stage2_layout_symbol_whitebox.jsonl").read_text(encoding="utf-8").strip().splitlines()[-1]
    try:
        wb = json.loads(wb_line)
    except Exception:
        wb = {}
    ha = (wb.get("hard_audit") or {}) if isinstance(wb, dict) else {}
    boundary = {
        "semantic_false": ha.get("semantic_interpretation_enabled") is False,
        "midplatform_false": ha.get("midplatform_invoked") is False,
        "scene_delta_false": ha.get("scene_delta_invoked") is False,
        "world_context_false": ha.get("world_context_invoked") is False,
        "downstream_zero": ha.get("downstream_invocation_count") == 0,
    }
    for k, ok in boundary.items():
        results.append(_case(f"E_{k}", ok, {"hard_audit": ha}))

    all_ok = all(r["ok"] for r in results)
    verdict = "GO" if all_ok else "NO_GO"
    print(
        json.dumps(
            {
                "verifier": "verify_ocr_stage2_layout_symbol_governance_eval_v0",
                "verdict": verdict,
                "output_root": str(out_root),
                "hard_blockers": [r["case"] for r in results if not r["ok"]],
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

