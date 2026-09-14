# -*- coding: utf-8 -*-
"""
Phase-Next-162 (optional):
Read-only execute pack summary builder.

目标：
- 从 151/155/158/159/160/161 的“既有产物”中抽取结构化摘要（路径级证据指针）。
- 不触发任何真实副作用；不运行真实 full controlled trial；不 default-on。

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
            phase="155",
            kind="doc",
            path="docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_TRIAL_GUARDRAIL_DEFINITION_V0.md",
            note="短窗试运行护栏宪法冻结（allow/deny + abort/recovery/final close）",
        ),
        ArtifactRef(
            phase="158",
            kind="doc",
            path="docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_READINESS_GO_NO_GO_PACK_V0.md",
            note="readiness go/no-go pack = go",
        ),
        ArtifactRef(
            phase="159",
            kind="doc",
            path="docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_EXECUTE_DEFINITION_V0.md",
            note="execute definition 宪法冻结（execute≠readiness；唯一进入条件；stop/final close）",
        ),
        ArtifactRef(
            phase="160",
            kind="code",
            path="capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_real_trial_execute_v0.py",
            note="first real trial execute runtime（显式入口+intent+approval+readiness_go+强制收口）",
        ),
        ArtifactRef(
            phase="161",
            kind="tool",
            path="tools/validate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_real_trial_execute_shadowed_validation_evaluation_v0.py",
            note="execute shadowed validation/evaluation（A–M 场景）= go",
        ),
        ArtifactRef(
            phase="162",
            kind="doc",
            path="docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_EXECUTE_GO_NO_GO_PACK_V0.md",
            note="execute go/no-go pack（本阶段主文档）",
        ),
        ArtifactRef(
            phase="162",
            kind="doc",
            path="docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_EXECUTE_EVIDENCE_MATRIX_V0.md",
            note="execute evidence matrix（151/155/158/159/160/161 证据矩阵）",
        ),
        ArtifactRef(
            phase="162",
            kind="doc",
            path="docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_EXECUTE_BLOCKER_AND_ALLOWLIST_V0.md",
            note="execute blocker & allowlist（下一阶段白/黑名单与阻断项定义）",
        ),
    ]

    summary = {
        "pack_id": "phase_next_162_first_controlled_short_window_real_trial_execute_go_no_go_pack_v0",
        "overall_recommendation": "go",
        "scope": "execute-legality-to-post-execute-decision-chain (not default-on; not full controlled trial; not full release)",
        "non_goals": [
            "no_new_runtime_main_implementation",
            "no_default_path",
            "no_full_controlled_trial",
            "no_side_effect_surface_expansion",
        ],
        "hard_blockers": [],
        "soft_followups": [
            "archive_phase_161_structured_json_output_as_pack_attachment",
            "tighten_reason_code_consistency_for_post_execute_decision_chain_docs",
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

