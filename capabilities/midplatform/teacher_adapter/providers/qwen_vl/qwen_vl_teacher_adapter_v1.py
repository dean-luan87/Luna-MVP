# -*- coding: utf-8 -*-
"""Qwen-VL Teacher Adapter — deterministic mock v1 (planning only)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from capabilities.midplatform.teacher_adapter.providers.qwen_vl.qwen_vl_teacher_types_v1 import (
    ALLOWED_INPUT_FIELDS,
    EVIDENCE_TYPES,
    FORBIDDEN_INPUT_FIELDS,
    FORBIDDEN_OUTPUT_TYPES,
    POLICY_REF,
    PROVIDER_ID,
    PROVIDER_LABEL,
    TEACHER_ROLE,
    candidate_meta,
)

FORBIDDEN_TEACHER_ROLES = ("planning_teacher", "learning_teacher")


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _scene(situation: Dict[str, Any]) -> str:
    return (situation.get("scene_profile_candidate") or {}).get("scene_type", "unknown_scene")


def _plan_goal(plan: Optional[Dict[str, Any]]) -> str:
    if not plan:
        return "unknown"
    return (plan.get("plan_goal_candidate") or {}).get("goal_type", "unknown")


def _validate_input_boundary(
    *,
    input_evidence: List[Dict[str, Any]],
    policy_context: Dict[str, Any],
    situation_candidate: Dict[str, Any],
) -> Optional[str]:
    for ev in input_evidence:
        for key in ev:
            if key in FORBIDDEN_INPUT_FIELDS:
                return f"forbidden_input_field:{key}"
    if policy_context.get("internal_state") or policy_context.get("fact_database"):
        return "forbidden_policy_context"
    if not situation_candidate:
        return "missing_situation_candidate"
    return None


def _mock_perception_output(
    *,
    mock_scenario: str,
    situation: Dict[str, Any],
    plan: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    scene = _scene(situation)
    plan_goal = _plan_goal(plan)

    if mock_scenario == "case_a_shopfront_possible_text_region":
        return {
            "evidence_type": "visual_attention_candidate",
            "scene_hypothesis_candidate": {
                "scene_type": scene,
                "confidence_candidate": 0.78,
                "candidate_only": True,
                "not_fact": True,
            },
            "visual_attention_candidate": {
                "attention_type": "possible_text_region",
                "regions": [
                    {
                        "region_id": "text_region_upper_center",
                        "label_candidate": "possible_sign_text",
                        "confidence_candidate": 0.74,
                        "candidate_only": True,
                        "not_fact": True,
                    }
                ],
                "candidate_only": True,
                "not_fact": True,
            },
            "task_clue_candidate": {
                "clue_type": "entrance_hint",
                "clue_text": "可能需要确认店铺入口位置",
                "candidate_only": True,
                "not_fact": True,
            },
            "supporting_reason": "upper center region shows high-contrast text-like pattern",
            "confidence_candidate": 0.74,
            "uncertainty": 0.26,
            "supports_plan": True,
        }

    if mock_scenario == "case_b_slam_mapping_rejected":
        return {
            "evidence_type": "task_clue_candidate",
            "task_clue_candidate": {
                "clue_type": "tool_suggestion",
                "clue_text": "启动 SLAM 建图读取文字",
                "tools_suggested": ["slam"],
                "candidate_only": True,
                "not_fact": True,
            },
            "teacher_suggests": "slam_for_text",
            "tools_suggested": ["slam"],
            "suggestion_text": "启动 SLAM 建图读取文字",
            "policy_risk_candidates": ["tool_mismatch"],
            "supporting_reason": "spatial mapping suggested for text task",
            "confidence_candidate": 0.55,
            "uncertainty": 0.45,
        }

    if mock_scenario == "case_c_unknown_scene_hypothesis":
        return {
            "evidence_type": "scene_hypothesis_candidate",
            "scene_hypothesis_candidate": {
                "scene_hypothesis_candidates": [
                    {"scene_type": "shopfront_sign", "confidence_candidate": 0.42, "candidate_only": True, "not_fact": True},
                    {"scene_type": "street_vendor", "confidence_candidate": 0.31, "candidate_only": True, "not_fact": True},
                ],
                "candidate_only": True,
                "not_fact": True,
            },
            "supporting_reason": "visual layout resembles outdoor storefront signage",
            "confidence_candidate": 0.42,
            "uncertainty": 0.58,
            "does_not_override_l1_scene": True,
        }

    if mock_scenario == "case_d_unsupported_brand_claim":
        return {
            "evidence_type": "scene_hypothesis_candidate",
            "scene_hypothesis_candidate": {
                "named_entity_claim": "Starbucks",
                "claim_text": "This is Starbucks",
                "candidate_only": True,
                "not_fact": True,
            },
            "unsupported_claim": True,
            "hallucination_risk": True,
            "supporting_ocr_evidence": False,
            "supporting_reason": "brand name asserted without OCR confirmation",
            "confidence_candidate": 0.82,
            "uncertainty": 0.18,
            "policy_risk_candidates": ["unsupported_claim"],
        }

    if mock_scenario == "case_e_navigate_task_clue_only":
        return {
            "evidence_type": "task_clue_candidate",
            "task_clue_candidate": {
                "clue_type": "pre_navigation_hint",
                "clue_text": "店招 OCR 可能有助于确认入口",
                "suggested_capability": "ocr",
                "alternative_evidence_only": True,
                "candidate_only": True,
                "not_fact": True,
            },
            "supporting_reason": "sign text may help entrance localization before navigation",
            "confidence_candidate": 0.66,
            "uncertainty": 0.34,
            "alternative_evidence_only": True,
        }

    if mock_scenario == "dryrun_case_b_unknown_indoor_hypothesis":
        return {
            "evidence_type": "scene_hypothesis_candidate",
            "scene_hypothesis_candidate": {
                "scene_hypothesis_candidates": [
                    {
                        "scene_type": "indoor_public_space",
                        "confidence_candidate": 0.4,
                        "candidate_only": True,
                        "not_fact": True,
                    },
                ],
                "candidate_only": True,
                "not_fact": True,
            },
            "supporting_reason": "layout suggests enclosed public area",
            "confidence_candidate": 0.4,
            "uncertainty": 0.4,
            "does_not_override_l1_scene": True,
        }

    if mock_scenario == "dryrun_case_c_navigation_context_challenge":
        return {
            "evidence_type": "task_clue_candidate",
            "task_clue_candidate": {
                "clue_type": "possible_navigation_context",
                "clue_text": "入口可能在右侧通道，导航前可先确认",
                "candidate_only": True,
                "not_fact": True,
            },
            "suggestion_type": "alternative_plan",
            "alternative_plan_goal": "navigate",
            "alternative_strategy": "navigation_support",
            "tools_suggested": ["detection", "depth"],
            "suggestion_text": "possible_navigation_context before OCR",
            "planning_output_optional": {
                "alternative_plan_candidate": {
                    "plan_goal_type": "navigate",
                    "strategy_type": "navigation_support",
                    "tools_suggested": ["detection", "depth"],
                    "suggested_summary": "possible_navigation_context",
                    "does_not_override_selected_plan": True,
                    "candidate_only": True,
                    "not_fact": True,
                },
            },
            "supporting_reason": "spatial layout may benefit navigation context",
            "confidence_candidate": 0.58,
            "uncertainty": 0.42,
        }

    if mock_scenario == "dryrun_case_d_wrong_scene_airport":
        return {
            "evidence_type": "scene_hypothesis_candidate",
            "scene_hypothesis_candidate": {
                "scene_type": "airport_terminal",
                "scene_hypothesis_candidates": [
                    {"scene_type": "airport_terminal", "confidence_candidate": 0.88, "candidate_only": True, "not_fact": True},
                ],
                "candidate_only": True,
                "not_fact": True,
            },
            "proposed_scene_type": "airport_terminal",
            "supporting_reason": "wide hall and signage resemble airport",
            "confidence_candidate": 0.88,
            "uncertainty": 0.12,
            "policy_risk_candidates": ["scene_conflict"],
        }

    if mock_scenario == "dryrun_case_e_unsupported_brand_claim":
        return {
            "evidence_type": "scene_hypothesis_candidate",
            "scene_hypothesis_candidate": {
                "named_entity_claim": "Starbucks",
                "claim_text": "This is Starbucks",
                "candidate_only": True,
                "not_fact": True,
            },
            "unsupported_claim": True,
            "hallucination_risk": True,
            "supporting_ocr_evidence": False,
            "supporting_reason": "brand name asserted without OCR confirmation",
            "confidence_candidate": 0.82,
            "uncertainty": 0.18,
            "policy_risk_candidates": ["unsupported_claim"],
        }

    return {
        "evidence_type": "scene_hypothesis_candidate",
        "scene_hypothesis_candidate": {
            "scene_hypothesis_candidates": [
                {"scene_type": scene, "confidence_candidate": 0.4, "candidate_only": True, "not_fact": True},
            ],
            "candidate_only": True,
            "not_fact": True,
        },
        "supporting_reason": "default deterministic mock",
        "confidence_candidate": 0.4,
        "uncertainty": 0.6,
    }


class QwenVLTeacherAdapter:
  """Qwen-VL Perception Teacher — evidence candidate only, no execution."""

  provider_id = PROVIDER_ID
  provider_label = PROVIDER_LABEL
  teacher_role = TEACHER_ROLE
  planning_only = True
  no_network = True

  def request_teacher_assistance(
      self,
      *,
      teacher_role: str,
      input_evidence: List[Dict[str, Any]],
      required_output_type: str,
      policy_context: Dict[str, Any],
      situation_candidate: Dict[str, Any],
      plan_candidate: Optional[Dict[str, Any]] = None,
      image_reference: Optional[str] = None,
      observation_candidate: Optional[Dict[str, Any]] = None,
      missing_information: Optional[List[Dict[str, Any]]] = None,
      mock_scenario: Optional[str] = None,
  ) -> Dict[str, Any]:
      """
      Request Qwen-VL perception assistance.
      Returns teacher_evidence_candidate — never teacher_result / teacher_fact.
      """
      request_id = _uid("qvr")
      trace_base = [{"stage": "qwen_vl_request", "ref": request_id}]

      if teacher_role in FORBIDDEN_TEACHER_ROLES:
          return {
              "request_id": request_id,
              "admission_status": "rejected",
              "reject_reason": f"role_not_allowed_in_phase:{teacher_role}",
              "teacher_evidence_candidate": None,
              "provider_id": PROVIDER_ID,
              "planning_only": True,
              "no_network": True,
              "no_tool_execution": True,
              "no_runner_invocation": True,
              "no_fact_write": True,
              **candidate_meta(trace_refs=trace_base),
          }

      if teacher_role != TEACHER_ROLE:
          return {
              "request_id": request_id,
              "admission_status": "rejected",
              "reject_reason": f"unsupported_teacher_role:{teacher_role}",
              "teacher_evidence_candidate": None,
              "provider_id": PROVIDER_ID,
              "planning_only": True,
              "no_network": True,
              **candidate_meta(trace_refs=trace_base),
          }

      if required_output_type in FORBIDDEN_OUTPUT_TYPES:
          return {
              "request_id": request_id,
              "admission_status": "rejected",
              "reject_reason": f"forbidden_output_type:{required_output_type}",
              "teacher_evidence_candidate": None,
              "provider_id": PROVIDER_ID,
              "planning_only": True,
              "no_network": True,
              **candidate_meta(trace_refs=trace_base),
          }

      boundary_err = _validate_input_boundary(
          input_evidence=input_evidence,
          policy_context=policy_context,
          situation_candidate=situation_candidate,
      )
      if boundary_err:
          return {
              "request_id": request_id,
              "admission_status": "rejected",
              "reject_reason": boundary_err,
              "teacher_evidence_candidate": None,
              "provider_id": PROVIDER_ID,
              "planning_only": True,
              "no_network": True,
              **candidate_meta(trace_refs=trace_base),
          }

      scenario = mock_scenario or "default"
      mock_out = _mock_perception_output(
          mock_scenario=scenario,
          situation=situation_candidate,
          plan=plan_candidate,
      )

      evidence_id = _uid("qtec")
      evidence_type = mock_out.get("evidence_type", "scene_hypothesis_candidate")
      if evidence_type not in EVIDENCE_TYPES:
          evidence_type = "scene_hypothesis_candidate"

      evidence: Dict[str, Any] = {
          "teacher_id": evidence_id,
          "evidence_id": evidence_id,
          "teacher_provider": PROVIDER_ID,
          "provider_id": PROVIDER_ID,
          "teacher_role": TEACHER_ROLE,
          "evidence_type": evidence_type,
          "output_type": evidence_type,
          "task_type": "perception_assistance",
          "confidence_candidate": mock_out.get("confidence_candidate", 0.5),
          "confidence": mock_out.get("confidence_candidate", 0.5),
          "supporting_reason": mock_out.get("supporting_reason", ""),
          "uncertainty": mock_out.get("uncertainty", 0.5),
          "supporting_evidence": mock_out.get("supporting_evidence", []),
          "conflict_candidates": mock_out.get("conflict_candidates", []),
          "policy_risk_candidates": mock_out.get("policy_risk_candidates", []),
          "scene_hypothesis_candidate": mock_out.get("scene_hypothesis_candidate"),
          "visual_attention_candidate": mock_out.get("visual_attention_candidate"),
          "task_clue_candidate": mock_out.get("task_clue_candidate"),
          "perception_output_optional": {
              "scene_hypothesis_candidates": (
                  (mock_out.get("scene_hypothesis_candidate") or {}).get("scene_hypothesis_candidates")
                  or []
              ),
              "visual_attention_candidate": mock_out.get("visual_attention_candidate"),
              "task_clue_candidate": mock_out.get("task_clue_candidate"),
              "uncertainty": mock_out.get("uncertainty", 0.5),
              "candidate_only": True,
              "not_fact": True,
          },
          "planning_output_optional": mock_out.get("planning_output_optional"),
          "suggestion_type": mock_out.get("suggestion_type"),
          "alternative_plan_goal": mock_out.get("alternative_plan_goal"),
          "alternative_strategy": mock_out.get("alternative_strategy"),
          "proposed_scene_type": mock_out.get("proposed_scene_type"),
          "supports_plan": mock_out.get("supports_plan", False),
          "alternative_evidence_only": mock_out.get("alternative_evidence_only", False),
          "teacher_suggests": mock_out.get("teacher_suggests"),
          "tools_suggested": mock_out.get("tools_suggested", []),
          "suggestion_text": mock_out.get("suggestion_text") or (
              (mock_out.get("task_clue_candidate") or {}).get("clue_text", "")
          ),
          "unsupported_claim": mock_out.get("unsupported_claim", False),
          "hallucination_risk": mock_out.get("hallucination_risk", False),
          "supporting_ocr_evidence": mock_out.get("supporting_ocr_evidence", True),
          "does_not_override_l1_scene": True,
          "does_not_override_l2_selected_plan": True,
          "no_runner_invocation": True,
          "no_fact_write": True,
          "requires_policy_review": True,
          "image_reference": image_reference,
          "observation_candidate_ref": (observation_candidate or {}).get("observation_id"),
          "missing_information_refs": [m.get("info_type") for m in (missing_information or [])],
          "stub_only": True,
          "deterministic_mock": True,
          "no_network": True,
          **candidate_meta(
              trace_refs=trace_base + [
                  {"stage": "qwen_vl_mock", "scenario": scenario},
                  {"stage": "teacher_evidence_candidate", "ref": evidence_id},
              ],
          ),
      }

      return {
          "request_id": request_id,
          "admission_status": "admitted",
          "teacher_role": TEACHER_ROLE,
          "provider_id": PROVIDER_ID,
          "provider_label": PROVIDER_LABEL,
          "teacher_evidence_candidate": evidence,
          "required_output_type": required_output_type,
          "allowed_input_fields_used": [f for f in ALLOWED_INPUT_FIELDS if f in (
              "image_reference" if image_reference else "",
              "situation_candidate",
              "plan_candidate" if plan_candidate else "",
              "observation_candidate" if observation_candidate else "",
          ) if f],
          "planning_only": True,
          "deterministic_mock_only": True,
          "no_network": True,
          "no_tool_execution": True,
          "no_runner_invocation": True,
          "no_fact_write": True,
          "no_direct_training": True,
          "validation_required": True,
          "policy_refs": [POLICY_REF],
          "trace_refs": trace_base + [{"stage": "qwen_vl_response", "ref": evidence_id}],
          **candidate_meta(trace_refs=trace_base),
      }


_default_adapter = QwenVLTeacherAdapter()


def request_teacher_assistance(
    *,
    teacher_role: str,
    input_evidence: List[Dict[str, Any]],
    required_output_type: str,
    policy_context: Dict[str, Any],
    situation_candidate: Dict[str, Any],
    plan_candidate: Optional[Dict[str, Any]] = None,
    image_reference: Optional[str] = None,
    observation_candidate: Optional[Dict[str, Any]] = None,
    missing_information: Optional[List[Dict[str, Any]]] = None,
    mock_scenario: Optional[str] = None,
) -> Dict[str, Any]:
    """Module-level convenience wrapper for QwenVLTeacherAdapter."""
    return _default_adapter.request_teacher_assistance(
        teacher_role=teacher_role,
        input_evidence=input_evidence,
        required_output_type=required_output_type,
        policy_context=policy_context,
        situation_candidate=situation_candidate,
        plan_candidate=plan_candidate,
        image_reference=image_reference,
        observation_candidate=observation_candidate,
        missing_information=missing_information,
        mock_scenario=mock_scenario,
    )
