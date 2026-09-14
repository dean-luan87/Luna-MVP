#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-001 — Verify RapidOCR synthetic eval outputs v0.
"""

from __future__ import annotations

import argparse
import json
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
    ap.add_argument("--dataset-root", required=True)
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--expected-count", type=int, default=200)
    args = ap.parse_args()

    dr = Path(args.dataset_root).expanduser()
    outp = Path(args.output_root).expanduser()
    if not dr.is_absolute() or not outp.is_absolute():
        raise SystemExit("ERROR: --dataset-root and --output-root must be absolute")
    dataset_root = dr.resolve()
    out_root = outp.resolve()

    results: List[Dict[str, Any]] = []
    results.append(_case("A_dataset_root_readable", dataset_root.is_dir(), {"dataset_root": str(dataset_root)}))
    results.append(_case("B_manifest_exists", (dataset_root / "manifest.jsonl").is_file(), {}))
    results.append(_case("C_output_root_exists", out_root.is_dir(), {"output_root": str(out_root)}))

    required = [
        "synthetic_eval_summary.json",
        "synthetic_sample_eval_matrix.json",
        "category_cer_summary.json",
        "chinese_recall_summary.json",
        "garbled_report.json",
        "failure_cases.json",
        "rapidocr_synthetic_trace.jsonl",
        "rapidocr_synthetic_replay.jsonl",
        "rapidocr_synthetic_whitebox.jsonl",
        "synthetic_eval_notes.md",
    ]
    for fn in required:
        p = out_root / fn
        ok = p.is_file()
        if fn.endswith((".jsonl", ".md")):
            ok = ok and _nonempty(p)
        results.append(_case(f"file_{fn}", ok, {"path": str(p)}))

    summ = _read_json(out_root / "synthetic_eval_summary.json")
    results.append(_case("D_provider_is_rapidocr", str(summ.get("provider") or "") == "rapidocr_onnxruntime_v0", {"provider": summ.get("provider")}))
    results.append(_case("E_no_runtime_integration", (summ.get("hard_audit") or {}).get("runtime_integration") is False, {"hard_audit": summ.get("hard_audit")}))

    mat = _read_json(out_root / "synthetic_sample_eval_matrix.json")
    results.append(_case("F_matrix_count", isinstance(mat, list) and len(mat) == int(args.expected_count), {"count": len(mat) if isinstance(mat, list) else None, "expected": int(args.expected_count)}))

    # Whitebox hard audit
    wb_line = (out_root / "rapidocr_synthetic_whitebox.jsonl").read_text(encoding="utf-8").strip().splitlines()[-1]
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
    }
    for k, ok in boundary.items():
        results.append(_case(f"G_{k}", ok, {"hard_audit": ha}))

    all_ok = all(r["ok"] for r in results)
    verdict = "GO" if all_ok else "NO_GO"
    print(json.dumps({"verifier": "verify_rapidocr_synthetic_eval_v0", "verdict": verdict, "dataset_root": str(dataset_root), "output_root": str(out_root), "hard_blockers": [r["case"] for r in results if not r["ok"]], "results": results}, ensure_ascii=False, indent=2))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

