# -*- coding: utf-8 -*-
"""
Resource Sufficiency Gate v0 (metadata-driven, pre-submit admission).

Hard constraints:
- Must NOT fabricate resource facts.
- Must ONLY consume runtime_context.metadata["resource_status_v0"] when present.
- When resource_status_v0 is missing, gate must not block the mainline.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

from capabilities.voice.schemas.voice_runtime_context import VoiceRuntimeContext


def evaluate_resource_status_v0(
    runtime_context: Optional[VoiceRuntimeContext],
) -> Tuple[bool, bool, str]:
    """
    Returns: (present, passed, reason)
    - present: resource_status_v0 exists and is a dict
    - passed: battery_ok and required_modules_ok are both True
    - reason:
        - "" when not present
        - "ok" when passed
        - "battery_insufficient" or "required_modules_unavailable" or "battery_and_modules" when failed
    """
    if runtime_context is None:
        return False, True, ""
    md = getattr(runtime_context, "metadata", None)
    if not isinstance(md, dict):
        return False, True, ""
    rs = md.get("resource_status_v0")
    if not isinstance(rs, dict):
        return False, True, ""

    def _b(v: Any) -> Optional[bool]:
        if isinstance(v, bool):
            return v
        return None

    battery_ok = _b(rs.get("battery_ok"))
    modules_ok = _b(rs.get("required_modules_ok"))

    # Missing fields are treated as "unknown" -> do not block v0.
    if battery_ok is None or modules_ok is None:
        return True, True, "ok"

    if battery_ok and modules_ok:
        return True, True, "ok"
    if (not battery_ok) and (not modules_ok):
        return True, False, "battery_and_modules"
    if not battery_ok:
        return True, False, "battery_insufficient"
    return True, False, "required_modules_unavailable"

