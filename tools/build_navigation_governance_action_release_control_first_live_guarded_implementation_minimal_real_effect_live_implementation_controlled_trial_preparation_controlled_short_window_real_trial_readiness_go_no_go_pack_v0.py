# -*- coding: utf-8 -*-
"""
Phase-Next-158 (optional):
Read-only pack summary builder.

目标：
- 从 151–157 的“既有产物”中抽取结构化摘要（路径级证据指针）。
- 不触发任何真实副作用；不运行真实 short-window trial execute。

说明：
- v0 仅做“证据指针 + 结论摘要”输出（JSON），不尝试解析全部文档内容。
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)


@dataclass(frozen=True)
class ArtifactRef:
    phase: str
    kind: str  # doc | code | tool
    path: str
    note: str

    def to_dict(self) -> Dict[str, Any]:
        return {"phase": self.phase, "kind": self.kind, "path": self.path, "note": self.note}


def build_summary_v0() -> Dict[str, Any]:
    artifacts: List[ArtifactRef] = [
        ArtifactRef(
            phase="151",
            kind="doc",
            path="docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_MINIMAL_REAL_ENABLEMENT_DEFINITION_V0.md",
            note="冻结 started/release/closure 边界（start_event_observed 唯一 started 判据）",
        ),
        ArtifactRef(
            phase="152",
            kind="code",
            path="capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_minimal_real_enablement_v0.py",
            note="minimal real enablement runtime（短时 se 窗口 + 强制 closure）",
        ),
        ArtifactRef(
            phase="153",
            kind="doc",
            path="docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_MINIMAL_REAL_ENABLEMENT_SHADOWED_LIVE_VALIDATION_EVALUATION_V0.md",
            note="minimal enablement shadowed validation/evaluation = go",
        ),
        ArtifactRef(
            phase="154",
            kind="doc",
            path="docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_MINIMAL_REAL_ENABLEMENT_CONTROLLED_SHORT_WINDOW_TRIAL_PREPARATION_GO_NO_GO_PACK_V0.md",
            note="short-window trial preparation go/no-go pack = go",
        ),
        ArtifactRef(
            phase="155",
            kind="doc",
            path="docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_TRIAL_GUARDRAIL_DEFINITION_V0.md",
            note="短窗试运行护栏宪法冻结（allow/deny + abort/recovery/closure）",
        ),
        ArtifactRef(
            phase="156",
            kind="code",
            path="capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_trial_v0.py",
            note="first controlled short-window trial runtime（带护栏执行器）",
        ),
        ArtifactRef(
            phase="157",
            kind="tool",
            path="tools/validate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_trial_shadowed_validation_evaluation_v0.py",
            note="short-window trial shadowed validation/evaluation（A–K 场景）= go",
        ),
        ArtifactRef(
            phase="158",
            kind="doc",
            path="docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_READINESS_GO_NO_GO_PACK_V0.md",
            note="readiness go/no-go pack（本阶段主文档）",
        ),
        ArtifactRef(
            phase="158",
            kind="doc",
            path="docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_READINESS_EVIDENCE_MATRIX_V0.md",
            note="readiness evidence matrix（151–157 证据矩阵）",
        ),
        ArtifactRef(
            phase="158",
            kind="doc",
            path="docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_READINESS_BLOCKER_AND_ALLOWLIST_V0.md",
            note="readiness blocker & allowlist（下一阶段白/黑名单与阻断项定义）",
        ),
    ]

    summary = {
        "pack_id": "phase_next_158_controlled_short_window_real_trial_readiness_go_no_go_pack_v0",
        "overall_recommendation": "go",
        "scope": "readiness-only (not execute; not default-on; not full controlled trial)",
        "non_goals": [
            "no_new_runtime_main_implementation",
            "no_default_path",
            "no_real_trial_execute",
            "no_full_controlled_trial",
            "no_side_effect_surface_expansion",
        ],
        "hard_blockers": [],
        "soft_followups": [
            "archive_phase_157_structured_json_output_as_pack_attachment",
            "tighten_reason_code_consistency_for_next_phase_execute_definition_docs",
            "add_runbook_checklist_for_human_confirmation_attempt_limit_time_limit (non-runtime)",
        ],
        "artifacts": [a.to_dict() for a in artifacts],
    }
    return summary


def main() -> int:
    print(json.dumps(build_summary_v0(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

