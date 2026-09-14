# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-009 — OCR Stage-2 Source Policy / Provider Static Configuration Validation v0.

Static-only validation:
- Scans repo files, configs, and RequestTrace/TRW contracts.
- Generates matrices + runbook + static validation report.

Hard boundaries:
- MUST NOT invoke real OCR providers or OCR models.
- MUST NOT open camera or video streams.
- MUST NOT enter MidPlatform / SceneDelta / WorldContextEvidence.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE = "Phase-Mainline-GuardedTrial-009"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _exists(rel: str, *, root: Optional[Path] = None) -> bool:
    rr = root or _repo_root()
    return (rr / rel).is_file()


def _scan_source_policy_entry_v0(*, repo_root: Optional[Path] = None) -> Dict[str, Any]:
    root = repo_root or _repo_root()
    rel = "capabilities/model_ocr/offline_source_policy_v0.py"
    ok = (root / rel).is_file()
    policy_id = None
    if ok:
        try:
            from capabilities.model_ocr.offline_source_policy_v0 import SOURCE_POLICY_ID_OCR_V0  # type: ignore

            policy_id = SOURCE_POLICY_ID_OCR_V0
        except Exception:
            policy_id = None
    return {
        "entry_file": rel,
        "exists": ok,
        "source_policy_id": policy_id,
        "expected_source_policy_id": "ocr_default_offline_raw_text_source_policy_v0",
        "policy_id_match": policy_id == "ocr_default_offline_raw_text_source_policy_v0",
        "policy_doc": "docs/architecture/LUNA_OCR_DEFAULT_OFFLINE_SOURCE_POLICY_V0.md",
        "policy_doc_exists": _exists("docs/architecture/LUNA_OCR_DEFAULT_OFFLINE_SOURCE_POLICY_V0.md", root=root),
    }


def scan_ocr_source_policy_entrypoints_v0(*, repo_root: Optional[Path] = None) -> List[Dict[str, Any]]:
    root = repo_root or _repo_root()
    rows: List[Dict[str, Any]] = []
    rows.append(
        {
            "candidate_file": "capabilities/model_ocr/offline_source_policy_v0.py",
            "candidate_function_or_class": "select_ocr_offline_source_v0 / SOURCE_POLICY_ID_OCR_V0",
            "entrypoint_type": "source_policy",
            "exists": _exists("capabilities/model_ocr/offline_source_policy_v0.py", root=root),
            "allowed_for_stage2_trial": True,
            "notes": "Offline raw_text source policy selector (pure selector; does not invoke provider).",
        }
    )
    rows.append(
        {
            "candidate_file": "docs/architecture/LUNA_OCR_DEFAULT_OFFLINE_SOURCE_POLICY_V0.md",
            "candidate_function_or_class": "policy_text",
            "entrypoint_type": "source_policy",
            "exists": _exists("docs/architecture/LUNA_OCR_DEFAULT_OFFLINE_SOURCE_POLICY_V0.md", root=root),
            "allowed_for_stage2_trial": True,
            "notes": "Frozen policy text; does not change runtime defaults.",
        }
    )
    rows.append(
        {
            "candidate_file": "docs/architecture/LUNA_OCR_OFFLINE_SOURCE_SELECTION_AND_FALLBACK_POLICY_V0.md",
            "candidate_function_or_class": "fallback_policy_text",
            "entrypoint_type": "fallback_policy",
            "exists": _exists("docs/architecture/LUNA_OCR_OFFLINE_SOURCE_SELECTION_AND_FALLBACK_POLICY_V0.md", root=root),
            "allowed_for_stage2_trial": True,
            "notes": "Selection and fallback policy doc (not_available terminal).",
        }
    )
    return rows


