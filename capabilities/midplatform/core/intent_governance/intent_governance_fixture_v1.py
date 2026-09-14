"""Synthetic fixtures for Intent Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from capabilities.midplatform.core.intent_governance.intent_core_types_v1 import (
    SourceRefV1,
)
from capabilities.midplatform.core.intent_governance.intent_io_types_v1 import (
    IntentGovernanceInputV1,
)


@dataclass(frozen=True)
class IntentFixtureCaseV1:
    case_id: str
    description: str
    request: IntentGovernanceInputV1
    expected_relations: Tuple[str, ...]
    expected_interactions: Tuple[str, ...]
    expects_carryover: bool
    low_resource_mode: bool
    synthetic_only: bool = True


def _ref(owner: str, ref_id: str, ref_type: str = "REFERENCE") -> SourceRefV1:
    return SourceRefV1(owner=owner, ref_id=ref_id, ref_type=ref_type)


def get_intent_synthetic_fixtures_v1() -> Tuple[IntentFixtureCaseV1, ...]:
    def mk(
        case_id: str,
        desc: str,
        relations: Tuple[str, ...],
        interactions: Tuple[str, ...],
        carryover: bool,
        low_resource: bool,
    ) -> IntentFixtureCaseV1:
        context = (_ref("Context Governance", f"ctx:{case_id}", "CONTEXT"),)
        pcn = (_ref("Personal Cognitive Network Governance", f"pcn:{case_id}", "PCN"),)
        source = (
            _ref("External Request Source", f"request:{case_id}", "REQUEST"),
            _ref("Cognitive Field", f"field:{case_id}", "FIELD"),
        )
        self_refs = (_ref("Self Layer / Self Governance", f"self:{case_id}", "SELF"),)
        role_refs = (_ref("Social Self / Role Governance", f"role:{case_id}", "ROLE"),)
        rel_refs = (
            _ref(
                "Social Self / Relationship Governance",
                f"rel:{case_id}",
                "RELATIONSHIP",
            ),
        )
        memory_refs = (_ref("Memory Governance", f"mem:{case_id}", "MEMORY"),)
        emotion_refs = (
            _ref("Emotion / Integration Governance", f"emo:{case_id}", "EMOTION"),
        )
        request = IntentGovernanceInputV1(
            scenario_id=case_id,
            context_refs=context,
            pcn_refs=pcn,
            source_refs=source,
            self_refs=self_refs,
            field_refs=(source[1],),
            role_refs=role_refs,
            relationship_refs=rel_refs,
            memory_refs=memory_refs,
            experience_refs=(),
            emotion_refs=emotion_refs,
            unknowns=("unknown:confidence", "unknown:alternative"),
            synthetic_only=True,
            candidate_only=True,
        )
        return IntentFixtureCaseV1(
            case_id=case_id,
            description=desc,
            request=request,
            expected_relations=relations,
            expected_interactions=interactions,
            expects_carryover=carryover,
            low_resource_mode=low_resource,
        )

    return (
        mk(
            "S01_WEATHER_QUERY_NO_LONG_TERM_INTENT",
            "weather short-lived query",
            ("SEEK",),
            ("COEXISTENCE",),
            False,
            False,
        ),
        mk(
            "S02_FINDING_KEYS_EXPLICIT_INTENT",
            "explicit find keys",
            ("SEEK",),
            ("TEMPORARY_DOMINANCE",),
            True,
            False,
        ),
        mk(
            "S03_FAMILY_FIELD_TEMPORARY_WORK_DOMINANCE",
            "family/work temporary dominance",
            ("SEEK", "MAINTAIN"),
            ("CONFLICT", "TEMPORARY_DOMINANCE"),
            True,
            False,
        ),
        mk(
            "S04_LONG_OVERTIME_WORK_FAMILY_COEXISTENCE",
            "overtime coexistence",
            ("SEEK", "MAINTAIN", "AVOID"),
            ("COEXISTENCE", "COMPETITION"),
            True,
            False,
        ),
        mk(
            "S05_UNFINISHED_WORK_CARRYOVER_HOME",
            "unfinished work carryover",
            ("SEEK",),
            ("REACTIVATION",),
            True,
            False,
        ),
        mk(
            "S06_SPOUSE_AND_COLLEAGUE_INTENTS_COEXIST",
            "dual role coexistence",
            ("MAINTAIN", "CHANGE"),
            ("COEXISTENCE", "CONFLICT"),
            True,
            False,
        ),
        mk(
            "S07_DIVORCED_BUT_COLLEAGUES",
            "historical/current relationship",
            ("MAINTAIN", "AVOID"),
            ("COEXISTENCE", "SUPPRESSION"),
            True,
            False,
        ),
        mk(
            "S08_OLD_RELATION_DORMANT_REACTIVATION",
            "dormant reactivation",
            ("AVOID", "SEEK", "UNKNOWN"),
            ("REACTIVATION", "SUPPRESSION"),
            True,
            True,
        ),
        mk(
            "S09_FEAR_CROSSING_SAFETY_AVOIDANCE",
            "emotion influence boundary",
            ("AVOID", "MAINTAIN"),
            ("TEMPORARY_DOMINANCE", "CONFLICT"),
            False,
            True,
        ),
        mk(
            "S10_SAYS_FINE_ABNORMAL_BEHAVIOR",
            "contradictory observations",
            ("UNKNOWN",),
            ("COEXISTENCE",),
            False,
            True,
        ),
        mk(
            "S11_LONG_TERM_ELECTRONIC_LIFE_DIRECTION",
            "long-term direction",
            ("SEEK", "MAINTAIN"),
            ("DORMANT", "REACTIVATION"),
            True,
            False,
        ),
        mk(
            "S12_LOW_RESOURCE_PROJECTION_SHRINK",
            "resource shrink",
            ("SEEK", "UNKNOWN"),
            ("SUPPRESSION", "AMPLIFICATION"),
            True,
            True,
        ),
    )
