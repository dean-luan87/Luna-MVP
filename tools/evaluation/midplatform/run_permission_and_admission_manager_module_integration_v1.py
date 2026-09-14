#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Mapping


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            return parent
    return here.parents[3]


WS_ROOT = _find_ws_root()
if str(WS_ROOT) not in sys.path:
    sys.path.insert(0, str(WS_ROOT))

from capabilities.midplatform.permission_and_admission_manager.module.permission_and_admission_module_api_v1 import (
    run_permission_and_admission_manager_module_v1,
)
from capabilities.midplatform.permission_and_admission_manager.module.permission_and_admission_manager_module_types_v1 import (
    BOUNDARY_FALSE_FIELDS,
)


def _base_payload(case_id: str) -> Dict[str, Any]:
    request_type_policies = {
        "evidence_admission": {
            "evidence_required": True,
            "provenance_required": True,
            "consent_required": False,
            "ownership_required": True,
            "authority_required": True,
            "allowed_authorities": ["admission_candidate", "read_candidate"],
            "allowed_operations": ["evaluate", "review", "candidate_decide"],
            "decision_mode": "allow",
        },
        "fact_admission_candidate": {
            "evidence_required": True,
            "provenance_required": True,
            "consent_required": False,
            "ownership_required": True,
            "authority_required": True,
            "allowed_authorities": ["admission_candidate"],
            "allowed_operations": ["evaluate", "review"],
            "decision_mode": "defer",
        },
        "state_candidate_admission": {
            "evidence_required": True,
            "provenance_required": True,
            "consent_required": False,
            "ownership_required": True,
            "authority_required": True,
            "allowed_authorities": ["admission_candidate"],
            "allowed_operations": ["evaluate", "review", "candidate_decide"],
            "decision_mode": "allow",
        },
        "model_admission": {
            "evidence_required": True,
            "provenance_required": True,
            "consent_required": False,
            "ownership_required": True,
            "authority_required": True,
            "allowed_authorities": ["admission_candidate"],
            "allowed_operations": ["evaluate", "candidate_decide"],
            "decision_mode": "allow",
        },
        "skill_admission": {
            "evidence_required": True,
            "provenance_required": True,
            "consent_required": False,
            "ownership_required": True,
            "authority_required": True,
            "allowed_authorities": ["admission_candidate"],
            "allowed_operations": ["evaluate", "candidate_decide"],
            "decision_mode": "allow",
        },
        "protocol_admission": {
            "evidence_required": True,
            "provenance_required": True,
            "consent_required": False,
            "ownership_required": True,
            "authority_required": True,
            "allowed_authorities": ["admission_candidate"],
            "allowed_operations": ["evaluate", "candidate_decide"],
            "decision_mode": "allow",
        },
        "capability_admission": {
            "evidence_required": True,
            "provenance_required": True,
            "consent_required": False,
            "ownership_required": True,
            "authority_required": True,
            "allowed_authorities": ["admission_candidate"],
            "allowed_operations": ["evaluate", "candidate_decide"],
            "decision_mode": "allow",
        },
        "human_correction_admission": {
            "evidence_required": True,
            "provenance_required": True,
            "consent_required": True,
            "ownership_required": True,
            "authority_required": True,
            "allowed_authorities": ["admission_candidate"],
            "allowed_operations": ["evaluate", "candidate_decide"],
            "decision_mode": "allow",
        },
        "action_candidate_admission": {
            "evidence_required": True,
            "provenance_required": True,
            "consent_required": False,
            "ownership_required": True,
            "authority_required": True,
            "allowed_authorities": ["admission_candidate"],
            "allowed_operations": ["evaluate", "candidate_decide"],
            "decision_mode": "allow",
        },
        "runtime_access_admission": {
            "evidence_required": True,
            "provenance_required": True,
            "consent_required": True,
            "ownership_required": True,
            "authority_required": True,
            "allowed_authorities": ["admission_candidate"],
            "allowed_operations": ["evaluate", "review", "candidate_decide"],
            "decision_mode": "allow",
        },
    }

    return {
        "request_id": f"pam_req_{case_id}",
        "request_type": "evidence_admission",
        "subject_ref": "subject_a",
        "resource_ref": "resource_x",
        "source_ref": f"source_{case_id}",
        "owner_ref": "subject_a",
        "consent_ref": {"status": "granted"},
        "evidence_refs": [f"evidence_{case_id}"],
        "provenance_refs": [f"provenance_{case_id}"],
        "requested_authority": "admission_candidate",
        "requested_operation": "evaluate",
        "policy_snapshot": {"request_type_policies": request_type_policies},
        "version_snapshot": {"schema": "v1"},
        "temporal_snapshot": {"revoked": False, "expired": False},
        "risk_context": {"risk_level": "low"},
        "trace_ref": f"trace_in_{case_id}",
    }