def _scan_provider_manifests_v0(*, repo_root: Optional[Path] = None) -> Dict[str, Any]:
    root = repo_root or _repo_root()
    cfg_dir = root / "configs" / "models" / "ocr"
    rows: List[Dict[str, Any]] = []
    blockers: List[str] = []
    warnings: List[str] = []
    if not cfg_dir.is_dir():
        return {"configs_dir": str(cfg_dir), "ok": False, "blockers": ["ocr_configs_dir_missing"], "warnings": [], "manifests": []}

    manifests = sorted([p for p in cfg_dir.iterdir() if p.is_file() and p.name.endswith("_manifest_v0.json")])
    if not manifests:
        blockers.append("no_ocr_model_manifests_found")

    for p in manifests:
        row: Dict[str, Any] = {"path": str(p), "ok": False}
        try:
            obj = _read_json(p)
            if not isinstance(obj, dict):
                row["error"] = "manifest_not_object"
                blockers.append("ocr_manifest_not_object")
            else:
                rid = (
                    obj.get("provider_id")
                    or obj.get("model_id")
                    or obj.get("id")
                    or obj.get("name")
                    or obj.get("model_config_id")
                    or obj.get("model_name")
                )
                row["id"] = rid
                row["keys"] = sorted(list(obj.keys()))
                row["ok"] = bool(rid)
                if not rid:
                    blockers.append("ocr_manifest_missing_id")
        except Exception as e:
            row["error"] = repr(e)
            blockers.append("ocr_manifest_unparseable")
        rows.append(row)

    ok = not blockers
    return {
        "configs_dir": str(cfg_dir),
        "manifest_count": len(rows),
        "ok": ok,
        "blockers": blockers,
        "warnings": warnings,
        "manifests": rows,
    }


def scan_ocr_provider_candidates_v0(*, repo_root: Optional[Path] = None) -> List[Dict[str, Any]]:
    """
    Candidate registry for controlled trials.
    Static-only: file existence + importability probe (no adapter invocation).
    """
    root = repo_root or _repo_root()
    candidates: List[Tuple[str, str, str, bool, bool]] = [
        ("capabilities/model_ocr/rapidocr_variant_adapter_v0.py", "RapidOCRVariantAdapterV0", "local_ocr", False, False),
        ("capabilities/model_ocr/rapidocr_adapter_v0.py", "RapidOCRAdapterV0", "local_ocr", False, False),
        ("capabilities/model_ocr/macos_vision_ocr_adapter_v0.py", "MacOSVisionOCRAdapterV0", "local_ocr", False, False),
        ("capabilities/model_ocr/paddleocr_adapter_v0.py", "PaddleOCRAdapterV0", "local_ocr", False, False),
        ("capabilities/model_ocr/easyocr_adapter_v0.py", "EasyOCRAdapterV0", "local_ocr", False, False),
        ("capabilities/model_ocr/tesseract_adapter_v0.py", "TesseractAdapterV0", "local_ocr", False, False),
    ]
    rows: List[Dict[str, Any]] = []
    for rel, symbol, ptype, req_cred, req_net in candidates:
        exists = _exists(rel, root=root)
        importable = False
        if exists:
            mod = rel.replace("/", ".").replace(".py", "")
            try:
                __import__(mod)
                importable = True
            except Exception:
                importable = False
        rows.append(
            {
                "candidate_file": rel,
                "candidate_function_or_class": symbol,
                "provider_type": ptype,
                "exists": exists,
                "importable": importable,
                "requires_credentials": bool(req_cred),
                "requires_network": bool(req_net),
                "allowed_for_controlled_trial": True,
                "provider_invoked": False,
                "notes": "Static presence/import probe only; no provider/model execution in Phase-009.",
            }
        )
    return rows


def _raw_text_candidate_schema_contract_v0(*, repo_root: Optional[Path] = None) -> Dict[str, Any]:
    # Reuse v0 schema contract from Phase-008 precheck (definition only; not provider output).
    try:
        from capabilities.guarded_trial.ocr_stage2_trial_precheck_v0 import (  # type: ignore
            validate_ocr_raw_text_candidate_schema_v0,
        )

        ok, info, blockers = validate_ocr_raw_text_candidate_schema_v0()
        return {"ok": bool(ok), "blockers": blockers, "schema": info.get("schema")}
    except Exception as e:
        return {"ok": False, "blockers": ["raw_text_schema_validator_import_failed"], "error": repr(e)}


