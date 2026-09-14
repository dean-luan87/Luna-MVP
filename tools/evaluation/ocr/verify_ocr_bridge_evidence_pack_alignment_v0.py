#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-OCR-Bridge-Evidence-Pack-Alignment-001 — Verifier for align_ocr_evidence_to_bridge_pack_v0 outputs.

No PaddleOCR, no OCR inference, no routing changes.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

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


def _joined_eligible(pack: Dict[str, Any]) -> str:
    evs = pack.get("eligible_text_evidence") if isinstance(pack.get("eligible_text_evidence"), list) else []
    return " ".join(str(e.get("text") or "") for e in evs if isinstance(e, dict))


def _chain_required_keys() -> Tuple[str, ...]:
    return (
        "adapter_contract_root",
        "materialize_root",
        "pinned_manifest_path",
        "raw_result_path",
        "normalized_result_path",
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--bridge-alignment-root",
        required=True,
        help="Output root of align_ocr_evidence_to_bridge_pack_v0.py",
    )
    args = ap.parse_args()

    root = _require_abs(args.bridge_alignment_root, "--bridge-alignment-root")
    blockers: List[str] = []
    soft: List[str] = []

    sum_p = root / "ocr_bridge_evidence_pack_alignment_summary.json"
    if not sum_p.is_file():
        blockers.append("missing_bridge_alignment_summary")
        summary: Dict[str, Any] = {}
    else:
        summary = _read_json(sum_p)

    align_root = Path(str(summary.get("evidence_alignment_root") or "")).expanduser()
    if not align_root.is_absolute():
        align_root = align_root.resolve()
    if not align_root.is_dir():
        blockers.append("evidence_alignment_root_missing_or_not_dir")

    al_sum_p = align_root / "ocr_evidence_alignment_summary.json"
    al_sum: Dict[str, Any] = {}
    if al_sum_p.is_file():
        al_sum = _read_json(al_sum_p)
    else:
        blockers.append("missing_upstream_ocr_evidence_alignment_summary")

    if al_sum.get("alignment_verdict") != "GO":
        blockers.append("upstream_ocr_evidence_contract_alignment_not_go")

    uni_p = align_root / "ocr_evidence_unified_result_v0.json"
    unified: Dict[str, Any] = {}
    if not uni_p.is_file():
        blockers.append("missing_unified_evidence_file")
    else:
        unified = _read_json(uni_p)

    cand_p = root / "ocr_bridge_evidence_pack_candidate_v0.json"
    if not cand_p.is_file():
        blockers.append("missing_bridge_pack_candidate")
    candidate_doc = _read_json(cand_p) if cand_p.is_file() else {}
    packs = candidate_doc.get("packs") if isinstance(candidate_doc.get("packs"), list) else []

    chain_out_p = root / "ocr_bridge_evidence_pack_source_reference_chain.json"
    if not chain_out_p.is_file():
        blockers.append("missing_bridge_source_reference_chain_file")
    chain_out: Dict[str, Any] = _read_json(chain_out_p) if chain_out_p.is_file() else {}

    mig_p = root / "ocr_bridge_evidence_pack_migration_notes.md"
    if not mig_p.is_file():
        blockers.append("missing_migration_notes")
    migration_text = mig_p.read_text(encoding="utf-8") if mig_p.is_file() else ""

    diff_p = root / "ocr_bridge_evidence_pack_field_diff.json"
    field_diff: Dict[str, Any] = _read_json(diff_p) if diff_p.is_file() else {}

    contract_ok = bool(summary.get("contract_reference_found"))
    if not contract_ok:
        soft.append("missing_contract_reference_cannot_go")

    lost = summary.get("lost_fields") if isinstance(summary.get("lost_fields"), list) else []
    if lost:
        blockers.append(f"skeleton_fields_lost_in_candidate:{lost}")

    aud_p = root / "ocr_bridge_evidence_pack_audit_report.json"
    aud: Dict[str, Any] = _read_json(aud_p) if aud_p.is_file() else {}
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
        if aud.get(k) is True:
            blockers.append(f"audit_flag_true:{k}")
    if aud.get("world_model_written") is True:
        blockers.append("world_model_written")
    if aud.get("midplatform_semantics_written") is True:
        blockers.append("midplatform_semantics_written")

    docs = unified.get("evidence_documents") if isinstance(unified.get("evidence_documents"), list) else []
    if not docs:
        blockers.append("unified_evidence_documents_empty")

    for pi, pack in enumerate(packs):
        if not isinstance(pack, dict):
            blockers.append(f"pack_not_dict:{pi}")
            continue
        flags = pack.get("evaluation_flags") if isinstance(pack.get("evaluation_flags"), dict) else {}
        if not flags:
            blockers.append(f"missing_evaluation_flags:pack_{pi}")
        else:
            if flags.get("evaluation_only") is not True:
                blockers.append(f"evaluation_only_not_true:pack_{pi}")
            if flags.get("not_runtime_input") is not True:
                blockers.append(f"not_runtime_input_not_true:pack_{pi}")
            if flags.get("not_midplatform_input") is not True:
                blockers.append(f"not_midplatform_input_not_true:pack_{pi}")
            if not str(flags.get("api_family") or "").strip():
                blockers.append(f"api_family_empty:pack_{pi}")
            if not str(flags.get("call_method") or "").strip():
                blockers.append(f"call_method_empty:pack_{pi}")

        ha = pack.get("hard_audit") if isinstance(pack.get("hard_audit"), dict) else {}
        for hk, bad in (
            ("runtime_integration", True),
            ("whitebox_integration", True),
            ("midplatform_invoked", True),
            ("mainline_routing_changed", True),
            ("world_write_invoked", True),
        ):
            if ha.get(hk) is bad:
                blockers.append(f"hard_audit:{hk}:pack_{pi}")

        udoc = docs[pi] if pi < len(docs) and isinstance(docs[pi], dict) else {}
        u_joined = str(udoc.get("text_joined") or "").strip()
        if not u_joined:
            blockers.append(f"unified_text_joined_empty:doc_{pi}")

        evs = pack.get("eligible_text_evidence") if isinstance(pack.get("eligible_text_evidence"), list) else []
        b_joined = _joined_eligible(pack).strip()
        if not evs:
            blockers.append(f"eligible_text_evidence_empty:pack_{pi}")
        if not b_joined:
            blockers.append(f"bridge_text_joined_empty:pack_{pi}")

        pchain = pack.get("paddleocr_source_reference_chain") if isinstance(pack.get("paddleocr_source_reference_chain"), dict) else {}
        for ck in _chain_required_keys():
            if not pchain.get(ck):
                blockers.append(f"pack_chain_missing:{ck}:pack_{pi}")

        u_items = udoc.get("evidence_items") if isinstance(udoc.get("evidence_items"), list) else []
        count_mismatch = len(u_items) != len(evs)
        if count_mismatch:
            blockers.append(f"item_count_mismatch:unified={len(u_items)}_bridge={len(evs)}:pack_{pi}")

        u_conf = udoc.get("confidence_summary") if isinstance(udoc.get("confidence_summary"), dict) else {}
        unc = pack.get("uncertainty") if isinstance(pack.get("uncertainty"), dict) else {}
        pack_conf = unc.get("paddleocr_confidence_summary") if isinstance(unc.get("paddleocr_confidence_summary"), dict) else {}
        if u_conf and not pack_conf:
            blockers.append(f"confidence_summary_not_mapped:pack_{pi}")

        if not count_mismatch:
            for ii, (uit, bit) in enumerate(zip(u_items, evs)):
                if not isinstance(uit, dict) or not isinstance(bit, dict):
                    blockers.append(f"item_not_dict:{pi}:{ii}")
                    continue
                if str(uit.get("text") or "") != str(bit.get("text") or ""):
                    blockers.append(f"text_mismatch:{pi}:{ii}")
                if "score" in uit and isinstance(uit.get("score"), (int, float)):
                    if "score" not in bit and not isinstance(bit.get("confidence"), (int, float)):
                        blockers.append(f"score_lost:{pi}:{ii}")
                    if "score" in bit and abs(float(bit["score"]) - float(uit["score"])) > 1e-9:
                        blockers.append(f"score_value_mismatch:{pi}:{ii}")
                if uit.get("polygon") is not None and bit.get("polygon") is None:
                    blockers.append(f"polygon_lost:{pi}:{ii}")
                if uit.get("reading_order_index") is not None and bit.get("reading_order_index") is None:
                    blockers.append(f"reading_order_index_lost:{pi}:{ii}")
                if str(uit.get("provider") or "") != str(bit.get("provider") or ""):
                    blockers.append(f"provider_mismatch:{pi}:{ii}")

    if field_diff.get("missing_in_candidate") and not migration_text.strip():
        blockers.append("field_diff_present_but_no_migration_notes")

    if blockers:
        verdict = "NO_GO"
    elif soft or not contract_ok:
        verdict = "CONDITIONAL_GO"
    else:
        verdict = "GO"

    rep = {
        "schema": "ocr_bridge_evidence_pack_verifier_report_v0",
        "phase": "Phase-OCR-Bridge-Evidence-Pack-Alignment-001",
        "bridge_alignment_root": str(root),
        "evidence_alignment_root": str(align_root) if align_root.is_dir() else str(summary.get("evidence_alignment_root") or ""),
        "verdict": verdict,
        "blockers": sorted(set(blockers)),
        "soft_warnings": sorted(set(soft)),
        "contract_reference_found": contract_ok,
        "upstream_alignment_verdict": al_sum.get("alignment_verdict"),
        "chain_out_keys_present": all(chain_out.get(k) for k in ("evidence_alignment_root", "bridge_alignment_output_root")),
    }
    (root / "ocr_bridge_evidence_pack_verifier_report.json").write_text(
        json.dumps(rep, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"bridge_alignment_root": str(root), "verdict": verdict, "blockers": rep["blockers"]}, ensure_ascii=False))
    return 0 if verdict != "NO_GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
