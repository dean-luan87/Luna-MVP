from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.navigation_manager.module.navigation_manager_module_types_v1 import (
    not_fact,
)


def build_navigation_guidance_candidate_v1(
    input_candidate: Mapping[str, Any],
    crossing_assessment: Mapping[str, Any],
    obstacle_assessment: Mapping[str, Any],
    deviation_assessment: Mapping[str, Any],
) -> Dict[str, Any]:
    crossing = crossing_assessment.get("crossing_assessment") or {}
    obstacle = obstacle_assessment.get("obstacle_risk_assessment") or {}
    deviation = deviation_assessment.get("deviation_assessment") or {}

    guidance_type = "continue"
    if bool(deviation.get("deviation_detected")):
        guidance_type = "reroute_candidate"
    elif bool(crossing.get("waiting_required")):
        guidance_type = "wait"
    elif bool(obstacle.get("attention_required")):
        guidance_type = "avoid"

    return {
        "schema_version": "navigation_manager_guidance_candidate_builder_v1",
        "guidance_candidate": {
            "candidate_id": f"guidance_{input_candidate.get('navigation_request_id')}",
            "guidance_type": guidance_type,
            "guidance_text_candidate": "请保持当前方向并根据前方环境调整步速。"
            if guidance_type == "continue"
            else (
                "检测到偏航，建议按候选路径重新对齐。"
                if guidance_type == "reroute_candidate"
                else (
                    "检测到过街风险，请先等待安全通行信号。"
                    if guidance_type == "wait"
                    else "前方存在障碍风险，建议绕行并保持安全距离。"
                )
            ),
            "candidate_only": True,
            **not_fact(),
        },
        **not_fact(),
    }
