"""Synthetic-only fixtures for PCN controlled skeleton."""

from __future__ import annotations

from typing import Dict, Tuple


def get_pcn_synthetic_fixtures_v1() -> Tuple[Dict[str, object], ...]:
    return (
        {
            "case_id": "SCN_01_WEATHER_QUERY",
            "title": "weather query",
            "synthetic_only": True,
            "context_id": "ctx-weather",
            "resource_label": "LOW",
            "source_refs": ["field-weather", "task-minimal"],
            "interaction_refs": [],
        },
        {
            "case_id": "SCN_02_TEMP_OVERTIME_AT_HOME",
            "title": "temporary overtime at home",
            "synthetic_only": True,
            "context_id": "ctx-home-temp-work",
            "resource_label": "HIGH",
            "source_refs": [
                "field-family-core",
                "field-work-temp",
                "role-family",
                "role-employee",
            ],
            "interaction_refs": [
                {
                    "interaction_reference": "ir-temp-occ-1",
                    "interaction_type": "TEMPORARY_OCCUPATION",
                    "related_refs": ["field-family-core", "field-work-temp"],
                    "source_context_ref": "ctx-home-temp-work",
                    "status": "CANDIDATE",
                }
            ],
            "new_link_candidate": True,
            "source_ref_a": "field-family-core",
            "source_ref_b": "field-work-temp",
        },
        {
            "case_id": "SCN_03_LONG_TERM_OVERTIME_AT_HOME",
            "title": "long-term overtime at home",
            "synthetic_only": True,
            "context_id": "ctx-home-long-work",
            "resource_label": "HIGH",
            "source_refs": [
                "field-family-core",
                "field-work-influence",
                "role-employee",
            ],
            "interaction_refs": [],
            "strengthening_candidate": True,
            "link_id": "link-home-work-influence",
        },
        {
            "case_id": "SCN_04_SPOUSE_AND_COLLEAGUE",
            "title": "spouse and colleague coexist",
            "synthetic_only": True,
            "context_id": "ctx-spouse-colleague",
            "resource_label": "HIGH",
            "source_refs": [
                "rel-spouse-active",
                "rel-colleague-active",
                "person-pair-a-b",
            ],
            "interaction_refs": [
                {
                    "interaction_reference": "ir-overlap-1",
                    "interaction_type": "OVERLAP",
                    "related_refs": ["rel-spouse-active", "rel-colleague-active"],
                    "source_context_ref": "ctx-spouse-colleague",
                    "status": "CANDIDATE",
                }
            ],
        },
        {
            "case_id": "SCN_05_DIVORCED_BUT_COLLEAGUE",
            "title": "former spouse and active colleague",
            "synthetic_only": True,
            "context_id": "ctx-divorce-colleague",
            "resource_label": "HIGH",
            "source_refs": [
                "rel-former-spouse-historical",
                "rel-colleague-active",
                "person-pair-a-b",
            ],
            "interaction_refs": [
                {
                    "interaction_reference": "ir-coexist-1",
                    "interaction_type": "COEXISTENCE",
                    "related_refs": [
                        "rel-former-spouse-historical",
                        "rel-colleague-active",
                    ],
                    "source_context_ref": "ctx-divorce-colleague",
                    "status": "CANDIDATE",
                }
            ],
            "weakening_candidate": True,
            "link_id": "link-former-spouse-salience",
        },
        {
            "case_id": "SCN_06_MEETING_TRIGGERS_HISTORICAL_SPOUSE",
            "title": "meeting triggers historical spouse relation",
            "synthetic_only": True,
            "context_id": "ctx-meeting-historical-trigger",
            "resource_label": "HIGH",
            "source_refs": ["rel-former-spouse-historical", "meeting-context"],
            "interaction_refs": [
                {
                    "interaction_reference": "ir-hist-react-1",
                    "interaction_type": "HISTORICAL_REACTIVATION",
                    "related_refs": ["rel-former-spouse-historical", "meeting-context"],
                    "source_context_ref": "ctx-meeting-historical-trigger",
                    "status": "CANDIDATE",
                }
            ],
            "reactivation_candidate": True,
            "link_id": "link-former-spouse-memory",
            "trigger_ref": "meeting-context",
            "historical_state_ref": "HISTORICAL",
        },
        {
            "case_id": "SCN_07_NEW_OLD_WORK_RESONANCE",
            "title": "new and old work field resonance",
            "synthetic_only": True,
            "context_id": "ctx-work-resonance",
            "resource_label": "HIGH",
            "source_refs": ["field-old-work", "field-new-work", "role-employee"],
            "interaction_refs": [
                {
                    "interaction_reference": "ir-resonance-1",
                    "interaction_type": "RESONANCE",
                    "related_refs": ["field-old-work", "field-new-work"],
                    "source_context_ref": "ctx-work-resonance",
                    "status": "CANDIDATE",
                }
            ],
        },
        {
            "case_id": "SCN_08_FATHER_VS_EMPLOYEE",
            "title": "father versus employee role competition",
            "synthetic_only": True,
            "context_id": "ctx-father-employee-competition",
            "resource_label": "HIGH",
            "source_refs": ["role-father", "role-employee", "task-family", "task-work"],
            "interaction_refs": [
                {
                    "interaction_reference": "ir-competition-1",
                    "interaction_type": "COMPETITION",
                    "related_refs": ["role-father", "role-employee"],
                    "source_context_ref": "ctx-father-employee-competition",
                    "status": "CANDIDATE",
                }
            ],
        },
        {
            "case_id": "SCN_09_COFOUNDERS_SPOUSE",
            "title": "spouse cofounders",
            "synthetic_only": True,
            "context_id": "ctx-spouse-cofounders",
            "resource_label": "HIGH",
            "source_refs": [
                "rel-spouse-active",
                "rel-cofounder-active",
                "field-startup",
            ],
            "interaction_refs": [
                {
                    "interaction_reference": "ir-overlap-9",
                    "interaction_type": "OVERLAP",
                    "related_refs": [
                        "rel-spouse-active",
                        "rel-cofounder-active",
                        "field-startup",
                    ],
                    "source_context_ref": "ctx-spouse-cofounders",
                    "status": "CANDIDATE",
                    "candidate_only": True,
                    "synthetic_only": True,
                    "source_mutation": False,
                },
                {
                    "interaction_reference": "ir-coexistence-9",
                    "interaction_type": "COEXISTENCE",
                    "related_refs": [
                        "rel-spouse-active",
                        "rel-cofounder-active",
                        "field-startup",
                    ],
                    "source_context_ref": "ctx-spouse-cofounders",
                    "status": "CANDIDATE",
                    "candidate_only": True,
                    "synthetic_only": True,
                    "source_mutation": False,
                },
                {
                    "interaction_reference": "ir-fusion-candidate-1",
                    "interaction_type": "FUSION_CANDIDATE",
                    "related_refs": [
                        "rel-spouse-active",
                        "rel-cofounder-active",
                        "field-startup",
                    ],
                    "source_context_ref": "ctx-spouse-cofounders",
                    "status": "CANDIDATE",
                    "candidate_only": True,
                    "synthetic_only": True,
                    "source_mutation": False,
                },
            ],
            "new_link_candidate": True,
            "source_ref_a": "rel-spouse-active",
            "source_ref_b": "rel-cofounder-active",
        },
        {
            "case_id": "SCN_10_DORMANT_OLD_FRIEND_REACTIVATION",
            "title": "dormant old friend reactivation",
            "synthetic_only": True,
            "context_id": "ctx-old-friend-reactivation",
            "resource_label": "LOW",
            "source_refs": ["rel-old-friend-dormant", "event-reunion"],
            "interaction_refs": [],
            "dormancy_candidate": False,
            "reactivation_candidate": True,
            "link_id": "link-old-friend",
            "trigger_ref": "event-reunion",
            "historical_state_ref": "DORMANT",
        },
        {
            "case_id": "SCN_11_STRONG_SUBJECTIVE_MISBELIEF",
            "title": "strong subjective wrong cognition",
            "synthetic_only": True,
            "context_id": "ctx-subjective-link",
            "resource_label": "HIGH",
            "source_refs": ["belief-failure-parents", "emotion-frustration"],
            "interaction_refs": [],
            "subjective": True,
            "truth_status": "UNVERIFIED_OR_SUBJECTIVE",
            "new_link_candidate": True,
            "source_ref_a": "belief-failure-parents",
            "source_ref_b": "emotion-frustration",
        },
        {
            "case_id": "SCN_12_HIGH_LOW_RESOURCE_DEGRADATION",
            "title": "high and low resource degradation",
            "synthetic_only": True,
            "context_id": "ctx-resource-contrast",
            "resource_label": "HIGH",
            "source_refs": [
                "role-employee",
                "role-parent",
                "rel-colleague-active",
                "rel-family-active",
                "field-work",
                "field-family",
            ],
            "interaction_refs": [
                {
                    "interaction_reference": "ir-resource-overlap-1",
                    "interaction_type": "OVERLAP",
                    "related_refs": ["field-work", "field-family"],
                    "source_context_ref": "ctx-resource-contrast",
                    "status": "CANDIDATE",
                }
            ],
        },
    )
