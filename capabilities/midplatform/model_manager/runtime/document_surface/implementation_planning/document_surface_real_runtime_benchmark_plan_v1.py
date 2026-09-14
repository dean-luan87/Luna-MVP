# -*- coding: utf-8 -*-
"""Document Surface — real runtime benchmark plan v1."""

from __future__ import annotations

from typing import Any, Dict, List

BENCHMARK_METRICS: List[Dict[str, Any]] = [
    {
        "metric_id": "surface_detection_candidate_rate",
        "description": "成功输出 surface candidate 的比例",
        "target_direction": "monitor",
        "accuracy_only": False,
    },
    {
        "metric_id": "false_surface_candidate_rate",
        "description": "假阳性 surface candidate 比例",
        "target_direction": "minimize",
        "accuracy_only": False,
    },
    {
        "metric_id": "overlap_relation_candidate_rate",
        "description": "重叠关系 hint 输出率",
        "target_direction": "monitor",
        "accuracy_only": False,
    },
    {
        "metric_id": "occlusion_hint_candidate_rate",
        "description": "遮挡 hint 输出率",
        "target_direction": "monitor",
        "accuracy_only": False,
    },
    {
        "metric_id": "attention_blocked_runtime_call_rate",
        "description": "blocked 区域 runtime 调用率",
        "target_value": 0,
        "accuracy_only": False,
    },
    {
        "metric_id": "no_ocr_leak_rate",
        "description": "无 OCR 泄漏合规率",
        "target_value": 1,
        "accuracy_only": False,
    },
    {
        "metric_id": "candidate_only_compliance_rate",
        "description": "candidate_only 合规率",
        "target_value": 1,
        "accuracy_only": False,
    },
    {
        "metric_id": "runtime_error_handling_rate",
        "description": "runtime error 正确返回率",
        "target_direction": "maximize",
        "accuracy_only": False,
    },
    {
        "metric_id": "ownership_package_compatibility_rate",
        "description": "Ownership Evidence Package 兼容率",
        "target_direction": "maximize",
        "accuracy_only": False,
    },
    {
        "metric_id": "text_owner_assignment_ready_rate",
        "description": "text owner assignment 就绪率",
        "target_direction": "monitor",
        "accuracy_only": False,
    },
]


def build_benchmark_plan() -> Dict[str, Any]:
    non_accuracy = [m for m in BENCHMARK_METRICS if not m.get("accuracy_only")]
    return {
        "plan_id": "document_surface_benchmark_plan_v1",
        "metric_count": len(BENCHMARK_METRICS),
        "metrics": BENCHMARK_METRICS,
        "non_accuracy_only_metrics": len(non_accuracy) == len(BENCHMARK_METRICS),
        "includes_efficiency_and_boundary_compliance": True,
        "includes_ownership_compatibility": True,
        "includes_no_ocr_leak": True,
        "planning_only": True,
        "candidate_only": True,
        "not_fact": True,
    }
