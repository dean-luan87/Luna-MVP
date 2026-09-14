#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-OCR-Bridge-Evidence-Pack-Alignment-001 — Map ocr_evidence_unified_result_v0 → OcrEvidencePackV0 candidate (evaluation-only).

No PaddleOCR, no OCR inference, no routing, no MidPlatform, no runtime.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.ocr_bridge.ocr_evidence_pack_contract_v0 import (  # noqa: E402
    build_ocr_evidence_pack_skeleton_v0,
)


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _polygon_to_aabb(poly: Any) -> List[float]:
    if not isinstance(poly, list) or not poly:
        return []
    xs: List[float] = []
    ys: List[float] = []
    for pt in poly:
        if isinstance(pt, (list, tuple)) and len(pt) >= 2:
            try:
                xs.append(float(pt[0]))
                ys.append(float(pt[1]))
            except (TypeError, ValueError):
                continue
    if not xs:
        return []
    return [min(xs), min(ys), max(xs), max(ys)]


def _contract_paths(repo: Path) -> Tuple[Path, Path]:
    md = repo / "docs" / "architecture" / "ocr_bridge" / "LUNA_OCR_EVIDENCE_PACK_CONTRACT_V0.md"
    impl = repo / "capabilities" / "ocr_bridge" / "ocr_evidence_pack_contract_v0.py"
    return md, impl


def _expected_pack_top_level_keys() -> Set[str]:
    sk = build_ocr_evidence_pack_skeleton_v0(
        pack_id="diff_probe",
        source_refs={
            "source_image_ref": "eval:probe",
            "source_provider_ref": "eval:probe",
            "source_quality_gate_ref": "eval:probe",
            "source_layout_ref": "eval:probe",
            "source_eligibility_gate_ref": "eval:probe",
        },
    )
    return set(sk.keys())


def _field_diff(expected: Set[str], candidate: Dict[str, Any]) -> Dict[str, Any]:
    ckeys = set(candidate.keys())
    return {
        "missing_in_candidate": sorted(expected - ckeys),
        "extra_in_candidate": sorted(ckeys - expected),
        "intersection": sorted(expected & ckeys),
    }


def _build_source_refs_for_pack(
    *,
    alignment_root: Path,
    adapter_root: Path,
    materialize_root: Path,
    pinned_manifest: Path,
    image_path: str,
) -> Dict[str, str]:
    return {
        "source_image_ref": f"eval:ocr_evidence_alignment:image_path={image_path}",
        "source_provider_ref": f"eval:paddleocr:adapter_root={adapter_root}",
        "source_quality_gate_ref": f"eval:ocr_evidence_alignment:{alignment_root}/ocr_evidence_confidence_summary.json",
        "source_layout_ref": f"eval:none:paddleocr_reading_order_only",
        "source_eligibility_gate_ref": f"eval:ocr_manifest:{materialize_root}",
        "routing_ref": f"eval:fixed_none:alignment={alignment_root}",
        "eval_paddleocr_alignment_root": str(alignment_root),
        "eval_paddleocr_adapter_root": str(adapter_root),
        "eval_pinned_manifest": str(pinned_manifest),
    }


