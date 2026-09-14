# -*- coding: utf-8 -*-
"""
Vision Mid-Platform Consume Stub v0 (read-only).

Hard boundaries:
- Does NOT decide/schedule/route; does NOT drive voice/memory/navigation.
- Does NOT fabricate slices or fill missing fields.
- Accepts only slices that already match the v0 schema surface.
- Does NOT add time/space anchors.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple


_REQUIRED_KEYS_V0: tuple[str, ...] = (
    "slice_id",
    "slice_type",
    "source_modules",
    "task_relevance",
    "stability",
    "confidence",
    "needs_rerecognition",
    "needs_confirmation",
    "network_allowed",
    "memory_worthy",
    "consume_priority",
    "lane",
    "can_enter_mainline",
)

_REQUIRED_CAND_KEYS_V0: tuple[str, ...] = (
    "candidate_id",
    "candidate_type",
    "source_modules",
    "upstream_slice_refs",
    "task_relevance",
    "stability",
    "confidence",
    "conflict_detected",
    "needs_rerecognition",
    "needs_confirmation",
    "network_verify_recommended",
    "memory_candidate",
    "consume_priority",
    "lane",
    "can_enter_mid_platform",
)


def _as_slice_list(slices: Any) -> List[Dict[str, Any]]:
    if slices is None:
        return []
    if isinstance(slices, dict):
        return [slices]
    if isinstance(slices, list):
        out: List[Dict[str, Any]] = []
        for x in slices:
            if isinstance(x, dict):
                out.append(x)
        return out
    return []


def _as_candidate_list(candidates: Any) -> List[Dict[str, Any]]:
    if candidates is None:
        return []
    if isinstance(candidates, dict):
        return [candidates]
    if isinstance(candidates, list):
        out: List[Dict[str, Any]] = []
        for x in candidates:
            if isinstance(x, dict):
                out.append(x)
        return out
    return []


def _is_valid_slice_v0(s: Dict[str, Any]) -> bool:
    # v0 stub: structural presence check only; no inference or coercion.
    for k in _REQUIRED_KEYS_V0:
        if k not in s:
            return False
    # Minimal type sanity (keep conservative).
    if not isinstance(s.get("source_modules"), list):
        return False
    if not isinstance(s.get("confidence"), (int, float)):
        return False
    if not isinstance(s.get("needs_rerecognition"), bool):
        return False
    if not isinstance(s.get("needs_confirmation"), bool):
        return False
    if not isinstance(s.get("network_allowed"), bool):
        return False
    if not isinstance(s.get("memory_worthy"), bool):
        return False
    if not isinstance(s.get("can_enter_mainline"), bool):
        return False
    return True


def _is_valid_candidate_v0(c: Dict[str, Any]) -> bool:
    for k in _REQUIRED_CAND_KEYS_V0:
        if k not in c:
            return False
    if not isinstance(c.get("source_modules"), list):
        return False
    if not isinstance(c.get("upstream_slice_refs"), list):
        return False
    if not isinstance(c.get("confidence"), (int, float)):
        return False
    if not isinstance(c.get("conflict_detected"), bool):
        return False
    if not isinstance(c.get("needs_rerecognition"), bool):
        return False
    if not isinstance(c.get("needs_confirmation"), bool):
        return False
    if not isinstance(c.get("network_verify_recommended"), bool):
        return False
    if not isinstance(c.get("memory_candidate"), bool):
        return False
    if not isinstance(c.get("can_enter_mid_platform"), bool):
        return False
    return True


def consume_vision_consumable_slices_stub_v0(
    *,
    slices: Any,
    candidates: Any = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, observation_dict).

    relevant-only behavior:
    - If no valid slices are provided -> (False, None)
    """
    lst = _as_slice_list(slices)
    valid: List[Dict[str, Any]] = []
    for s in lst:
        if _is_valid_slice_v0(s):
            valid.append(s)

    clst = _as_candidate_list(candidates)
    cvalid: List[Dict[str, Any]] = []
    for c in clst:
        if _is_valid_candidate_v0(c):
            cvalid.append(c)

    if (not valid) and (not cvalid):
        return False, None

    types = []
    for s in valid:
        t = str(s.get("slice_type") or "").strip()
        if t:
            types.append(t)

    # stable de-dup keep order
    types2: List[str] = []
    seen = set()
    for t in types:
        if t in seen:
            continue
        seen.add(t)
        types2.append(t)

    c_types = []
    for c in cvalid:
        ct = str(c.get("candidate_type") or "").strip()
        if ct:
            c_types.append(ct)
    c_types2: List[str] = []
    seen2 = set()
    for t in c_types:
        if t in seen2:
            continue
        seen2.add(t)
        c_types2.append(t)

    out: Dict[str, Any] = {
        "consume_attempted": True,
        "consume_scope": "vision_mid_platform_consume_stub_v0",
        "consume_mode": "read_only",
    }
    if valid:
        out["slice_count"] = len(valid)
        out["slice_types"] = types2
    if cvalid:
        out["candidate_count"] = len(cvalid)
        out["candidate_types"] = c_types2
    return True, out

