# -*- coding: utf-8
"""Luna Situation Understanding — UI payload builder v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from capabilities.midplatform.situation_understanding.luna_situation_understanding_types_v1 import (
    POLICY_REF,
)


FORBIDDEN_UI_COPY = (
    "已识别为店招",
    "已确认场景",
    "OCR 已执行",
    "SLAM 已关闭",
    "模型已经判断",
    "最终结论",
    "confirmed",
    "已识别为",
    "读取成功",
    "导航到",
)


def normalize_situation_candidate_for_ui(candidate: Dict[str, Any]) -> Dict[str, Any]:
    scene = dict(candidate.get("scene_profile_candidate", {}))
    scene.setdefault("owned_by", "situation_understanding_layer")
    return {
        "situation_id": candidate.get("situation_id", ""),
        "scene_profile_candidate": scene,
        "survival_context": candidate.get("survival_context", {}),
        "task_clue_candidates": candidate.get("task_clue_candidates", []),
        "missing_information_candidates": candidate.get("missing_information_candidates", []),
        "attention_target_hints": candidate.get("attention_target_hints", []),
        "model_need_hints": candidate.get("model_need_hints", {
            "likely_needed": [], "optional": [], "not_needed": [],
        }),
        "uncertainty": candidate.get("uncertainty", {}),
        "candidate_only": True,
        "not_fact": True,
        "trace_refs": candidate.get("trace_refs", []),
        "policy_refs": candidate.get("policy_refs", [POLICY_REF]),
        "no_runner_invocation": candidate.get("no_runner_invocation", True),
        "no_fact_write": candidate.get("no_fact_write", True),
    }


def build_runner_conflict_trace_for_ui(dryrun: Dict[str, Any]) -> List[Dict[str, Any]]:
    traces: List[Dict[str, Any]] = []
    scene_trace = dryrun.get("scene_resolution_trace", {})
    traces.extend(scene_trace.get("conflict_traces", []))
    optional = dryrun.get("conflict_trace_optional") or []
    traces.extend(optional)
    seen = set()
    unique: List[Dict[str, Any]] = []
    for t in traces:
        key = json_key(t)
        if key not in seen:
            seen.add(key)
            unique.append(t)
    return unique


def json_key(obj: Dict[str, Any]) -> str:
    return str(sorted(obj.items()))


def build_model_need_hint_summary(candidate: Dict[str, Any]) -> Dict[str, List[str]]:
    hints = candidate.get("model_need_hints", {})
    return {
        "likely_needed": [h.get("capability_type", "") for h in hints.get("likely_needed", [])],
        "optional": [h.get("capability_type", "") for h in hints.get("optional", [])],
        "not_needed": [h.get("capability_type", "") for h in hints.get("not_needed", [])],
    }


def build_situation_badges(payload: Dict[str, Any]) -> List[str]:
    badges = ["candidate_only", "not_fact", "no_runner_invocation", "no_fact_write"]
    scene = payload.get("scene_profile_candidate", {})
    if scene.get("owned_by") == "situation_understanding_layer":
        badges.append("scene_owned_by_situation_layer")
    if payload.get("conflict_trace"):
        badges.append("runner_scene_hint_conflict")
    return badges


def build_ui_payload_from_dryrun_result(dryrun: Dict[str, Any]) -> Dict[str, Any]:
    """Build TestBoard UI payload from dryrun adapter output."""
    candidate = normalize_situation_candidate_for_ui(
        dryrun.get("situation_understanding_candidate", {})
    )
    conflict = build_runner_conflict_trace_for_ui(dryrun)
    runner_ev = dryrun.get("runner_scene_hint_evidence_record") or {}
    summary = build_model_need_hint_summary(candidate)
    payload = {
        "situation_id": candidate.get("situation_id", ""),
        "job_id": dryrun.get("job_id", ""),
        "scene_profile_candidate": candidate["scene_profile_candidate"],
        "survival_context": candidate["survival_context"],
        "task_clue_candidates": candidate["task_clue_candidates"],
        "missing_information_candidates": candidate["missing_information_candidates"],
        "attention_target_hints": candidate["attention_target_hints"],
        "model_need_hints": candidate["model_need_hints"],
        "model_need_hint_summary": summary,
        "uncertainty": candidate.get("uncertainty", {}),
        "runner_scene_hint_evidence": runner_ev,
        "conflict_trace": conflict,
        "badges": build_situation_badges({"scene_profile_candidate": candidate["scene_profile_candidate"], "conflict_trace": conflict}),
        "candidate_only": True,
        "not_fact": True,
        "trace_refs": candidate.get("trace_refs", []),
        "policy_refs": candidate.get("policy_refs", [POLICY_REF]),
        "no_runner_invocation": True,
        "no_fact_write": True,
        "dryrun_only": True,
    }
    return payload


def audit_ui_copy(text: str) -> List[str]:
    violations = []
    for forbidden in FORBIDDEN_UI_COPY:
        if forbidden in text:
            violations.append(forbidden)
    return violations
