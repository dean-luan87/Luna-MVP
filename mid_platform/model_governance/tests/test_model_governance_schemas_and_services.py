# -*- coding: utf-8 -*-
"""P0 + P1 + P2 占位：registry、路由、治理预检、蜂巢/图书馆/建议留痕对象最小单测。"""
from __future__ import annotations

from pathlib import Path

import pytest

from mid_platform.model_governance.records.model_governance_record_writer import (
    ModelGovernanceRecordWriter,
)
from mid_platform.model_governance.records.model_quality_record_writer import ModelQualityRecordWriter
from mid_platform.model_governance.records.model_usage_record_writer import ModelUsageRecordWriter
from mid_platform.model_governance.governance.model_fallback_plan import (
    ERROR_GOVERNANCE_BLOCKED,
    ERROR_INVALID_OUTPUT,
    ERROR_SCHEMA_FAIL,
    ERROR_TIMEOUT,
    ModelFallbackPlan,
    resolve_backup_model_id_if_needed,
    resolve_fallback_action,
)
from mid_platform.model_governance.governance.model_governance_decision_record import (
    ModelGovernanceDecisionRecord,
)
from mid_platform.model_governance.governance.model_governance_decision_service import (
    ModelGovernanceDecisionService,
)
from mid_platform.model_governance.governance.model_recommendation_intake_record import (
    ModelRecommendationIntakeRecord,
)
from mid_platform.model_governance.hive.hive_model_recommendation import (
    HiveModelRecommendation,
    sample_recommendation,
)
from mid_platform.model_governance.hive.hive_model_score_input_pack import (
    HiveModelScoreInputPack,
    sample_input_pack,
)
from mid_platform.model_governance.hive.hive_model_score_record import (
    HiveModelScoreRecord,
    sample_score_record,
)
from mid_platform.model_governance.library.library_experience_package import LibraryExperiencePackage
from mid_platform.model_governance.library.library_experience_record import LibraryExperienceRecord
from mid_platform.model_governance.library.library_validation_record import LibraryValidationRecord
from mid_platform.model_governance.registry.model_registry_service import ModelRegistryService
from mid_platform.model_governance.registry.model_task_card_service import ModelTaskCardService
from mid_platform.model_governance.schemas.model_governance_record import ModelGovernanceRecord
from mid_platform.model_governance.schemas.model_quality_record import ModelQualityRecord
from mid_platform.model_governance.schemas.model_registry_card import ModelRegistryCard
from mid_platform.model_governance.schemas.model_task_card import ModelTaskCard
from mid_platform.model_governance.routing.model_route_decision import ModelRouteDecision
from mid_platform.model_governance.routing.model_route_policy import ModelRoutePolicy
from mid_platform.model_governance.routing.model_route_selector import select_route
from mid_platform.model_governance.schemas.model_usage_record import ModelUsageRecord


def _card(
    model_id: str,
    *,
    enabled: bool = True,
    allowed_in_mainline: bool = True,
    allowed_in_shadow_mode: bool = True,
    role_type: str = "production",
    deployment_type: str = "local",
    status: str = "active",
) -> ModelRegistryCard:
    return ModelRegistryCard(
        model_id=model_id,
        display_name=model_id,
        provider="local",
        version="1",
        deployment_type=deployment_type,
        runtime_location="device",
        role_type=role_type,
        capability_domains=["voice"],
        supported_tasks=["t1"],
        input_contract_id="c_in",
        input_contract_version="1",
        output_contract_id="c_out",
        output_contract_version="1",
        allowed_in_mainline=allowed_in_mainline,
        allowed_in_shadow_mode=allowed_in_shadow_mode,
        allowed_for_user_facing=False,
        fallback_target_model_id=None,
        fallback_to_rule_chain=True,
        latency_tier="low",
        cost_tier="low",
        schema_guard_required=True,
        self_judgement_forbidden=True,
        auto_promotion_forbidden=True,
        enabled=enabled,
        status=status,
        priority=1,
        owner_module="test",
    )


def test_registry_card_roundtrip() -> None:
    c = _card("m1")
    c2 = ModelRegistryCard.from_dict(c.to_dict())
    assert c2.model_id == "m1"


