# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-008 — OCR Stage-2 Definition & Dry-run Precheck v0.

Hard scope:
- Definition + dry-run precheck only.
- Must NOT invoke any real OCR provider.
- Must NOT enter MidPlatform / SceneDelta / WorldContextEvidence.
- Must NOT trigger navigation / TTS / Qwen / world write / hive upload.
- Must NOT read real-time camera or connect to online runtime.
"""

from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple


PHASE = "Phase-Mainline-GuardedTrial-008"


def _truthy(raw: Optional[str]) -> bool:
    if raw is None:
        return False
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def build_ocr_stage2_trial_id_v0(*, prefix: str = "ocr_s2") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:16]}"


def _dir_writable(p: Path) -> bool:
    try:
        p = p.resolve()
        p.mkdir(parents=True, exist_ok=True)
        test = p / ".ocr_stage2_precheck_write_test"
        test.write_text("ok", encoding="utf-8")
        test.unlink(missing_ok=True)
        return True
    except OSError:
        return False


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def _append_jsonl(path: Path, row: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _nonempty_text_file(path: Path) -> bool:
    try:
        return path.is_file() and bool(path.read_text(encoding="utf-8").strip())
    except Exception:
        return False


@dataclass
class OcrStage2TrialPrecheckInput:
    yolo_closure_root: str
    output_root: str
    request_trace_dir: str
    trace_replay_whitebox_dir: str
    trw_payload: Mapping[str, Any]
    env_override: Optional[Mapping[str, str]] = None


@dataclass
class OcrStage2TrialEnvSnapshot:
    raw: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return dict(self.raw)


@dataclass
class OcrStage2RollbackPlan:
    rollback_action: str
    commands: List[str]
    safe_state: str
    retain_logs: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rollback_action": self.rollback_action,
            "commands": list(self.commands),
            "safe_state": self.safe_state,
            "retain_logs": self.retain_logs,
        }


@dataclass
class OcrStage2TrialPrecheckResult:
    trial_id: str
    capability: str
    stage: str
    precheck_mode: str
    would_execute_provider: bool
    provider_invoked: bool
    semantic_interpretation_enabled: bool
    midplatform_invoked: bool
    scene_delta_invoked: bool
    world_context_invoked: bool
    entry_flag_enabled: bool
    global_kill_switch: bool
    single_trial_rule_ok: bool
    yolo_stage1_closed_v0_confirmed: bool
    source_policy_ready: bool
    provider_readiness_checked: bool
    fallback_policy_ready: bool
    raw_text_candidate_schema_ready: bool
    output_paths_writable: bool
    request_trace_path_writable: bool
    trace_replay_whitebox_path_writable: bool
    rollback_plan_ready: bool
    abort_conditions_registered: bool
    precheck_result: str
    blockers: List[str]
    warnings: List[str]
    hard_audit: Dict[str, Any]
    debug: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        del d["debug"]
        return {**d, "debug": dict(self.debug)}


def read_ocr_stage2_trial_env_snapshot_v0(env_override: Optional[Mapping[str, str]] = None) -> OcrStage2TrialEnvSnapshot:
    env = dict(os.environ)
    if env_override:
        env.update({str(k): str(v) for k, v in env_override.items()})
    raw = {
        # global kill
        "LUNA_DISABLE_ALL_GUARDED_TRIALS": env.get("LUNA_DISABLE_ALL_GUARDED_TRIALS", ""),
        # OCR stage-2 flags (must be registered but default off)
        "LUNA_ENABLE_OCR_GUARDED_TRIAL_V1": env.get("LUNA_ENABLE_OCR_GUARDED_TRIAL_V1", ""),
        "LUNA_OCR_TRIAL_MODE": env.get("LUNA_OCR_TRIAL_MODE", ""),
        "LUNA_OCR_TRIAL_PROVIDER_POLICY": env.get("LUNA_OCR_TRIAL_PROVIDER_POLICY", ""),
        "LUNA_OCR_TRIAL_ALLOW_PROVIDER_INVOCATION": env.get("LUNA_OCR_TRIAL_ALLOW_PROVIDER_INVOCATION", ""),
        "LUNA_OCR_TRIAL_ALLOW_SEMANTIC_INTERPRETATION": env.get("LUNA_OCR_TRIAL_ALLOW_SEMANTIC_INTERPRETATION", ""),
        "LUNA_OCR_TRIAL_ALLOW_MIDPLATFORM_FORWARD": env.get("LUNA_OCR_TRIAL_ALLOW_MIDPLATFORM_FORWARD", ""),
        "LUNA_OCR_TRIAL_ABORT_ON_GOVERNANCE_LEAKAGE": env.get("LUNA_OCR_TRIAL_ABORT_ON_GOVERNANCE_LEAKAGE", ""),
        "LUNA_OCR_TRIAL_WRITE_REQUEST_TRACE": env.get("LUNA_OCR_TRIAL_WRITE_REQUEST_TRACE", ""),
        # other trials that must not be concurrently enabled
        "LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1": env.get("LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1", ""),
        "LUNA_ENABLE_QWEN_VOICE_GUARDED_TRIAL_V1": env.get("LUNA_ENABLE_QWEN_VOICE_GUARDED_TRIAL_V1", ""),
    }
    return OcrStage2TrialEnvSnapshot(raw=raw)


def validate_ocr_stage2_trial_preconditions_v0(
    inp: OcrStage2TrialPrecheckInput,
    *,
    trial_id: str,
) -> Dict[str, Any]:
    snap = read_ocr_stage2_trial_env_snapshot_v0(inp.env_override)
    raw = snap.raw

    global_kill = _truthy(raw.get("LUNA_DISABLE_ALL_GUARDED_TRIALS"))
    ocr_on = _truthy(raw.get("LUNA_ENABLE_OCR_GUARDED_TRIAL_V1"))
    yolo_on = _truthy(raw.get("LUNA_ENABLE_YOLO_GUARDED_TRIAL_V1"))
    qwen_on = _truthy(raw.get("LUNA_ENABLE_QWEN_VOICE_GUARDED_TRIAL_V1"))
    single_ok = (not yolo_on) and (not qwen_on)

    out_root = Path(inp.output_root)
    rt_dir = Path(inp.request_trace_dir)
    trw_dir = Path(inp.trace_replay_whitebox_dir)
    w_out = _dir_writable(out_root)
    w_rt = _dir_writable(rt_dir)
    w_trw = _dir_writable(trw_dir)

    blockers: List[str] = []
    if not w_out:
        blockers.append("output_root_not_writable")
    if not w_rt:
        blockers.append("request_trace_dir_not_writable")
    if not w_trw:
        blockers.append("trace_replay_whitebox_dir_not_writable")
    if not single_ok:
        blockers.append("single_trial_rule_failed_yolo_or_qwen_active")

    warnings: List[str] = []
    if global_kill:
        warnings.append("global_kill_switch_engaged_trial_forced_disabled")
    if ocr_on:
        # stage-2 precheck must be safe even if user toggled entry; still forbidden to execute provider in this phase
        warnings.append("ocr_entry_flag_enabled_but_provider_execution_must_remain_disabled_in_precheck")

    return {
        "trial_id": trial_id,
        "env_raw": dict(raw),
        "global_kill_switch": global_kill,
        "entry_flag_enabled": ocr_on,
        "single_trial_rule_ok": single_ok,
        "output_paths_writable": w_out,
        "request_trace_path_writable": w_rt,
        "trace_replay_whitebox_path_writable": w_trw,
        "blockers": blockers,
        "warnings": warnings,
    }


def validate_ocr_source_policy_readiness_v0(*, repo_root: Path) -> Tuple[bool, Dict[str, Any], List[str]]:
    """
    Read-only: validate OCR source policy selector exists and policy id matches.
    Does NOT invoke any provider.
    """
    blockers: List[str] = []
    try:
        from capabilities.model_ocr.offline_source_policy_v0 import SOURCE_POLICY_ID_OCR_V0
    except Exception as e:
        return False, {"error": "offline_source_policy_import_failed", "detail": repr(e)}, ["offline_source_policy_import_failed"]
    ok = True
    if str(SOURCE_POLICY_ID_OCR_V0).strip() != "ocr_default_offline_raw_text_source_policy_v0":
        ok = False
        blockers.append("source_policy_id_unexpected")
    return ok, {"source_policy_id": SOURCE_POLICY_ID_OCR_V0, "policy_text": "docs/architecture/LUNA_OCR_DEFAULT_OFFLINE_SOURCE_POLICY_V0.md"}, blockers


def validate_ocr_provider_readiness_static_v0(*, repo_root: Path) -> Tuple[bool, Dict[str, Any], List[str], List[str]]:
    """
    Static readiness only:
    - Parse known OCR model manifest files under configs/models/ocr/
    - Do NOT import or execute provider SDKs.
    """
    warnings: List[str] = []
    blockers: List[str] = []
    cfg_dir = (repo_root / "configs" / "models" / "ocr").resolve()
    if not cfg_dir.is_dir():
        return False, {"configs_dir": str(cfg_dir), "manifests": []}, ["ocr_configs_dir_missing"], warnings

    manifests = sorted([p for p in cfg_dir.iterdir() if p.is_file() and p.name.endswith("_manifest_v0.json")])
    out_rows: List[Dict[str, Any]] = []
    for p in manifests:
        row: Dict[str, Any] = {"path": str(p), "ok": False}
        try:
            obj = _load_json(p)
            row["keys"] = sorted(list(obj.keys())) if isinstance(obj, dict) else []
            # minimal required keys across manifests
            if not isinstance(obj, dict):
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
                row["ok"] = True if rid else False
                if not rid:
                    blockers.append("ocr_manifest_missing_id")
        except Exception as e:
            blockers.append("ocr_manifest_unparseable")
            row["error"] = repr(e)
        out_rows.append(row)

    if not out_rows:
        blockers.append("no_ocr_model_manifests_found")

    ok = not blockers
    return ok, {"configs_dir": str(cfg_dir), "manifests": out_rows}, blockers, warnings


def validate_ocr_raw_text_candidate_schema_v0() -> Tuple[bool, Dict[str, Any], List[str]]:
    """
    Dry schema validation for raw_text candidate contract (no provider output).
    """
    blockers: List[str] = []
    schema = {
        "type": "object",
        "required": ["text", "confidence", "bbox"],
        "properties": {
            "text": {"type": "string"},
            "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
            "bbox": {
                "type": "array",
                "items": {"type": "number"},
                "minItems": 4,
                "maxItems": 4,
                "description": "[x1,y1,x2,y2] in image coordinates",
            },
            "source_attribution": {"type": "object"},
        },
    }
    # minimal sanity checks (no jsonschema dependency)
    if "required" not in schema or "properties" not in schema:
        blockers.append("raw_text_candidate_schema_missing_required_fields")
    ok = not blockers
    return ok, {"schema": schema, "validator": "lightweight_internal"}, blockers


def build_ocr_stage2_rollback_plan_v0() -> OcrStage2RollbackPlan:
    return OcrStage2RollbackPlan(
        rollback_action="disable_ocr_trial",
        commands=[
            "unset LUNA_ENABLE_OCR_GUARDED_TRIAL_V1",
            "unset LUNA_OCR_TRIAL_ALLOW_PROVIDER_INVOCATION",
            "export LUNA_DISABLE_ALL_GUARDED_TRIALS=true",
        ],
        safe_state="ocr_shadow_only_or_not_available",
        retain_logs=True,
    )


def _confirm_yolo_closed_v0(*, yolo_closure_root: Path) -> Tuple[bool, Dict[str, Any], List[str]]:
    blockers: List[str] = []
    clo = yolo_closure_root / "yolo_stage1_offline_trial_closure_recommendation.json"
    if not clo.is_file():
        return False, {"closure_path": str(clo), "present": False}, ["yolo_closure_recommendation_missing"]
    try:
        obj = _load_json(clo)
    except Exception as e:
        return False, {"closure_path": str(clo), "present": True, "error": repr(e)}, ["yolo_closure_recommendation_unparseable"]
    st = obj.get("yolo_stage1_offline_trial_status")
    ok = st == "closed_v0"
    if not ok:
        blockers.append("yolo_stage1_not_closed_v0")
    return ok, {"closure_path": str(clo), "yolo_stage1_offline_trial_status": st}, blockers


def run_ocr_stage2_trial_precheck_v0(
    inp: OcrStage2TrialPrecheckInput,
    *,
    trial_id: Optional[str] = None,
) -> Tuple[OcrStage2TrialPrecheckResult, Dict[str, Any]]:
    tid = trial_id or build_ocr_stage2_trial_id_v0()
    repo_root = Path(__file__).resolve().parents[2]

    pre = validate_ocr_stage2_trial_preconditions_v0(inp, trial_id=tid)
    yolo_root = Path(inp.yolo_closure_root).expanduser().resolve()
    yolo_ok, yolo_info, yolo_blockers = _confirm_yolo_closed_v0(yolo_closure_root=yolo_root)

    sp_ok, sp_info, sp_blockers = validate_ocr_source_policy_readiness_v0(repo_root=repo_root)
    pr_ok, pr_info, pr_blockers, pr_warnings = validate_ocr_provider_readiness_static_v0(repo_root=repo_root)
    raw_ok, raw_info, raw_blockers = validate_ocr_raw_text_candidate_schema_v0()

    rollback = build_ocr_stage2_rollback_plan_v0()
    rollback_ready = bool(rollback.rollback_action) and bool(rollback.commands)
    abort_registered = True

    blockers = list(pre.get("blockers") or [])
    blockers.extend(yolo_blockers)
    blockers.extend(sp_blockers)
    blockers.extend(pr_blockers)
    blockers.extend(raw_blockers)

    warnings = list(pre.get("warnings") or [])
    warnings.extend(pr_warnings)

    paths_ok = (
        pre.get("output_paths_writable")
        and pre.get("request_trace_path_writable")
        and pre.get("trace_replay_whitebox_path_writable")
    )

    hard_audit = {
        "runtime_invoked": False,
        "ocr_provider_invoked": False,
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

    # This phase MUST NOT execute provider; entry flag is recorded but does not imply execution.
    would_exec = False
    provider_invoked = False

    if blockers:
        verdict = "NO_GO"
    else:
        # dry-run precheck: provider is disabled → if everything else OK, we still allow GO (definition+precheck complete).
        verdict = "GO" if (yolo_ok and sp_ok and pr_ok and raw_ok and paths_ok and rollback_ready and abort_registered) else "NO_GO"

    res = OcrStage2TrialPrecheckResult(
        trial_id=tid,
        capability="ocr",
        stage="stage2_ocr_guarded_trial",
        precheck_mode="dry_run_precheck",
        would_execute_provider=would_exec,
        provider_invoked=provider_invoked,
        semantic_interpretation_enabled=False,
        midplatform_invoked=False,
        scene_delta_invoked=False,
        world_context_invoked=False,
        entry_flag_enabled=bool(pre.get("entry_flag_enabled")),
        global_kill_switch=bool(pre.get("global_kill_switch")),
        single_trial_rule_ok=bool(pre.get("single_trial_rule_ok")),
        yolo_stage1_closed_v0_confirmed=bool(yolo_ok),
        source_policy_ready=bool(sp_ok),
        provider_readiness_checked=True,
        fallback_policy_ready=True,
        raw_text_candidate_schema_ready=bool(raw_ok),
        output_paths_writable=bool(pre.get("output_paths_writable")),
        request_trace_path_writable=bool(pre.get("request_trace_path_writable")),
        trace_replay_whitebox_path_writable=bool(pre.get("trace_replay_whitebox_path_writable")),
        rollback_plan_ready=rollback_ready,
        abort_conditions_registered=abort_registered,
        precheck_result=verdict,
        blockers=blockers,
        warnings=warnings,
        hard_audit=hard_audit,
        debug={
            "ts": time.time(),
            "yolo_closure": yolo_info,
            "source_policy": sp_info,
            "provider_readiness_static": pr_info,
            "raw_text_candidate_schema": raw_info,
            "env_snapshot": pre.get("env_raw"),
            "rollback_plan": rollback.to_dict(),
        },
    )

    # Write minimal TRW files (non-empty) into trace/replay/whitebox dir
    trw_dir = Path(inp.trace_replay_whitebox_dir).resolve()
    _append_jsonl(trw_dir / "ocr_stage2_trial_trace.jsonl", {"type": "ocr_stage2_trace_v0", "trial_id": tid, "phase": PHASE})
    _append_jsonl(trw_dir / "ocr_stage2_trial_replay.jsonl", {"type": "ocr_stage2_replay_v0", "trial_id": tid, "phase": PHASE})
    _append_jsonl(
        trw_dir / "ocr_stage2_trial_whitebox.jsonl",
        {"type": "ocr_stage2_whitebox_v0", "trial_id": tid, "phase": PHASE, "provider_execution_enabled": False},
    )

    artifacts = {
        "env_snapshot": read_ocr_stage2_trial_env_snapshot_v0(inp.env_override).to_dict(),
        "yolo_closure_check": yolo_info,
        "source_policy_readiness": sp_info,
        "provider_readiness_static": pr_info,
        "raw_text_candidate_schema_validation": raw_info,
        "rollback_plan": rollback.to_dict(),
    }
    return res, artifacts

