from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from capabilities.evaluation.a_route_information_need_formation.engine_v1 import ARouteInformationNeedFormationEvaluationEngineV1
from capabilities.evaluation.a_route_information_need_formation.verifier_v1 import verify as verify_r01
from capabilities.evaluation.a_route_minimum_relevant_cognitive_view.engine_v1 import ARouteMinimumRelevantCognitiveViewEvaluationEngineV1
from capabilities.evaluation.a_route_minimum_relevant_cognitive_view.verifier_v1 import verify as verify_r02
from capabilities.evaluation.a_route_required_cognitive_condition_formation.verifier_v1 import verify as verify_r03
from capabilities.evaluation.cognitive_branch_governance.engine_v1 import CognitiveBranchGovernanceEvaluationEngineV1
from capabilities.evaluation.cognitive_branch_governance.verifier_v1 import verify as verify_r04
from capabilities.evaluation.cognitive_requirement_alternative_satisfaction_basis.engine_v1 import CognitiveRequirementAlternativeSatisfactionBasisEvaluationEngineV1
from capabilities.evaluation.cognitive_requirement_alternative_satisfaction_basis.verifier_v1 import verify as verify_r05
from capabilities.evaluation.governed_cognitive_branch_formation.engine_v1 import GovernedCognitiveBranchFormationEvaluationEngineV1
from capabilities.evaluation.governed_cognitive_branch_formation.verifier_v1 import verify as verify_r06
from capabilities.evaluation.information_acquisition_strategy_candidate_formation.engine_v1 import InformationAcquisitionStrategyFormationEvaluationEngineV1
from capabilities.evaluation.information_acquisition_strategy_candidate_formation.verifier_v1 import verify as verify_r07
from capabilities.evaluation.observation_perception_routing_controlled.engine_v1 import PerceptionRoutingEvaluationEngineV1
from capabilities.evaluation.observation_perception_routing_controlled.verifier_v1 import verify as verify_r08
from capabilities.evaluation.perception_routing_admission_compatibility_controlled.engine_v1 import PerceptionRoutingAdmissionCompatibilityEvaluationEngineV1
from capabilities.evaluation.perception_routing_admission_compatibility_controlled.verifier_v1 import verify as verify_r09
from capabilities.evaluation.perception_provider_runtime_target_preparation_controlled.engine_v1 import ProviderRuntimeTargetPreparationEvaluationEngineV1
from capabilities.evaluation.perception_provider_runtime_target_preparation_controlled.verifier_v1 import verify as verify_r10
from capabilities.evaluation.perception_routing_admission_order_adjudication_controlled.engine_v1 import build_runtime_admission_order_summary_v1
from capabilities.evaluation.perception_routing_admission_order_adjudication_controlled.verifier_v1 import verify as verify_r11
from capabilities.evaluation.strategy_coordination_controlled.engine_v1 import StrategyCoordinationEvaluationEngineV1
from capabilities.evaluation.strategy_coordination_controlled.verifier_v1 import verify as verify_r12
from capabilities.evaluation.evidence_context_field_current_world_controlled.engine_v1 import EvidenceContextFieldCurrentWorldControlledEngineV1
from capabilities.evaluation.evidence_context_field_current_world_controlled.verifier_v1 import verify as verify_r13


ROOT = Path(__file__).resolve().parents[2]


def _artifact(name: str) -> dict:
    return json.loads((ROOT / "_eval_out" / name / "runner_summary_v1.json").read_text(encoding="utf-8"))


def _r03() -> dict:
    return _artifact("a_route_required_cognitive_condition_formation_v1")


SURFACES = (
    ("R01", lambda: ARouteInformationNeedFormationEvaluationEngineV1().run(), verify_r01),
    ("R02", lambda: ARouteMinimumRelevantCognitiveViewEvaluationEngineV1().run(), verify_r02),
    ("R03", _r03, verify_r03),
    ("R04", lambda: CognitiveBranchGovernanceEvaluationEngineV1().run(), verify_r04),
    ("R05", lambda: CognitiveRequirementAlternativeSatisfactionBasisEvaluationEngineV1().run(), verify_r05),
    ("R06", lambda: GovernedCognitiveBranchFormationEvaluationEngineV1().run(), verify_r06),
    ("R07", lambda: InformationAcquisitionStrategyFormationEvaluationEngineV1().run(), verify_r07),
    ("R08", lambda: PerceptionRoutingEvaluationEngineV1().run(), verify_r08),
    ("R09", lambda: PerceptionRoutingAdmissionCompatibilityEvaluationEngineV1().run(), verify_r09),
    ("R10", lambda: ProviderRuntimeTargetPreparationEvaluationEngineV1().run(), verify_r10),
    ("R11", build_runtime_admission_order_summary_v1, verify_r11),
    ("R12", lambda: StrategyCoordinationEvaluationEngineV1().run(), verify_r12),
    ("R13", lambda: EvidenceContextFieldCurrentWorldControlledEngineV1().run(), verify_r13),
)


def _mutate(summary: dict, surface_id: str) -> dict:
    result = copy.deepcopy(summary)
    cases = result.get("cases", [])
    assert cases
    target = cases[0]
    target["result"] = {}
    result.update({"all_checks_passed": True, "passed_count": 99999, "final_decision": "GO"})
    return result


@pytest.mark.parametrize("surface_id,factory,verifier", SURFACES, ids=[item[0] for item in SURFACES])
def test_p2_canonical_positive(surface_id, factory, verifier) -> None:
    assert verifier(factory())["all_checks_passed"] is True


@pytest.mark.parametrize("surface_id,factory,verifier", SURFACES, ids=[item[0] for item in SURFACES])
def test_p2_producer_result_tamper_is_rejected(surface_id, factory, verifier) -> None:
    assert verifier(_mutate(factory(), surface_id))["all_checks_passed"] is False


def test_p2_same_artifact_expected_and_result_tamper_is_rejected() -> None:
    summary = _artifact("a_route_information_need_formation_v1")
    case = summary["cases"][0]
    case["expected_status"] = "FORGED"
    case["result"]["status"] = "FORGED"
    assert verify_r01(summary)["all_checks_passed"] is False
