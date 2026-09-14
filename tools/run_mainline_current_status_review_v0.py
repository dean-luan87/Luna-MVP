#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-StatusReview-001 — Read-only mainline status matrix (YOLO / OCR / Voice / OCRBridge / Evaluation).

Does NOT invoke providers, does NOT modify runtime, does NOT call MidPlatform.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Tuple

StatusT = str  # GO | CONDITIONAL_GO | NO_GO | closed_v0
ScopeT = str  # runtime | shadow | design_only | evaluation_only | rfc_only


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _row(
    *,
    module: str,
    phase: str,
    status: StatusT,
    scope: ScopeT,
    runtime_connected: bool,
    midplatform_connected: bool,
    whitebox_connected: bool,
    provider_invoked: bool,
    world_write_invoked: bool,
    mainline_side_effect: bool,
    next_allowed_action: str,
    blocked_action: str,
    notes: str = "",
) -> Dict[str, Any]:
    return {
        "module": module,
        "phase": phase,
        "status": status,
        "scope": scope,
        "runtime_connected": runtime_connected,
        "midplatform_connected": midplatform_connected,
        "whitebox_connected": whitebox_connected,
        "provider_invoked": provider_invoked,
        "world_write_invoked": world_write_invoked,
        "mainline_side_effect": mainline_side_effect,
        "next_allowed_action": next_allowed_action,
        "blocked_action": blocked_action,
        "notes": notes,
    }


