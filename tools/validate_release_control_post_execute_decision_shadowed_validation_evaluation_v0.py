# -*- coding: utf-8 -*-
"""Phase-Next-165: Shadowed validation/evaluation for Phase-Next-164.

NOTE: 原计划的超长文件名在 macOS 上超过文件名长度上限（255），因此采用本短文件名承载同等功能。
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)


@dataclass(frozen=True)
class ScenarioResult:
    scenario_name: str
    expected_outcome: Dict[str, Any]
    actual_outcome: Dict[str, Any]
    explicit_decision_entry_seen: bool
    execute_closed_seen: bool
    side_effects_released_false_seen: bool
    execute_legality_seen: bool
    evidence_complete_seen: bool
    boundary_violation_seen: bool
    allowed_outcome_selected: Optional[str]
    forbidden_outcome_blocked: bool
    human_confirmation_required: bool
    requires_new_governance_definition: bool
    allows_retry_now: bool
    closed_safe_state_preserved: bool
    illegal_state_detected: bool
    pass_or_fail: str
    evaluation_reason_codes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            'scenario_name': self.scenario_name,
            'expected_outcome': dict(self.expected_outcome),
            'actual_outcome': dict(self.actual_outcome),
            'explicit_decision_entry_seen': bool(self.explicit_decision_entry_seen),
            'execute_closed_seen': bool(self.execute_closed_seen),
            'side_effects_released_false_seen': bool(self.side_effects_released_false_seen),
            'execute_legality_seen': bool(self.execute_legality_seen),
            'evidence_complete_seen': bool(self.evidence_complete_seen),
            'boundary_violation_seen': bool(self.boundary_violation_seen),
            'allowed_outcome_selected': self.allowed_outcome_selected,
            'forbidden_outcome_blocked': bool(self.forbidden_outcome_blocked),
            'human_confirmation_required': bool(self.human_confirmation_required),
            'requires_new_governance_definition': bool(self.requires_new_governance_definition),
            'allows_retry_now': bool(self.allows_retry_now),
            'closed_safe_state_preserved': bool(self.closed_safe_state_preserved),
            'illegal_state_detected': bool(self.illegal_state_detected),
            'pass_or_fail': str(self.pass_or_fail),
            'evaluation_reason_codes': list(self.evaluation_reason_codes),
        }


def _mk_execute_result(*, closed=True, se_false=True, status='real_trial_execute_success', reason='ok', abort_trigger_id=None, stop_trigger_id=None, trace_ok=True) -> dict:
    return {
        'ok': True,
        'status': status,
        'reason': reason,
        'payload': {
            'state': {
                'closed': bool(closed),
                'side_effects_released': False if se_false else True,
                'abort_trigger_id': abort_trigger_id,
                'stop_trigger_id': stop_trigger_id,
            },
            'trace': {'order': ['x'] if trace_ok else []},
        },
    }


def _summarize(out: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    payload = out.get('payload') if isinstance(out, dict) else None
    payload = payload if isinstance(payload, dict) else {}
    state = payload.get('state') if isinstance(payload.get('state'), dict) else {}
    trace = payload.get('trace') if isinstance(payload.get('trace'), dict) else {}

    observed = {
        'explicit_decision_entry_seen': bool(state.get('explicit_decision_entry_seen') is True),
        'execute_closed_seen': bool(state.get('execute_closed_seen') is True),
        'side_effects_released_false_seen': bool(state.get('side_effects_released_false_seen') is True),
        'execute_legality_seen': bool(state.get('execute_legality_seen') is True),
        'evidence_complete_seen': bool(state.get('evidence_complete_seen') is True),
        'boundary_violation_seen': bool(state.get('boundary_violation_seen') is True),
        'allowed_outcome_selected': state.get('allowed_outcome_selected'),
        'forbidden_outcome_blocked': bool(state.get('forbidden_outcome_blocked') is True),
        'human_confirmation_required': bool(state.get('human_confirmation_required') is True),
        'requires_new_governance_definition': bool(state.get('requires_new_governance_definition') is True),
        'allows_retry_now': bool(state.get('allows_retry_now') is True),
        'closed_safe_state_preserved': bool(state.get('closed_safe_state_preserved') is True),
        'illegal_state_detected': bool(state.get('illegal_state_detected') is True),
        'decision_completed': bool(state.get('decision_completed') is True),
    }

    actual = {
        'ok': bool(out.get('ok') is True) if isinstance(out, dict) else False,
        'status': str(out.get('status') or '') if isinstance(out, dict) else 'non_dict',
        'reason': str(out.get('reason') or '') if isinstance(out, dict) else 'non_dict',
        'allowed_outcome_selected': state.get('allowed_outcome_selected'),
        'state': dict(state),
        'trace_order': list(trace.get('order') or []) if isinstance(trace.get('order'), list) else [],
    }
    return actual, observed


def _run_scenario(*, name: str, expected: Dict[str, Any], run_fn: Callable[[], Dict[str, Any]]) -> ScenarioResult:
    out = run_fn()
    actual, obs = _summarize(out)

    reason_codes: List[str] = []
    passed = True

    def _chk_bool(key: str, actual_val: Any):
        nonlocal passed
        exp = expected.get(key)
        if exp is None:
            return
        if bool(exp) != bool(actual_val):
            passed = False
            reason_codes.append(f'mismatch_{key}')

    def _chk_str(key: str, actual_val: Any):
        nonlocal passed
        exp = expected.get(key)
        if exp is None:
            return
        if str(exp) != str(actual_val):
            passed = False
            reason_codes.append(f'mismatch_{key}')

    _chk_str('status', actual.get('status'))
    _chk_str('allowed_outcome_selected', obs.get('allowed_outcome_selected'))

    _chk_bool('explicit_decision_entry_seen', obs.get('explicit_decision_entry_seen'))
    _chk_bool('execute_closed_seen', obs.get('execute_closed_seen'))
    _chk_bool('side_effects_released_false_seen', obs.get('side_effects_released_false_seen'))
    _chk_bool('execute_legality_seen', obs.get('execute_legality_seen'))
    _chk_bool('evidence_complete_seen', obs.get('evidence_complete_seen'))
    _chk_bool('boundary_violation_seen', obs.get('boundary_violation_seen'))
    _chk_bool('forbidden_outcome_blocked', obs.get('forbidden_outcome_blocked'))
    _chk_bool('human_confirmation_required', obs.get('human_confirmation_required'))
    _chk_bool('requires_new_governance_definition', obs.get('requires_new_governance_definition'))
    _chk_bool('allows_retry_now', obs.get('allows_retry_now'))
    _chk_bool('closed_safe_state_preserved', obs.get('closed_safe_state_preserved'))
    _chk_bool('illegal_state_detected', obs.get('illegal_state_detected'))

    if obs.get('closed_safe_state_preserved') is not True:
        passed = False
        reason_codes.append('closed_safe_state_not_preserved')
    if obs.get('allows_retry_now') is True:
        passed = False
        reason_codes.append('auto_retry_detected')
    if obs.get('decision_completed') is not True:
        passed = False
        reason_codes.append('decision_not_completed')

    return ScenarioResult(
        scenario_name=name,
        expected_outcome=dict(expected),
        actual_outcome=dict(actual),
        explicit_decision_entry_seen=bool(obs.get('explicit_decision_entry_seen')),
        execute_closed_seen=bool(obs.get('execute_closed_seen')),
        side_effects_released_false_seen=bool(obs.get('side_effects_released_false_seen')),
        execute_legality_seen=bool(obs.get('execute_legality_seen')),
        evidence_complete_seen=bool(obs.get('evidence_complete_seen')),
        boundary_violation_seen=bool(obs.get('boundary_violation_seen')),
        allowed_outcome_selected=obs.get('allowed_outcome_selected'),
        forbidden_outcome_blocked=bool(obs.get('forbidden_outcome_blocked')),
        human_confirmation_required=bool(obs.get('human_confirmation_required')),
        requires_new_governance_definition=bool(obs.get('requires_new_governance_definition')),
        allows_retry_now=bool(obs.get('allows_retry_now')),
        closed_safe_state_preserved=bool(obs.get('closed_safe_state_preserved')),
        illegal_state_detected=bool(obs.get('illegal_state_detected')),
        pass_or_fail='pass' if passed else 'fail',
        evaluation_reason_codes=reason_codes,
    )


def main() -> int:
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_real_trial_post_execute_decision_v0 import (
        run_first_controlled_short_window_real_trial_post_execute_decision_v0,
    )

    from tools.verify_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_real_trial_post_execute_decision_v0 import (
        main as verifier_main,
    )

    if int(verifier_main()) != 0:
        raise SystemExit(2)

    base = dict(
        explicit_post_execute_decision_entry_v0={'intent': True},
        execute_result_v0=_mk_execute_result(),
        execute_go_no_go_pack_v0={'overall_evaluation': 'go'},
        post_execute_decision_definition_v0={'frozen': '163'},
        context={'phase': 'p165'},
    )

    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_real_trial_post_execute_decision_v0 import (
        run_first_controlled_short_window_real_trial_post_execute_decision_v0 as run,
    )

    results: List[ScenarioResult] = []

    b_a = dict(base); b_a['execute_result_v0'] = _mk_execute_result(closed=False)
    results.append(_run_scenario(name='A.no_legal_final_close', expected={'status':'not_eligible','allowed_outcome_selected':'remain_closed_safe','execute_closed_seen':False}, run_fn=lambda: run(**b_a)))

    b_b = dict(base); b_b['execute_result_v0'] = _mk_execute_result(se_false=False)
    results.append(_run_scenario(name='B.se_not_false', expected={'status':'not_eligible','allowed_outcome_selected':'remain_closed_safe','side_effects_released_false_seen':False}, run_fn=lambda: run(**b_b)))

    b_c = dict(base); b_c['execute_result_v0'] = _mk_execute_result(trace_ok=False)
    results.append(_run_scenario(name='C.evidence_incomplete', expected={'status':'decided','allowed_outcome_selected':'remain_closed_safe','evidence_complete_seen':False}, run_fn=lambda: run(**b_c)))

    results.append(_run_scenario(name='D.clean_success_case', expected={'status':'decided','allowed_outcome_selected':'retry_allowed_under_same_guardrails','human_confirmation_required':True,'allows_retry_now':False,'closed_safe_state_preserved':True}, run_fn=lambda: run(**base)))

    b_e = dict(base); b_e['execute_result_v0'] = _mk_execute_result(abort_trigger_id='unauthorized_side_effect_surface')
    results.append(_run_scenario(name='E.boundary_violation_case', expected={'status':'decided','allowed_outcome_selected':'retry_not_allowed_until_new_definition','requires_new_governance_definition':True,'boundary_violation_seen':True}, run_fn=lambda: run(**b_e)))

    b_f = dict(base); b_f['explicit_post_execute_decision_entry_v0'] = {'intent': True, 'widening_needed': True}
    results.append(_run_scenario(name='F.widening_needed_case', expected={'status':'decided','allowed_outcome_selected':'escalate_for_new_governance_definition','requires_new_governance_definition':True}, run_fn=lambda: run(**b_f)))

    for nm, probe in [
        ('G.forbidden_reopen_probe','implicit_reopen'),
        ('H.forbidden_retry_probe','implicit_execute_retry'),
        ('I.forbidden_widen_probe','implicit_widening'),
        ('L.forbidden_full_trial_continuation_probe','implicit_full_trial_continuation'),
        ('M.forbidden_default_on_transition_probe','implicit_default_on_transition'),
    ]:
        b = dict(base)
        b['explicit_post_execute_decision_entry_v0'] = {'intent': True, 'requested_forbidden_outcome_probe': probe}
        results.append(_run_scenario(name=nm, expected={'status':'blocked','allowed_outcome_selected':'remain_closed_safe','forbidden_outcome_blocked':True}, run_fn=lambda b=b: run(**b)))

    b_j = dict(base); b_j['explicit_post_execute_decision_entry_v0'] = None
    results.append(_run_scenario(name='J.default_path_probe', expected={'status':'blocked','allowed_outcome_selected':'remain_closed_safe','explicit_decision_entry_seen':False}, run_fn=lambda: run(**b_j)))

    b_k = dict(base); b_k['explicit_post_execute_decision_entry_v0'] = {'intent': True, 'structural_safety_issue': True}
    results.append(_run_scenario(name='K.structural_safety_issue', expected={'status':'decided','allowed_outcome_selected':'stop_and_block_further_real_action','requires_new_governance_definition':True}, run_fn=lambda: run(**b_k)))

    total = len(results)
    passed = sum(1 for r in results if r.pass_or_fail == 'pass')
    failed = total - passed

    entry_gate_integrity = all(r.pass_or_fail=='pass' for r in results if r.scenario_name in {'J.default_path_probe'})
    final_close_prereq_integrity = all(r.pass_or_fail=='pass' for r in results if r.scenario_name in {'A.no_legal_final_close','B.se_not_false'})
    allowed_outcome_integrity = all(r.pass_or_fail=='pass' for r in results if r.scenario_name in {'C.evidence_incomplete','D.clean_success_case','E.boundary_violation_case','F.widening_needed_case','K.structural_safety_issue'})
    forbidden_block_integrity = all(r.pass_or_fail=='pass' for r in results if r.scenario_name.startswith(('G.','H.','I.','L.','M.')))
    closed_safe_state_integrity = all(r.closed_safe_state_preserved is True for r in results)
    no_auto_retry_integrity = all(r.allows_retry_now is False for r in results)

    overall = 'go' if failed==0 else 'no_go'
    next_step = 'consider Phase-Next-166 post-execute decision go/no-go pack v0' if overall=='go' else 'fix validation failures before any go/no-go pack'

    report = {
        'total_scenarios': total,
        'passed_scenarios': passed,
        'failed_scenarios': failed,
        'entry_gate_integrity': bool(entry_gate_integrity),
        'final_close_prerequisite_integrity': bool(final_close_prereq_integrity),
        'allowed_outcome_integrity': bool(allowed_outcome_integrity),
        'forbidden_block_integrity': bool(forbidden_block_integrity),
        'closed_safe_state_integrity': bool(closed_safe_state_integrity),
        'no_auto_retry_integrity': bool(no_auto_retry_integrity),
        'overall_evaluation': overall,
        'recommended_next_step': next_step,
        'scenarios': [r.to_dict() for r in results],
    }

    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if overall in ('go','conditional_go') else 3


if __name__ == '__main__':
    raise SystemExit(main())
