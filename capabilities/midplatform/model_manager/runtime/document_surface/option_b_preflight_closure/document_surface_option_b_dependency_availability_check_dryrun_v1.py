# -*- coding: utf-8 -*-
"""Dependency availability check dryrun."""

from __future__ import annotations

from typing import Any, Dict


def run_dependency_availability_check_dryrun(*, fixture: Dict[str, Any], run_id: str) -> Dict[str, Any]:
    dep = fixture.get("dependency_profile") or {}
    ok = dep.get("controlled", dep.get("type") in ("python_builtin_or_existing", "declared_only"))
    status = "dependency_available_candidate" if ok else "dependency_missing_or_uncontrolled_candidate"
    return {
        "model_candidate_id": fixture["model_candidate_id"],
        "dependency_availability_check_candidate": status,
        "dependency_status_candidate": status,
        "install_performed": False,
        "download_performed": False,
        "import_performed": False,
        "abort_reason": None if ok else "dependency_missing",
        "preflight_run_id": run_id,
        "candidate_only": True,
        "not_fact": True,
    }
