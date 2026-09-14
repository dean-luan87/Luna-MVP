import pytest


from decision_monitor.evidence_ledger import EvidenceLedger, EvidenceLedgerEntry
from decision_monitor.hypothesis_layer import Hypothesis, HypothesisLayer
from decision_monitor.confirmation_input_bridge import ConfirmationInputBridgeResult
from decision_monitor.evidence_hypothesis_whitebox_trace import build_evidence_hypothesis_whitebox_trace


def _ledger_container():
    return EvidenceLedger(
        entries=[
            EvidenceLedgerEntry(
                claim_summary="容器候选：cup | 目标疑似在容器内（object_search_hint）",
                supporting_evidence=["vision:container=cup", "vision:target=bottle_in_container"],
                missing_evidence=["需要打开容器确认"],
                evidence_confidence=0.72,
            ),
            EvidenceLedgerEntry(
                claim_summary="当前主要空间结构：前方可通行主区成立",
                supporting_evidence=["traversable ..."],
                evidence_confidence=0.55,
            ),
        ]
    )


def _ledger_occlusion():
    return EvidenceLedger(
        entries=[
            EvidenceLedgerEntry(
                claim_summary="遮挡候选：cup | 目标与容器显著重叠，疑似遮挡（object_search_hint）",
                supporting_evidence=["vision:overlap_ratio=0.40"],
                missing_evidence=["需要清理遮挡或调整视角复核目标"],
                evidence_confidence=0.62,
            )
        ]
    )


def test_container_evidence_hypothesis_has_alignment_bonus_and_exclusion():
    ledger = _ledger_container()
    layer = HypothesisLayer(
        hypotheses=[
            Hypothesis(
                hypothesis_summary="cup",
                hypothesis_type="container_candidate",
                hypothesis_confidence=0.65,
            ),
            Hypothesis(
                hypothesis_summary="遮挡候选",
                hypothesis_type="occluded_object_candidate",
                hypothesis_confidence=0.35,
            ),
        ],
        dominant_hypothesis_type="container_candidate",
        hypothesis_reason_summary="dominant=navigation n=2",
    )
    out = build_evidence_hypothesis_whitebox_trace(evidence_ledger=ledger, hypothesis_layer=layer)
    assert out.whitebox_applied is True
    assert len(out.reasoning_steps) >= 3
    assert len(out.weight_allocation) >= 2
    # container should have container_alignment_bonus
    c = next((w for w in out.weight_allocation if w.candidate_id == "container_candidate"), None)
    assert c is not None
    assert "container_alignment_bonus" in c.weight_components
    assert len(out.exclusion_log) >= 1


def test_occlusion_evidence_hypothesis_has_alignment_bonus():
    ledger = _ledger_occlusion()
    layer = HypothesisLayer(
        hypotheses=[
            Hypothesis(
                hypothesis_summary="目标或交互对象可能被遮挡",
                hypothesis_type="occluded_object_candidate",
                hypothesis_confidence=0.50,
            ),
            Hypothesis(
                hypothesis_summary="路径延续",
                hypothesis_type="path_continuation_candidate",
                hypothesis_confidence=0.30,
            ),
        ],
        dominant_hypothesis_type="occluded_object_candidate",
    )
    out = build_evidence_hypothesis_whitebox_trace(evidence_ledger=ledger, hypothesis_layer=layer)
    o = next((w for w in out.weight_allocation if w.candidate_id == "occluded_object_candidate"), None)
    assert o is not None
    assert "occlusion_alignment_bonus" in o.weight_components


def test_feedback_can_penalize_container_hypothesis_weight():
    ledger = _ledger_container()
    layer = HypothesisLayer(
        hypotheses=[
            Hypothesis(
                hypothesis_summary="cup",
                hypothesis_type="container_candidate",
                hypothesis_confidence=0.65,
            ),
            Hypothesis(
                hypothesis_summary="遮挡候选",
                hypothesis_type="occluded_object_candidate",
                hypothesis_confidence=0.35,
            ),
        ],
        dominant_hypothesis_type="container_candidate",
    )
    cib = ConfirmationInputBridgeResult(
        confirmation_input_type="opened_container",
        confirmation_input_raw_text="我打开了，没有",
    )
    out = build_evidence_hypothesis_whitebox_trace(evidence_ledger=ledger, hypothesis_layer=layer, confirmation_input_bridge=cib)
    c = next((w for w in out.weight_allocation if w.candidate_id == "container_candidate"), None)
    assert c is not None
    assert "user_denied_penalty" in c.weight_components
    assert out.interaction_trace and out.interaction_trace[0].mapped_confirmation_type == "opened_container"


def test_user_visible_explanation_exists():
    ledger = _ledger_container()
    layer = HypothesisLayer(hypotheses=[], dominant_hypothesis_type=None)
    out = build_evidence_hypothesis_whitebox_trace(evidence_ledger=ledger, hypothesis_layer=layer)
    assert out.user_visible_explanation is not None
    assert out.user_visible_explanation.user_visible_reason_evidence

