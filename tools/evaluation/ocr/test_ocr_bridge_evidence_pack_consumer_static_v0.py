#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-OCR-Bridge-Evidence-Pack-Consumer-Static-Test-001 — Static consumer walk on bridge pack candidate.

No PaddleOCR, no OCR inference, no routing, no runtime / MidPlatform.
"""

from __future__ import annotations

import argparse
import json
import sys
import traceback
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.ocr_bridge.ocr_evidence_pack_contract_v0 import (  # noqa: E402
    build_ocr_evidence_pack_skeleton_v0,
)
from capabilities.ocr_bridge.ocr_evidence_pack_validator_v0 import (  # noqa: E402
    validate_ocr_evidence_pack_v0,
)


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _access_field(obj: Any, key: str) -> Tuple[bool, str, Any]:
    """Return (ok, kind, value_preview)."""
    if not isinstance(obj, dict):
        return False, "not_dict", None
    if key not in obj:
        return False, "missing", None
    v = obj[key]
    return True, type(v).__name__, v


def _walk_eligible_items(pack: Dict[str, Any], pack_index: int) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Field matrix rows + item walk rows."""
    matrix: List[Dict[str, Any]] = []
    walks: List[Dict[str, Any]] = []
    evs = pack.get("eligible_text_evidence") if isinstance(pack.get("eligible_text_evidence"), list) else []
    for ii, it in enumerate(evs):
        if not isinstance(it, dict):
            walks.append({"pack_index": pack_index, "item_index": ii, "error": "not_dict"})
            continue
        eid = str(it.get("evidence_id") or f"idx_{ii}")
        row_checks: Dict[str, Any] = {"evidence_id": eid, "pack_index": pack_index, "item_index": ii}

        def add_field(fname: str) -> None:
            ok, kind, val = _access_field(it, fname)
            matrix.append(
                {
                    "pack_index": pack_index,
                    "item_index": ii,
                    "field": fname,
                    "accessible": ok,
                    "value_kind": kind,
                    "present": fname in it,
                }
            )
            row_checks[f"{fname}_accessible"] = ok

        for fname in ("text", "confidence", "bbox", "polygon", "score", "reading_order_index"):
            add_field(fname)

        refs = it.get("source_refs") if isinstance(it.get("source_refs"), dict) else {}
        for rk in ("source_image_ref", "provider_ref", "quality_gate_ref", "routing_ref"):
            ok = rk in refs and str(refs.get(rk) or "").strip() != ""
            matrix.append(
                {
                    "pack_index": pack_index,
                    "item_index": ii,
                    "field": f"source_refs.{rk}",
                    "accessible": ok,
                    "value_kind": "str" if ok else "missing",
                    "present": rk in refs,
                }
            )
            row_checks[f"source_refs.{rk}_accessible"] = ok

        walks.append(row_checks)

    return matrix, walks


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bridge-alignment-root", required=True, help="Output root of align_ocr_evidence_to_bridge_pack_v0.py")
    ap.add_argument("--output-root", default="", help="Default: <bridge-alignment-root>/ocr_bridge_pack_consumer_static_v0")
    args = ap.parse_args()

    bridge_root = _require_abs(args.bridge_alignment_root, "--bridge-alignment-root")
    if args.output_root.strip():
        out_root = _require_abs(args.output_root, "--output-root")
    else:
        out_root = (bridge_root / "ocr_bridge_pack_consumer_static_v0").resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    errors: List[str] = []
    soft: List[str] = []

    sum_align = bridge_root / "ocr_bridge_evidence_pack_alignment_summary.json"
    if not sum_align.is_file():
        errors.append("missing_bridge_alignment_summary")
        al_summary: Dict[str, Any] = {}
    else:
        al_summary = _read_json(sum_align)

    if al_summary.get("bridge_pack_verdict") != "GO":
        errors.append(f"bridge_pack_verdict_not_go:{al_summary.get('bridge_pack_verdict')}")

    ver_align = bridge_root / "ocr_bridge_evidence_pack_verifier_report.json"
    align_verifier: Dict[str, Any] = {}
    if not ver_align.is_file():
        errors.append("missing_bridge_alignment_verifier_report")
    else:
        align_verifier = _read_json(ver_align)
        if align_verifier.get("verdict") != "GO":
            errors.append(f"bridge_alignment_verifier_not_go:{align_verifier.get('verdict')}")

    cand_p = bridge_root / "ocr_bridge_evidence_pack_candidate_v0.json"
    mapping_p = bridge_root / "ocr_bridge_evidence_pack_mapping_matrix.json"
    chain_p = bridge_root / "ocr_bridge_evidence_pack_source_reference_chain.json"
    audit_in_p = bridge_root / "ocr_bridge_evidence_pack_audit_report.json"

    for p, label in (
        (cand_p, "candidate"),
        (mapping_p, "mapping_matrix"),
        (chain_p, "source_reference_chain"),
        (audit_in_p, "bridge_audit"),
    ):
        if not p.is_file():
            errors.append(f"missing_input:{label}:{p}")

    candidate_doc: Dict[str, Any] = {}
    if cand_p.is_file():
        candidate_doc = _read_json(cand_p)

    packs = candidate_doc.get("packs") if isinstance(candidate_doc.get("packs"), list) else []
    if not packs:
        errors.append("candidate_packs_empty")

    mapping_doc = _read_json(mapping_p) if mapping_p.is_file() else {}
    chain_doc = _read_json(chain_p) if chain_p.is_file() else {}
    bridge_audit_in = _read_json(audit_in_p) if audit_in_p.is_file() else {}
    if isinstance(bridge_audit_in, dict):
        for k in (
            "network_request_invoked",
            "ocr_routing_changed",
            "rapidocr_replaced",
            "runtime_integration",
            "whitebox_integration",
            "midplatform_invoked",
            "paddleocr_invoked",
            "ocr_inference_invoked",
        ):
            if bridge_audit_in.get(k) is True:
                errors.append(f"bridge_audit_flag_true:{k}")
        if bridge_audit_in.get("world_model_written") is True:
            errors.append("bridge_audit_world_model_written")
        if bridge_audit_in.get("midplatform_semantics_written") is True:
            errors.append("bridge_audit_midplatform_semantics_written")

    field_matrix: List[Dict[str, Any]] = []
    item_walks: List[Dict[str, Any]] = []
    validation_reports: List[Dict[str, Any]] = []
    loader_exceptions: List[str] = []

    non_ocr: set = set()

    for pi, pack in enumerate(packs):
        if not isinstance(pack, dict):
            errors.append(f"pack_not_dict:{pi}")
            continue
        try:
            val = validate_ocr_evidence_pack_v0(pack=pack, non_ocr_types=non_ocr)
            validation_reports.append({"pack_index": pi, **val})
            if not val.get("validation_passed"):
                errors.append(f"validator_failed_pack_{pi}")
        except Exception:
            loader_exceptions.append(traceback.format_exc())
            errors.append(f"validator_exception_pack_{pi}")
            validation_reports.append({"pack_index": pi, "validation_passed": False, "error": "exception"})

        mrows, wrows = _walk_eligible_items(pack, pi)
        field_matrix.extend(mrows)
        item_walks.extend(wrows)

        evs = pack.get("eligible_text_evidence") if isinstance(pack.get("eligible_text_evidence"), list) else []
        if not evs:
            errors.append(f"eligible_text_evidence_empty:{pi}")
        for ii, it in enumerate(evs):
            if not isinstance(it, dict):
                errors.append(f"eligible_item_not_dict:{pi}:{ii}")
                continue
            if not str(it.get("text") or "").strip():
                errors.append(f"empty_text:{pi}:{ii}")
            if "confidence" not in it:
                errors.append(f"missing_confidence_key:{pi}:{ii}")
            bbox = it.get("bbox")
            if bbox is not None and not isinstance(bbox, list):
                errors.append(f"bbox_bad_type:{pi}:{ii}")

        ef = pack.get("evaluation_flags") if isinstance(pack.get("evaluation_flags"), dict) else {}
        if not ef:
            errors.append(f"missing_evaluation_flags:pack_{pi}")
        else:
            if ef.get("evaluation_only") is not True:
                errors.append(f"evaluation_only_not_true:pack_{pi}")

    # Provisional / extended keys (consumer must tolerate via dict access).
    provisional_report: Dict[str, Any] = {
        "schema": "ocr_bridge_pack_consumer_static_provisional_field_report_v0",
        "phase": "Phase-OCR-Bridge-Evidence-Pack-Consumer-Static-Test-001",
        "known_pack_level_extensions": [
            "evaluation_flags",
            "paddleocr_source_reference_chain",
        ],
        "known_item_level_extensions": ["polygon", "score", "reading_order_index"],
        "access_policy": "dict_get_optional_extensions_no_schema_enforcement",
        "per_pack": [],
    }
    for pi, pack in enumerate(packs):
        if not isinstance(pack, dict):
            continue
        entry: Dict[str, Any] = {"pack_index": pi, "pack_level": {}, "eligible_items": []}
        for k in ("evaluation_flags", "paddleocr_source_reference_chain"):
            entry["pack_level"][k] = {
                "present": k in pack,
                "readable_via_get": True,
                "type": type(pack.get(k)).__name__ if k in pack else None,
            }
        evs = pack.get("eligible_text_evidence") if isinstance(pack.get("eligible_text_evidence"), list) else []
        for ii, it in enumerate(evs):
            if not isinstance(it, dict):
                continue
            ext = {}
            for k in ("polygon", "score", "reading_order_index"):
                ext[k] = {"present": k in it, "value_kind": type(it.get(k)).__name__ if k in it else None}
            entry["eligible_items"].append({"item_index": ii, "extensions": ext})
        provisional_report["per_pack"].append(entry)

    # Uncertainty / confidence_summary
    unc_results: List[Dict[str, Any]] = []
    for pi, pack in enumerate(packs):
        if not isinstance(pack, dict):
            continue
        u = pack.get("uncertainty") if isinstance(pack.get("uncertainty"), dict) else {}
        pcs = u.get("paddleocr_confidence_summary") if isinstance(u.get("paddleocr_confidence_summary"), dict) else None
        unc_results.append(
            {
                "pack_index": pi,
                "uncertainty_accessible": isinstance(pack.get("uncertainty"), dict),
                "paddleocr_confidence_summary_accessible": pcs is not None,
                "paddleocr_confidence_summary_keys": sorted(pcs.keys()) if pcs else [],
            }
        )
        evn = len(pack.get("eligible_text_evidence") or []) if isinstance(pack.get("eligible_text_evidence"), list) else 0
        if evn > 0 and not pcs:
            errors.append(f"paddleocr_confidence_summary_missing_or_not_dict:pack_{pi}")

    # Source chain on pack
    chain_access: List[Dict[str, Any]] = []
    for pi, pack in enumerate(packs):
        if not isinstance(pack, dict):
            continue
        ch = pack.get("paddleocr_source_reference_chain") if isinstance(pack.get("paddleocr_source_reference_chain"), dict) else {}
        req = ("adapter_contract_root", "materialize_root", "pinned_manifest_path", "raw_result_path", "normalized_result_path")
        chain_access.append(
            {
                "pack_index": pi,
                "chain_present": bool(ch),
                "keys_present": {k: bool(ch.get(k)) for k in req},
            }
        )
        for k in req:
            if not ch.get(k):
                errors.append(f"source_chain_missing_key:{k}:pack_{pi}")

    # Consumer-side audit (static test did not invoke runtime).
    consumer_audit = {
        "schema": "ocr_bridge_pack_consumer_static_audit_report_v0",
        "phase": "Phase-OCR-Bridge-Evidence-Pack-Consumer-Static-Test-001",
        "network_request_invoked": False,
        "paddleocr_invoked": False,
        "ocr_inference_invoked": False,
        "ocr_routing_changed": False,
        "rapidocr_replaced": False,
        "runtime_integration": False,
        "whitebox_integration": False,
        "midplatform_invoked": False,
        "world_model_written": False,
        "midplatform_semantics_written": False,
        "mainline_touched": False,
        "bridge_alignment_audit_echo": (
            {k: bridge_audit_in.get(k) for k in (
                "network_request_invoked",
                "ocr_routing_changed",
                "rapidocr_replaced",
                "runtime_integration",
                "whitebox_integration",
                "midplatform_invoked",
                "paddleocr_invoked",
                "ocr_inference_invoked",
                "world_model_written",
                "midplatform_semantics_written",
            )}
            if isinstance(bridge_audit_in, dict)
            else {}
        ),
    }

    for pi, pack in enumerate(packs):
        if not isinstance(pack, dict):
            continue
        ha = pack.get("hard_audit") if isinstance(pack.get("hard_audit"), dict) else {}
        for k, bad in (
            ("runtime_integration", True),
            ("whitebox_integration", True),
            ("midplatform_invoked", True),
            ("mainline_routing_changed", True),
            ("world_write_invoked", True),
        ):
            if ha.get(k) is bad:
                errors.append(f"hard_audit_bad:{k}:pack_{pi}")

    sk = build_ocr_evidence_pack_skeleton_v0(
        pack_id="consumer_probe",
        source_refs={
            "source_image_ref": "x",
            "source_provider_ref": "x",
            "source_quality_gate_ref": "x",
            "source_layout_ref": "x",
            "source_eligibility_gate_ref": "x",
        },
    )
    skeleton_keys = set(sk.keys())
    for pi, pack in enumerate(packs):
        if isinstance(pack, dict):
            extra = sorted(set(pack.keys()) - skeleton_keys)
            if extra:
                soft.append(f"pack_{pi}_extra_top_level_keys:{extra}")

    for row in field_matrix:
        if row.get("field") == "text" and row.get("accessible") is not True:
            errors.append(f"text_not_accessible:pack_{row.get('pack_index')}:item_{row.get('item_index')}")
        if row.get("field") == "confidence" and row.get("accessible") is not True:
            errors.append(f"confidence_not_accessible:pack_{row.get('pack_index')}:item_{row.get('item_index')}")

    for row in field_matrix:
        if row.get("field") in ("polygon", "score", "reading_order_index") and row.get("present") and not row.get("accessible"):
            errors.append(
                f"provisional_field_inaccessible:{row.get('field')}:pack_{row.get('pack_index')}:item_{row.get('item_index')}"
            )

    verdict = "NO_GO" if errors else "GO"

    summary = {
        "schema": "ocr_bridge_pack_consumer_static_summary_v0",
        "phase": "Phase-OCR-Bridge-Evidence-Pack-Consumer-Static-Test-001",
        "consumer_static_verdict": verdict,
        "bridge_alignment_output_root": str(bridge_root),
        "consumer_static_output_root": str(out_root),
        "input_candidate_path": str(cand_p),
        "contract_loader_module": "capabilities.ocr_bridge.ocr_evidence_pack_validator_v0",
        "contract_loader_function": "validate_ocr_evidence_pack_v0",
        "skeleton_reference": "capabilities.ocr_bridge.ocr_evidence_pack_contract_v0.build_ocr_evidence_pack_skeleton_v0",
        "pack_count": len(packs),
        "eligible_text_evidence_total_count": sum(
            len(p.get("eligible_text_evidence") or []) for p in packs if isinstance(p, dict)
        ),
        "bridge_alignment_summary_verdict": al_summary.get("bridge_pack_verdict"),
        "bridge_alignment_verifier_verdict": align_verifier.get("verdict"),
        "validation_reports": validation_reports,
        "loader_exceptions": loader_exceptions,
        "uncertainty_access_results": unc_results,
        "source_chain_access": chain_access,
        "errors": errors,
        "soft_warnings": soft,
    }

    _write_json(out_root / "ocr_bridge_pack_consumer_static_summary.json", summary)
    _write_json(out_root / "ocr_bridge_pack_consumer_static_field_access_matrix.json", {"rows": field_matrix})
    _write_json(out_root / "ocr_bridge_pack_consumer_static_item_walk_report.json", {"items": item_walks})
    _write_json(out_root / "ocr_bridge_pack_consumer_static_provisional_field_report.json", provisional_report)
    _write_json(
        out_root / "ocr_bridge_pack_consumer_static_source_chain_report.json",
        {
            "schema": "ocr_bridge_pack_consumer_static_source_chain_report_v0",
            "file_chain_document_keys": sorted(chain_doc.keys()) if isinstance(chain_doc, dict) else [],
            "mapping_row_count": len(mapping_doc.get("rows") or []) if isinstance(mapping_doc.get("rows"), list) else 0,
            "per_pack_chain_access": chain_access,
        },
    )
    _write_json(out_root / "ocr_bridge_pack_consumer_static_audit_report.json", consumer_audit)

    notes = "\n".join(
        [
            "# OCR Bridge Pack — Consumer Static Test v0",
            "",
            f"- **consumer_static_verdict**: `{verdict}`",
            f"- **bridge_alignment_output_root**: `{bridge_root}`",
            f"- **Loader**: `validate_ocr_evidence_pack_v0` (design-time static validator).",
            "",
            "## Limits",
            "",
            "- No PaddleOCR / OCR inference; no runtime / MidPlatform / routing changes.",
            "",
        ]
    )
    (out_root / "ocr_bridge_pack_consumer_static_notes.md").write_text(notes, encoding="utf-8")

    print(json.dumps({"consumer_static_output_root": str(out_root), "consumer_static_verdict": verdict}, ensure_ascii=False))
    return 0 if verdict != "NO_GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
