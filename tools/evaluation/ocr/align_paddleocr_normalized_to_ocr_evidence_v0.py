#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-OCR-Evidence-Contract-Alignment-001 — Map PaddleOCR adapter normalized result → unified OCR evidence v0.

Evaluation-only: no mainline, no routing, no RapidOCR replacement, no MidPlatform semantics.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import statistics
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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


def _confidence_from_scores(scores: List[Optional[float]]) -> Dict[str, Any]:
    vals = [float(s) for s in scores if s is not None and isinstance(s, (int, float))]
    if not vals:
        return {"item_count": len(scores), "score_min": None, "score_max": None, "score_mean": None}
    return {
        "item_count": len(scores),
        "score_min": round(min(vals), 6),
        "score_max": round(max(vals), 6),
        "score_mean": round(statistics.mean(vals), 6),
    }


def _build_evidence_document(
    *,
    norm_block: Dict[str, Any],
    raw_block: Optional[Dict[str, Any]],
    adapter_root: Path,
    materialize_root: Path,
    pinned_path: Path,
    model_root: str,
    run_at: str,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], Dict[str, Any]]:
    """Returns (unified_doc, item_matrix_rows, polygon_summary)."""
    image_path = str(norm_block.get("image_path") or "")
    provider = str(norm_block.get("provider") or "paddleocr")
    api_family = str(norm_block.get("api_family") or "current_api")
    call_method = str(norm_block.get("call_method") or "unknown")
    text_joined = str(norm_block.get("text_joined") or "").strip()
    text_items = norm_block.get("text_items") if isinstance(norm_block.get("text_items"), list) else []

    evidence_items: List[Dict[str, Any]] = []
    matrix_rows: List[Dict[str, Any]] = []
    poly_present = 0
    score_present = 0

    for it in text_items:
        if not isinstance(it, dict):
            continue
        idx = int(it.get("index", len(evidence_items)))
        text = str(it.get("text") or "")
        score = it.get("score")
        if score is not None and isinstance(score, (int, float)):
            score_present += 1
        poly = it.get("polygon")
        if isinstance(poly, list) and poly:
            poly_present += 1
        ev = {
            "source_index": idx,
            "text": text,
            "score": float(score) if isinstance(score, (int, float)) else None,
            "polygon": poly if isinstance(poly, list) else None,
            "box_type": "polygon",
            "reading_order_index": idx,
            "layout_block_id": None,
            "provider": provider,
            "call_method": call_method,
            "raw_field_refs": {
                "text": f"rec_texts[{idx}]",
                "score": f"rec_scores[{idx}]",
                "polygon": f"rec_polys[{idx}]",
            },
        }
        evidence_items.append(ev)
        matrix_rows.append(
            {
                "source_index": idx,
                "text": text,
                "has_score": score is not None,
                "has_polygon": bool(poly),
                "provider": provider,
                "call_method": call_method,
            }
        )

    if not text_joined and evidence_items:
        text_joined = " ".join(e["text"] for e in evidence_items if e.get("text"))

    scores_list: List[Optional[float]] = [e.get("score") for e in evidence_items]
    conf = _confidence_from_scores(scores_list)

    chain = {
        "adapter_contract_root": str(adapter_root),
        "materialize_root": str(materialize_root),
        "pinned_manifest_path": str(pinned_path),
        "model_root": model_root,
        "raw_result_path": str(adapter_root / "paddleocr_api_adapter_raw_result.json"),
        "normalized_result_path": str(adapter_root / "paddleocr_api_adapter_normalized_result.json"),
        "adapter_summary_path": str(adapter_root / "paddleocr_api_adapter_contract_summary.json"),
        "adapter_audit_path": str(adapter_root / "paddleocr_api_adapter_audit_report.json"),
    }
    if raw_block is not None:
        chain["source_raw_result_ref"] = "paddleocr_api_adapter_raw_result.json#results"
    chain["source_normalized_result_ref"] = "paddleocr_api_adapter_normalized_result.json#results"

    unified = {
        "schema_version": "ocr_evidence_unified_result_v0",
        "phase": "Phase-OCR-Evidence-Contract-Alignment-001",
        "provider": provider,
        "api_family": api_family,
        "call_method": call_method,
        "image_path": image_path,
        "evaluation_run_at": run_at,
        "text_joined": text_joined,
        "evidence_items": evidence_items,
        "confidence_summary": conf,
        "reading_order_candidate": {
            "strategy": "provider_order",
            "confidence": "low_to_medium",
            "reason": "PaddleOCR output order used; no layout governance applied",
        },
        "layout_assumption": {
            "layout_blocking_applied": False,
            "line_grouping_applied": False,
            "multi_region_assignment_applied": False,
        },
        "source_reference_chain": chain,
        "limits": [
            "evaluation_only",
            "not_runtime_provider",
            "not_midplatform_input",
            "no_layout_governance",
            "no_scene_interpretation",
        ],
    }

    poly_summary = {
        "items_total": len(evidence_items),
        "polygon_present_count": poly_present,
        "score_present_count": score_present,
    }
    return unified, matrix_rows, poly_summary


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=str(REPO_ROOT))
    ap.add_argument("--adapter-contract-root", required=True)
    ap.add_argument("--materialize-root", required=True)
    ap.add_argument("--pinned-manifest", required=True)
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()

    adapter_root = _require_abs(args.adapter_contract_root, "--adapter-contract-root")
    materialize_root = _require_abs(args.materialize_root, "--materialize-root")
    pinned_path = _require_abs(args.pinned_manifest, "--pinned-manifest")

    if args.output_root.strip():
        out_root = _require_abs(args.output_root, "--output-root")
    else:
        stamp = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        out_root = (Path.home() / "LunaRuntime" / "logs" / "evaluation" / f"ocr_evidence_contract_alignment_001_{stamp}").resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    sum_p = adapter_root / "paddleocr_api_adapter_contract_summary.json"
    if not sum_p.is_file():
        raise SystemExit(f"ERROR: missing adapter summary: {sum_p}")
    adapter_summary = json.loads(sum_p.read_text(encoding="utf-8"))
    if adapter_summary.get("adapter_contract_verdict") != "GO":
        raise SystemExit(
            f"ERROR: adapter_contract_verdict must be GO, got {adapter_summary.get('adapter_contract_verdict')}"
        )

    norm_p = adapter_root / "paddleocr_api_adapter_normalized_result.json"
    raw_p = adapter_root / "paddleocr_api_adapter_raw_result.json"
    audit_p = adapter_root / "paddleocr_api_adapter_audit_report.json"
    for p, label in ((norm_p, "normalized"), (raw_p, "raw"), (audit_p, "audit")):
        if not p.is_file():
            raise SystemExit(f"ERROR: missing adapter {label}: {p}")

    normalized = json.loads(norm_p.read_text(encoding="utf-8"))
    raw_doc = json.loads(raw_p.read_text(encoding="utf-8"))
    adapter_audit = json.loads(audit_p.read_text(encoding="utf-8"))

    pinned = json.loads(pinned_path.read_text(encoding="utf-8"))
    model_root = str(pinned.get("model_root") or "")

    run_at = _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    norm_results = normalized.get("results") if isinstance(normalized.get("results"), list) else []
    raw_results = raw_doc.get("results") if isinstance(raw_doc.get("results"), list) else []

    evidence_documents: List[Dict[str, Any]] = []
    all_matrix: List[Dict[str, Any]] = []
    polygon_summaries: List[Dict[str, Any]] = []

    for i, block in enumerate(norm_results):
        if not isinstance(block, dict):
            continue
        raw_block = raw_results[i] if i < len(raw_results) and isinstance(raw_results[i], dict) else None
        ud, rows, ps = _build_evidence_document(
            norm_block=block,
            raw_block=raw_block,
            adapter_root=adapter_root,
            materialize_root=materialize_root,
            pinned_path=pinned_path,
            model_root=model_root,
            run_at=run_at,
        )
        evidence_documents.append(ud)
        for r in rows:
            r["document_index"] = i
        all_matrix.extend(rows)
        polygon_summaries.append({"document_index": i, **ps})

    alignment_verdict = "NO_GO"
    errors: List[str] = []
    if adapter_summary.get("adapter_contract_verdict") != "GO":
        alignment_verdict = "NO_GO"
        errors.append("adapter_contract_not_go")
    elif not evidence_documents:
        alignment_verdict = "NO_GO"
        errors.append("no_evidence_documents")
    else:
        alignment_verdict = "GO"
        for i, doc in enumerate(evidence_documents):
            items = doc.get("evidence_items") or []
            joined = str(doc.get("text_joined") or "").strip()
            if not items or not joined:
                alignment_verdict = "NO_GO"
                errors.append(f"empty_items_or_joined:doc_{i}")
                break
            raw_r = raw_results[i].get("raw") if i < len(raw_results) and isinstance(raw_results[i], dict) else None
            if _raw_contains_rec_texts(raw_r) and not items:
                alignment_verdict = "NO_GO"
                errors.append(f"raw_has_text_no_items:doc_{i}")
                break
        if alignment_verdict == "GO":
            for doc in evidence_documents:
                for it in doc.get("evidence_items") or []:
                    if not isinstance(it, dict):
                        continue
                    if it.get("score") is None or it.get("polygon") is None:
                        alignment_verdict = "CONDITIONAL_GO"
            if alignment_verdict == "GO":
                for ps in polygon_summaries:
                    tot = int(ps.get("items_total") or 0)
                    if tot <= 0:
                        continue
                    if int(ps.get("polygon_present_count") or 0) < tot:
                        alignment_verdict = "CONDITIONAL_GO"
                        break

    alignment_audit = {
        "schema": "ocr_evidence_alignment_audit_report_v0",
        "phase": "Phase-OCR-Evidence-Contract-Alignment-001",
        "network_request_invoked": bool(adapter_audit.get("network_request_invoked")),
        "ocr_routing_changed": bool(adapter_audit.get("ocr_routing_changed")),
        "rapidocr_replaced": bool(adapter_audit.get("rapidocr_replaced")),
        "runtime_integration": bool(adapter_audit.get("runtime_integration")),
        "whitebox_integration": bool(adapter_audit.get("whitebox_integration")),
        "midplatform_invoked": bool(adapter_audit.get("midplatform_invoked")),
        "mainline_touched": bool(adapter_audit.get("mainline_touched")),
        "world_model_written": False,
        "midplatform_semantics_written": False,
        "adapter_contract_verdict": adapter_summary.get("adapter_contract_verdict"),
    }

    if alignment_audit["network_request_invoked"]:
        alignment_verdict = "NO_GO"
        errors.append("network_request_invoked")

    unified_payload = {
        "schema": "ocr_evidence_unified_bundle_v0",
        "phase": "Phase-OCR-Evidence-Contract-Alignment-001",
        "evaluation_run_at": run_at,
        "evidence_documents": evidence_documents,
    }

    chain_only = {
        "adapter_contract_root": str(adapter_root),
        "materialize_root": str(materialize_root),
        "pinned_manifest_path": str(pinned_path),
        "model_root": model_root,
        "raw_result_path": str(raw_p),
        "normalized_result_path": str(norm_p),
    }

    summary = {
        "schema": "ocr_evidence_alignment_summary_v0",
        "phase": "Phase-OCR-Evidence-Contract-Alignment-001",
        "alignment_verdict": alignment_verdict,
        "adapter_contract_root": str(adapter_root),
        "materialize_root": str(materialize_root),
        "pinned_manifest_path": str(pinned_path),
        "model_root": model_root,
        "evidence_document_count": len(evidence_documents),
        "errors": errors,
        "alignment_audit": alignment_audit,
    }

    _write_json(out_root / "ocr_evidence_unified_result_v0.json", unified_payload)
    _write_json(out_root / "ocr_evidence_item_matrix.json", {"schema": "ocr_evidence_item_matrix_v0", "rows": all_matrix})
    _write_json(out_root / "ocr_evidence_source_reference_chain.json", chain_only)
    _write_json(
        out_root / "ocr_evidence_confidence_summary.json",
        {"schema": "ocr_evidence_confidence_summary_v0", "by_document": [d.get("confidence_summary") for d in evidence_documents]},
    )
    _write_json(out_root / "ocr_evidence_alignment_audit_report.json", alignment_audit)
    _write_json(out_root / "ocr_evidence_alignment_summary.json", summary)

    notes = "\n".join(
        [
            "# OCR Evidence Contract Alignment v0",
            "",
            f"- **alignment_verdict**: `{alignment_verdict}`",
            f"- **output_root**: `{out_root}`",
            "",
            "## Scope limits",
            "",
            "- No complex reading-order governance, no layout ownership, no MidPlatform interpretation.",
            "- Evaluation-only; not runtime provider; not MidPlatform input.",
            "",
        ]
    )
    (out_root / "ocr_evidence_alignment_notes.md").write_text(notes, encoding="utf-8")

    print(json.dumps({"alignment_output_root": str(out_root), "alignment_verdict": alignment_verdict}, ensure_ascii=False))
    return 0 if alignment_verdict != "NO_GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
