#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Phase-CoreCapability-StatusReview-001
YOLO / OCR / Voice Core Capability Closure Review v0.

Read-only review tool:
- Scans docs/architecture/README.md and known closure review documents.
- Checks existence of key output roots under logs/.
- Emits summary JSON matrices + next-phase option hints.

Hard boundaries:
- No runtime wiring changes.
- No new capability implementation.
- No real TTS/playback.
"""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any, Dict, List, Optional


def _now() -> float:
    return time.time()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _exists(path: Path) -> bool:
    try:
        return path.exists()
    except Exception:
        return False


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_md(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


@dataclass(frozen=True)
class CapabilityRowV0:
    capability: str
    phase_name: str
    status: str  # done|closed_v0|conditional_go|definition_only|skeleton_only|future_branch|unknown
    scope: str
    runtime_connected: bool
    real_output_allowed: bool
    trace_replay_whitebox: str  # none|local|adapter|request_trace_shadow
    request_trace_mapped: bool
    hard_blockers: List[str] = field(default_factory=list)
    soft_followups: List[str] = field(default_factory=list)
    recommended_next: str = ""


def _infer_status_from_docs(*docs: Path) -> str:
    """
    Conservative status inference:
    - Prefer explicit frozen markers: "closed_v0" or "closure_recommendation: GO".
    - Only return conditional_go when no closed_v0/GO marker is present.
    """
    for d in docs:
        if not _exists(d):
            continue
        txt = _read_text(d).lower()
        if "closed_v0" in txt:
            return "closed_v0"
        # Common closure phrasing patterns
        if "closure_recommendation" in txt and "go" in txt:
            return "closed_v0"
        if "closure 结论" in txt and "go" in txt:
            return "closed_v0"
        if "冻结结论" in txt and "closed_v0" in txt:
            return "closed_v0"
        if "conditional_go" in txt:
            return "conditional_go"
        if "closure" in txt or "closure review" in txt:
            return "done"
        return "done"
    return "unknown"


def _capability_rows(repo: Path, *, phase_002_root: Path, phase_005_root: Path) -> List[CapabilityRowV0]:
    docs = repo / "docs" / "architecture"

    # Evidence anchors (docs)
    yolo_closure = docs / "LUNA_YOLO_OFFLINE_PERCEPTION_SOURCE_CLOSURE_REVIEW_V0.md"
    yolo_status_matrix = docs / "LUNA_YOLO_OFFLINE_PERCEPTION_CAPABILITY_STATUS_MATRIX_V0.md"
    yolo_bridge_closure = docs / "LUNA_YOLO_OCR_OFFLINE_BRIDGE_CLOSURE_REVIEW_V0.md"

    ocr_offline_closure = docs / "LUNA_OCR_OFFLINE_SOURCE_POLICY_CLOSURE_REVIEW_V0.md"
    midplatform_closure = docs / "LUNA_MIDPLATFORM_OCR_BRIDGE_CLOSURE_REVIEW_V0.md"

    scene_delta_closure = docs / "LUNA_SCENE_DELTA_CLOSURE_REVIEW_V0.md"
    world_context_closure = docs / "LUNA_WORLD_CONTEXT_EVIDENCE_CLOSURE_REVIEW_V0.md"
    write_readiness_closure = docs / "LUNA_WORLD_MODEL_WRITE_READINESS_CLOSURE_REVIEW_V0.md"

    voice_closure = docs / "LUNA_VOICE_OUTPUT_GOVERNANCE_CLOSURE_REVIEW_V0.md"

    # Observability anchors
    voice_request_trace_shadow = _exists(phase_005_root / "voice_output_request_chains.json")

    rows: List[CapabilityRowV0] = []

    # YOLO (core perception)
    rows.append(
        CapabilityRowV0(
            capability="yolo",
            phase_name="Phase-ModelPerception-Closure-001 (YOLO offline perception source)",
            status=_infer_status_from_docs(yolo_closure, yolo_status_matrix),
            scope="OptionA_phone_local_offline_evaluation_only",
            runtime_connected=False,
            real_output_allowed=False,
            trace_replay_whitebox="local",
            request_trace_mapped=False,
            hard_blockers=[],
            soft_followups=[
                "YOLO request_trace shadow mapping not unified with core TRW (future adapter/mapping)",
                "runtime integration explicitly blocked (needs separate phase + gates)",
            ],
            recommended_next="OCR/YOLO/Voice unified RequestTrace mapping (core stage namespace unification)",
        )
    )

    # OCR offline source policy (closure)
    rows.append(
        CapabilityRowV0(
            capability="ocr",
            phase_name="Phase-ModelOCR-010 (offline source policy closure)",
            status=_infer_status_from_docs(ocr_offline_closure),
            scope="offline_source_policy_only",
            runtime_connected=False,
            real_output_allowed=False,
            trace_replay_whitebox="local",
            request_trace_mapped=False,
            soft_followups=["OCR request_trace shadow mapping not established as core chain"],
            recommended_next="OCR/YOLO RequestTrace mapping adapter (shadow) + stage namespace unification",
        )
    )

    # MidPlatform OCR bridge
    rows.append(
        CapabilityRowV0(
            capability="midplatform",
            phase_name="Phase-ModelOCR-MidPlatform-Bridge-003 (OCR→MidPlatform bridge)",
            status=_infer_status_from_docs(midplatform_closure),
            scope="offline_skeleton_only",
            runtime_connected=False,
            real_output_allowed=False,
            trace_replay_whitebox="local",
            request_trace_mapped=False,
            soft_followups=["MidPlatform bridge not wired to real MidPlatform runtime"],
            recommended_next="RequestTrace unification across OCR/MidPlatform (shadow)",
        )
    )

    # YOLO×OCR offline bridge (integration chain between yolo and ocr)
    rows.append(
        CapabilityRowV0(
            capability="yolo_ocr_bridge",
            phase_name="Phase-ModelOCR-YOLO-Bridge-004 (YOLO×OCR offline bridge closure)",
            status=_infer_status_from_docs(yolo_bridge_closure),
            scope="offline_bridge_trace_replay_whitebox",
            runtime_connected=False,
            real_output_allowed=False,
            trace_replay_whitebox="local",
            request_trace_mapped=False,
            soft_followups=["bridge sample scale minimal (documented); expand as future branch"],
            recommended_next="Core RequestTrace mapping for perception bridge outputs (shadow)",
        )
    )

    # Scene delta
    rows.append(
        CapabilityRowV0(
            capability="scene_delta",
            phase_name="Phase-MidPlatform-SceneDelta-003 (SceneDelta closure)",
            status=_infer_status_from_docs(scene_delta_closure),
            scope="offline_skeleton_only",
            runtime_connected=False,
            real_output_allowed=False,
            trace_replay_whitebox="local",
            request_trace_mapped=False,
            recommended_next="Unify trace/replay/whitebox into RequestTrace view (shadow)",
        )
    )

    # World context evidence
    rows.append(
        CapabilityRowV0(
            capability="world_context",
            phase_name="Phase-WorldModel-ContextEvidence-004 (WorldContextEvidence closure)",
            status=_infer_status_from_docs(world_context_closure),
            scope="candidate_only_offline_skeleton",
            runtime_connected=False,
            real_output_allowed=False,
            trace_replay_whitebox="local",
            request_trace_mapped=False,
            recommended_next="RequestTrace mapping across OCR→MidPlatform→SceneDelta→WorldContext (shadow)",
        )
    )

    # Write readiness
    rows.append(
        CapabilityRowV0(
            capability="write_readiness",
            phase_name="Phase-WorldModel-WriteReadiness-003 (WriteReadiness closure)",
            status=_infer_status_from_docs(write_readiness_closure),
            scope="definition_only_governance_layer",
            runtime_connected=False,
            real_output_allowed=False,
            trace_replay_whitebox="none",
            request_trace_mapped=False,
            recommended_next="Do not implement runtime writes; next is mapping/observability unification only",
        )
    )

    # Voice output governance
    voice_trw_level = "request_trace_shadow" if voice_request_trace_shadow else "adapter"
    rows.append(
        CapabilityRowV0(
            capability="voice",
            phase_name="Phase-Voice-OutputGovernance-006 (closed_v0 offline/shadow governance chain)",
            status=_infer_status_from_docs(voice_closure),
            scope="offline_shadow_governance_chain",
            runtime_connected=False,
            real_output_allowed=False,
            trace_replay_whitebox=voice_trw_level,
            request_trace_mapped=bool(voice_request_trace_shadow),
            soft_followups=["trace_id/session_id injection still missing (future branch)"],
            recommended_next="Unify core capability RequestTrace stage namespace (YOLO/OCR/Voice)",
        )
    )

    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True, help="Output root under logs/")
    args = ap.parse_args()

    repo = Path(__file__).resolve().parents[1]
    out_root = Path(args.output_root)
    out_root.mkdir(parents=True, exist_ok=True)

    readme = repo / "docs" / "architecture" / "README.md"

    phase_002_root = repo / "logs" / "voice_output_governance_002_test_run"
    phase_004_root = repo / "logs" / "voice_output_trw_adapter_004_test_run"
    phase_005_root = repo / "logs" / "voice_output_request_trace_extractor_005_test_run"

    rows = _capability_rows(repo, phase_002_root=phase_002_root, phase_005_root=phase_005_root)
    rows_json = [asdict(r) for r in rows]

    closure_matrix = [
        {
            "capability": r.capability,
            "status": r.status,
            "scope": r.scope,
            "runtime_connected": r.runtime_connected,
            "real_output_allowed": r.real_output_allowed,
        }
        for r in rows
    ]

    trw_matrix = [
        {
            "capability": r.capability,
            "trace_replay_whitebox": r.trace_replay_whitebox,
            "request_trace_mapped": r.request_trace_mapped,
            "notes": r.soft_followups,
        }
        for r in rows
        if r.capability in ("yolo", "ocr", "voice")
    ]

    gaps: List[Dict[str, Any]] = []
    # Hard/soft gaps inferred from rows
    for r in rows:
        for hb in r.hard_blockers:
            gaps.append({"capability": r.capability, "severity": "hard", "gap": hb})
        for sf in r.soft_followups:
            gaps.append({"capability": r.capability, "severity": "soft", "gap": sf})

    next_phase_options = {
        "A": "YOLO core closure (only if missing; current offline perception closure exists)",
        "B": "OCR / YOLO TRW RequestTrace Mapping (shadow)",
        "C": "Unified Core Capability TRW (stage namespace unification across YOLO/OCR/Voice)",
        "D": "Voice governed_submit shadow (still no real playback)",
        "E": "Real runtime readiness review (definition-only; no wiring)",
    }

    recommendation = {
        "recommended_next": "C (Unified Core Capability TRW) then B (OCR/YOLO RequestTrace mapping), keep real runtime blocked",
        "rationale": [
            "Voice already has request_trace_shadow; YOLO/OCR do not.",
            "Unifying observability reduces risk of 'done in docs' vs 'not visible in debug'.",
            "Runtime wiring remains blocked; next step should be observability/mapping only.",
        ],
    }

    summary = {
        "phase": "Phase-CoreCapability-StatusReview-001",
        "tool": "run_core_capability_status_review_v0.py",
        "generated_at_s": _now(),
        "inputs": {
            "docs_architecture_readme": str(readme),
            "phase_002_voice_root": str(phase_002_root) if _exists(phase_002_root) else None,
            "phase_004_voice_adapter_root": str(phase_004_root) if _exists(phase_004_root) else None,
            "phase_005_voice_request_trace_root": str(phase_005_root) if _exists(phase_005_root) else None,
        },
        "capabilities_count": len(rows),
        "boundaries": {
            "no_runtime_connected": True,
            "no_real_tts": True,
            "no_real_world_model_write": True,
        },
    }

    _write_json(out_root / "core_capability_status_summary.json", summary)
    _write_json(out_root / "core_capability_phase_matrix.json", rows_json)
    _write_json(out_root / "core_capability_closure_matrix.json", closure_matrix)
    _write_json(out_root / "core_capability_trw_observability_matrix.json", trw_matrix)
    _write_json(out_root / "core_capability_gap_register.json", gaps)
    _write_json(out_root / "core_capability_next_phase_recommendation.json", recommendation)

    _write_md(
        out_root / "review_notes.md",
        "\n".join(
            [
                "# Phase-CoreCapability-StatusReview-001 Review Notes",
                "",
                f"- output_root: `{str(out_root)}`",
                f"- generated_at: {time.strftime('%Y-%m-%d %H:%M:%S')}",
                "",
                "## Summary",
                f"- rows: {len(rows)}",
                "- This review is definition/skeleton/closure aware; it does not claim runtime readiness.",
                "",
            ]
        ),
    )

    print(str(out_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

