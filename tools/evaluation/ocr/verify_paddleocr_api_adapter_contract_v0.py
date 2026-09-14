#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-API-Adapter-Contract-001 — Verifier for paddleocr_current_api_adapter_contract_v0 outputs.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _raw_contains_rec_texts(raw: Any) -> bool:
    if isinstance(raw, list):
        for block in raw:
            if isinstance(block, dict):
                rt = block.get("rec_texts")
                if isinstance(rt, list) and any(isinstance(t, str) and t.strip() for t in rt):
                    return True
                for v in block.values():
                    if _raw_contains_rec_texts(v):
                        return True
    if isinstance(raw, dict):
        rt = raw.get("rec_texts")
        if isinstance(rt, list) and any(isinstance(t, str) and t.strip() for t in rt):
            return True
        for v in raw.values():
            if _raw_contains_rec_texts(v):
                return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--adapter-root", required=True, help="Output root of paddleocr_current_api_adapter_contract_v0.py")
    ap.add_argument("--materialize-root", default="", help="Optional; else read from adapter summary.")
    args = ap.parse_args()

    root = _require_abs(args.adapter_root, "--adapter-root")
    blockers: List[str] = []

    sum_p = root / "paddleocr_api_adapter_contract_summary.json"
    if not sum_p.is_file():
        blockers.append("missing_adapter_summary")
    summary: Dict[str, Any] = _read_json(sum_p) if sum_p.is_file() else {}

    mat_root = Path(str(args.materialize_root or summary.get("materialize_root") or "")).expanduser()
    if not mat_root.is_absolute() or not mat_root.is_dir():
        blockers.append("missing_or_invalid_materialize_root")
    else:
        mat_sum_p = mat_root / "paddleocr_manifest_v1_cache_materialize_summary.json"
        if not mat_sum_p.is_file():
            blockers.append("missing_materialize_summary")
        else:
            ms = _read_json(mat_sum_p)
            if ms.get("materialize_verdict") != "GO":
                blockers.append("materialize_verdict_not_go")

    pinned_path = Path(str(summary.get("pinned_manifest") or ""))
    if not pinned_path.is_file():
        blockers.append("missing_pinned_manifest")

    for name in (
        "paddleocr_api_adapter_constructor_report.json",
        "paddleocr_api_adapter_call_report.json",
        "paddleocr_api_adapter_raw_result.json",
        "paddleocr_api_adapter_normalized_result.json",
        "paddleocr_api_adapter_error_report.json",
        "paddleocr_api_adapter_audit_report.json",
    ):
        if not (root / name).is_file():
            blockers.append(f"missing:{name}")

    cons_p = root / "paddleocr_api_adapter_constructor_report.json"
    cons: Dict[str, Any] = _read_json(cons_p) if cons_p.is_file() else {}
    if cons.get("constructor_ok") is not True:
        blockers.append("constructor_not_ok")

    audit_p = root / "paddleocr_api_adapter_audit_report.json"
    audit: Dict[str, Any] = _read_json(audit_p) if audit_p.is_file() else {}
    if audit.get("network_request_invoked") is True:
        blockers.append("network_request_invoked")
    if audit.get("ocr_routing_changed") is True:
        blockers.append("ocr_routing_changed")
    if audit.get("rapidocr_replaced") is True:
        blockers.append("rapidocr_replaced")
    if audit.get("runtime_integration") is True:
        blockers.append("runtime_integration")
    if audit.get("whitebox_integration") is True:
        blockers.append("whitebox_integration")
    if audit.get("midplatform_invoked") is True:
        blockers.append("midplatform_invoked")
    if audit.get("model_cache_modified") is True:
        blockers.append("model_cache_modified")
    if int(audit.get("sample_count") or 0) > 3:
        blockers.append("sample_count_gt_3")

    av = str(summary.get("adapter_contract_verdict") or "")
    if av == "GO" and cons.get("constructor_ok") is not True:
        blockers.append("adapter_go_but_constructor_failed")

    norm_p = root / "paddleocr_api_adapter_normalized_result.json"
    norm_doc: Dict[str, Any] = _read_json(norm_p) if norm_p.is_file() else {}
    results = norm_doc.get("results") if isinstance(norm_doc.get("results"), list) else []
    raw_p = root / "paddleocr_api_adapter_raw_result.json"
    raw_doc: Dict[str, Any] = _read_json(raw_p) if raw_p.is_file() else {}
    raw_results = raw_doc.get("results") if isinstance(raw_doc.get("results"), list) else []

    for i, (rw, nm) in enumerate(zip(raw_results, results)):
        if not isinstance(rw, dict) or not isinstance(nm, dict):
            blockers.append(f"malformed_result_pair:{i}")
            continue
        raw = rw.get("raw")
        if not _required_normalized_keys(nm):
            blockers.append(f"normalized_missing_keys:{i}")
        raw_has = _raw_contains_rec_texts(raw)
        joined = str(nm.get("text_joined") or "").strip()
        items = nm.get("text_items")
        n_items = len(items) if isinstance(items, list) else 0
        if raw_has and (not joined or n_items == 0):
            blockers.append(f"raw_has_text_but_normalized_empty:{i}")

    call_p = root / "paddleocr_api_adapter_call_report.json"
    call_doc: Dict[str, Any] = _read_json(call_p) if call_p.is_file() else {}
    calls = call_doc.get("calls") if isinstance(call_doc.get("calls"), list) else []
    for i, c in enumerate(calls):
        if not isinstance(c, dict):
            continue
        if c.get("ok") is True and not c.get("call_method"):
            blockers.append(f"call_missing_method:{i}")

    verdict = "NO_GO" if blockers or av == "NO_GO" else ("GO" if av == "GO" else "CONDITIONAL_GO")

    rep = {
        "schema": "paddleocr_api_adapter_verifier_report_v0",
        "phase": "Phase-PaddleOCR-API-Adapter-Contract-001",
        "adapter_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "adapter_contract_verdict_from_summary": av,
    }
    (root / "paddleocr_api_adapter_verifier_report.json").write_text(
        json.dumps(rep, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"adapter_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict != "NO_GO" else 2


def _required_normalized_keys(nm: Dict[str, Any]) -> bool:
    for k in (
        "provider",
        "api_family",
        "call_method",
        "image_path",
        "text_items",
        "text_joined",
        "duration_ms",
        "error",
    ):
        if k not in nm:
            return False
    return True


if __name__ == "__main__":
    raise SystemExit(main())
