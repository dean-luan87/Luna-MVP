#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-OCRBridge-Review-001 — Read-only interface freeze review from Design-001 artifacts + repo docs.

No MidPlatform, no runtime, no OCR provider calls.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.ocr_bridge.ocr_evidence_pack_contract_v0 import OCR_EVIDENCE_PACK_VERSION  # noqa: E402

OCR_BRIDGE_DOC_DIR = Path(REPO_ROOT) / "docs" / "architecture" / "ocr_bridge"

REVIEW_DOCS = [
    "LUNA_OCR_MIDPLATFORM_INTERFACE_FREEZE_V0.md",
    "LUNA_OCR_EVIDENCE_PACK_MINIMUM_REQUIRED_FIELDS_V0.md",
    "LUNA_OCR_FACT_TEXT_LAYER_ENTRY_POLICY_V0.md",
    "LUNA_OCR_RUNTIME_SOURCE_REF_REQUIREMENTS_V0.md",
    "LUNA_OCR_BRIDGE_REVIEW_GO_NO_GO_PACK_V0.md",
    "LUNA_OCR_EVIDENCE_GOVERNANCE_AUTHORITY_FREEZE_V0.md",
]

DESIGN_DOCS = [
    "LUNA_OCR_EVIDENCE_PACK_CONTRACT_V0.md",
    "LUNA_OCR_EVIDENCE_TYPES_V0.md",
    "LUNA_OCR_MIDPLATFORM_FORWARDING_CONTRACT_V0.md",
    "LUNA_OCR_DISTORTION_PREVENTION_TO_CONTRACT_MAPPING_V0.md",
    "LUNA_OCR_BRIDGE_DESIGN_TEST_MATRIX_V0.md",
    "LUNA_OCR_BRIDGE_DESIGN_GO_NO_GO_PACK_V0.md",
]

PACK_MIN_KEYS = [
    "pack_id",
    "pack_version",
    "source_image_ref",
    "source_provider_ref",
    "source_quality_gate_ref",
    "source_layout_ref",
    "source_eligibility_gate_ref",
    "eligible_text_evidence",
    "conditional_text_evidence",
    "symbol_evidence",
    "glyph_evidence",
    "layout_evidence",
    "rejected_or_uncertain_evidence",
    "fact_text_layer_candidates",
    "must_not_enter_fact_text_layer",
    "reading_order",
    "uncertainty",
    "midplatform_contract",
    "hard_audit",
]

EVIDENCE_ITEM_MIN = ["evidence_id", "evidence_type", "should_enter_fact_text_layer", "source_refs"]

CONTRACT_PY = Path(REPO_ROOT) / "capabilities" / "ocr_bridge" / "ocr_evidence_pack_contract_v0.py"
TYPES_PY = Path(REPO_ROOT) / "capabilities" / "ocr_bridge" / "ocr_evidence_types_v0.py"
FORWARD_PY = Path(REPO_ROOT) / "capabilities" / "ocr_bridge" / "ocr_midplatform_forwarding_contract_v0.py"
VALIDATOR_PY = Path(REPO_ROOT) / "capabilities" / "ocr_bridge" / "ocr_evidence_pack_validator_v0.py"


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _freeze_doc_assertions(freeze_md: Path) -> Tuple[bool, List[str]]:
    notes: List[str] = []
    if not freeze_md.is_file():
        return False, ["missing_freeze_doc"]
    t = freeze_md.read_text(encoding="utf-8")
    ok = True
    if "raw_text_joined" not in t:
        ok = False
        notes.append("freeze_doc_missing_raw_text_joined_keyword")
    if "MidPlatform" not in t and "中台" not in t:
        ok = False
        notes.append("freeze_doc_missing_midplatform_context")
    if not any(x in t for x in ("禁止", "不得", "不接")):
        ok = False
        notes.append("freeze_doc_missing_prohibition_language")
    return ok, notes


def _pack_top_eval_marked(pack: Dict[str, Any]) -> bool:
    for k in (
        "source_image_ref",
        "source_provider_ref",
        "source_quality_gate_ref",
        "source_layout_ref",
        "source_eligibility_gate_ref",
    ):
        v = pack.get(k)
        if not isinstance(v, str) or "eval:" not in v:
            return False
    return True


