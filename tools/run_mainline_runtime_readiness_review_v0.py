#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-RuntimeReadiness-001 — YOLO / OCR / Qwen Voice runtime readiness review (read-only).

Does NOT connect runtime, does NOT call providers, does NOT modify code or default policy.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE = "Phase-Mainline-RuntimeReadiness-001"
REVIEW_ID = "mainline_runtime_readiness_review_v0"

# R0..R3 only (policy: no R4/R5 in this phase)
ReadinessLevel = str


@dataclass
class CapabilityRow:
    capability: str
    current_status: str
    runtime_connected: bool
    request_trace_shadow: bool
    unified_observability: bool
    runtime_readiness_level: ReadinessLevel
    required_before_runtime: List[str]
    hard_blockers: List[str]
    soft_followups: List[str]
    recommended_next_phase: str

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        return d


# (scan_key, repo_relative_or_workspace_relative, root: "repo" | "workspace_min")
CANDIDATE_LOG_PATHS: List[Tuple[str, str, str]] = [
    ("luna_core_voice_gov_regression_006", "logs/voice_output_governance_regression_006_test_run", "repo"),
    (
        "luna_core_voice_qwen_rt_003",
        "logs/voice_qwen_governed_entry_request_trace_003_20260506_040125Z",
        "repo",
    ),
    ("wsm_rt_shadow_002", "logs/core_capability_request_trace_shadow_002_20260430_160600", "workspace_min"),
    ("luna_core_unified_trace_003", "logs/core_capability_unified_request_trace_view_003_20260430_163000", "repo"),
    ("luna_core_unified_export_004", "logs/core_capability_unified_export_004_20260430_163700", "repo"),
]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _utc_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def _exists(p: Path) -> bool:
    return p.is_dir() or p.is_file()


def _scan_optional_logs(repo: Path, wsm: Optional[Path]) -> Dict[str, Any]:
    out: Dict[str, Any] = {"repo": str(repo), "workspace_min": str(wsm) if wsm else None, "paths": {}}
    for key, rel, root_kind in CANDIDATE_LOG_PATHS:
        if root_kind == "workspace_min":
            p = (wsm / rel) if wsm else Path(rel)
        else:
            p = repo / rel
        out["paths"][key] = {"path": str(p), "exists": p.is_dir(), "root": root_kind}
    # glob latest voice qwen 003 if default missing
    if not out["paths"].get("luna_core_voice_qwen_rt_003", {}).get("exists"):
        globs = sorted(repo.glob("logs/voice_qwen_governed_entry_request_trace_003_*"), reverse=True)
        if globs:
            g = globs[0]
            out["paths"]["luna_core_voice_qwen_rt_003_glob"] = {"path": str(g), "exists": g.is_dir()}
    return out


