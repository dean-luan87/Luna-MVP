# -*- coding: utf-8 -*-
"""
OcrEvidencePack shadow serialization v0 (Phase-OCRBridge-Implementation-001).

Builds validated OcrEvidencePackV0 JSON alongside shadow-only envelopes and trace rows.
Does not invoke MidPlatform, OCR providers, or mutate mainline runtime.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

from capabilities.ocr_bridge.ocr_evidence_pack_contract_v0 import (
    OCR_EVIDENCE_PACK_VERSION,
    build_ocr_evidence_pack_from_eval_routing_pack_v0,
    load_non_ocr_types_from_boundary_map_v0,
)

FORBIDDEN_SOURCE_PREFIXES = (
    "runtime:",
    "production:",
    "midplatform:",
    "scene_delta:",
    "world_context:",
)

ALLOWED_SHADOW_OFFLINE_PREFIXES = ("eval:", "shadow:", "offline_trial:")


def _collect_ref_strings(obj: Any, out: List[str]) -> None:
    if isinstance(obj, str):
        if obj.strip():
            out.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            _collect_ref_strings(v, out)
    elif isinstance(obj, list):
        for v in obj:
            _collect_ref_strings(v, out)


def validate_shadow_source_refs_v0(*, pack: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensures no forged runtime-style refs; collects missing top-level OCRBridge source refs.
    """
    missing: List[str] = []
    forged: List[str] = []
    for k in (
        "source_image_ref",
        "source_provider_ref",
        "source_quality_gate_ref",
        "source_layout_ref",
        "source_eligibility_gate_ref",
    ):
        v = pack.get(k)
        if not isinstance(v, str) or not v.strip():
            missing.append(k)

    all_refs: List[str] = []
    _collect_ref_strings(pack, all_refs)
    seen = set()
    for ref in all_refs:
        if ref in seen:
            continue
        seen.add(ref)
        lower = ref.lower()
        if any(lower.startswith(p) for p in FORBIDDEN_SOURCE_PREFIXES):
            forged.append(ref)
        # empty already handled via missing keys

    classified: List[Dict[str, Any]] = []
    for ref in sorted(seen):
        kind = "other"
        if ref.startswith("eval:"):
            kind = "eval"
        elif ref.startswith("shadow:"):
            kind = "shadow"
        elif ref.startswith("offline_trial:"):
            kind = "offline_trial"
        classified.append({"ref": ref, "class": kind})

    return {
        "missing_source_refs": missing,
        "forged_runtime_like_refs": forged,
        "ref_inventory_classified": classified,
        "validation_ok": len(forged) == 0,
        "source_ref_status": "shadow_or_offline_ref",
    }


def _shadow_trace_replay_audit_refs(
    *,
    eligibility_gate_root: str,
    bridge_review_root: str,
    rfc_root: str,
    shadow_pack_id: str,
) -> Dict[str, str]:
    return {
        "trace_ref": f"shadow:ocr_bridge_implementation_001:trace:{shadow_pack_id}",
        "replay_ref": f"shadow:ocr_bridge_implementation_001:replay:{shadow_pack_id}",
        "audit_ref": f"shadow:ocr_bridge_implementation_001:audit:{shadow_pack_id}",
        "eligibility_gate_bundle_ref": f"shadow:eligibility_gate_root:{eligibility_gate_root}",
        "bridge_review_bundle_ref": f"shadow:bridge_review_root:{bridge_review_root}",
        "rfc_bundle_ref": f"shadow:rfc_root:{rfc_root}",
    }


