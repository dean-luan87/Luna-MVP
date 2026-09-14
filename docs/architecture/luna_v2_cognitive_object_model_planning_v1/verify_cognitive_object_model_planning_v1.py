#!/usr/bin/env python3
import json
import sys
from pathlib import Path

BASE = Path("docs/architecture/luna_v2_cognitive_object_model_planning_v1")

REQUIRED_FILES = [
    "luna_world_object_model_v1.md",
    "world_object_envelope_schema_v1.json",
    "living_field_object_schema_v1.json",
    "perspective_object_schema_v1.json",
    "living_context_object_schema_v1.json",
    "attachment_object_schema_v1.json",
    "subjective_causality_object_schema_v1.json",
    "cognition_action_object_schema_v1.json",
    "world_object_relationship_matrix_v1.json",
    "world_object_lifecycle_and_revision_v1.json",
    "cognitive_object_model_existing_asset_mapping_v1.json",
    "cognitive_object_model_summary_v1.json",
    "verify_cognitive_object_model_planning_v1.py",
]

checks = {}
failed_checks = []

for name in REQUIRED_FILES:
    p = BASE / name
    exists = p.is_file()
    checks[f"{name}_exists"] = exists
    if not exists:
        failed_checks.append(f"{name}_exists")

json_files = [
    p
    for p in [
        BASE / "world_object_envelope_schema_v1.json",
        BASE / "living_field_object_schema_v1.json",
        BASE / "perspective_object_schema_v1.json",
        BASE / "living_context_object_schema_v1.json",
        BASE / "attachment_object_schema_v1.json",
        BASE / "subjective_causality_object_schema_v1.json",
        BASE / "cognition_action_object_schema_v1.json",
        BASE / "world_object_relationship_matrix_v1.json",
        BASE / "world_object_lifecycle_and_revision_v1.json",
        BASE / "cognitive_object_model_existing_asset_mapping_v1.json",
        BASE / "cognitive_object_model_summary_v1.json",
    ]
    if (BASE / name).is_file()
]
for p in json_files:
    try:
        json.loads(p.read_text(encoding="utf-8"))
        checks[f"{p.name}_json_valid"] = True
    except json.JSONDecodeError:
        checks[f"{p.name}_json_valid"] = False
        failed_checks.append(f"{p.name}_json_valid")

# taxonomy
text = (BASE / "luna_world_object_model_v1.md").read_text(encoding="utf-8")
for t in [
    "entity",
    "state",
    "event",
    "relation",
    "projection",
    "attachment",
    "belief",
    "request",
    "decision_candidate",
    "feedback",
]:
    ok = f"- {t}" in text or f"- {t}\n" in text
    checks[f"taxonomy_{t}"] = ok
    if not ok:
        failed_checks.append(f"taxonomy_{t}")

# envelope fields
envelope = json.loads(
    (BASE / "world_object_envelope_schema_v1.json").read_text(encoding="utf-8")
)
fields = envelope.get("fields", {})
required_envelope = [
    "object_id",
    "object_type",
    "schema_version",
    "lifecycle_status",
    "owner_scope",
    "source_scope",
    "perspective_scope",
    "field_scope",
    "temporal_validity",
    "confidence",
    "evidence_refs",
    "trace_refs",
    "governance_refs",
    "candidate_only",
    "not_fact",
    "created_at",
    "updated_at",
    "revision",
    "supersedes_ref",
    "revoked",
    "revocation_reason",
    "unresolved_fields",
    "extension_data",
]
for field in required_envelope:
    ok = field in fields
    checks[f"envelope_field_{field}"] = ok
    if not ok:
        failed_checks.append(f"envelope_field_{field}")

# living field objects
living_field = json.loads(
    (BASE / "living_field_object_schema_v1.json").read_text(encoding="utf-8")
)
for obj in [
    "SpaceAnchor",
    "FieldDefinition",
    "FieldInstance",
    "FieldState",
    "FieldRelation",
    "FieldEvent",
    "FieldTimeline",
    "TemporalValidity",
    "ActiveFieldProjection",
]:
    ok = obj in living_field.get("objects", {})
    checks[f"living_field_{obj}"] = ok
    if not ok:
        failed_checks.append(f"living_field_{obj}")

