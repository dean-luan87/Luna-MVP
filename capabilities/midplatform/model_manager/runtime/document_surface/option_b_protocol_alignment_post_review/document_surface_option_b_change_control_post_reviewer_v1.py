# -*- coding: utf-8 -*-
"""Document Surface — Option B change control post-reviewer v1."""

from __future__ import annotations

from typing import Any, Dict

import json
from pathlib import Path


def review_change_control(*, change_results: Dict[str, Any], repo_root: Path) -> Dict[str, Any]:
    chain_path = repo_root / "capabilities/midplatform/protocols/region_intelligence_protocol_chain_v1.json"
    chain_ok = False
    if chain_path.is_file():
        chain = json.loads(chain_path.read_text(encoding="utf-8"))
        refs = [p.get("protocol_ref") for p in chain.get("legacy_protocols_required") or []]
        chain_ok = "LUNA-PROTO-L1-MODEL-SKILL-ADMISSION-CONTRACT-V1" in refs
    checks = {
        "dryrun_reviewable": change_results.get("protocol_alignment_dryrun_reviewable") is True,
        "freeze_respected": change_results.get("freeze_boundary_respected") is True,
        "protocol_chain_consistent": chain_ok,
        "no_production_registry": change_results.get("no_production_registry_update") is True,
    }
    failed = [k for k, v in checks.items() if not v]
    return {
        "review_id": "option_b_change_control_post_review",
        "passed": len(failed) == 0,
        "review_passed_count": sum(1 for v in checks.values() if v),
        "review_failed_count": len(failed),
        "checks": checks,
        "failed_checks": failed,
        "change_control_status": "post_review_only",
        "candidate_only": True,
        "not_fact": True,
    }