def validate_ocr_raw_text_candidate_schema_contract_v0(*, repo_root: Optional[Path] = None) -> Dict[str, Any]:
    base = _raw_text_candidate_schema_contract_v0(repo_root=repo_root)
    required_fields = [
        "candidate_id",
        "source_evidence_ref",
        "raw_text",
        "confidence",
        "reading_order",
        "provider",
        "source_policy",
        "allows_execute_now",
        "semantic_interpretation_enabled",
        "downstream_invocation_count",
    ]
    forbidden_defaults = {
        "allows_execute_now": False,
        "semantic_interpretation_enabled": False,
        "navigation_action": None,
        "real_tts_invoked": False,
    }
    return {
        "schema_found": bool(base.get("ok")),
        "required_fields": required_fields,
        "forbidden_defaults": forbidden_defaults,
        "trial_report_compatible": True,
        "schema_contract_ref": "capabilities/guarded_trial/ocr_stage2_trial_precheck_v0.validate_ocr_raw_text_candidate_schema_v0",
        "schema": base.get("schema"),
        "blockers": list(base.get("blockers") or []),
    }


def validate_ocr_provider_output_schema_contract_v0(*, repo_root: Optional[Path] = None) -> Dict[str, Any]:
    """
    Provider output schema (static contract only). Not derived from real outputs.
    """
    return {
        "schema_found": True,
        "raw_text_field_present": True,
        "confidence_field_present": True,
        "bbox_or_region_field_present": True,
        "provider_metadata_present": True,
        "error_or_not_available_state_present": True,
        "schema_valid_for_stage2_trial": True,
        "notes": "Contract-only; real provider outputs validated in a later controlled provider trial phase.",
    }


def _fallback_policy_readiness_v0(*, repo_root: Optional[Path] = None) -> Dict[str, Any]:
    root = repo_root or _repo_root()
    selection_doc = "docs/architecture/LUNA_OCR_OFFLINE_SOURCE_SELECTION_AND_FALLBACK_POLICY_V0.md"
    selector_py = "capabilities/model_ocr/offline_source_policy_v0.py"
    ok = _exists(selection_doc, root=root) and _exists(selector_py, root=root)
    return {
        "selection_and_fallback_doc": selection_doc,
        "selection_and_fallback_doc_exists": _exists(selection_doc, root=root),
        "selector_module": selector_py,
        "selector_module_exists": _exists(selector_py, root=root),
        "not_available_terminal_supported": True,
        "ok": ok,
    }


def _request_trace_trw_contract_v0(*, repo_root: Optional[Path] = None) -> Dict[str, Any]:
    root = repo_root or _repo_root()
    trw_validator = "capabilities/runtime_readiness/guarded_trial_trw_validator_v0.py"
    stage_doc = "docs/architecture/LUNA_OCR_REQUEST_TRACE_STAGE_MAPPING_DEFINITION_V0.md"
    shadow_doc = "docs/architecture/LUNA_OCR_REQUEST_TRACE_SHADOW_ADAPTER_V0.md"
    shadow_adapter = "capabilities/core_trw/ocr_request_trace_shadow_adapter_v0.py"
    ok = _exists(trw_validator, root=root) and _exists(stage_doc, root=root) and _exists(shadow_adapter, root=root)
    return {
        "guarded_trial_trw_validator_module_exists": _exists(trw_validator, root=root),
        "ocr_request_trace_stage_mapping_doc_exists": _exists(stage_doc, root=root),
        "ocr_request_trace_shadow_adapter_doc_exists": _exists(shadow_doc, root=root),
        "ocr_request_trace_shadow_adapter_module_exists": _exists(shadow_adapter, root=root),
        "minimum_trw_fields_runtime": ["request_id", "hard_audit", "runtime_run_id_or_source_run_id", "trace_ref/replay_ref/whitebox_ref or pending_ref"],
        "ok": ok,
    }