def test_task_card_roundtrip() -> None:
    tc = ModelTaskCard(
        task_card_id="tc1",
        model_id="m1",
        task_name="n",
        task_code="c",
        task_domain="voice_task_parse",
        task_goal="g",
        task_responsibility="r",
        task_boundary="b",
        task_non_responsibility="x",
        input_sources=["asr"],
        input_contract="ic",
        input_required_fields=["text"],
        input_optional_fields=[],
        processing_mode="single_pass",
        processing_constraints=[],
        processing_forbidden_behaviors=[],
        output_contract="oc",
        output_required_fields=[],
        output_optional_fields=[],
        output_downstream_consumers=[],
        success_criteria="schema_ok",
        failure_criteria="timeout",
        quality_metrics=[],
        fallback_behavior="clarification",
    )
    tc2 = ModelTaskCard.from_dict(tc.to_dict())
    assert tc2.task_card_id == "tc1"


def test_usage_quality_governance_records_roundtrip() -> None:
    u = ModelUsageRecord(
        record_id="u1",
        model_id="m1",
        task_type="t",
        caller_module="cap.test",
        input_contract_version="1",
        output_contract_version="1",
        latency_ms=1.0,
        success=True,
        cost_estimate=0.0,
        timestamp=0.0,
    )
    assert ModelUsageRecord.from_dict(u.to_dict()).record_id == "u1"
    q = ModelQualityRecord(
        record_id="q1",
        model_id="m1",
        task_type="t",
        validator_passed=True,
        mixed_preserved=None,
        clarification_needed=None,
        unsupported_quality=None,
        quality_label="ok",
        notes=None,
        timestamp=0.0,
    )
    assert ModelQualityRecord.from_dict(q.to_dict()).model_id == "m1"
    g = ModelGovernanceRecord(
        record_id="g1",
        model_id="m1",
        task_type="t",
        fallback_triggered=False,
        degradation_triggered=False,
        schema_violation=False,
        illegal_mapping=False,
        governance_blocked=False,
        policy_violation=False,
        timestamp=0.0,
    )
    assert ModelGovernanceRecord.from_dict(g.to_dict()).record_id == "g1"


def test_registry_service_register_list_filter() -> None:
    svc = ModelRegistryService()
    svc.register(_card("primary", deployment_type="cloud"))
    svc.register(_card("backup", deployment_type="local"))
    svc.register(_card("disabled_m", enabled=False))
    assert svc.get("primary") is not None
    assert len(svc.list_enabled()) == 2
    enabled_ids = {c.model_id for c in svc.list_enabled()}
    assert "primary" in enabled_ids and "backup" in enabled_ids
    assert "disabled_m" not in enabled_ids
    assert len(svc.filter(role_type="production")) == 3
    assert len(svc.filter(deployment_type="cloud")) == 1
    assert len(svc.filter(status="active")) == 3


def test_registry_schema_missing_required_key_raises() -> None:
    with pytest.raises(KeyError):
        ModelRegistryCard.from_dict({"model_id": "x"})


def _minimal_task_card(task_card_id: str, model_id: str, task_domain: str) -> ModelTaskCard:
    return ModelTaskCard(
        task_card_id=task_card_id,
        model_id=model_id,
        task_name="n",
        task_code="c",
        task_domain=task_domain,
        task_goal="g",
        task_responsibility="r",
        task_boundary="b",
        task_non_responsibility="x",
        input_sources=[],
        input_contract="ic",
        input_required_fields=["a"],
        input_optional_fields=[],
        processing_mode="single_pass",
        processing_constraints=[],
        processing_forbidden_behaviors=[],
        output_contract="oc",
        output_required_fields=[],
        output_optional_fields=[],
        output_downstream_consumers=[],
        success_criteria="",
        failure_criteria="",
        quality_metrics=[],
        fallback_behavior="",
    )


def test_task_card_service_bindings() -> None:
    ts = ModelTaskCardService()
    ts.register(_minimal_task_card("tc1", "m1", "d"))
    assert len(ts.list_for_model("m1")) == 1
    assert len(ts.list_by_task_domain("d")) == 1


def test_task_card_two_cards_same_model_and_domain_lookup() -> None:
    ts = ModelTaskCardService()
    ts.register(_minimal_task_card("tc_a", "m1", "voice_task_parse"))
    ts.register(_minimal_task_card("tc_b", "m1", "voice_task_parse"))
    assert len(ts.list_for_model("m1")) == 2
    by_dom = ts.list_by_task_domain("voice_task_parse")
    assert len(by_dom) == 2
    assert {x.task_card_id for x in by_dom} == {"tc_a", "tc_b"}


