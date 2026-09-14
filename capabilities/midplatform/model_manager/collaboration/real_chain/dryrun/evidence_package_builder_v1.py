# -*- coding: utf-8 -*-
"""Evidence Package Builder — slot execution → evidence package v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.model_manager.collaboration.real_chain.evidence_fusion_adapter_v1 import (
    build_evidence_package,
)


def build_packages_from_executions(
    executions: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Convert slot execution results to evidence packages."""
    packages: List[Dict[str, Any]] = []
    for ex in executions:
        if ex.get("status") == "skipped":
            continue
        packages.append(build_evidence_package(
            slot_id=ex.get("slot_id", ""),
            provider_id=ex.get("provider_id", ""),
            evidence_type=ex.get("evidence_type", "evidence_candidate"),
            payload=ex.get("payload") or {},
            status="collected" if ex.get("status") == "completed" else "failed",
        ))
        packages[-1]["evidence_id"] = ex.get("evidence_id")
        packages[-1]["provider_execution_id"] = ex.get("provider_execution_id")
    return packages


def build_fusion_evidence_package(
    packages: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Case A fusion shape — evidence package, not merged fact."""
    collected = [p for p in packages if p.get("status") == "collected"]
    text_pkg = next((p for p in collected if p.get("evidence_type") == "ocr_text_candidate"), {})
    region_pkg = next((p for p in collected if p.get("evidence_type") == "text_region_candidate"), {})
    context_pkg = next((p for p in collected if p.get("evidence_type") == "context_evidence_candidate"), {})

    return {
        "evidence_package_summary": {
            "text": (text_pkg.get("payload") or {}).get("text", ""),
            "region": (region_pkg.get("payload") or {}).get("region", "shopfront_area_candidate"),
            "context": (context_pkg.get("payload") or {}).get("context", "commercial_sign_candidate"),
            "confidence": "candidate",
        },
        "not_merged_fact": True,
        "forbidden_example": "阿叔阿姨的店 + 餐厅 = 事实",
        "candidate_only": True,
        "not_fact": True,
    }
