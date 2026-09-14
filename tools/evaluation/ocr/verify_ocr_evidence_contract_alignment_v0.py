#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-OCR-Evidence-Contract-Alignment-001 — Verifier for align_paddleocr_normalized_to_ocr_evidence_v0 outputs.
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


def _doc_required_keys(doc: Dict[str, Any]) -> bool:
    for k in (
        "schema_version",
        "provider",
        "api_family",
        "call_method",
        "image_path",
        "evaluation_run_at",
        "evidence_items",
        "text_joined",
        "source_reference_chain",
        "confidence_summary",
        "reading_order_candidate",
        "layout_assumption",
        "limits",
    ):
        if k not in doc:
            return False
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--alignment-root", required=True, help="Output root of align_paddleocr_normalized_to_ocr_evidence_v0.py")
    ap.add_argument("--adapter-contract-root", default="", help="Optional; else from alignment summary.")
    args = ap.parse_args()

    root = _require_abs(args.alignment_root, "--alignment-root")
    blockers: List[str] = []

    sum_p = root / "ocr_evidence_alignment_summary.json"
    if not sum_p.is_file():
        blockers.append("missing_alignment_summary")
    summary: Dict[str, Any] = _read_json(sum_p) if sum_p.is_file() else {}

    adapter_root = Path(str(args.adapter_contract_root or summary.get("adapter_contract_root") or "")).expanduser()
    ads: Dict[str, Any] = {}
    if not adapter_root.is_absolute() or not adapter_root.is_dir():
        blockers.append("missing_or_invalid_adapter_contract_root")
    else:
        ad_sum = adapter_root / "paddleocr_api_adapter_contract_summary.json"
        if not ad_sum.is_file():
            blockers.append("missing_adapter_contract_summary")
        else:
            ads = _read_json(ad_sum)
            if ads.get("adapter_contract_verdict") != "GO":
                blockers.append("adapter_contract_verdict_not_go")

    norm_p = adapter_root / "paddleocr_api_adapter_normalized_result.json" if adapter_root.is_dir() else None
    if norm_p and not norm_p.is_file():
        blockers.append("missing_adapter_normalized_result")
    raw_p = adapter_root / "paddleocr_api_adapter_raw_result.json" if adapter_root.is_dir() else None
    raw_doc: Dict[str, Any] = _read_json(raw_p) if raw_p and raw_p.is_file() else {}
    raw_results = raw_doc.get("results") if isinstance(raw_doc.get("results"), list) else []

    uni_p = root / "ocr_evidence_unified_result_v0.json"
    if not uni_p.is_file():
        blockers.append("missing_unified_result")
    unified: Dict[str, Any] = _read_json(uni_p) if uni_p.is_file() else {}
    docs = unified.get("evidence_documents") if isinstance(unified.get("evidence_documents"), list) else []

    for name in (
        "ocr_evidence_item_matrix.json",
        "ocr_evidence_source_reference_chain.json",
        "ocr_evidence_confidence_summary.json",
        "ocr_evidence_alignment_audit_report.json",
    ):
        if not (root / name).is_file():
            blockers.append(f"missing:{name}")

    aud_p = root / "ocr_evidence_alignment_audit_report.json"
    aud: Dict[str, Any] = _read_json(aud_p) if aud_p.is_file() else {}
    for k in (
        "network_request_invoked",
        "ocr_routing_changed",
        "rapidocr_replaced",
        "runtime_integration",
        "whitebox_integration",
        "midplatform_invoked",
    ):
        if aud.get(k) is True:
            blockers.append(str(k))

    if aud.get("world_model_written") is True:
        blockers.append("world_model_written")
    if aud.get("midplatform_semantics_written") is True:
        blockers.append("midplatform_semantics_written")

    av = str(summary.get("alignment_verdict") or "")
    if av == "GO" and ads and ads.get("adapter_contract_verdict") != "GO":
        blockers.append("alignment_go_but_adapter_not_go")

    for di, doc in enumerate(docs):
        if not isinstance(doc, dict):
            blockers.append(f"doc_not_dict:{di}")
            continue
        if not _doc_required_keys(doc):
            blockers.append(f"doc_missing_keys:{di}")
        chain = doc.get("source_reference_chain") if isinstance(doc.get("source_reference_chain"), dict) else {}
        for ck in (
            "adapter_contract_root",
            "materialize_root",
            "pinned_manifest_path",
            "raw_result_path",
            "normalized_result_path",
        ):
            if not chain.get(ck):
                blockers.append(f"chain_missing:{ck}:doc_{di}")
        items = doc.get("evidence_items") if isinstance(doc.get("evidence_items"), list) else []
        joined = str(doc.get("text_joined") or "").strip()
        if not items:
            blockers.append(f"evidence_items_empty:doc_{di}")
        if not joined:
            blockers.append(f"text_joined_empty:doc_{di}")
        raw_r = raw_results[di].get("raw") if di < len(raw_results) and isinstance(raw_results[di], dict) else None
        if _raw_contains_rec_texts(raw_r) and not items:
            blockers.append(f"raw_has_text_evidence_empty:doc_{di}")
        for ii, it in enumerate(items):
            if not isinstance(it, dict):
                blockers.append(f"item_not_dict:{di}:{ii}")
                continue
            if "text" not in it or "source_index" not in it:
                blockers.append(f"item_missing_core:{di}:{ii}")
            if "score" not in it:
                blockers.append(f"item_missing_score_key:{di}:{ii}")
            if "polygon" not in it:
                blockers.append(f"item_missing_polygon_key:{di}:{ii}")
            if it.get("provider") != doc.get("provider"):
                blockers.append(f"item_provider_mismatch:{di}:{ii}")
            if it.get("call_method") != doc.get("call_method"):
                blockers.append(f"item_call_method_mismatch:{di}:{ii}")

    verdict = "NO_GO" if blockers or av == "NO_GO" else ("GO" if av == "GO" else "CONDITIONAL_GO")

    rep = {
        "schema": "ocr_evidence_alignment_verifier_report_v0",
        "phase": "Phase-OCR-Evidence-Contract-Alignment-001",
        "alignment_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "alignment_verdict_from_summary": av,
    }
    (root / "ocr_evidence_alignment_verifier_report.json").write_text(
        json.dumps(rep, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"alignment_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict != "NO_GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