def build_shadow_ocr_evidence_pack_v0(
    *,
    routing_pack: Dict[str, Any],
    eligibility_gate_root: str,
    boundary_eval_root: str,
    bridge_review_root: str,
    rfc_root: str,
    pack_id: Optional[str] = None,
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """
    Returns (shadow_envelope, pack, source_ref_report).

    Pack is OcrEvidencePackV0-shaped; midplatform forward & fact layer are forced OFF for this phase.
    """
    shadow_pack_id = f"ocr_shadow_{uuid.uuid4().hex[:16]}"
    rid = pack_id or f"ocr_pack_{uuid.uuid4().hex[:12]}"

    pack = build_ocr_evidence_pack_from_eval_routing_pack_v0(
        routing_pack=routing_pack,
        eligibility_gate_root=eligibility_gate_root,
        boundary_eval_root=boundary_eval_root,
        pack_id=rid,
    )
    # Re-id pack to align with shadow id for trace correlation (optional clarity)
    pack["pack_id"] = rid

    ref_report = validate_shadow_source_refs_v0(pack=pack)
    missing = ref_report.get("missing_source_refs") or []

    pack.setdefault("midplatform_contract", {})
    # Phase-001: never forward / never fact layer from this binding path
    pack["midplatform_contract"].update(
        {
            "allowed_to_forward_to_midplatform": False,
            "allowed_to_enter_fact_text_layer": False,
            "requires_human_or_higher_layer_review": True,
            "forwarding_mode": "blocked",
        }
    )
    if missing:
        # Conservative: explicit blocked when refs incomplete
        pack["midplatform_contract"]["forwarding_mode"] = "blocked"

    pack["hard_audit"] = {
        "runtime_integration": False,
        "whitebox_integration": False,
        "mainline_side_effect": False,
        "mainline_routing_changed": False,
        "midplatform_invoked": False,
        "scene_delta_invoked": False,
        "world_context_invoked": False,
        "navigation_action": None,
        "world_write_invoked": False,
        "hive_upload_invoked": False,
    }

    bind_refs = _shadow_trace_replay_audit_refs(
        eligibility_gate_root=eligibility_gate_root,
        bridge_review_root=bridge_review_root,
        rfc_root=rfc_root,
        shadow_pack_id=shadow_pack_id,
    )
    ref_report["binding_refs"] = bind_refs
    ref_report["missing_source_refs"] = missing

    envelope = {
        "shadow_pack_id": shadow_pack_id,
        "pack_version": OCR_EVIDENCE_PACK_VERSION,
        "ocr_evidence_pack_id": pack.get("pack_id"),
        "source_ref_status": "shadow_or_offline_ref",
        "midplatform_forwarding_enabled": False,
        "fact_text_layer_enabled": False,
        "runtime_side_effect": False,
        "phase": "Phase-OCRBridge-Implementation-001",
        "binding_roots": {
            "eligibility_gate_root": eligibility_gate_root,
            "bridge_review_root": bridge_review_root,
            "rfc_root": rfc_root,
            "boundary_eval_root": boundary_eval_root,
        },
        "trace_replay_audit": bind_refs,
    }

    return envelope, pack, ref_report


def serialize_ocr_evidence_pack_shadow_v0(*, shadow_envelope: Dict[str, Any], pack: Dict[str, Any]) -> Dict[str, Any]:
    """Wrapper JSON for on-disk shadow artifact (validator runs on inner `pack`)."""
    return {"shadow_envelope": shadow_envelope, "pack": pack}


def build_shadow_pack_trace_record_v0(
    *,
    shadow_envelope: Dict[str, Any],
    validation_passed: bool,
    forwarding_mode: str,
) -> Dict[str, Any]:
    """Single trace row for jsonl."""
    return {
        "phase": "Phase-OCRBridge-Implementation-001",
        "shadow_pack_id": shadow_envelope.get("shadow_pack_id"),
        "ocr_evidence_pack_id": shadow_envelope.get("ocr_evidence_pack_id"),
        "validation_passed": validation_passed,
        "forwarding_mode": forwarding_mode,
        "midplatform_forwarding_enabled": shadow_envelope.get("midplatform_forwarding_enabled"),
        "fact_text_layer_enabled": shadow_envelope.get("fact_text_layer_enabled"),
        "runtime_side_effect": shadow_envelope.get("runtime_side_effect"),
    }


def read_routing_pack_from_eligibility_root_v0(eligibility_gate_root: Path) -> Dict[str, Any]:
    p = eligibility_gate_root / "ocr_evidence_routing_pack.json"
    if not p.is_file():
        raise FileNotFoundError(f"missing routing pack: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def resolve_boundary_eval_root_v0(eligibility_gate_root: Path, boundary_eval_override: str) -> Path:
    if boundary_eval_override.strip():
        return Path(boundary_eval_override).expanduser().resolve()
    summ = eligibility_gate_root / "ocr_eligibility_gate_summary.json"
    if summ.is_file():
        data = json.loads(summ.read_text(encoding="utf-8"))
        ber = str(data.get("boundary_eval_root") or "").strip()
        if ber:
            return Path(ber).expanduser().resolve()
    raise FileNotFoundError(
        "boundary_eval_root: pass explicit path or ensure ocr_eligibility_gate_summary.json has boundary_eval_root"
    )


def read_env_flags_for_report_v0() -> Dict[str, Any]:
    """Read-only snapshot of env (no mutation)."""
    import os

    keys = [
        "LUNA_DISABLE_OCR_BRIDGE_RUNTIME_V1",
        "LUNA_ENABLE_OCR_EVIDENCE_PACK_SHADOW_V1",
        "LUNA_ENABLE_OCR_EVIDENCE_PACK_VALIDATE_V1",
        "LUNA_ENABLE_OCR_EVIDENCE_PACK_FORWARD_MIDPLATFORM_V1",
        "LUNA_ENABLE_OCR_FACT_TEXT_LAYER_CANDIDATES_V1",
    ]
    return {k: os.environ.get(k) for k in keys}


__all__ = [
    "ALLOWED_SHADOW_OFFLINE_PREFIXES",
    "FORBIDDEN_SOURCE_PREFIXES",
    "build_shadow_ocr_evidence_pack_v0",
    "build_shadow_pack_trace_record_v0",
    "read_env_flags_for_report_v0",
    "read_routing_pack_from_eligibility_root_v0",
    "resolve_boundary_eval_root_v0",
    "serialize_ocr_evidence_pack_shadow_v0",
    "validate_shadow_source_refs_v0",
]