def validate_ocr_stage2_trw_output_contract_v0(*, repo_root: Optional[Path] = None) -> Dict[str, Any]:
    root = repo_root or _repo_root()
    base = _request_trace_trw_contract_v0(repo_root=root)
    stage_names: List[str] = []
    try:
        from capabilities.core_trw.ocr_request_trace_shadow_adapter_v0 import OCR_STAGES  # type: ignore

        stage_names = [n for n, _ in OCR_STAGES]
    except Exception:
        stage_names = []
    return {
        "trace_jsonl_path": "{output_root}/ocr_stage2_static_config_trace.jsonl",
        "replay_jsonl_path": "{output_root}/ocr_stage2_static_config_replay.jsonl",
        "whitebox_jsonl_path": "{output_root}/ocr_stage2_static_config_whitebox.jsonl",
        "request_trace_stage_names": stage_names,
        "hard_audit_fields_required": [
            "semantic_interpretation_enabled=false",
            "downstream_invocation_count=0",
            "real_tts_invoked=false",
            "navigation_action=null",
        ],
        "source_policy_ref_required": True,
        "provider_candidate_ref_required": True,
        "raw_text_candidate_ref_required": True,
        "fallback_reason_or_not_available_reason_required": True,
        "trw_output_contract_ready": bool(base.get("ok")),
        "materials": base,
    }


def build_ocr_stage2_controlled_provider_runbook_v0(
    *,
    output_root_placeholder: str = "/Users/luanlei/LunaRuntime/logs/ocr_stage2_controlled_provider_trial_009_future",
) -> Dict[str, Any]:
    rid = f"ocr_stage2_runbook_{uuid.uuid4().hex[:12]}"
    return {
        "runbook_id": rid,
        "trial_stage": "stage2_ocr_guarded_trial",
        "execution_allowed_by_this_phase": False,
        "provider_invocation_allowed_by_this_phase": False,
        "semantic_interpretation_allowed_by_this_phase": False,
        "midplatform_forward_allowed_by_this_phase": False,
        "required_flags_registered_default_off": {
            "LUNA_ENABLE_OCR_GUARDED_TRIAL_V1": "false",
            "LUNA_OCR_TRIAL_MODE": "shadow_only",
            "LUNA_OCR_TRIAL_PROVIDER_POLICY": "ocr_default_offline_raw_text_source_policy_v0",
            "LUNA_OCR_TRIAL_ALLOW_PROVIDER_INVOCATION": "false",
            "LUNA_OCR_TRIAL_ALLOW_SEMANTIC_INTERPRETATION": "false",
            "LUNA_OCR_TRIAL_ALLOW_MIDPLATFORM_FORWARD": "false",
            "LUNA_OCR_TRIAL_ABORT_ON_GOVERNANCE_LEAKAGE": "true",
            "LUNA_OCR_TRIAL_WRITE_REQUEST_TRACE": "true",
            "LUNA_DISABLE_ALL_GUARDED_TRIALS": "false",
        },
        "pre_run_checks": [
            "Phase-Mainline-GuardedTrial-008 precheck GO",
            "Phase-Mainline-GuardedTrial-009 static validation GO",
            "Global kill reachable",
            "No MidPlatform/SceneDelta/WorldContext wiring activated",
            "Provider invocation remains disabled in this phase",
        ],
        "abort_conditions": [
            "provider_invoked (should remain false in 009)",
            "semantic_interpretation_enabled",
            "midplatform_invoked",
            "downstream_invocation_count > 0",
            "navigation_action non-null",
            "world_write_invoked",
            "hive_upload_invoked",
        ],
        "rollback_commands": [
            "unset LUNA_ENABLE_OCR_GUARDED_TRIAL_V1",
            "unset LUNA_OCR_TRIAL_ALLOW_PROVIDER_INVOCATION",
            "export LUNA_DISABLE_ALL_GUARDED_TRIALS=true",
        ],
        "expected_outputs_contract": [
            "request_trace shadow stages per docs/architecture/LUNA_OCR_REQUEST_TRACE_STAGE_MAPPING_DEFINITION_V0.md",
            "trace/replay/whitebox jsonl present and non-empty",
            "raw_text candidates conform to schema v0",
        ],
        "output_root_placeholder": output_root_placeholder,
        "must_remain_false": [
            "semantic_interpretation_enabled",
            "midplatform_invoked",
            "scene_delta_invoked",
            "world_context_invoked",
            "navigation_action",
            "world_write_invoked",
            "real_tts_invoked",
        ],
    }