def _boundary_preserved(result: Mapping[str, Any]) -> bool:
    return all(result.get(field) is False for field in BOUNDARY_FALSE_FIELDS)


def run_integration() -> Dict[str, Any]:
    scenarios: Dict[str, Dict[str, Any]] = {}

    scenarios["valid_evidence_admission"] = _base_payload("valid_evidence_admission")

    valid_model = _base_payload("valid_model_admission_candidate")
    valid_model["request_type"] = "model_admission"
    scenarios["valid_model_admission_candidate"] = valid_model

    valid_protocol = _base_payload("valid_protocol_admission_candidate")
    valid_protocol["request_type"] = "protocol_admission"
    scenarios["valid_protocol_admission_candidate"] = valid_protocol

    valid_capability = _base_payload("valid_capability_admission_candidate")
    valid_capability["request_type"] = "capability_admission"
    scenarios["valid_capability_admission_candidate"] = valid_capability

    missing_request_id = _base_payload("missing_request_id")
    missing_request_id["request_id"] = ""
    scenarios["missing_request_id"] = missing_request_id

    missing_request_type = _base_payload("missing_request_type")
    missing_request_type["request_type"] = ""
    scenarios["missing_request_type"] = missing_request_type

    unknown_request_type = _base_payload("unknown_request_type")
    unknown_request_type["request_type"] = "unknown_admission"
    scenarios["unknown_request_type"] = unknown_request_type

    missing_subject = _base_payload("missing_subject")
    missing_subject["subject_ref"] = ""
    scenarios["missing_subject"] = missing_subject

    missing_resource = _base_payload("missing_resource")
    missing_resource["resource_ref"] = ""
    scenarios["missing_resource"] = missing_resource

    evidence_insufficient = _base_payload("evidence_insufficient")
    evidence_insufficient["evidence_refs"] = []
    scenarios["evidence_insufficient"] = evidence_insufficient

    provenance_invalid = _base_payload("provenance_invalid")
    provenance_invalid["risk_context"] = {"provenance_invalid": True}
    scenarios["provenance_invalid"] = provenance_invalid

    consent_required = _base_payload("consent_required")
    consent_required["request_type"] = "human_correction_admission"
    consent_required["consent_ref"] = None
    scenarios["consent_required"] = consent_required

    consent_denied = _base_payload("consent_denied")
    consent_denied["request_type"] = "human_correction_admission"
    consent_denied["consent_ref"] = {"status": "denied"}
    scenarios["consent_denied"] = consent_denied

    ownership_unresolved = _base_payload("ownership_unresolved")
    ownership_unresolved["owner_ref"] = ""
    scenarios["ownership_unresolved"] = ownership_unresolved

    ownership_denied = _base_payload("ownership_denied")
    ownership_denied["owner_ref"] = "subject_b"
    scenarios["ownership_denied"] = ownership_denied

    authority_insufficient = _base_payload("authority_insufficient")
    authority_insufficient["requested_authority"] = "runtime_execute"
    scenarios["authority_insufficient"] = authority_insufficient

    runtime_boundary_blocked = _base_payload("runtime_boundary_blocked")
    runtime_boundary_blocked["risk_context"] = {"runtime_boundary_blocked": True}
    scenarios["runtime_boundary_blocked"] = runtime_boundary_blocked

    risk_blocked = _base_payload("risk_blocked")
    risk_blocked["risk_context"] = {"risk_level": "high", "risk_blocked": True}
    scenarios["risk_blocked"] = risk_blocked

    conflict_unresolved = _base_payload("conflict_unresolved")
    conflict_unresolved["risk_context"] = {
        "conflict_unresolved": True,
        "conflict_count": 2,
    }
    scenarios["conflict_unresolved"] = conflict_unresolved

    revoked_or_expired = _base_payload("revoked_or_expired")
    revoked_or_expired["temporal_snapshot"] = {
        "revoked": True,
        "expired": False,
        "revocation_reason": "policy_revoked",
    }
    scenarios["revoked_or_expired"] = revoked_or_expired

    expected_status = {
        "valid_evidence_admission": "admission_candidate_ready",
        "valid_model_admission_candidate": "admission_candidate_ready",
        "valid_protocol_admission_candidate": "admission_candidate_ready",
        "valid_capability_admission_candidate": "admission_candidate_ready",
        "missing_request_id": "invalid_input",
        "missing_request_type": "invalid_input",
        "unknown_request_type": "invalid_input",
        "missing_subject": "invalid_input",
        "missing_resource": "invalid_input",
        "evidence_insufficient": "evidence_insufficient",
        "provenance_invalid": "provenance_invalid",
        "consent_required": "consent_required",
        "consent_denied": "consent_denied",
        "ownership_unresolved": "ownership_unresolved",
        "ownership_denied": "ownership_denied",
        "authority_insufficient": "authority_insufficient",
        "runtime_boundary_blocked": "boundary_blocked",
        "risk_blocked": "risk_blocked",
        "conflict_unresolved": "conflict_unresolved",
        "revoked_or_expired": "revoked",
    }

    rows = []
    failed_cases = []
    trace_present_all = True
    replay_present_all = True
    diagnostics_present_all = True
    boundary_preserved = True
    deterministic_replay = True
    unhandled_exceptions = 0

    for case_id, payload in scenarios.items():
        try:
            result = run_permission_and_admission_manager_module_v1(payload)
            module_status = str(result.get("module_status") or "")
        except Exception:  # noqa: BLE001
            result = {}
            module_status = "exception"
            unhandled_exceptions += 1

        if not result.get("trace_ref"):
            trace_present_all = False
        if not result.get("replay_key"):
            replay_present_all = False
        if not isinstance(result.get("diagnostics"), dict):
            diagnostics_present_all = False
        if not _boundary_preserved(result):
            boundary_preserved = False

        case_pass = module_status == expected_status[case_id]
        case_pass = case_pass and isinstance(
            result.get("admission_decision_candidate"), dict
        )
        case_pass = case_pass and isinstance(result.get("diagnostics"), dict)
        case_pass = (
            case_pass
            and bool(result.get("trace_ref"))
            and bool(result.get("replay_key"))
        )
        case_pass = case_pass and _boundary_preserved(result)

        if case_id == "valid_evidence_admission":
            repeat = run_permission_and_admission_manager_module_v1(payload)
            deterministic_replay = deterministic_replay and (
                result.get("trace_ref") == repeat.get("trace_ref")
                and result.get("replay_key") == repeat.get("replay_key")
                and result.get("module_status") == repeat.get("module_status")
            )

        if not case_pass:
            failed_cases.append(case_id)

        rows.append(
            {
                "case_id": case_id,
                "expected_status": expected_status[case_id],
                "module_status": module_status,
                "passed": case_pass,
                "trace_ref": result.get("trace_ref"),
                "replay_key": result.get("replay_key"),
            }
        )

    total_cases = len(scenarios)
    passed_cases = total_cases - len(failed_cases)

    return {
        "phase": "Phase-Luna-Permission-And-Admission-Manager-Functional-Module-Consolidation-And-Integration-v1-001",
        "total_cases": total_cases,
        "passed_cases": passed_cases,
        "failed_cases": failed_cases,
        "deterministic_replay": deterministic_replay,
        "diagnostics_present_all": diagnostics_present_all,
        "trace_present_all": trace_present_all,
        "replay_present_all": replay_present_all,
        "boundary_preserved": boundary_preserved,
        "unhandled_exceptions": unhandled_exceptions,
        "rows": rows,
        "integration_pass": passed_cases == total_cases
        and failed_cases == []
        and deterministic_replay
        and diagnostics_present_all
        and trace_present_all
        and replay_present_all
        and boundary_preserved
        and unhandled_exceptions == 0,
    }


def main() -> int:
    report = run_integration()
    output_root = Path(
        "_tmp_eval_out/permission_and_admission_manager_module_integration_v1_smoke_v0"
    ).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    output_path = (
        output_root / "permission_and_admission_manager_module_integration_v1.json"
    )
    output_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "integration_pass": report["integration_pass"],
                "total_cases": report["total_cases"],
                "passed_cases": report["passed_cases"],
                "failed_cases": report["failed_cases"],
                "deterministic_replay": report["deterministic_replay"],
                "diagnostics_present_all": report["diagnostics_present_all"],
                "trace_present_all": report["trace_present_all"],
                "replay_present_all": report["replay_present_all"],
                "boundary_preserved": report["boundary_preserved"],
                "unhandled_exceptions": report["unhandled_exceptions"],
                "output": str(output_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if report["integration_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
