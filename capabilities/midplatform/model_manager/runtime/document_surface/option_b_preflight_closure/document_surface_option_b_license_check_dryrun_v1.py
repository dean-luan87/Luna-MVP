# -*- coding: utf-8 -*-
"""License check dryrun."""

from __future__ import annotations

from typing import Any, Dict


def run_license_check_dryrun(*, fixture: Dict[str, Any], run_id: str) -> Dict[str, Any]:
    lic = fixture.get("license_status_candidate", "")
    ok = lic in ("clear", "clear_candidate")
    status = "license_cleared_candidate" if ok else "license_not_cleared_candidate"
    return {
        "model_candidate_id": fixture["model_candidate_id"],
        "license_check_candidate": status,
        "license_status_candidate": status,
        "abort_reason": None if ok else "license_unknown",
        "preflight_run_id": run_id,
        "candidate_only": True,
        "not_fact": True,
    }