def _phase_status_matrix() -> List[Dict[str, Any]]:
    na_design = "Continue design/RFC; offline eval; shadow wiring per authorize phase"
    blk = "Uncontrolled MidPlatform; unguarded fact layer; hive/world write; navigation without governance"
    return [
        _row(
            module="YOLO",
            phase="Stage-1 005-Fix (10-frame)",
            status="closed_v0",
            scope="evaluation_only",
            runtime_connected=False,
            midplatform_connected=False,
            whitebox_connected=False,
            provider_invoked=False,
            world_write_invoked=False,
            mainline_side_effect=False,
            next_allowed_action="OCR Stage-2 / downstream design references",
            blocked_action=blk,
            notes="Offline trial closed.",
        ),
        _row(
            module="YOLO",
            phase="Stage-1 006 (50/100/200 multi-window)",
            status="GO",
            scope="evaluation_only",
            runtime_connected=False,
            midplatform_connected=False,
            whitebox_connected=False,
            provider_invoked=False,
            world_write_invoked=False,
            mainline_side_effect=False,
            next_allowed_action=na_design,
            blocked_action=blk,
        ),
        _row(
            module="YOLO",
            phase="Stage-1 007 (offline trial regression closed_v0)",
            status="closed_v0",
            scope="evaluation_only",
            runtime_connected=False,
            midplatform_connected=False,
            whitebox_connected=False,
            provider_invoked=False,
            world_write_invoked=False,
            mainline_side_effect=False,
            next_allowed_action="Close book on Stage-1 offline; reference for Stage-2",
            blocked_action=blk,
        ),
        _row(
            module="OCR",
            phase="008 precheck",
            status="GO",
            scope="shadow",
            runtime_connected=False,
            midplatform_connected=False,
            whitebox_connected=False,
            provider_invoked=False,
            world_write_invoked=False,
            mainline_side_effect=False,
            next_allowed_action="Stage2 controlled path expansion",
            blocked_action="Bypass approval gate",
        ),
        _row(
            module="OCR",
            phase="009 static config",
            status="GO",
            scope="shadow",
            runtime_connected=False,
            midplatform_connected=False,
            whitebox_connected=False,
            provider_invoked=False,
            world_write_invoked=False,
            mainline_side_effect=False,
            next_allowed_action="Trial runner wiring (still gated)",
            blocked_action="Unvalidated config in prod",
        ),
        _row(
            module="OCR",
            phase="010 approval gate",
            status="GO",
            scope="shadow",
            runtime_connected=False,
            midplatform_connected=False,
            whitebox_connected=False,
            provider_invoked=False,
            world_write_invoked=False,
            mainline_side_effect=False,
            next_allowed_action="Minimal real OCR trial (historically Vision; pivoted)",
            blocked_action="OCR without approval",
        ),
        _row(
            module="OCR",
            phase="011 minimal real OCR (Vision pivot)",
            status="GO",
            scope="shadow",
            runtime_connected=False,
            midplatform_connected=False,
            whitebox_connected=False,
            provider_invoked=False,
            world_write_invoked=False,
            mainline_side_effect=False,
            next_allowed_action="RapidOCR primary path (012)",
            blocked_action="macOS Vision as unchecked mainline dependency",
            notes="macOS Vision was used in early trial; mainline pivoted to RapidOCR.",
        ),
        _row(
            module="OCR",
            phase="012 RapidOCR mainline provider",
            status="GO",
            scope="shadow",
            runtime_connected=False,
            midplatform_connected=False,
            whitebox_connected=False,
            provider_invoked=False,
            world_write_invoked=False,
            mainline_side_effect=False,
            next_allowed_action="012-Improve-B governance; OCRBridge shadow later",
            blocked_action="Replace gate with ad-hoc provider swap",
        ),
        _row(
            module="OCR",
            phase="012-Improve-B layout/symbol/glyph/reading-order governance",
            status="GO",
            scope="shadow",
            runtime_connected=False,
            midplatform_connected=False,
            whitebox_connected=False,
            provider_invoked=False,
            world_write_invoked=False,
            mainline_side_effect=False,
            next_allowed_action="Pack evidence shapes toward OCRBridge; offline eval",
            blocked_action="Governance output as sole MidPlatform text",
        ),
        _row(
            module="Evaluation Tools",
            phase="Foundation-001",
            status="closed_v0",
            scope="evaluation_only",
            runtime_connected=False,
            midplatform_connected=False,
            whitebox_connected=False,
            provider_invoked=False,
            world_write_invoked=False,
            mainline_side_effect=False,
            next_allowed_action="OCR harness phases",
            blocked_action="Treat eval output as production routing",
        ),
        _row(
            module="Evaluation Tools",
            phase="OCR-002 Chinese font",
            status="CONDITIONAL_GO",
            scope="evaluation_only",
            runtime_connected=False,
            midplatform_connected=False,
            whitebox_connected=False,
            provider_invoked=False,
            world_write_invoked=False,
            mainline_side_effect=False,
            next_allowed_action="Real font / sample hardening",
            blocked_action="Promote CONDITIONAL to prod without archive",
        ),
        _row(
            module="Evaluation Tools",
            phase="OCR-003 RapidOCR quality gate eval",
            status="GO",
            scope="evaluation_only",
            runtime_connected=False,
            midplatform_connected=False,
            whitebox_connected=False,
            provider_invoked=False,
            world_write_invoked=False,
            mainline_side_effect=False,
            next_allowed_action="OCR-004+",
            blocked_action=blk,
        ),
        _row(
            module="Evaluation Tools",
            phase="OCR-004 input image quality gate",
            status="GO",
            scope="evaluation_only",
            runtime_connected=False,
            midplatform_connected=False,
            whitebox_connected=False,
            provider_invoked=False,
            world_write_invoked=False,
            mainline_side_effect=False,
            next_allowed_action="OCR-005 merge",
            blocked_action=blk,
        ),
        _row(
            module="Evaluation Tools",
            phase="OCR-005 quality × accuracy merge",
            status="GO",
            scope="evaluation_only",
            runtime_connected=False,
            midplatform_connected=False,
            whitebox_connected=False,
            provider_invoked=False,
            world_write_invoked=False,
            mainline_side_effect=False,
            next_allowed_action="OCR-006 boundary",
            blocked_action=blk,
        ),
        _row(
            module="Evaluation Tools",
            phase="OCR-006 capability boundary",
            status="CONDITIONAL_GO",
            scope="evaluation_only",
            runtime_connected=False,
            midplatform_connected=False,
            whitebox_connected=False,
            provider_invoked=False,
            world_write_invoked=False,
            mainline_side_effect=False,
            next_allowed_action="OCR-007 gate sim; real samples phase",
            blocked_action="Use boundary map as runtime router",
        ),
        _row(
            module="Evaluation Tools",
            phase="OCR-007 eligibility gate simulator",
            status="GO",
            scope="evaluation_only",
            runtime_connected=False,
            midplatform_connected=False,
            whitebox_connected=False,
            provider_invoked=False,
            world_write_invoked=False,
            mainline_side_effect=False,
            next_allowed_action="OCRBridge design from eval artifacts",
            blocked_action="Import eval routing pack as runtime source",
        ),
        _row(
            module="OCRBridge",
            phase="Design-001",
            status="GO",
            scope="design_only",
            runtime_connected=False,
            midplatform_connected=False,
            whitebox_connected=False,
            provider_invoked=False,
            world_write_invoked=False,
            mainline_side_effect=False,
            next_allowed_action="Review-001 freeze",
            blocked_action="Forward OcrEvidencePack to MidPlatform",
        ),
        _row(
            module="OCRBridge",
            phase="Review-001",
            status="GO",
            scope="design_only",
            runtime_connected=False,
            midplatform_connected=False,
            whitebox_connected=False,
            provider_invoked=False,
            world_write_invoked=False,
            mainline_side_effect=False,
            next_allowed_action="Implementation-RFC-001",
            blocked_action="Treat eval:* refs as runtime refs",
        ),
        _row(
            module="OCRBridge",
            phase="Implementation-RFC-001",
            status="GO",
            scope="rfc_only",
            runtime_connected=False,
            midplatform_connected=False,
            whitebox_connected=False,
            provider_invoked=False,
            world_write_invoked=False,
            mainline_side_effect=False,
            next_allowed_action="Authorize shadow implementation phase",
            blocked_action="Real wiring without flags + hard gate",
        ),
        _row(
            module="Voice",
            phase="OutputGovernance 007–009 (per README index)",
            status="GO",
            scope="design_only",
            runtime_connected=False,
            midplatform_connected=False,
            whitebox_connected=False,
            provider_invoked=False,
            world_write_invoked=False,
            mainline_side_effect=False,
            next_allowed_action="VoiceInteraction-Readiness planning",
            blocked_action="Full prod voice chain without governance",
        ),
        _row(
            module="Voice",
            phase="Qianwen 000–003 inventory / entry / TRW",
            status="GO",
            scope="design_only",
            runtime_connected=False,
            midplatform_connected=False,
            whitebox_connected=False,
            provider_invoked=False,
            world_write_invoked=False,
            mainline_side_effect=False,
            next_allowed_action="RuntimeReadiness continuation",
            blocked_action="Uncontrolled Qwen in prod path",
        ),
        _row(
            module="Voice",
            phase="Policy: Qianwen preferred + TTS fallback",
            status="GO",
            scope="design_only",
            runtime_connected=False,
            midplatform_connected=False,
            whitebox_connected=False,
            provider_invoked=False,
            world_write_invoked=False,
            mainline_side_effect=False,
            next_allowed_action="Documented mainline voice stack when ready",
            blocked_action="Remove fallback policy without ADR",
        ),
        _row(
            module="Voice",
            phase="Full voice interaction (ASR multi-turn semantics)",
            status="NO_GO",
            scope="design_only",
            runtime_connected=False,
            midplatform_connected=False,
            whitebox_connected=False,
            provider_invoked=False,
            world_write_invoked=False,
            mainline_side_effect=False,
            next_allowed_action="VoiceInteraction-Readiness-001",
            blocked_action="Mark as completed in prod",
            notes="User baseline: full interaction module not connected.",
        ),
    ]