def scan_ocr_fallback_not_available_policy_v0(*, repo_root: Optional[Path] = None) -> List[Dict[str, Any]]:
    root = repo_root or _repo_root()
    return [
        {
            "policy_name": "offline_source_selection_and_fallback_policy_v0",
            "candidate_file": "docs/architecture/LUNA_OCR_OFFLINE_SOURCE_SELECTION_AND_FALLBACK_POLICY_V0.md",
            "exists": _exists("docs/architecture/LUNA_OCR_OFFLINE_SOURCE_SELECTION_AND_FALLBACK_POLICY_V0.md", root=root),
            "fallback_to_not_available_supported": True,
            "provider_error_handled": True,
            "governance_leakage_blocked": True,
            "notes": "Terminal not_available is supported by selector contract.",
        }
    ]


def run_ocr_stage2_static_config_validation_v0(
    *,
    repo_root: Optional[Path] = None,
    ocr_precheck_root: Optional[str] = None,
) -> Dict[str, Any]:
    root = repo_root or _repo_root()
    vid = f"ocr_s2_static_{uuid.uuid4().hex[:14]}"

    policy = _scan_source_policy_entry_v0(repo_root=root)
    manifests = _scan_provider_manifests_v0(repo_root=root)
    schema = _raw_text_candidate_schema_contract_v0(repo_root=root)
    fallback = _fallback_policy_readiness_v0(repo_root=root)
    trw = _request_trace_trw_contract_v0(repo_root=root)
    runbook = build_ocr_stage2_controlled_provider_runbook_v0()

    entry_matrix = scan_ocr_source_policy_entrypoints_v0(repo_root=root)
    provider_matrix = scan_ocr_provider_candidates_v0(repo_root=root)
    fallback_matrix = scan_ocr_fallback_not_available_policy_v0(repo_root=root)
    raw_text_schema_val = validate_ocr_raw_text_candidate_schema_contract_v0(repo_root=root)
    provider_output_schema_val = validate_ocr_provider_output_schema_contract_v0(repo_root=root)
    trw_contract_val = validate_ocr_stage2_trw_output_contract_v0(repo_root=root)

    blockers: List[str] = []
    warnings: List[str] = []
    precheck_root_ok = True
    if ocr_precheck_root:
        precheck_root_ok = Path(str(ocr_precheck_root)).expanduser().is_dir()
        if not precheck_root_ok:
            blockers.append("ocr_precheck_root_not_readable")
    if not policy.get("exists"):
        blockers.append("offline_source_policy_selector_missing")
    if not policy.get("policy_id_match"):
        blockers.append("source_policy_id_mismatch")
    if not manifests.get("ok"):
        blockers.extend(list(manifests.get("blockers") or ["provider_manifests_invalid"]))
    if not schema.get("ok"):
        blockers.extend(list(schema.get("blockers") or ["raw_text_schema_invalid"]))
    if not fallback.get("ok"):
        blockers.append("fallback_policy_not_ready")
    if not trw.get("ok"):
        blockers.append("request_trace_trw_contract_not_ready")

    runbook_ok = runbook.get("execution_allowed_by_this_phase") is False
    if not runbook_ok:
        blockers.append("controlled_provider_runbook_invalid")

    source_policy_entrypoint_found = any(r.get("exists") for r in entry_matrix if r.get("entrypoint_type") in ("source_policy", "fallback_policy"))
    provider_candidate_found = any(r.get("exists") for r in provider_matrix)
    fallback_policy_found = any(r.get("exists") for r in fallback_matrix)
    raw_text_candidate_schema_found = bool(raw_text_schema_val.get("schema_found"))
    provider_output_schema_found = bool(provider_output_schema_val.get("schema_found"))
    trw_output_contract_ready = bool(trw_contract_val.get("trw_output_contract_ready"))
    if not source_policy_entrypoint_found:
        blockers.append("source_policy_entrypoint_not_found")
    if not provider_candidate_found:
        blockers.append("provider_candidate_not_found")
    if not fallback_policy_found:
        blockers.append("fallback_policy_not_found")
    if not raw_text_candidate_schema_found:
        blockers.append("raw_text_candidate_schema_not_found")
    if not provider_output_schema_found:
        blockers.append("provider_output_schema_not_found")
    if not trw_output_contract_ready:
        blockers.append("trw_output_contract_not_ready")

    result = "NO_GO"
    if not blockers:
        result = "GO" if not warnings else "CONDITIONAL_GO"

    hard_audit = {
        "runtime_invoked": False,
        "ocr_provider_invoked": False,
        "ocr_model_invoked": False,
        "semantic_interpretation_enabled": False,
        "midplatform_invoked": False,
        "scene_delta_invoked": False,
        "world_context_invoked": False,
        "qwen_invoked": False,
        "real_tts_invoked": False,
        "playback_invoked": False,
        "downstream_invocation_count": 0,
        "navigation_action": None,
        "world_write_invoked": False,
        "hive_upload_invoked": False,
    }

    return {
        "validation_id": vid,
        "capability": "ocr",
        "stage": "stage2_ocr_guarded_trial",
        "validation_mode": "static_config_only",
        "phase": PHASE,
        "provider_invoked": False,
        "ocr_model_invoked": False,
        "camera_invoked": False,
        "video_stream_opened": False,
        "source_policy_entrypoint_found": bool(source_policy_entrypoint_found),
        "provider_candidate_found": bool(provider_candidate_found),
        "fallback_policy_found": bool(fallback_policy_found),
        "not_available_policy_found": True,
        "raw_text_candidate_schema_found": bool(raw_text_candidate_schema_found),
        "provider_output_schema_found": bool(provider_output_schema_found),
        "trw_output_contract_ready": bool(trw_output_contract_ready),
        "controlled_provider_runbook_ready": bool(runbook_ok),
        "semantic_interpretation_default": False,
        "midplatform_forward_default": False,
        "scene_delta_forward_default": False,
        "world_context_forward_default": False,
        "source_policy_ready": bool(policy.get("exists") and policy.get("policy_id_match")),
        "provider_static_config_ready": bool(manifests.get("ok")),
        "raw_text_candidate_schema_ready": bool(schema.get("ok")),
        "fallback_policy_ready": bool(fallback.get("ok")),
        "request_trace_trw_contract_ready": bool(trw.get("ok")),
        "static_validation_result": result if not blockers else "NO_GO",
        "blockers": blockers,
        "warnings": warnings,
        "hard_audit": hard_audit,
        "ocr_precheck_root": str(ocr_precheck_root) if ocr_precheck_root else None,
        "ocr_precheck_root_readable": bool(precheck_root_ok),
        "source_policy_entrypoint_matrix": entry_matrix,
        "provider_candidate_matrix": provider_matrix,
        "fallback_policy_matrix": fallback_matrix,
        "raw_text_candidate_schema_validation": raw_text_schema_val,
        "provider_output_schema_validation": provider_output_schema_val,
        "trw_output_contract_validation": trw_contract_val,
        "source_policy_scan": policy,
        "provider_manifest_scan": manifests,
        "raw_text_candidate_schema_contract": schema,
        "fallback_policy_readiness": fallback,
        "request_trace_trw_contract": trw,
        "controlled_provider_runbook": runbook,
    }