def _iter_all_strings(obj: Any, path: str = "") -> List[Tuple[str, str]]:
    out: List[Tuple[str, str]] = []
    if isinstance(obj, str):
        return [(path, obj)]
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.extend(_iter_all_strings(v, f"{path}.{k}" if path else k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.extend(_iter_all_strings(v, f"{path}[{i}]"))
    return out


def _no_forged_runtime_refs(pack: Dict[str, Any]) -> Tuple[bool, List[str]]:
    bad: List[str] = []
    for pth, s in _iter_all_strings(pack):
        if "https://" in s:
            bad.append(f"https_in:{pth}")
        if s.startswith("runtime:") or s.startswith("prod:"):
            bad.append(f"forged_prefix:{pth}")
    return len(bad) == 0, bad


def _build_required_fields_matrix(pack: Dict[str, Any]) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    for k in PACK_MIN_KEYS:
        rows.append({"field": k, "required": True, "present": k in pack and pack.get(k) is not None})
    ev_checks: Dict[str, Any] = {}
    for bucket in (
        "eligible_text_evidence",
        "conditional_text_evidence",
        "symbol_evidence",
        "glyph_evidence",
        "layout_evidence",
        "rejected_or_uncertain_evidence",
    ):
        items = pack.get(bucket) or []
        missing = 0
        for it in items:
            if not isinstance(it, dict):
                missing += 1
                continue
            for f in EVIDENCE_ITEM_MIN:
                if f not in it or (f == "source_refs" and not isinstance(it.get(f), dict)):
                    missing += 1
                    break
        ev_checks[bucket] = {"count": len(items), "items_missing_min_fields": missing}
    return {"pack_level": rows, "evidence_buckets": ev_checks, "pack_version_expected": OCR_EVIDENCE_PACK_VERSION}


def _forwarding_mode_matrix() -> Dict[str, Any]:
    return {
        "forwarding_modes": {
            "blocked": {
                "criteria": [
                    "missing critical source refs",
                    "quality gate NO_GO on fact path",
                    "eligibility gate NO_GO on fact path",
                    "distortion violation",
                    "non-OCR attempting fact text layer",
                    "reading_order uncertain with non-empty fact_text_layer_candidates",
                    "symbol/glyph raw or fact flags true",
                ]
            },
            "evidence_only": {
                "criteria": [
                    "only symbol/glyph/layout/rejected evidence substantive paths",
                    "no fact text layer write",
                    "higher-layer review only",
                ]
            },
            "conditional_evidence": {
                "criteria": [
                    "OCR text present with uncertainty",
                    "preprocess/layout/provider_fallback/manual_review hints",
                    "no fact text layer write",
                ]
            },
            "eligible_text_only": {
                "criteria": [
                    "eligible domain",
                    "quality gate pass (GO per policy doc; CONDITIONAL_GO only if explicitly allowed in implementation RFC)",
                    "eligibility gate pass",
                    "reading order reliable (reading_order_uncertain=false, global available)",
                    "no distortion violation",
                    "non-empty fact_text_layer_candidates allowed only under above",
                ],
            },
        },
        "notes": "Normative freeze for MidPlatform-facing forwarding_mode vocabulary.",
    }


def _fact_text_policy_matrix() -> Dict[str, Any]:
    return {
        "allowed_in_fact_text_layer_candidates": [
            "eligible_text_evidence items meeting all strong conditions in LUNA_OCR_FACT_TEXT_LAYER_ENTRY_POLICY_V0.md",
        ],
        "never_fact_text_layer": [
            "non-OCR domain evidence as text fact",
            "symbol_evidence",
            "glyph_evidence",
            "layout_evidence (as global single fact string)",
            "conditional_text_evidence",
            "rejected_or_uncertain_evidence",
        ],
        "reading_order_rule": "If reading_order_uncertain=true, fact_text_layer_candidates MUST be empty (design-default + implementation MUST).",
    }


def _future_runtime_refs_matrix() -> Dict[str, Any]:
    names = [
        "image_frame_ref",
        "crop_or_roi_ref",
        "ocr_provider_invocation_ref",
        "raw_candidate_ref",
        "layout_governance_ref",
        "image_quality_gate_ref",
        "eligibility_gate_ref",
        "reading_order_ref",
        "trace_ref",
        "replay_ref",
        "audit_ref",
    ]
    return {
        "refs": [{"ref_name": n, "design_phase": "placeholder_eval_or_doc_only", "implementation_phase": "must_bind_real_ref"} for n in names],
        "rules": [
            "Do not forge production trace/replay URLs in design tools.",
            "eval:* strings are acceptable only for Evaluation Tools derived artifacts.",
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--design-root", required=True, help="OCRBridge-Design-001 output root (contains ocr_evidence_pack_example.json).")
    ap.add_argument("--luna-core-root", default=REPO_ROOT, help="Luna-Core repo root for doc/code checks.")
    ap.add_argument("--output-root", default="", help="Absolute review output directory.")
    args = ap.parse_args()

    design_root = _require_abs(args.design_root, "--design-root")
    luna_core = _require_abs(args.luna_core_root, "--luna-core-root")

    if args.output_root.strip():
        out_root = _require_abs(args.output_root, "--output-root")
    else:
        stamp = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        out_root = (Path.home() / "LunaRuntime" / "logs" / f"ocr_bridge_review_001_{stamp}").resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    issues: List[str] = []
    doc_dir = luna_core / "docs" / "architecture" / "ocr_bridge"

    review_present = {fn: (doc_dir / fn).is_file() for fn in REVIEW_DOCS}
    design_present = {fn: (doc_dir / fn).is_file() for fn in DESIGN_DOCS}
    code_present = {
        "ocr_evidence_pack_contract_v0.py": CONTRACT_PY.is_file(),
        "ocr_evidence_types_v0.py": TYPES_PY.is_file(),
        "ocr_midplatform_forwarding_contract_v0.py": FORWARD_PY.is_file(),
        "ocr_evidence_pack_validator_v0.py": VALIDATOR_PY.is_file(),
    }
    if not all(review_present.values()):
        issues.append("missing_review_docs")
    if not all(design_present.values()):
        issues.append("missing_design_docs")
    if not all(code_present.values()):
        issues.append("missing_contract_code")

    pack_path = design_root / "ocr_evidence_pack_example.json"
    if not pack_path.is_file():
        raise SystemExit(f"ERROR: missing {pack_path}")
    pack = json.loads(pack_path.read_text(encoding="utf-8"))

    freeze_md = doc_dir / "LUNA_OCR_MIDPLATFORM_INTERFACE_FREEZE_V0.md"
    freeze_ok, freeze_notes = _freeze_doc_assertions(freeze_md)

    pack_version_ok = pack.get("pack_version") == OCR_EVIDENCE_PACK_VERSION
    if not pack_version_ok:
        issues.append("pack_version_mismatch")

    matrix_fields = _build_required_fields_matrix(pack)
    pack_fields_ok = all(r["present"] for r in matrix_fields["pack_level"])
    if not pack_fields_ok:
        issues.append("pack_missing_required_fields")
    ev_ok = all(v.get("items_missing_min_fields", 1) == 0 for v in matrix_fields["evidence_buckets"].values())
    if not ev_ok:
        issues.append("evidence_missing_min_fields")

    eval_marked = _pack_top_eval_marked(pack)
    if not eval_marked:
        issues.append("top_level_source_refs_not_eval_marked")

    no_forge, forge_detail = _no_forged_runtime_refs(pack)
    if not no_forge:
        issues.extend(forge_detail)

    ha = pack.get("hard_audit") or {}
    audit_ok = (
        ha.get("midplatform_invoked") is False
        and ha.get("runtime_integration") is False
        and ha.get("whitebox_integration") is False
        and ha.get("mainline_routing_changed", False) is False
    )
    if not audit_ok:
        issues.append("hard_audit_not_clean")

    verdict = "GO" if not issues and freeze_ok else "NO_GO"

    summary = {
        "phase": "Phase-OCRBridge-Review-001",
        "verdict": verdict,
        "design_input_root": str(design_root),
        "review_output_root": str(out_root),
        "luna_core_root": str(luna_core),
        "docs": {"review": review_present, "design": design_present, "code": code_present},
        "midplatform_raw_text_joined_direct_input_forbidden_doc": freeze_ok,
        "freeze_doc_notes": freeze_notes,
        "pack_version_ok": pack_version_ok,
        "pack_minimum_fields_ok": pack_fields_ok and ev_ok,
        "eval_placeholder_top_refs_ok": eval_marked,
        "runtime_refs_not_forged_ok": no_forge,
        "hard_audit_clean": audit_ok,
        "issues": issues,
        "scope": "interface_review_freeze_only",
    }

    _write_json(out_root / "ocr_bridge_interface_freeze_summary.json", summary)
    _write_json(out_root / "ocr_bridge_required_fields_matrix.json", matrix_fields)
    _write_json(out_root / "ocr_bridge_forwarding_mode_matrix.json", _forwarding_mode_matrix())
    _write_json(out_root / "ocr_bridge_fact_text_entry_policy_matrix.json", _fact_text_policy_matrix())
    _write_json(out_root / "ocr_bridge_future_runtime_source_refs_matrix.json", _future_runtime_refs_matrix())

    notes = out_root / "ocr_bridge_review_notes.md"
    notes.write_text(
        "\n".join(
            [
                "# OCR Bridge — Interface Review & Freeze (v0)",
                "",
                f"- **design_input_root**: `{design_root}`",
                f"- **review_output_root**: `{out_root}`",
                f"- **verdict**: `{verdict}`",
                "",
                "## Frozen statements",
                "",
                "- MidPlatform **must** consume `OcrEvidencePackV0`, not raw `raw_text_joined` as sole OCR input.",
                "- Review phase **does not** wire runtime, MidPlatform, or whitebox.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(json.dumps({"output_root": str(out_root), "verdict": verdict}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