def test_record_writers_jsonl(tmp_path: Path) -> None:
    uw = ModelUsageRecordWriter(tmp_path)
    qw = ModelQualityRecordWriter(tmp_path)
    gw = ModelGovernanceRecordWriter(tmp_path)
    uw.write(
        ModelUsageRecord(
            record_id="u1",
            model_id="m1",
            task_type="t",
            caller_module="cap.test",
            input_contract_version="1",
            output_contract_version="1",
            latency_ms=10.0,
            success=True,
            cost_estimate=0.01,
            timestamp=1.0,
        )
    )
    qw.write(
        ModelQualityRecord(
            record_id="q1",
            model_id="m1",
            task_type="t",
            validator_passed=True,
            mixed_preserved=None,
            clarification_needed=None,
            unsupported_quality=None,
            quality_label="ok",
            notes=None,
            timestamp=1.0,
        )
    )
    gw.write(
        ModelGovernanceRecord(
            record_id="g1",
            model_id="m1",
            task_type="t",
            fallback_triggered=False,
            degradation_triggered=False,
            schema_violation=False,
            illegal_mapping=False,
            governance_blocked=False,
            policy_violation=False,
            timestamp=1.0,
        )
    )
    assert (tmp_path / "usage_records.jsonl").read_text(encoding="utf-8").count("\n") == 1
    assert (tmp_path / "quality_records.jsonl").read_text(encoding="utf-8").count("\n") == 1
    assert (tmp_path / "governance_records.jsonl").read_text(encoding="utf-8").count("\n") == 1


def test_registry_persist_json(tmp_path: Path) -> None:
    p = tmp_path / "reg.json"
    svc = ModelRegistryService()
    svc.register(_card("m1"))
    svc.persist(p)
    svc2 = ModelRegistryService(p)
    assert svc2.get("m1") is not None


# --- P1：路由与治理骨架 ---


def test_route_selector_primary_success() -> None:
    reg = ModelRegistryService()
    reg.register(_card("primary", enabled=True))
    policy = ModelRoutePolicy(
        policy_id="p1",
        task_domain_to_primary={"d": "primary"},
        task_domain_to_fallback={"d": "fallback"},
        fallback_to_rule_chain=True,
    )
    dec = select_route(task_domain="d", caller_scope="mainline", registry=reg, policy=policy)
    assert dec.selected_model_id == "primary"
    assert dec.fallback_applied is False
    assert dec.selection_reason == "primary"


def test_route_selector_fallback() -> None:
    reg = ModelRegistryService()
    reg.register(_card("primary", enabled=False))
    reg.register(_card("fallback", enabled=True))
    policy = ModelRoutePolicy(
        policy_id="p1",
        task_domain_to_primary={"d": "primary"},
        task_domain_to_fallback={"d": "fallback"},
        fallback_to_rule_chain=True,
    )
    dec = select_route(task_domain="d", caller_scope="mainline", registry=reg, policy=policy)
    assert dec.selected_model_id == "fallback"
    assert dec.fallback_applied is True


def test_route_selector_rule_chain() -> None:
    reg = ModelRegistryService()
    reg.register(_card("bad", enabled=False))
    policy = ModelRoutePolicy(
        policy_id="p1",
        task_domain_to_primary={"d": "bad"},
        fallback_to_rule_chain=True,
    )
    dec = select_route(task_domain="d", caller_scope="mainline", registry=reg, policy=policy)
    assert dec.selected_model_id is None
    assert dec.selection_reason == "rule_chain"


def test_route_selector_reject_without_rule_chain() -> None:
    reg = ModelRegistryService()
    reg.register(_card("bad", enabled=False))
    policy = ModelRoutePolicy(
        policy_id="p1",
        task_domain_to_primary={"d": "bad"},
        fallback_to_rule_chain=False,
    )
    dec = select_route(task_domain="d", caller_scope="mainline", registry=reg, policy=policy)
    assert dec.selected_model_id is None
    assert dec.selection_reason == "reject"


def test_resolve_fallback_action_maps_errors() -> None:
    plan = ModelFallbackPlan(
        plan_id="fp1",
        model_id="m1",
        on_timeout="backup_model",
        on_invalid_output="rule_chain",
        on_schema_fail="clarification",
        on_governance_blocked="reject",
        backup_model_id="m2",
    )
    assert resolve_fallback_action(plan, ERROR_TIMEOUT) == "backup_model"
    assert resolve_backup_model_id_if_needed(plan, ERROR_TIMEOUT) == "m2"
    assert resolve_fallback_action(plan, ERROR_INVALID_OUTPUT) == "rule_chain"
    assert resolve_fallback_action(plan, ERROR_SCHEMA_FAIL) == "clarification"
    assert resolve_fallback_action(plan, ERROR_GOVERNANCE_BLOCKED) == "reject"