# perspective objects
perspective = json.loads(
    (BASE / "perspective_object_schema_v1.json").read_text(encoding="utf-8")
)
for obj in [
    "PerspectiveDefinition",
    "PerspectiveState",
    "PerspectiveWeight",
    "PerspectiveConflict",
    "PerspectiveSelectionCandidate",
]:
    ok = obj in perspective.get("objects", {})
    checks[f"perspective_{obj}"] = ok
    if not ok:
        failed_checks.append(f"perspective_{obj}")

# living context objects
living_context = json.loads(
    (BASE / "living_context_object_schema_v1.json").read_text(encoding="utf-8")
)
for obj in ["LivingContext", "ContextSignal", "ContextSnapshot", "ExperienceRecord"]:
    ok = obj in living_context.get("objects", {})
    checks[f"living_context_{obj}"] = ok
    if not ok:
        failed_checks.append(f"living_context_{obj}")

# attachment objects
attachment = json.loads(
    (BASE / "attachment_object_schema_v1.json").read_text(encoding="utf-8")
)
for obj in [
    "MeaningAttachment",
    "MemoryAttachment",
    "EmotionAttachment",
    "ContextTrigger",
]:
    ok = obj in attachment.get("objects", {})
    checks[f"attachment_{obj}"] = ok
    if not ok:
        failed_checks.append(f"attachment_{obj}")

# subjective causality objects
subjective = json.loads(
    (BASE / "subjective_causality_object_schema_v1.json").read_text(encoding="utf-8")
)
for obj in [
    "physical_causal_candidate",
    "institutional_causal_candidate",
    "social_causal_candidate",
    "subjective_causal_belief",
    "emotional_association",
    "narrative_explanation",
]:
    ok = obj in subjective.get("objects", {})
    checks[f"subjective_{obj}"] = ok
    if not ok:
        failed_checks.append(f"subjective_{obj}")

# cognition action objects
cognition = json.loads(
    (BASE / "cognition_action_object_schema_v1.json").read_text(encoding="utf-8")
)
for obj in [
    "ExpectationCandidate",
    "AttentionCandidate",
    "ObservationRequest",
    "InteractionDecisionCandidate",
    "FeedbackCandidate",
    "CognitiveRevision",
    "PersonalityDevelopmentCandidate",
]:
    ok = obj in cognition.get("objects", {})
    checks[f"cognition_{obj}"] = ok
    if not ok:
        failed_checks.append(f"cognition_{obj}")

# relationship matrix
matrix = json.loads(
    (BASE / "world_object_relationship_matrix_v1.json").read_text(encoding="utf-8")
)
checks["relationship_count_20"] = len(matrix.get("relationships", [])) >= 20
if not checks["relationship_count_20"]:
    failed_checks.append("relationship_count_20")

# lifecycle states
lifecycle = json.loads(
    (BASE / "world_object_lifecycle_and_revision_v1.json").read_text(encoding="utf-8")
)
for state in [
    "proposed",
    "observed",
    "admitted_candidate",
    "active_candidate",
    "suspended",
    "expired",
    "superseded",
    "revoked",
    "archived",
]:
    ok = state in lifecycle.get("lifecycle_states", [])
    checks[f"lifecycle_{state}"] = ok
    if not ok:
        failed_checks.append(f"lifecycle_{state}")

