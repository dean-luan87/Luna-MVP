# -*- coding: utf-8 -*-
"""Vision provider selection skeleton v0 — default stub only; no real models."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

from .vision_provider_registry_v0 import build_default_vision_provider_registry_v0, snapshot_registry_v0
from .vision_provider_stub_adapter_v0 import VisionStubAdapterV0, merge_stub_results_v0
from .vision_recognition_audit_v0 import build_vision_recognition_adapter_selection_audit_v0


def _env_truthy(name: str) -> bool:
    v = os.environ.get(name, "").strip().lower()
    return v in ("1", "true", "yes", "on")


def read_real_provider_env_flags_v0() -> Dict[str, bool]:
    return {
        "LUNA_ENABLE_VISION_REAL_PROVIDER_V0": _env_truthy("LUNA_ENABLE_VISION_REAL_PROVIDER_V0"),
        "LUNA_ENABLE_YOLO_RUNTIME_PROVIDER_V0": _env_truthy("LUNA_ENABLE_YOLO_RUNTIME_PROVIDER_V0"),
        "LUNA_ENABLE_SUPERVISION_RUNTIME_PROVIDER_V0": _env_truthy("LUNA_ENABLE_SUPERVISION_RUNTIME_PROVIDER_V0"),
        "LUNA_ENABLE_VLM_RUNTIME_PROVIDER_V0": _env_truthy("LUNA_ENABLE_VLM_RUNTIME_PROVIDER_V0"),
    }


def real_provider_requested_from_env_v0(flags: Dict[str, bool]) -> bool:
    return any(flags.values())


def real_provider_allowed_skeleton_v0() -> bool:
    """This phase never allows invoking real providers."""
    return False


def collect_packs_from_bundle_v0(bundle: Dict[str, Any]) -> List[Dict[str, Any]]:
    packs = bundle.get("packs")
    if isinstance(packs, list):
        return [p for p in packs if isinstance(p, dict)]
    if bundle.get("schema_version") == "vision_provider_input_pack_v0" and isinstance(bundle.get("input_units"), list):
        return [bundle]
    return []


def detect_full_frame_direct_to_provider_v0(packs: List[Dict[str, Any]]) -> bool:
    """True if any unit would send full-frame pixels as provider input (forbidden in skeleton)."""
    for pack in packs:
        src = str(pack.get("source_image_ref") or "")
        for u in pack.get("input_units") or []:
            if not isinstance(u, dict):
                continue
            ut = str(u.get("unit_type") or "")
            if ut in ("full_frame", "full_frame_low_priority_stub"):
                return True
            im = str(u.get("image_ref") or "")
            if src and im and im == src:
                return True
    return False


def select_vision_provider_skeleton_v0(
    *,
    registry: Dict[str, Any],
    env_flags: Dict[str, bool],
    full_frame_direct: bool,
) -> Dict[str, Any]:
    """Build ``vision_provider_selection_report_v0``."""
    requested = real_provider_requested_from_env_v0(env_flags)
    allowed = real_provider_allowed_skeleton_v0()
    reasons: List[str] = ["default_stub_provider"]
    if requested:
        reasons.append("real_provider_env_requested_but_blocked_skeleton_v0")
    if full_frame_direct:
        reasons.append("full_frame_path_detected_in_pack_units")

    return {
        "schema_version": "vision_provider_selection_report_v0",
        "selected_provider": "vision_stub",
        "selected_provider_level": "stub",
        "real_provider_requested": bool(requested),
        "real_provider_allowed": bool(allowed),
        "real_provider_invoked": False,
        "provider_selection_reason_codes": reasons,
        "provider_registry_snapshot": snapshot_registry_v0(registry),
        "real_provider_env_flags": dict(env_flags),
        "full_frame_direct_to_provider": bool(full_frame_direct),
    }


def build_recognition_candidate_matrix_v0(
    *,
    packs: List[Dict[str, Any]],
    stub_merged: Dict[str, Any],
    selected_provider: str,
) -> Dict[str, Any]:
    """Join stub items with pack/unit context for evaluation matrix."""
    items_by_unit: Dict[str, Dict[str, Any]] = {}
    for it in stub_merged.get("items") or []:
        if isinstance(it, dict):
            uid = str(it.get("unit_id") or "")
            if uid:
                items_by_unit[uid] = it

    rows: List[Dict[str, Any]] = []
    for pack in packs:
        pid = str(pack.get("pack_id") or "")
        sf = str(pack.get("source_frame_id") or "")
        for u in pack.get("input_units") or []:
            if not isinstance(u, dict):
                continue
            uid = str(u.get("unit_id") or "")
            st = items_by_unit.get(uid) or {}
            rows.append(
                {
                    "pack_id": pid,
                    "source_frame_id": sf,
                    "unit_id": uid,
                    "roi_id": str(u.get("roi_id") or ""),
                    "unit_type": str(u.get("unit_type") or ""),
                    "crop_image_ref": str(u.get("image_ref") or ""),
                    "selected_provider": selected_provider,
                    "stub_label": st.get("label"),
                    "stub_confidence": st.get("confidence"),
                    "synthetic": True,
                }
            )
    return {"schema": "vision_recognition_candidate_matrix_v0", "rows": rows}


def run_vision_recognition_adapter_selection_skeleton_v0(roi_proposal_root: Path) -> Dict[str, Any]:
    """Load ROI stub artifacts; select stub; run synthetic recognition; emit evaluation bundle."""
    root = roi_proposal_root.resolve()
    pack_path = root / "vision_provider_input_pack.json"
    cand_roi_path = root / "vision_roi_proposal_candidate.json"
    roi_audit_path = root / "vision_roi_proposal_audit_report.json"
    for p in (pack_path, cand_roi_path, roi_audit_path):
        if not p.is_file():
            raise FileNotFoundError(p)

    bundle = json.loads(pack_path.read_text(encoding="utf-8"))
    packs = collect_packs_from_bundle_v0(bundle)
    if not packs:
        raise ValueError("vision_provider_input_pack.json: no packs")

    full_frame_direct = detect_full_frame_direct_to_provider_v0(packs)
    registry = build_default_vision_provider_registry_v0()
    env_flags = read_real_provider_env_flags_v0()
    selection = select_vision_provider_skeleton_v0(
        registry=registry,
        env_flags=env_flags,
        full_frame_direct=full_frame_direct,
    )

    adapter = VisionStubAdapterV0()
    per_pack_results: List[Dict[str, Any]] = []
    for pack in packs:
        if not adapter.supports_input_pack(pack):
            continue
        per_pack_results.append(adapter.run(pack, {}, None))
    stub_merged = merge_stub_results_v0(per_pack_results)

    input_units_count = sum(len(p.get("input_units") or []) for p in packs)
    items = stub_merged.get("items") or []
    audit = build_vision_recognition_adapter_selection_audit_v0(
        selected_provider="vision_stub",
        full_frame_direct_to_provider=full_frame_direct,
    )

    matrix = build_recognition_candidate_matrix_v0(
        packs=packs,
        stub_merged=stub_merged,
        selected_provider="vision_stub",
    )

    summary = {
        "phase": "Phase-Vision-Lightweight-Recognition-Adapter-Selection-001",
        "schema": "vision_recognition_adapter_selection_summary_v0",
        "vision_roi_proposal_root": str(root),
        "pack_count": len(packs),
        "input_units_count": input_units_count,
        "stub_result_items_count": len(items),
        "selected_provider": "vision_stub",
        "selected_provider_level": "stub",
    }

    return {
        "summary": summary,
        "registry_snapshot": snapshot_registry_v0(registry),
        "selection_report": selection,
        "stub_result": stub_merged,
        "candidate_matrix": matrix,
        "audit": audit,
    }