def test_resolve_fallback_action_backup_without_id_raises() -> None:
    plan = ModelFallbackPlan(
        plan_id="fp1",
        model_id="m1",
        on_timeout="backup_model",
        on_invalid_output="rule_chain",
        on_schema_fail="clarification",
        on_governance_blocked="reject",
        backup_model_id=None,
    )
    with pytest.raises(ValueError, match="backup_model_id"):
        resolve_fallback_action(plan, ERROR_TIMEOUT)


def test_route_policy_fallback_model_id_alias() -> None:
    p = ModelRoutePolicy(
        policy_id="x",
        task_domain_to_primary={},
        default_fallback_model_id="fb1",
    )
    assert p.fallback_model_id == "fb1"


def test_route_decision_roundtrip() -> None:
    d = ModelRouteDecision(
        task_domain="d",
        selected_model_id="m1",
        selection_reason="primary",
        fallback_applied=False,
        fallback_reason=None,
        governance_constraints={"k": "v"},
    )
    d2 = ModelRouteDecision.from_dict(d.to_dict())
    assert d2.selected_model_id == "m1"
    assert d2.governance_constraints == {"k": "v"}


def test_governance_blocks_not_allowed_in_mainline() -> None:
    g = ModelGovernanceDecisionService()
    r = g.precheck_mainline(_card("x", allowed_in_mainline=False))
    assert r.allowed is False
    assert "not_allowed_in_mainline" in r.reasons


def test_governance_blocks_role_conflict() -> None:
    g = ModelGovernanceDecisionService()
    r = g.precheck_mainline(_card("x", role_type="review"))
    assert r.allowed is False
    assert "role_conflict_mainline_requires_production" in r.reasons


def test_governance_blocks_mainline_unsafe() -> None:
    g = ModelGovernanceDecisionService()
    d = _card("x", allowed_in_mainline=True).to_dict()
    d["self_judgement_forbidden"] = False
    bad = ModelRegistryCard.from_dict(d)
    r = g.precheck_mainline(bad)
    assert r.allowed is False
    assert "self_judgement_not_forbidden" in r.reasons


# --- P2：仅 schema 占位，无自动闭环 ---


def test_p2_hive_sample_roundtrip() -> None:
    p = sample_input_pack()
    assert HiveModelScoreInputPack.from_dict(p.to_dict()).sample_size == p.sample_size
    s = sample_score_record()
    assert HiveModelScoreRecord.from_dict(s.to_dict()).model_id == s.model_id
    r = sample_recommendation()
    assert HiveModelRecommendation.from_dict(r.to_dict()).recommendation_id == r.recommendation_id


def test_p2_library_roundtrip() -> None:
    ler = LibraryExperienceRecord(
        experience_id="e1",
        source_scope="individual_luna",
        source_task_type="t",
        source_model_id="m1",
        problem_type="timeout_pattern",
        context_summary="c",
        evidence_refs=["ref1"],
        raw_confidence=0.2,
        library_status="draft",
    )
    assert LibraryExperienceRecord.from_dict(ler.to_dict()).experience_id == "e1"
    lep = LibraryExperiencePackage(
        package_id="p1",
        package_type="failure_pattern_package",
        applicable_domains=["d"],
        applicable_models=["m1"],
        summary="s",
    )
    assert LibraryExperiencePackage.from_dict(lep.to_dict()).package_id == "p1"
    lvr = LibraryValidationRecord(
        validation_id="v1",
        target_package_id="p1",
        validation_scope="task_specific",
        sample_size=3,
        validation_result="needs_more_data",
        confidence_level="low",
    )
    assert LibraryValidationRecord.from_dict(lvr.to_dict()).validation_id == "v1"


def test_p2_intake_and_decision_record_roundtrip() -> None:
    mir = ModelRecommendationIntakeRecord(
        recommendation_id="r1",
        model_id="m1",
        recommendation_type="keep_observing",
        intake_status="received",
        intake_timestamp="t",
    )
    assert ModelRecommendationIntakeRecord.from_dict(mir.to_dict()).intake_status == "received"
    mgr = ModelGovernanceDecisionRecord(
        decision_record_id="d1",
        recommendation_id="r1",
        model_id="m1",
        decision_result="defer",
        decision_reason="insufficient_evidence",
    )
    assert ModelGovernanceDecisionRecord.from_dict(mgr.to_dict()).decision_result == "defer"