def _runtime_connection_matrix(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    any_rt = any(r.get("runtime_connected") for r in rows)
    any_mp = any(r.get("midplatform_connected") for r in rows)
    any_wb = any(r.get("whitebox_connected") for r in rows)
    any_pv = any(r.get("provider_invoked") for r in rows)
    return {
        "aggregate": {
            "any_runtime_connected": any_rt,
            "any_midplatform_connected": any_mp,
            "any_whitebox_connected": any_wb,
            "any_provider_invoked_by_this_review_tool": False,
            "world_write_invoked_any": False,
            "ocr_runtime_mainline_fully_connected": False,
            "ocr_midplatform_forwarding": False,
            "rapidocr_primary_documented": True,
            "macos_vision_mainline": False,
            "paddleocr_trial_done": False,
        },
        "expected_for_this_review_phase": {
            "any_midplatform_connected": False,
            "any_whitebox_connected": False,
            "review_tool_provider_invoked": False,
        },
    }


def _design_vs_runtime_matrix() -> Dict[str, Any]:
    return {
        "definitions": {
            "runtime": "Behavior affecting prod or controlled trial runtime path (not claimed here for OCRBridge).",
            "shadow": "Side-channel or gated trial (OCR Stage-2 stack intent).",
            "design_only": "Docs + contracts + RFC matrices only.",
            "evaluation_only": "Offline harness; no mainline routing.",
            "rfc_only": "Binding plan + flags; no code wiring.",
        },
        "rules": [
            "Evaluation Tools outputs MUST NOT be promoted to runtime routing without separate phase.",
            "OcrEvidencePack eval:* MUST NOT be used as runtime source refs.",
            "MidPlatform consumes only OcrEvidencePackV0 at future wire time; raw_text_joined forbidden as sole input.",
        ],
    }


def _evaluation_tools_matrix() -> Dict[str, Any]:
    return {
        "foundation": "closed_v0",
        "ocr_002": "CONDITIONAL_GO",
        "ocr_003_through_005": "GO",
        "ocr_006": "CONDITIONAL_GO",
        "ocr_007": "GO",
        "runtime_integration": False,
        "whitebox_integration": False,
        "mainline_side_effect": False,
    }


def _ocr_bridge_matrix() -> Dict[str, Any]:
    return {
        "design_contract": "GO",
        "interface_freeze": "GO",
        "implementation_rfc": "GO",
        "real_implementation": False,
        "midplatform_forwarding": False,
        "principles": [
            "MidPlatform only OcrEvidencePackV0",
            "No raw_text_joined direct to MidPlatform",
            "OCR provider has no authority to write facts",
            "OCRBridge is evidence encapsulation only",
            "MidPlatform governs composition and fact admission",
        ],
    }


def _voice_matrix() -> Dict[str, Any]:
    return {
        "qwen_voice_primary_policy": "documented",
        "tts_fallback_preserved": True,
        "full_voice_interaction_connected": False,
        "asr_multiturn_mainline": False,
        "notes": "Align with README voice index; no live Qwen call in this review tool.",
    }


def _next_step_recommendation() -> Dict[str, Any]:
    return {
        "options": [
            {
                "id": "A",
                "name": "OCRBridge-Implementation-001",
                "summary": "OcrEvidencePack shadow serialization binding; still no MidPlatform forward.",
            },
            {
                "id": "B",
                "name": "VoiceInteraction-Readiness-001",
                "summary": "Gap analysis: ASR, multi-turn, semantic context, Qianwen mainline invocation.",
            },
            {
                "id": "C",
                "name": "PaddleOCR-Readiness-001",
                "summary": "PaddleOCR provider readiness + manifest; do not replace RapidOCR as primary.",
            },
            {
                "id": "D",
                "name": "EvaluationTools-OCR-RealSamples-001",
                "summary": "Real samples + human labels to tighten OCR-006 boundary credibility.",
            },
            {
                "id": "E",
                "name": "Mainline-IntegrationPlan-001",
                "summary": "Consolidate YOLO/OCR/Voice into next integration roadmap.",
            },
        ],
        "recommended_next_step": "Option E then A (integration plan before shadow binding), unless voice is higher priority then B.",
        "execution": "none_by_this_tool",
    }


def _check_docs(repo: Path) -> Tuple[List[str], List[str]]:
    """Return (warnings, missing)."""
    anchors = [
        "docs/architecture/ocr_bridge/LUNA_OCR_MIDPLATFORM_INTERFACE_FREEZE_V0.md",
        "docs/architecture/ocr_bridge/LUNA_OCR_EVIDENCE_GOVERNANCE_AUTHORITY_FREEZE_V0.md",
        "docs/architecture/ocr_bridge/LUNA_OCR_BRIDGE_RUNTIME_BINDING_RFC_V0.md",
        "docs/architecture/evaluation/LUNA_EVALUATION_TOOLS_OVERVIEW_V0.md",
        "docs/architecture/README.md",
        "docs/architecture/LUNA_MAINLINE_CURRENT_STATUS_REVIEW_V0.md",
        "docs/architecture/LUNA_MAINLINE_PHASE_STATUS_MATRIX_V0.md",
        "docs/architecture/LUNA_MAINLINE_DESIGN_RUNTIME_BOUNDARY_MATRIX_V0.md",
        "docs/architecture/LUNA_MAINLINE_NEXT_STEP_DECISION_OPTIONS_V0.md",
        "docs/architecture/LUNA_MAINLINE_STATUS_REVIEW_GO_NO_GO_PACK_V0.md",
    ]
    missing: List[str] = []
    for rel in anchors:
        if not (repo / rel).is_file():
            missing.append(rel)
    warnings: List[str] = []
    if missing:
        warnings.append("anchor_docs_missing:" + ",".join(missing))
    else:
        warnings.append("anchor_docs_present")
    return warnings, missing


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--workspace-min-root", default="", help="Recorded for context only; not scanned by default.")
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()

    repo = _require_abs(args.repo_root, "--repo-root")
    ws = Path(args.workspace_min_root).expanduser().resolve() if args.workspace_min_root.strip() else None

    if args.output_root.strip():
        out = _require_abs(args.output_root, "--output-root")
    else:
        stamp = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        out = (Path.home() / "LunaRuntime" / "logs" / f"mainline_status_review_001_{stamp}").resolve()
    out.mkdir(parents=True, exist_ok=True)

    rows = _phase_status_matrix()
    doc_warnings, doc_missing = _check_docs(repo)

    summary = {
        "phase": "Phase-Mainline-StatusReview-001",
        "repo_root": str(repo),
        "workspace_min_root": str(ws) if ws else None,
        "output_root": str(out),
        "review_tool_invoked_provider": False,
        "review_tool_modified_runtime": False,
        "yolo_stage1_status": "closed_v0_for_005fix_and_007_with_006_GO",
        "docs_status_warnings": doc_warnings,
        "docs_missing_anchors": doc_missing,
        "verdict": "GO" if not doc_missing else "CONDITIONAL_GO",
    }

    _write_json(out / "mainline_status_review_summary.json", summary)
    _write_json(out / "mainline_phase_status_matrix.json", {"rows": rows, "schema_version": "v0"})
    _write_json(out / "mainline_runtime_connection_matrix.json", _runtime_connection_matrix(rows))
    _write_json(out / "mainline_design_vs_runtime_matrix.json", _design_vs_runtime_matrix())
    _write_json(out / "mainline_evaluation_tools_matrix.json", _evaluation_tools_matrix())
    _write_json(out / "mainline_ocr_bridge_status_matrix.json", _ocr_bridge_matrix())
    _write_json(out / "mainline_voice_status_matrix.json", _voice_matrix())
    _write_json(out / "mainline_next_step_recommendation.json", _next_step_recommendation())
    _write_json(
        out / "mainline_docs_consistency_warning_report.json",
        {"missing_anchor_docs": doc_missing, "warnings": doc_warnings, "note": "Spot-check only; expand anchors as needed."},
    )

    notes = out / "mainline_status_review_notes.md"
    notes.write_text(
        "\n".join(
            [
                "# Mainline Current Status Review (v0)",
                "",
                f"- **repo_root**: `{repo}`",
                f"- **output_root**: `{out}`",
                "",
                "Read-only consolidation. No provider calls. No runtime edits.",
                "",
                "## Verdict",
                "",
                f"- **{summary['verdict']}** (anchor doc check)",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(json.dumps({"output_root": str(out), "verdict": summary["verdict"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
