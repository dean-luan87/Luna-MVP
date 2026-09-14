# -*- coding: utf-8 -*-
"""Luna Document Surface — Option B admission planning processor v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from capabilities.midplatform.model_manager.runtime.document_surface.option_b_admission_planning.document_surface_option_b_admission_planning_adapter_v1 import (
    PLAN_DIR,
    run_option_b_admission_planning,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_admission_planning.document_surface_option_b_model_candidate_types_v1 import (
    build_option_b_candidate_family_evaluation,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_admission_planning.document_surface_option_b_output_contract_compatibility_v1 import (
    build_output_contract_compatibility,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_admission_planning.document_surface_option_b_preflight_requirements_v1 import (
    build_preflight_requirements,
)


def _load(root: Path, name: str) -> Dict[str, Any]:
    p = root / PLAN_DIR / name
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}


def run_processor() -> Dict[str, Any]:
    return run_option_b_admission_planning(write_outputs=False)


def run_case_a() -> Dict[str, Any]:
    f = build_option_b_candidate_family_evaluation()
    return {
        "abcd": f.get("all_families_abcd_evaluated") is True,
        "no_active": f.get("no_active_model_selected") is True,
        "no_exec": f.get("no_download_install_execution") is True,
    }


def run_case_b() -> Dict[str, Any]:
    r = run_option_b_admission_planning(write_outputs=False)
    rev = r.get("registry_review") or {}
    return {
        "schema": rev.get("schema_complete") is True,
        "active_false": rev.get("active_status_default_false") is True,
        "preflight": rev.get("preflight_required") is True,
        "controlled": rev.get("controlled_execution_required") is True,
    }


def run_case_c() -> Dict[str, Any]:
    d = run_option_b_admission_planning(write_outputs=False).get("dependency_policy") or {}
    return {
        "install": d.get("install_allowed") is False,
        "download": d.get("download_allowed") is False,
        "exec": d.get("execution_allowed") is False,
        "silent": d.get("no_silent_install") is True and d.get("no_silent_download") is True,
    }


def run_case_d() -> Dict[str, Any]:
    lp = run_option_b_admission_planning(write_outputs=False).get("license_policy") or {}
    blocks = lp.get("block_conditions") or []
    return {
        "count": len(blocks) >= 8,
        "has_next_action": all(b.get("next_action") for b in blocks),
        "has_forbidden": all(b.get("forbidden_workaround") for b in blocks),
    }


def run_case_e() -> Dict[str, Any]:
    c = build_output_contract_compatibility()
    return {
        "allowed": len(c.get("allowed_output_types") or []) >= 6,
        "forbidden": "caption" in (c.get("forbidden_output_types") or []),
        "wrapper": c.get("caption_text_semantic_blocked_or_wrapper") is True,
    }


def run_case_f() -> Dict[str, Any]:
    p = build_preflight_requirements()
    return {
        "complete": p.get("all_checks_required") is True,
        "skip_forbidden": p.get("preflight_skip_forbidden") is True,
    }


def run_case_g() -> Dict[str, Any]:
    a = run_option_b_admission_planning(write_outputs=False).get("abort_rollback") or {}
    rb = a.get("rollback_policy") or {}
    return {
        "abort_count": len(a.get("abort_conditions") or []) >= 12,
        "no_registry": rb.get("no_active_registry_update") is True,
        "no_ocr_fallback": rb.get("no_fallback_to_ocr_vlm_layout") is True,
    }


def run_case_h() -> Dict[str, Any]:
    r = run_option_b_admission_planning(write_outputs=False)
    return {
        "protocol": r.get("protocol_compliance_check") == "required",
        "chain": r.get("existing_midplatform_protocol_chain_extension") is True,
        "branch": r.get("protocol_patch_not_new_branch") is True,
        "co": r.get("candidate_only") is True,
        "nf": r.get("not_fact") is True,
    }
