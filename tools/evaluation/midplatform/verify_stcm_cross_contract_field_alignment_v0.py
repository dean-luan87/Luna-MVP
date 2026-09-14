#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-STCM-Contract-Field-Alignment-001 — Static verifier + report generator for STCM cross-contract alignment.

No model execution; no runtime wiring; no routing changes.
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


def _require_repo(p: str) -> Path:
    pp = Path(p).expanduser().resolve()
    if not pp.is_dir():
        raise SystemExit(f"ERROR: --repo-root must be directory: {p}")
    return pp


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


REQUIRED_ALIGNMENT_SECTIONS = (
    "## 1. OCRRequest → ModelCallDeadline",
    "## 2. OCRDispatchDecision → ModelCallDeadline / InformationValueAssessment",
    "## 3. OcrEvidencePack → SpatiotemporalAnchor",
    "## 4. Voice Output Governance → ModelCallOutcome / voice_notice_policy",
    "## 5. Vision 输出 → SpatiotemporalAnchor",
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=str(REPO_ROOT))
    ap.add_argument("--output-root", default="", help="Default: <repo-root>/_eval_out/stcm_cross_contract_field_alignment_v0")
    args = ap.parse_args()

    repo = _require_repo(args.repo_root)
    if args.output_root.strip():
        out_root = Path(args.output_root).expanduser().resolve()
    else:
        out_root = (repo / "_eval_out" / "stcm_cross_contract_field_alignment_v0").resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    blockers: List[str] = []
    soft: List[str] = []
    matrix: List[Dict[str, Any]] = []

    stcm_docs = [
        repo / "docs/architecture/midplatform/LUNA_SPATIOTEMPORAL_CONSISTENCY_MANAGER_V0.md",
        repo / "docs/architecture/midplatform/LUNA_MODEL_CALL_DEADLINE_AND_TIMEOUT_POLICY_V0.md",
        repo / "docs/architecture/midplatform/LUNA_INFORMATION_VALUE_AND_FALLBACK_POLICY_V0.md",
        repo / "docs/architecture/midplatform/LUNA_CROSS_MODAL_TIME_SPACE_GOVERNANCE_V0.md",
    ]
    for d in stcm_docs:
        matrix.append({"artifact": str(d.relative_to(repo)), "exists": d.is_file(), "role": "stcm_input"})
        if not d.is_file():
            blockers.append(f"missing_stcm_doc:{d.name}")

    stcm_cfg = repo / "configs/midplatform/spatiotemporal_consistency_manager_v0.example.json"
    matrix.append({"artifact": str(stcm_cfg.relative_to(repo)), "exists": stcm_cfg.is_file(), "role": "stcm_config"})
    if not stcm_cfg.is_file():
        blockers.append("missing_stcm_config")

    ocr_gov = repo / "docs/architecture/ocr/LUNA_OCR_PROVIDER_RUNTIME_GOVERNANCE_STANDARD_V0.md"
    matrix.append({"artifact": str(ocr_gov.relative_to(repo)), "exists": ocr_gov.is_file(), "role": "ocr_governance"})
    if not ocr_gov.is_file():
        blockers.append("missing_ocr_governance_standard")

    ocr_cfg = repo / "configs/ocr/ocr_provider_runtime_governance_v0.example.json"
    matrix.append({"artifact": str(ocr_cfg.relative_to(repo)), "exists": ocr_cfg.is_file(), "role": "ocr_governance_config"})
    if not ocr_cfg.is_file():
        blockers.append("missing_ocr_governance_config")

    pack_md = repo / "docs/architecture/ocr_bridge/LUNA_OCR_EVIDENCE_PACK_CONTRACT_V0.md"
    matrix.append({"artifact": str(pack_md.relative_to(repo)), "exists": pack_md.is_file(), "role": "ocr_evidence_pack_md"})
    if not pack_md.is_file():
        blockers.append("missing_ocr_evidence_pack_contract_md")

    pack_py = repo / "capabilities/ocr_bridge/ocr_evidence_pack_contract_v0.py"
    matrix.append({"artifact": str(pack_py.relative_to(repo)), "exists": pack_py.is_file(), "role": "ocr_evidence_pack_py"})
    if not pack_py.is_file():
        blockers.append("missing_ocr_evidence_pack_py")

    align_md = repo / "docs/architecture/midplatform/LUNA_STCM_CROSS_CONTRACT_FIELD_ALIGNMENT_V0.md"
    matrix.append({"artifact": str(align_md.relative_to(repo)), "exists": align_md.is_file(), "role": "alignment_doc"})
    if not align_md.is_file():
        blockers.append("missing_alignment_doc")
    else:
        atxt = align_md.read_text(encoding="utf-8")
        for sec in REQUIRED_ALIGNMENT_SECTIONS:
            if sec not in atxt:
                blockers.append(f"missing_alignment_section:{sec}")

    ex_path = repo / "configs/midplatform/stcm_cross_contract_field_alignment_v0.example.json"
    matrix.append({"artifact": str(ex_path.relative_to(repo)), "exists": ex_path.is_file(), "role": "alignment_example"})
    example: Dict[str, Any] = {}
    if not ex_path.is_file():
        blockers.append("missing_alignment_example_json")
    else:
        example = _read_json(ex_path)
        if str(example.get("schema_version") or "") != "stcm_cross_contract_field_alignment_v0":
            blockers.append("bad_alignment_example_schema_version")
        maps = example.get("mappings") if isinstance(example.get("mappings"), dict) else {}
        for mk in (
            "ocr_request_to_model_call_deadline",
            "ocr_dispatch_to_iv_assessment",
            "ocr_evidence_pack_to_spatiotemporal_anchor",
            "voice_output_to_model_call_outcome",
            "vision_output_to_spatiotemporal_anchor",
        ):
            if mk not in maps or not isinstance(maps.get(mk), list) or len(maps.get(mk) or []) == 0:
                blockers.append(f"missing_or_empty_mapping:{mk}")

    missing_refs: List[str] = []
    voice_paths: List[Tuple[str, Path]] = [
        ("voice_definition_v0", repo / "docs/architecture/LUNA_VOICE_OUTPUT_GOVERNANCE_DEFINITION_V0.md"),
        ("voice_priority_expiry_v0", repo / "docs/architecture/LUNA_VOICE_OUTPUT_PRIORITY_EXPIRY_SUPPRESSION_POLICY_V0.md"),
        ("voice_time_governance_v1", repo / "docs/architecture/voice/LUNA_VOICE_TIME_GOVERNANCE_V1.md"),
    ]
    voice_found = False
    for label, vp in voice_paths:
        matrix.append({"artifact": str(vp.relative_to(repo)), "exists": vp.is_file(), "role": f"voice_ref:{label}"})
        if vp.is_file():
            voice_found = True
        else:
            missing_refs.append(f"missing_voice_ref:{label}")
    if not voice_found:
        blockers.append("missing_voice_contract_reference:no_primary_voice_doc")

    vision_paths: List[Tuple[str, Path]] = [
        ("navigation_perception_signal_v0", repo / "docs/architecture/LUNA_NAVIGATION_PERCEPTION_SIGNAL_CONTRACT_V0.md"),
        ("yolo_to_perception_mapping_v0", repo / "docs/architecture/LUNA_YOLO_TO_PERCEPTION_SIGNAL_ADAPTER_MAPPING_V0.md"),
    ]
    vision_found = False
    for label, vp in vision_paths:
        matrix.append({"artifact": str(vp.relative_to(repo)), "exists": vp.is_file(), "role": f"vision_ref:{label}"})
        if vp.is_file():
            vision_found = True
        else:
            missing_refs.append(f"missing_vision_ref:{label}")
    if not vision_found:
        blockers.append("missing_vision_contract_reference:no_primary_vision_doc")

    readme = repo / "docs/architecture/README.md"
    if not readme.is_file():
        blockers.append("missing_architecture_readme")
    else:
        rtxt = readme.read_text(encoding="utf-8")
        if "STCM-Contract-Field-Alignment-001" not in rtxt and "stcm_cross_contract_field_alignment" not in rtxt.lower():
            blockers.append("readme_missing_stcm_alignment_index")

    gaps = example.get("known_gaps") if isinstance(example.get("known_gaps"), list) else []
    conflicts = example.get("known_conflicts") if isinstance(example.get("known_conflicts"), list) else []

    if blockers:
        verdict = "NO_GO"
    elif missing_refs:
        verdict = "CONDITIONAL_GO"
        soft = sorted(set(missing_refs))
    else:
        verdict = "GO"

    _write_json(out_root / "stcm_gap_report.json", {"gaps": gaps, "schema": "stcm_gap_report_v0"})
    _write_json(out_root / "stcm_conflict_report.json", {"conflicts": conflicts, "schema": "stcm_conflict_report_v0"})
    _write_json(
        out_root / "stcm_missing_contract_reference_report.json",
        {"missing_refs": missing_refs, "voice_primary_resolved": voice_found, "vision_primary_resolved": vision_found},
    )
    _write_json(
        out_root / "stcm_cross_contract_field_matrix.json",
        {"rows": matrix, "mappings_keys": sorted((example.get("mappings") or {}).keys()) if example else []},
    )

    summary = {
        "schema": "stcm_cross_contract_alignment_summary_v0",
        "phase": "Phase-STCM-Contract-Field-Alignment-001",
        "verdict": verdict,
        "repo_root": str(repo),
        "output_root": str(out_root),
        "blockers": sorted(set(blockers)),
        "soft_warnings": sorted(set(soft)),
        "voice_contract_reference_found": voice_found,
        "vision_contract_reference_found": vision_found,
    }
    _write_json(out_root / "stcm_cross_contract_alignment_summary.json", summary)

    notes = "\n".join(
        [
            "# STCM Cross-Contract Field Alignment v0",
            "",
            f"- **verdict**: `{verdict}`",
            f"- **alignment_doc**: `{align_md}`",
            "- See `stcm_gap_report.json` / `stcm_conflict_report.json` for design gaps and naming tensions.",
            "",
        ]
    )
    (out_root / "stcm_alignment_notes.md").write_text(notes, encoding="utf-8")

    rep = {
        "schema": "stcm_cross_contract_alignment_verifier_report_v0",
        "phase": "Phase-STCM-Contract-Field-Alignment-001",
        "verdict": verdict,
        "output_root": str(out_root),
        "blockers": sorted(set(blockers)),
        "soft_warnings": sorted(set(soft)),
    }
    _write_json(out_root / "stcm_cross_contract_alignment_verifier_report.json", rep)

    print(json.dumps({"verifier_output_root": str(out_root), "verdict": verdict, "blockers": rep["blockers"]}, ensure_ascii=False))
    return 0 if verdict != "NO_GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