# existing asset mapping coverage
mapping = json.loads(
    (BASE / "cognitive_object_model_existing_asset_mapping_v1.json").read_text(
        encoding="utf-8"
    )
)
required_assets = [
    "Situation Understanding",
    "Observation Attention",
    "Region Intelligence",
    "Ownership Understanding",
    "Field-Centric Object Role",
    "Model Manager",
    "Model Test Lens",
    "Human Correction",
    "Evidence Chain",
    "Runtime Boundary",
    "Model / Skill Admission",
    "Candidate / Fact Admission",
    "Task Manager",
    "Followup Runner",
    "OCR Evidence",
    "Vision Evidence",
    "Network-Assisted Situation Learning",
    "Emotional Engine",
    "Memory System",
    "Interaction Governance",
]
checks["existing_asset_coverage"] = all(
    any(m.get("existing_asset") == name for m in mapping.get("mappings", []))
    for name in required_assets
)
if not checks["existing_asset_coverage"]:
    failed_checks.append("existing_asset_coverage")

checks["physical_move_allowed_false"] = all(
    not m.get("physical_move_allowed", True) for m in mapping.get("mappings", [])
)
if not checks["physical_move_allowed_false"]:
    failed_checks.append("physical_move_allowed_false")

checks["rewrite_required_false"] = all(
    not m.get("rewrite_required", True) for m in mapping.get("mappings", [])
)
if not checks["rewrite_required_false"]:
    failed_checks.append("rewrite_required_false")

# summary flags
summary = json.loads(
    (BASE / "cognitive_object_model_summary_v1.json").read_text(encoding="utf-8")
)
checks["summary_flatten_false"] = (
    summary.get("everything_flattened_into_untyped_object") is False
)
checks["summary_runtime_false"] = (
    summary.get("real_runtime_implementation_allowed") is False
)
checks["summary_database_false"] = summary.get("database_selection_allowed") is False
checks["summary_migration_false"] = summary.get("directory_migration_allowed") is False
checks["summary_training_false"] = summary.get("model_training_allowed") is False
checks["summary_production_false"] = (
    summary.get("production_activation_allowed") is False
)
checks["summary_personality_false"] = (
    summary.get("autonomous_personality_mutation_allowed") is False
)
checks["summary_candidate_only_true"] = summary.get("candidate_only") is True
checks["summary_not_fact_true"] = summary.get("not_fact") is True
checks["summary_blocker_count_zero"] = summary.get("blocker_count") == 0
checks["summary_final_decision_matches"] = (
    summary.get("final_decision") == "LUNA_V2_COGNITIVE_OBJECT_MODEL_PLANNING_GO"
)
checks["summary_next_phase_matches"] = (
    summary.get("recommended_next_phase")
    == "Phase-Luna-Field-Kernel-Technical-Architecture-Planning-v1-001"
)
for name in [
    "summary_flatten_false",
    "summary_runtime_false",
    "summary_database_false",
    "summary_migration_false",
    "summary_training_false",
    "summary_production_false",
    "summary_personality_false",
    "summary_candidate_only_true",
    "summary_not_fact_true",
    "summary_blocker_count_zero",
    "summary_final_decision_matches",
    "summary_next_phase_matches",
]:
    if not checks[name]:
        failed_checks.append(name)

passed_count = sum(1 for v in checks.values() if v)
failed_count = len(failed_checks)
blocker_count = 1 if failed_count > 0 else 0
final_decision = (
    "LUNA_V2_COGNITIVE_OBJECT_MODEL_PLANNING_GO"
    if failed_count == 0
    else "LUNA_V2_COGNITIVE_OBJECT_MODEL_PLANNING_BLOCKED"
)
next_phase = "Phase-Luna-Field-Kernel-Technical-Architecture-Planning-v1-001"

print("CHECKS")
print(json.dumps(checks, ensure_ascii=False, indent=2))
print("FAILED_CHECKS")
print(json.dumps(failed_checks, ensure_ascii=False, indent=2))
print("PASSED_CHECK_COUNT")
print(passed_count)
print("FAILED_CHECK_COUNT")
print(failed_count)
print("BLOCKER_COUNT")
print(blocker_count)
print("FINAL_DECISION")
print(final_decision)
print("NEXT")
print(next_phase)

sys.exit(1 if failed_count > 0 else 0)
