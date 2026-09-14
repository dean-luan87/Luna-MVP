# -*- coding: utf-8 -*-
"""Phase-Next-166 (optional): Read-only post-execute decision pack summary builder.

短文件名说明：tools 目录在当前工作区是符号链接，且超长文件名可能触发 macOS 文件名长度上限。
本工具用短文件名承载与长命名等价的“只读证据指针汇总”功能。
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class ArtifactRef:
    phase: str
    kind: str
    path: str
    note: str

    def to_dict(self) -> Dict[str, Any]:
        return {'phase': self.phase, 'kind': self.kind, 'path': self.path, 'note': self.note}


def build_summary_v0() -> Dict[str, Any]:
    artifacts: List[ArtifactRef] = [
        ArtifactRef('151','doc','docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_MINIMAL_REAL_ENABLEMENT_DEFINITION_V0.md','close 后 se=false 基础边界'),
        ArtifactRef('155','doc','docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_TRIAL_GUARDRAIL_DEFINITION_V0.md','short-window guardrail 冻结'),
        ArtifactRef('162','doc','docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_EXECUTE_GO_NO_GO_PACK_V0.md','execute pack = go'),
        ArtifactRef('163','doc','docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_POST_EXECUTE_DECISION_DEFINITION_V0.md','post-execute decision 宪法冻结'),
        ArtifactRef('164','code','capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_real_trial_post_execute_decision_v0.py','post-execute decision runtime（只读治理性）'),
        ArtifactRef('165','tool','tools/validate_release_control_post_execute_decision_shadowed_validation_evaluation_v0.py','post-execute decision shadowed validation = go'),
        ArtifactRef('166','doc','docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_POST_EXECUTE_DECISION_GO_NO_GO_PACK_V0.md','post-execute decision go/no-go pack（本阶段）'),
        ArtifactRef('166','doc','docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_POST_EXECUTE_DECISION_EVIDENCE_MATRIX_V0.md','decision evidence matrix'),
        ArtifactRef('166','doc','docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_POST_EXECUTE_DECISION_BLOCKER_AND_ALLOWLIST_V0.md','decision blocker & allowlist'),
    ]

    return {
        'pack_id': 'phase_next_166_post_execute_decision_go_no_go_pack_v0',
        'overall_recommendation': 'go',
        'scope': 'decision-legality-to-post-decision-governance-chain (not retry/reopen; not default-on; not full controlled trial; not full release)',
        'non_goals': [
            'no_new_runtime_main_implementation',
            'no_default_path',
            'no_retry_runtime',
            'no_reopen_runtime',
            'no_full_controlled_trial',
            'no_side_effect_surface_expansion',
        ],
        'hard_blockers': [],
        'soft_followups': [
            'archive_phase_165_structured_json_output_as_pack_attachment',
            'tighten_reason_code_consistency_for_post_decision_governance_chain_docs',
            'add_runbook_checklist_for_human_confirmation_and_evidence_review (non-runtime)',
        ],
        'artifacts': [a.to_dict() for a in artifacts],
    }


def main() -> int:
    print(json.dumps(build_summary_v0(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