def _build_readiness_matrix(
    log_scan: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Static review — levels capped at R3. No R4/R5.
    """
    rows: List[CapabilityRow] = []

    # YOLO
    rows.append(
        CapabilityRow(
            capability="yolo",
            current_status="closed_v0",
            runtime_connected=False,
            request_trace_shadow=True,
            unified_observability=True,
            runtime_readiness_level="R2_shadow_ready",
            required_before_runtime=[
                "真实 detector runtime 与 frame ingestion 主链合同",
                "受控 env 与短窗 trial 退出条件",
                "RequestTrace stage 与真实 request_id 注入一致",
            ],
            hard_blockers=[
                "真实 frame 主链与在线推理未纳入本仓库 runtime readiness 验收",
            ],
            soft_followups=["与 vision 主设备/相机 pipeline 契约", "性能与热路径回归基线"],
            recommended_next_phase="Phase-Mainline-RuntimeReadiness-002 (YOLO guarded trial scoping)",
        )
    )

    # OCR
    rows.append(
        CapabilityRow(
            capability="ocr",
            current_status="closed_v0",
            runtime_connected=False,
            request_trace_shadow=True,
            unified_observability=True,
            runtime_readiness_level="R2_shadow_ready",
            required_before_runtime=[
                "OCR provider 受控调用与 source policy 在 runtime 下可证明",
                "MidPlatform 证据链与拒绝策略在真实时序下可回归",
            ],
            hard_blockers=["真实 OCR runtime 主链未闭合（离线与 shadow 已闭合）"],
            soft_followups=["多源策略与 GPU/CPU 资源门控"],
            recommended_next_phase="Phase-Mainline-RuntimeReadiness-002 (OCR provider trial)",
        )
    )

    # Voice governance (umbrella)
    rows.append(
        CapabilityRow(
            capability="voice_governance",
            current_status="closed_v0",
            runtime_connected=False,
            request_trace_shadow=True,
            unified_observability=True,
            runtime_readiness_level="R2_shadow_ready",
            required_before_runtime=[
                "governed submit 与主链 submit 的硬审计一致",
            ],
            hard_blockers=[],
            soft_followups=["扩大 query/export 与真实 JSONL 源对齐"],
            recommended_next_phase="保持与 Voice Output Governance 回归基线同步",
        )
    )

    # Qwen voice / TTS governed entry
    qwen_blockers = [
        "run_tts_unified_entry 前未强制 voice_output_governance_v0 / GovernedVoiceProviderEntry（真实链）",
        "VoiceOutputPlaneV1 execute_tts 路径仍声明不接 SpeechGate（与「全量治理」目标存在差距）",
    ]
    qwen_soft = ["Piper/qwen 链路与超时/熔断在真实网络下复测"]
    if log_scan.get("paths", {}).get("luna_core_voice_qwen_rt_003", {}).get("exists") or log_scan.get("paths", {}).get(
        "luna_core_voice_qwen_rt_003_glob", {}
    ).get("exists"):
        qwen_soft.insert(0, "影子侧 RequestTrace 阶段映射已闭合（logs 存在）；真实 runtime 仍待接线验收")

    rows.append(
        CapabilityRow(
            capability="qwen_voice",
            current_status="shadow_ready",
            runtime_connected=False,
            request_trace_shadow=True,
            unified_observability=True,
            runtime_readiness_level="R2_shadow_ready",
            required_before_runtime=[
                "单一受控入口：governance → governed entry → run_tts_unified_entry",
                "LUNA_ENABLE_GOVERNED_QWEN_ENTRY_V1 等显式 trial 开关（建议，默认 false）",
                "diff_audit 与 provider 健康在真实链上可观测",
            ],
            hard_blockers=qwen_blockers,
            soft_followups=qwen_soft,
            recommended_next_phase="Phase-Voice-Qianwen-004+ (guarded wiring to unified entry)",
        )
    )

    # MidPlatform (evidence consumer)
    rows.append(
        CapabilityRow(
            capability="midplatform",
            current_status="closed_v0",
            runtime_connected=False,
            request_trace_shadow=True,
            unified_observability=True,
            runtime_readiness_level="R2_shadow_ready",
            required_before_runtime=["OCR/MidPlatform 真源时序与 backpressure 合同"],
            hard_blockers=["跨域真实执行仍非本阶段范围"],
            soft_followups=["证据 schema 版本化"],
            recommended_next_phase="与 OCR runtime trial 同步闸口",
        )
    )

    # Scene delta
    rows.append(
        CapabilityRow(
            capability="scene_delta",
            current_status="closed_v0",
            runtime_connected=False,
            request_trace_shadow=True,
            unified_observability=True,
            runtime_readiness_level="R2_shadow_ready",
            required_before_runtime=["SceneDelta 与 runtime tick 对齐"],
            hard_blockers=[],
            soft_followups=["大规模场景下的快照开销"],
            recommended_next_phase="runtime fusion 前的增量契约冻结",
        )
    )

    # World context evidence
    rows.append(
        CapabilityRow(
            capability="world_context",
            current_status="closed_v0",
            runtime_connected=False,
            request_trace_shadow=True,
            unified_observability=True,
            runtime_readiness_level="R2_shadow_ready",
            required_before_runtime=["WorldContext 写入边界与非编造审计"],
            hard_blockers=[],
            soft_followups=["与导航/场景任务的接口分层"],
            recommended_next_phase="world evidence runtime ingestion review",
        )
    )

    return [r.to_dict() for r in rows]


def _wiring_candidate_matrix() -> List[Dict[str, Any]]:
    def wp(
        capability: str,
        pt: str,
        *,
        allowed: bool,
        bypass: str,
        notes: str,
    ) -> Dict[str, Any]:
        return {
            "capability": capability,
            "wiring_point": pt,
            "allowed_in_next_phase": allowed,
            "default_enabled": False,
            "requires_env_flag": True,
            "requires_shadow_compare": True,
            "requires_abort_switch": True,
            "bypass_risk": bypass,
            "notes": notes,
        }

    return [
        wp(
            "yolo",
            "frame_ingestion_point",
            allowed=True,
            bypass="high",
            notes="帧入口若无 trace/session，将破坏 Unified Core View。",
        ),
        wp(
            "yolo",
            "detector_invocation_point",
            allowed=True,
            bypass="high",
            notes="推理输出必须带 RequestTrace stage 与硬审计占位。",
        ),
        wp(
            "yolo",
            "observation_loop_or_offline_mainline_equivalent",
            allowed=True,
            bypass="medium",
            notes="在线 tick 与离线回放对齐前需 shadow diff。",
        ),
        wp(
            "yolo",
            "request_trace_stage_emission_point",
            allowed=True,
            bypass="high",
            notes="旁路 stage 将导致 trace 与 Core View 漂移。",
        ),
        wp(
            "ocr",
            "ocr_source_policy_selector",
            allowed=True,
            bypass="medium",
            notes="策略旁路会导致不可审计 OCR 源。",
        ),
        wp(
            "ocr",
            "yolo_to_ocr_bridge_proposal_point",
            allowed=True,
            bypass="medium",
            notes="bridge 仅提案；下游必须显式接纳。",
        ),
        wp(
            "ocr",
            "ocr_provider_invocation_point",
            allowed=True,
            bypass="high",
            notes="无 TRW 注入则不可比 shadow。",
        ),
        wp(
            "ocr",
            "midplatform_evidence_input_point",
            allowed=True,
            bypass="medium",
            notes="证据泄漏需 kill switch 阻断下游消费。",
        ),
        wp(
            "ocr",
            "request_trace_stage_emission_point",
            allowed=True,
            bypass="high",
            notes="与 YOLO/Voice 共用 namespace，禁止私有 shadow channel。",
        ),
        wp(
            "qwen_voice",
            "before_run_tts_unified_entry",
            allowed=True,
            bypass="high",
            notes="真实链闸门：未接线前保持 dry-run；禁止旁路 TTS。",
        ),
        wp(
            "qwen_voice",
            "before_voice_output_plane_submit",
            allowed=True,
            bypass="high",
            notes="submit 前必须具备 governance + hard_audit。",
        ),
        wp(
            "qwen_voice",
            "before_actual_provider_invocation",
            allowed=True,
            bypass="high",
            notes="provider health / timeout / fallback 必须可观测。",
        ),
        wp(
            "qwen_voice",
            "after_voice_output_governance_decision",
            allowed=True,
            bypass="high",
            notes="治理决策是唯一合法放行文本源之一。",
        ),
        wp(
            "qwen_voice",
            "governed_provider_entry_dry_run_point",
            allowed=True,
            bypass="low",
            notes="shadow 已闭合；下一跳为显式 trial flag 下的真实链克隆。",
        ),
        wp(
            "qwen_voice",
            "request_trace_stage_emission_point",
            allowed=True,
            bypass="medium",
            notes="与 Phase-Qianwen RequestTrace 映射一致；禁止重复字段口径。",
        ),
    ]


def _env_flag_matrix() -> List[Dict[str, Any]]:
    return [
        {
            "flag_name": "LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1",
            "capability": "voice",
            "purpose": "允许 VoiceOutputPlane submit 闭环（仍可比 shadow）",
            "default_value": False,
            "required_before_wiring": True,
            "rollback_behavior": "置 0：回到 dry-run / shadow-only submit",
            "owner": "runtime",
        },
        {
            "flag_name": "LUNA_REAL_OUTPUT_SUBMIT_V1_EXECUTE_TTS",
            "capability": "voice",
            "purpose": "submit 内是否调用 run_tts_unified_entry",
            "default_value": False,
            "required_before_wiring": True,
            "rollback_behavior": "置 0：仅 dry-run observation",
            "owner": "runtime",
        },
        {
            "flag_name": "LUNA_ENABLE_REAL_PLAYBACK_EXECUTION_V1",
            "capability": "voice",
            "purpose": "playback plane / audio worker 真执行",
            "default_value": False,
            "required_before_wiring": True,
            "rollback_behavior": "置 0：不落地扬声器队列",
            "owner": "runtime",
        },
        {
            "flag_name": "LUNA_ENABLE_GOVERNED_QWEN_ENTRY_V1",
            "capability": "qwen_voice",
            "purpose": "（建议）强制 governed entry 进入真实 TTS 前置路径",
            "default_value": False,
            "required_before_wiring": True,
            "rollback_behavior": "置 0：仅影子链/离线 skeleton",
            "owner": "sandbox",
        },
        {
            "flag_name": "LUNA_ENABLE_QWEN_PRIMARY_VOICE_MODE_V1",
            "capability": "qwen_voice",
            "purpose": "（建议）显式启用 online_prefer_qwen 模板 trial（与 yaml 默认无关）",
            "default_value": False,
            "required_before_wiring": True,
            "rollback_behavior": "关闭：回到 offline_only/piper baseline",
            "owner": "sandbox",
        },
        {
            "flag_name": "LUNA_*_YOLO_RUNTIME_TRIAL_V1",
            "capability": "yolo",
            "purpose": "（占位）YOLO 受控 trial 总闸 — 具体名在接线 PR 冻结",
            "default_value": False,
            "required_before_wiring": True,
            "rollback_behavior": "关闭：仅 shadow/offline 推理",
            "owner": "sandbox",
        },
        {
            "flag_name": "LUNA_*_OCR_RUNTIME_TRIAL_V1",
            "capability": "ocr",
            "purpose": "（占位）OCR 受控 trial 总闸",
            "default_value": False,
            "required_before_wiring": True,
            "rollback_behavior": "关闭：跳过在线 OCR provider",
            "owner": "sandbox",
        },
    ]


def _trw_requirement_matrix() -> List[Dict[str, Any]]:
    fields = [
        "request_id",
        "trace_id",
        "session_id",
        "source_run_id",
        "runtime_run_id",
        "trace_ref",
        "replay_ref",
        "whitebox_ref",
        "hard_audit",
        "provider_health",
        "latency_ms",
        "timeout_ms",
        "fallback_chain",
        "suppression_or_block_reason",
    ]
    return [
        {
            "subsystem": "yolo",
            "required_fields": fields,
            "notes": "帧级与检测级 id 需可关联；与 OCR/Voice 共用 Core RequestTrace namespace。",
        },
        {
            "subsystem": "ocr",
            "required_fields": fields,
            "notes": "source policy 决策必须可写入 TRW。",
        },
        {
            "subsystem": "qwen_voice",
            "required_fields": fields + ["provider_input_text", "spoken_text", "text_diff_audit"],
            "notes": "与 Phase-009 导出字段相容；real_* 硬审计保持 false 直至显式 trial。",
        },
    ]


def _abort_rollback_matrix() -> List[Dict[str, Any]]:
    return [
        {
            "trigger": "qwen_timeout_or_network",
            "subsystem": "qwen_voice",
            "abort_condition": "hard_timeout / circuit_breaker open",
            "rollback_action": "fallback Piper 或 suppress（按 policy）",
            "fallback_path": "tts_fallback_manager chain",
            "safe_default": "offline_only / Piper-only",
            "user_affected": "may_hear_alternate_voice_or_silence",
            "runtime_can_continue": True,
            "shadow_evidence_retained": True,
        },
        {
            "trigger": "governance_decision_not_accepted",
            "subsystem": "qwen_voice",
            "abort_condition": "final_action not in allowed synthesis set",
            "rollback_action": "block submit / no provider invoke",
            "fallback_path": "none",
            "safe_default": "no speech",
            "user_affected": "no_playback",
            "runtime_can_continue": True,
            "shadow_evidence_retained": True,
        },
        {
            "trigger": "diff_audit_missing_or_inconsistent",
            "subsystem": "qwen_voice",
            "abort_condition": "audit schema violation",
            "rollback_action": "block provider invocation",
            "fallback_path": "none",
            "safe_default": "no synthesis",
            "user_affected": "no_playback",
            "runtime_can_continue": True,
            "shadow_evidence_retained": True,
        },
        {
            "trigger": "ocr_provider_unavailable",
            "subsystem": "ocr",
            "abort_condition": "provider health unhealthy",
            "rollback_action": "not_available / defer",
            "fallback_path": "secondary source or skip",
            "safe_default": "no OCR output",
            "user_affected": "degraded_text_pipeline",
            "runtime_can_continue": True,
            "shadow_evidence_retained": True,
        },
        {
            "trigger": "yolo_detector_failure",
            "subsystem": "yolo",
            "abort_condition": "inference error / empty frame",
            "rollback_action": "degraded observation / skip tick",
            "fallback_path": "last_good_observation optional",
            "safe_default": "no detection output",
            "user_affected": "reduced_vision_context",
            "runtime_can_continue": True,
            "shadow_evidence_retained": True,
        },
    ]


def _blocker_register(matrix: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in matrix:
        cap = row.get("capability")
        for b in row.get("hard_blockers") or []:
            out.append(
                {
                    "blocker_id": f"MR001-{cap}-{len(out)}",
                    "severity": "hard",
                    "capability": cap,
                    "description": b,
                    "phase_to_fix": "post-Mainline-RuntimeReadiness-001",
                }
            )
    out.append(
        {
            "blocker_id": "MR001-global-no-killswitch-no-wire",
            "severity": "hard",
            "capability": "mainline",
            "description": "未定义 trial 总闸与 abort/rollback 即接真实主链 → NO_GO",
            "phase_to_fix": "Phase-Mainline-RuntimeReadiness-002+",
        }
    )
    return out


def run_review(*, repo: Path, workspace_min: Optional[Path], out_root: Path) -> Dict[str, Any]:
    log_scan = _scan_optional_logs(repo, workspace_min)
    matrix = _build_readiness_matrix(log_scan)
    wiring = _wiring_candidate_matrix()
    envf = _env_flag_matrix()
    trw = _trw_requirement_matrix()
    abortm = _abort_rollback_matrix()
    blockers = _blocker_register(matrix)

    summary = {
        "phase": PHASE,
        "review_id": REVIEW_ID,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repo_root": str(repo),
        "workspace_min": str(workspace_min) if workspace_min else None,
        "output_root": str(out_root),
        "constraints": {
            "no_runtime_wiring": True,
            "no_real_provider_calls": True,
            "no_default_policy_change": True,
            "readiness_level_cap": "R3_guarded_wiring_ready_max",
            "forbid_R4_R5_in_this_review": True,
        },
        "log_scan": log_scan,
        "readiness_level_summary": {
            "yolo": "R2_shadow_ready",
            "ocr": "R2_shadow_ready",
            "voice_governance": "R2_shadow_ready",
            "qwen_voice": "R2_shadow_ready",
            "midplatform": "R2_shadow_ready",
            "scene_delta": "R2_shadow_ready",
            "world_context": "R2_shadow_ready",
        },
        "verdict_hint": "CONDITIONAL_GO",
        "verdict_notes": "Matrices complete; real runtime mainline still open — hard blockers registered.",
        "verdict": {
            "phase_review_documentation": "GO",
            "guarded_wiring_preparation_next_phase": "CONDITIONAL_GO",
            "real_runtime_or_provider_activation": "NO_GO",
            "rationale": "Readiness matrices + registers complete without wiring runtime; optional local log snapshots may be absent; real mainline remains NO_GO until kill-switch/TRW/abort paths are enforced on-device.",
        },
    }

    out_root.mkdir(parents=True, exist_ok=True)
    (out_root / "mainline_runtime_readiness_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "mainline_runtime_readiness_matrix.json").write_text(
        json.dumps(matrix, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "mainline_runtime_blocker_register.json").write_text(
        json.dumps(blockers, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "mainline_runtime_wiring_candidate_matrix.json").write_text(
        json.dumps(wiring, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "mainline_runtime_env_flag_matrix.json").write_text(
        json.dumps(envf, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "mainline_runtime_trw_requirement_matrix.json").write_text(
        json.dumps(trw, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_root / "mainline_runtime_abort_rollback_requirement_matrix.json").write_text(
        json.dumps(abortm, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    notes = [
        f"# {PHASE} — review notes",
        "",
        "Read-only review. No code changes, no runtime connections.",
        "",
        "## Log paths scanned",
        "",
        "```json",
        json.dumps(log_scan, ensure_ascii=False, indent=2),
        "```",
        "",
        "## Verdict",
        "",
        "- **CONDITIONAL_GO**: matrices + registers generated; some optional log roots may be missing locally.",
        "- **NO_GO** if anyone wires real runtime without kill switches / TRW / abort paths.",
        "",
    ]
    (out_root / "review_notes.md").write_text("\n".join(notes), encoding="utf-8")

    return summary


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=str(_repo_root()))
    ap.add_argument("--workspace-min-root", default="", help="Luna-Workspace-Min root for optional logs")
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()

    repo = Path(args.repo_root).resolve()
    wsm = Path(args.workspace_min_root).resolve() if args.workspace_min_root else None
    if wsm and not wsm.is_dir():
        wsm = None

    out = Path(args.output_root) if args.output_root else repo / "logs" / f"mainline_runtime_readiness_001_{_utc_tag()}"
    summary = run_review(repo=repo, workspace_min=wsm, out_root=out)
    print(
        json.dumps(
            {"ok": True, "output_root": str(out), "verdict_hint": summary.get("verdict_hint"), "verdict": summary.get("verdict")},
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