def _map_unified_doc_to_pack(
    doc: Dict[str, Any],
    *,
    alignment_root: Path,
    adapter_root: Path,
    materialize_root: Path,
    pinned_manifest: Path,
    mapping_rows: List[Dict[str, Any]],
    provisional: List[str],
) -> Dict[str, Any]:
    pack_id = f"paddleocr_bridge_align_{uuid.uuid4().hex[:12]}"
    image_path = str(doc.get("image_path") or "")
    source_refs = _build_source_refs_for_pack(
        alignment_root=alignment_root,
        adapter_root=adapter_root,
        materialize_root=materialize_root,
        pinned_manifest=pinned_manifest,
        image_path=image_path,
    )
    pack = build_ocr_evidence_pack_skeleton_v0(pack_id=pack_id, source_refs=source_refs)

    eligible: List[Dict[str, Any]] = []
    items = doc.get("evidence_items") if isinstance(doc.get("evidence_items"), list) else []
    for it in items:
        if not isinstance(it, dict):
            continue
        idx = int(it.get("source_index", len(eligible)))
        poly = it.get("polygon")
        bbox = _polygon_to_aabb(poly)
        ev = {
            "evidence_id": f"paddleocr_eligible_{idx}",
            "evidence_type": "eligible_text",
            "text": str(it.get("text") or ""),
            "bbox": bbox,
            "layout_group_id": f"lg_paddleocr_{pack_id}_{idx}",
            "provider": str(it.get("provider") or "paddleocr"),
            "confidence": float(it["score"]) if isinstance(it.get("score"), (int, float)) else 0.0,
            "cer_estimate": None,
            "quality_gate": "CONDITIONAL_GO",
            "should_enter_fact_text_layer": False,
            "source_candidate_ids": [f"paddleocr_line_{idx}"],
            "source_refs": {
                "source_image_ref": source_refs["source_image_ref"],
                "provider_ref": f"eval:paddleocr:{it.get('call_method')}",
                "quality_gate_ref": source_refs["source_quality_gate_ref"],
                "layout_ref": source_refs["source_layout_ref"],
                "eligibility_gate_ref": source_refs["source_eligibility_gate_ref"],
                "routing_ref": source_refs["routing_ref"],
                "eval_paddleocr_raw_field_refs": it.get("raw_field_refs") if isinstance(it.get("raw_field_refs"), dict) else {},
            },
        }
        if isinstance(it.get("score"), (int, float)):
            ev["score"] = float(it["score"])
            provisional.append(f"eligible_text_evidence[{idx}].score")
        if poly is not None:
            ev["polygon"] = poly
            provisional.append(f"eligible_text_evidence[{idx}].polygon")
        if it.get("reading_order_index") is not None:
            ev["reading_order_index"] = it.get("reading_order_index")
            provisional.append(f"eligible_text_evidence[{idx}].reading_order_index")
        eligible.append(ev)
        mapping_rows.append(
            {
                "unified_path": f"evidence_items[{idx}]",
                "bridge_path": f"eligible_text_evidence[{idx}]",
                "evidence_type": "eligible_text",
            }
        )

    pack["eligible_text_evidence"] = eligible
    ro = doc.get("reading_order_candidate") if isinstance(doc.get("reading_order_candidate"), dict) else {}
    pack["reading_order"] = {
        "global_reading_order_available": True,
        "global_reading_order_confidence": 0.35 if str(ro.get("confidence") or "").startswith("low") else 0.6,
        "reading_order_uncertain": True,
        "reason": [
            str(ro.get("reason") or "paddleocr_provider_order"),
            "ocr_bridge_alignment_v0_no_layout_governance",
        ],
    }
    conf = doc.get("confidence_summary") if isinstance(doc.get("confidence_summary"), dict) else {}
    pack["uncertainty"] = {
        "has_uncertainty": True,
        "reasons": ["paddleocr_evaluation_alignment_v0", "not_validated_for_fact_text_layer"],
        "requires_preprocess": False,
        "requires_layout_branch": True,
        "requires_symbol_branch": False,
        "requires_glyph_branch": False,
        "requires_manual_review": True,
        "requires_provider_fallback": False,
        "paddleocr_confidence_summary": conf,
    }

    pack["evaluation_flags"] = {
        "evaluation_only": True,
        "not_runtime_input": True,
        "not_midplatform_input": True,
        "api_family": str(doc.get("api_family") or "current_api"),
        "call_method": str(doc.get("call_method") or ""),
    }
    provisional.append("evaluation_flags")

    chain = doc.get("source_reference_chain") if isinstance(doc.get("source_reference_chain"), dict) else {}
    pack["paddleocr_source_reference_chain"] = chain
    provisional.append("paddleocr_source_reference_chain")

    return pack


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=str(REPO_ROOT))
    ap.add_argument("--evidence-alignment-root", required=True)
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()

    repo = _require_abs(args.repo_root, "--repo-root")
    align_root = _require_abs(args.evidence_alignment_root, "--evidence-alignment-root")

    if args.output_root.strip():
        out_root = _require_abs(args.output_root, "--output-root")
    else:
        stamp = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        out_root = (Path.home() / "LunaRuntime" / "logs" / "evaluation" / f"ocr_bridge_evidence_pack_alignment_001_{stamp}").resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    al_sum_p = align_root / "ocr_evidence_alignment_summary.json"
    if not al_sum_p.is_file():
        raise SystemExit(f"ERROR: missing {al_sum_p}")
    al_sum = json.loads(al_sum_p.read_text(encoding="utf-8"))
    if al_sum.get("alignment_verdict") != "GO":
        raise SystemExit(f"ERROR: alignment_verdict must be GO, got {al_sum.get('alignment_verdict')}")

    uni_p = align_root / "ocr_evidence_unified_result_v0.json"
    matrix_p = align_root / "ocr_evidence_item_matrix.json"
    chain_p = align_root / "ocr_evidence_source_reference_chain.json"
    conf_p = align_root / "ocr_evidence_confidence_summary.json"
    aud_p = align_root / "ocr_evidence_alignment_audit_report.json"
    for p, label in (
        (uni_p, "unified"),
        (matrix_p, "item_matrix"),
        (chain_p, "chain"),
        (conf_p, "confidence"),
        (aud_p, "alignment_audit"),
    ):
        if not p.is_file():
            raise SystemExit(f"ERROR: missing {label}: {p}")

    unified = json.loads(uni_p.read_text(encoding="utf-8"))
    chain_file = json.loads(chain_p.read_text(encoding="utf-8"))
    alignment_audit = json.loads(aud_p.read_text(encoding="utf-8"))

    adapter_root = Path(str(chain_file.get("adapter_contract_root") or "")).resolve()
    materialize_root = Path(str(chain_file.get("materialize_root") or "")).resolve()
    pinned_manifest = Path(str(chain_file.get("pinned_manifest_path") or "")).resolve()

    md_path, impl_path = _contract_paths(repo)
    contract_md_found = md_path.is_file()
    contract_impl_found = impl_path.is_file()
    contract_reference_found = contract_md_found and contract_impl_found
    contract_reference_paths = {
        "LUNA_OCR_EVIDENCE_PACK_CONTRACT_V0.md": str(md_path) if contract_md_found else None,
        "ocr_evidence_pack_contract_v0.py": str(impl_path) if contract_impl_found else None,
    }

    docs = unified.get("evidence_documents") if isinstance(unified.get("evidence_documents"), list) else []
    mapping_rows: List[Dict[str, Any]] = []
    provisional_fields: List[str] = []
    pack_candidates: List[Dict[str, Any]] = []

    for doc in docs:
        if isinstance(doc, dict):
            pack_candidates.append(
                _map_unified_doc_to_pack(
                    doc,
                    alignment_root=align_root,
                    adapter_root=adapter_root,
                    materialize_root=materialize_root,
                    pinned_manifest=pinned_manifest,
                    mapping_rows=mapping_rows,
                    provisional=provisional_fields,
                )
            )

    primary = pack_candidates[0] if pack_candidates else {}
    expected_keys = _expected_pack_top_level_keys()
    diff = _field_diff(expected_keys, primary)

    lost_in_bridge = list(diff.get("missing_in_candidate") or [])
    bridge_audit = {
        "schema": "ocr_bridge_evidence_pack_audit_report_v0",
        "phase": "Phase-OCR-Bridge-Evidence-Pack-Alignment-001",
        "network_request_invoked": False,
        "ocr_routing_changed": False,
        "rapidocr_replaced": False,
        "runtime_integration": False,
        "whitebox_integration": False,
        "midplatform_invoked": False,
        "mainline_touched": False,
        "world_model_written": False,
        "midplatform_semantics_written": False,
        "paddleocr_invoked": False,
        "ocr_inference_invoked": False,
        "alignment_audit_echo": {k: alignment_audit.get(k) for k in ("network_request_invoked", "ocr_routing_changed")},
    }

    bridge_verdict = "NO_GO"
    errors = []
    if al_sum.get("alignment_verdict") != "GO":
        bridge_verdict = "NO_GO"
        errors.append("alignment_verdict_not_go")
    elif not pack_candidates:
        bridge_verdict = "NO_GO"
        errors.append("no_pack_candidates")
    else:
        for p in pack_candidates:
            evs = p.get("eligible_text_evidence") or []
            joined = " ".join(str(e.get("text") or "") for e in evs if isinstance(e, dict))
            if not evs or not joined.strip():
                bridge_verdict = "NO_GO"
                errors.append("empty_eligible_evidence_or_text")
                break
        else:
            if not contract_reference_found:
                bridge_verdict = "CONDITIONAL_GO"
                errors.append("missing_contract_reference")
            else:
                bridge_verdict = "GO"
                if lost_in_bridge:
                    bridge_verdict = "CONDITIONAL_GO"
                    errors.append(f"skeleton_keys_missing_in_candidate:{lost_in_bridge}")

    summary = {
        "schema": "ocr_bridge_evidence_pack_alignment_summary_v0",
        "phase": "Phase-OCR-Bridge-Evidence-Pack-Alignment-001",
        "bridge_pack_verdict": bridge_verdict,
        "evidence_alignment_root": str(align_root),
        "adapter_contract_root": str(adapter_root),
        "materialize_root": str(materialize_root),
        "pinned_manifest_path": str(pinned_manifest),
        "contract_reference_found": contract_reference_found,
        "contract_reference_paths": contract_reference_paths,
        "pack_candidate_count": len(pack_candidates),
        "errors": errors,
        "bridge_audit": bridge_audit,
        "provisional_fields": sorted(set(provisional_fields)),
        "lost_fields": sorted(set(lost_in_bridge)),
    }

    chain_out = {
        **chain_file,
        "evidence_alignment_root": str(align_root),
        "bridge_alignment_output_root": str(out_root),
        "ocr_evidence_unified_result_ref": str(uni_p),
    }

    _write_json(out_root / "ocr_bridge_evidence_pack_candidate_v0.json", {"packs": pack_candidates})
    _write_json(out_root / "ocr_bridge_evidence_pack_field_diff.json", diff)
    _write_json(out_root / "ocr_bridge_evidence_pack_mapping_matrix.json", {"rows": mapping_rows})
    _write_json(out_root / "ocr_bridge_evidence_pack_source_reference_chain.json", chain_out)
    _write_json(out_root / "ocr_bridge_evidence_pack_audit_report.json", bridge_audit)
    _write_json(out_root / "ocr_bridge_evidence_pack_alignment_summary.json", summary)

    notes = "\n".join(
        [
            "# OCR Bridge Evidence Pack Alignment v0",
            "",
            f"- **bridge_pack_verdict**: `{bridge_verdict}`",
            f"- **contract_reference_found**: `{contract_reference_found}`",
            "",
            "## Limits",
            "",
            "- No PaddleOCR execution; no OCR inference; no routing; no MidPlatform.",
            "",
            "## Provisional / extension fields",
            "",
            json.dumps(sorted(set(provisional_fields)), ensure_ascii=False, indent=2),
            "",
            "## Field diff (skeleton vs primary candidate top-level)",
            "",
            json.dumps(diff, ensure_ascii=False, indent=2),
            "",
        ]
    )
    (out_root / "ocr_bridge_evidence_pack_migration_notes.md").write_text(notes, encoding="utf-8")

    print(json.dumps({"bridge_alignment_output_root": str(out_root), "bridge_pack_verdict": bridge_verdict}, ensure_ascii=False))
    return 0 if bridge_verdict != "NO_GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
