# -*- coding: utf-8 -*-
"""Governance Constraint Module Legacy Extraction Planning v1.

Legacy extraction planning only: map validated governance chains to future constraint module sources.
Does not modify legacy phases, rewrite docs, or generate constraint modules.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Governance-Constraint-Module-Legacy-Extraction-Planning-v1-001"
PLANNING_SCOPE = "governance_constraint_module_legacy_extraction_planning_only"
SOURCE_CHAIN = "governance_constraint_module_legacy_extraction_planning_v1"

FINAL_DECISION = "GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Governance-Constraint-Module-Legacy-Extraction-DryRun-v1-001"

MAIN_MIGRATION_RESUME_PHASE = "Phase-Registry-Generation-Authorization-Planning-v1-001"
MAIN_MIGRATION_PAUSED = True

LEGACY_CHAINS: Tuple[Dict[str, Any], ...] = (
    {
        "legacy_chain_id": "LC01",
        "legacy_chain_name": "Migration Rollback Rehearsal Execution chain",
        "covered_phases": [
            "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Planning-v1-001",
            "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-DryRun-v1-001",
            "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Post-DryRun-Review-v1-001",
        ],
        "eval_out_hint": "main_project_structure_migration_rollback_rehearsal_execution",
        "primary_governance_value": "rollback rehearsal execution gate and non-execution freeze",
        "candidate_constraint_domains": [
            "RollbackRehearsalConstraint",
            "MigrationExecutionConstraint",
            "ProtectedAssetConstraint",
            "FileOperationConstraint",
        ],
    },
    {
        "legacy_chain_id": "LC02",
        "legacy_chain_name": "Real Rollback Rehearsal Pre-Authorization chain",
        "covered_phases": [
            "Phase-Real-Rollback-Rehearsal-Pre-Authorization-Planning-v1-001",
            "Phase-Real-Rollback-Rehearsal-Pre-Authorization-DryRun-v1-001",
            "Phase-Real-Rollback-Rehearsal-Pre-Authorization-Post-DryRun-Review-v1-001",
            "Phase-Real-Rollback-Rehearsal-Pre-Authorization-Roadmap-Decision-v1-001",
        ],
        "eval_out_hint": "real_rollback_rehearsal_pre_authorization",
        "primary_governance_value": "pre-authorization gate before real rollback rehearsal",
        "candidate_constraint_domains": [
            "RollbackRehearsalConstraint",
            "OwnerOperatorApprovalConstraint",
            "MigrationExecutionConstraint",
        ],
    },
    {
        "legacy_chain_id": "LC03",
        "legacy_chain_name": "Governance Debt Register chain",
        "covered_phases": [
            "Phase-Governance-Debt-Register-Planning-v1-001",
            "Phase-Governance-Debt-Register-DryRun-v1-001",
            "Phase-Governance-Debt-Register-Post-DryRun-Review-v1-001",
        ],
        "eval_out_hint": "governance_debt_register",
        "primary_governance_value": "debt categorization and carryover without debt fix execution",
        "candidate_constraint_domains": [
            "GovernanceCanonicalPhaseContract",
            "NonClaimsConstraint",
            "VerifierBaselineConstraint",
        ],
    },
    {
        "legacy_chain_id": "LC04",
        "legacy_chain_name": "Permission Semantics Canonicalization chain",
        "covered_phases": [
            "Phase-Permission-Semantics-Canonicalization-Planning-v1-001",
            "Phase-Permission-Semantics-Canonicalization-DryRun-v1-001",
            "Phase-Permission-Semantics-Canonicalization-Post-DryRun-Review-v1-001",
        ],
        "eval_out_hint": "permission_semantics_canonicalization",
        "primary_governance_value": "permission semantics canonical vocabulary and ready semantics",
        "candidate_constraint_domains": ["SemanticStateConstraint", "NonClaimsConstraint"],
    },
    {
        "legacy_chain_id": "LC05",
        "legacy_chain_name": "Terminology Canonical Table chain",
        "covered_phases": [
            "Phase-Terminology-Canonical-Table-Planning-v1-001",
            "Phase-Terminology-Canonical-Table-DryRun-v1-001",
            "Phase-Terminology-Canonical-Table-Post-DryRun-Review-v1-001",
        ],
        "eval_out_hint": "terminology_canonical_table",
        "primary_governance_value": "terminology canonical table and disambiguation",
        "candidate_constraint_domains": ["TerminologyConstraint", "NonClaimsConstraint"],
    },
    {
        "legacy_chain_id": "LC06",
        "legacy_chain_name": "Success Claim Gate Canonicalization chain",
        "covered_phases": [
            "Phase-Success-Claim-Gate-Canonicalization-Planning-v1-001",
            "Phase-Success-Claim-Gate-Canonicalization-DryRun-v1-001",
            "Phase-Success-Claim-Gate-Canonicalization-Post-DryRun-Review-v1-001",
        ],
        "eval_out_hint": "success_claim_gate_canonicalization",
        "primary_governance_value": "success claim gate and success_claim_allowed=false baseline",
        "candidate_constraint_domains": ["SuccessClaimGateConstraint", "EvidenceChainConstraint"],
    },
    {
        "legacy_chain_id": "LC07",
        "legacy_chain_name": "Evidence Chain Governance chain",
        "covered_phases": [
            "Phase-Evidence-Chain-Governance-Planning-v1-001",
            "Phase-Evidence-Chain-Governance-DryRun-v1-001",
            "Phase-Evidence-Chain-Governance-Post-DryRun-Review-v1-001",
            "Phase-Evidence-Chain-Governance-Roadmap-Decision-v1-001",
        ],
        "eval_out_hint": "evidence_chain_governance",
        "primary_governance_value": "evidence chain governance; summary/verifier_report ≠ evidence",
        "candidate_constraint_domains": ["EvidenceChainConstraint", "SuccessClaimGateConstraint"],
    },
    {
        "legacy_chain_id": "LC08",
        "legacy_chain_name": "Owner/Operator Approval Protocol chain",
        "covered_phases": [
            "Phase-Owner-Operator-Approval-Protocol-Planning-v1-001",
            "Phase-Owner-Operator-Approval-Protocol-DryRun-v1-001",
            "Phase-Owner-Operator-Approval-Protocol-Post-DryRun-Review-v1-001",
            "Phase-Owner-Operator-Approval-Protocol-Roadmap-Decision-v1-001",
        ],
        "eval_out_hint": "owner_operator_approval_protocol",
        "primary_governance_value": "owner/operator planning ≠ approval granted",
        "candidate_constraint_domains": ["OwnerOperatorApprovalConstraint", "SemanticStateConstraint"],
    },
    {
        "legacy_chain_id": "LC09",
        "legacy_chain_name": "Boundary Object Registry chain",
        "covered_phases": [
            "Phase-Boundary-Object-Registry-Planning-v1-001",
            "Phase-Boundary-Object-Registry-DryRun-v1-001",
            "Phase-Boundary-Object-Registry-Post-DryRun-Review-v1-001",
            "Phase-Boundary-Object-Registry-Roadmap-Decision-v1-001",
        ],
        "eval_out_hint": "boundary_object_registry",
        "primary_governance_value": "boundary object registry planning/dry-run/review ≠ registry generated",
        "candidate_constraint_domains": ["BoundaryObjectRegistryConstraint", "ProtectedAssetConstraint"],
    },
    {
        "legacy_chain_id": "LC10",
        "legacy_chain_name": "Boundary Object Registry Generation chain",
        "covered_phases": [
            "Phase-Boundary-Object-Registry-Generation-Planning-v1-001",
            "Phase-Boundary-Object-Registry-Generation-DryRun-v1-001",
            "Phase-Boundary-Object-Registry-Generation-Post-DryRun-Review-v1-001",
            "Phase-Boundary-Object-Registry-Generation-Roadmap-Decision-v1-001",
        ],
        "eval_out_hint": "boundary_object_registry_generation",
        "primary_governance_value": "generation mechanism consumable ≠ generation authorized",
        "candidate_constraint_domains": ["RegistryGenerationConstraint", "BoundaryObjectRegistryConstraint"],
    },
    {
        "legacy_chain_id": "LC11",
        "legacy_chain_name": "Migration Governance Constraints / Anti-Incident Rules",
        "covered_phases": ["Phase-Migration-Governance-Development-Constraints-v1-001"],
        "eval_out_hint": "migration_governance_development_constraints",
        "primary_governance_value": "canonical development constraints and anti-incident rules",
        "candidate_constraint_domains": [
            "GovernanceCanonicalPhaseContract",
            "NonClaimsConstraint",
            "VerifierBaselineConstraint",
        ],
    },
    {
        "legacy_chain_id": "LC12",
        "legacy_chain_name": "Boundary Object Registry early DryRun / Generation DryRun related chain",
        "covered_phases": [
            "Phase-Boundary-Object-Registry-DryRun-v1-001",
            "Phase-Boundary-Object-Registry-Generation-DryRun-v1-001",
        ],
        "eval_out_hint": "boundary_object_registry_generation_dryrun",
        "primary_governance_value": "dry-run consumability without execution permission release",
        "candidate_constraint_domains": ["BoundaryObjectRegistryConstraint", "RegistryGenerationConstraint"],
    },
)

CONSTRAINT_DOMAINS: Tuple[str, ...] = (
    "GovernanceCanonicalPhaseContract",
    "SemanticStateConstraint",
    "TerminologyConstraint",
    "SuccessClaimGateConstraint",
    "EvidenceChainConstraint",
    "OwnerOperatorApprovalConstraint",
    "BoundaryObjectRegistryConstraint",
    "RegistryGenerationConstraint",
    "MigrationExecutionConstraint",
    "RollbackRehearsalConstraint",
    "ProtectedAssetConstraint",
    "FileOperationConstraint",
    "VerifierBaselineConstraint",
    "NonClaimsConstraint",
)

FROZEN_FIELD_PATTERNS: Tuple[Tuple[str, str, Tuple[str, ...]], ...] = (
    ("*_generated_now=false", "false", ("Planning", "DryRun", "Post-DryRun Review", "Roadmap Decision")),
    ("*_registered_now=false", "false", ("Planning", "DryRun", "Post-DryRun Review", "Roadmap Decision")),
    ("*_authorized_now=false", "false", ("Planning", "DryRun", "Post-DryRun Review", "Roadmap Decision")),
    ("*_executed_now=false", "false", ("Planning", "DryRun", "Post-DryRun Review", "Roadmap Decision")),
    ("*_committed_now=false", "false", ("Planning", "DryRun", "Post-DryRun Review", "Roadmap Decision")),
    ("*_validated_now=false", "false", ("Planning", "DryRun", "Post-DryRun Review", "Roadmap Decision")),
    ("*_checked_now=false", "false", ("Planning", "DryRun", "Post-DryRun Review", "Roadmap Decision")),
    ("success_claim_allowed=false", "false", ("Planning", "DryRun", "Post-DryRun Review", "Roadmap Decision", "Closure")),
    ("authorization_granted_now=false", "false", ("Planning", "DryRun", "Post-DryRun Review", "Roadmap Decision")),
    ("file_operation_executed_now=false", "false", ("Planning", "DryRun", "Post-DryRun Review", "Roadmap Decision")),
    ("protected_asset_modified_now=false", "false", ("Planning", "DryRun", "Post-DryRun Review", "Roadmap Decision")),
    ("human_review_queue_modified_now=false", "false", ("Planning", "DryRun", "Post-DryRun Review", "Roadmap Decision")),
    ("dnae_or_permanent_block_modified_now=false", "false", ("Planning", "DryRun", "Post-DryRun Review", "Roadmap Decision")),
    ("verifier_modified_now=false", "false", ("Planning", "DryRun", "Post-DryRun Review", "Roadmap Decision")),
    ("phase_template_modified_now=false", "false", ("Planning", "DryRun", "Post-DryRun Review", "Roadmap Decision")),
    ("automation_implemented_now=false", "false", ("Planning", "DryRun", "Post-DryRun Review", "Roadmap Decision")),
    ("documentation_auto_sync_executed_now=false", "false", ("Planning", "DryRun", "Post-DryRun Review", "Roadmap Decision")),
    ("runtime_invoked=false", "false", ("Planning", "DryRun", "Post-DryRun Review", "Roadmap Decision", "Closure")),
    ("write_allowed=false", "false", ("Planning", "DryRun", "Post-DryRun Review", "Roadmap Decision", "Closure")),
    ("real_rehearsal_execution_allowed=false", "false", ("Planning", "DryRun", "Post-DryRun Review", "Roadmap Decision")),
    ("real_migration_execution_allowed=false", "false", ("Planning", "DryRun", "Post-DryRun Review", "Roadmap Decision")),
    ("batch_arming_allowed=false", "false", ("Planning", "DryRun", "Post-DryRun Review", "Roadmap Decision")),
    ("legacy_phase_modified_now=false", "false", ("Legacy Extraction Planning",)),
    ("legacy_document_rewritten_now=false", "false", ("Legacy Extraction Planning",)),
    ("governance_constraint_module_generated_now=false", "false", ("Legacy Extraction Planning",)),
)

PHASE_MODES: Tuple[Tuple[str, str, str, str], ...] = (
    ("Planning", "define scope and artifacts only; no execution", "planning artifact generation", "real execution / authorization / file operation"),
    ("DryRun", "simulate consumability without execution", "dry-run artifact generation", "real execution / permission release"),
    ("Post-DryRun Review", "review dry-run safety; no permission release", "review artifact generation", "permission release / real execution"),
    ("Roadmap Decision", "select next route; no authorization grant", "roadmap decision artifact generation", "authorization grant / real execution"),
    ("Generation Planning", "plan generation mechanism; no generation", "generation planning artifacts", "registry generation / entry generation"),
    ("Generation DryRun", "simulate generation consumability; no generation", "generation dry-run artifacts", "registry generation / entry commit"),
    ("Generation Post-DryRun Review", "review generation dry-run; no generation", "generation review artifacts", "registry generation / source final validation"),
    ("Authorization Planning", "plan authorization schema; no authorization request", "authorization planning artifacts", "authorization request / grant"),
    ("Authorization DryRun", "simulate authorization consumability; no grant", "authorization dry-run artifacts", "authorization grant"),
    ("Authorization Post-DryRun Review", "review authorization dry-run; no grant", "authorization review artifacts", "authorization grant / execution window"),
    ("Execution Planning", "plan execution gate; no execution", "execution planning artifacts", "real execution / file operation"),
    ("Execution DryRun", "simulate execution gate; no execution", "execution dry-run artifacts", "real execution"),
    ("Execution Post-DryRun Review", "review execution dry-run; no execution", "execution review artifacts", "real execution"),
    ("Closure", "close validated chain; freeze boundaries", "closure artifact generation", "permission release / real execution"),
    ("Roadmap Re-entry", "re-enter roadmap after closure; no execution", "roadmap re-entry artifacts", "real execution / authorization grant"),
)

DOMAIN_CONSTRAINTS: Tuple[Tuple[str, str, Tuple[str, ...], str], ...] = (
    (
        "Permission Semantics",
        "semantic state and ready semantics disambiguation",
        ("Permission Semantics Canonicalization chain",),
        "governance_domain_permission_semantics_v1.json",
    ),
    (
        "Terminology",
        "terminology canonical table and vocabulary",
        ("Terminology Canonical Table chain",),
        "governance_domain_terminology_v1.json",
    ),
    (
        "Success Claim Gate",
        "success claim gate and success_claim_allowed=false",
        ("Success Claim Gate Canonicalization chain",),
        "governance_domain_success_claim_gate_v1.json",
    ),
    (
        "Evidence Chain",
        "evidence chain governance; summary ≠ evidence",
        ("Evidence Chain Governance chain",),
        "governance_domain_evidence_chain_v1.json",
    ),
    (
        "Owner/Operator Approval",
        "owner/operator planning ≠ approval granted",
        ("Owner/Operator Approval Protocol chain",),
        "governance_domain_owner_operator_approval_v1.json",
    ),
    (
        "Boundary Object Registry",
        "registry planning/dry-run/review ≠ registry generated",
        ("Boundary Object Registry chain",),
        "governance_domain_boundary_object_registry_v1.json",
    ),
    (
        "Registry Generation",
        "generation mechanism consumable ≠ generation authorized",
        ("Boundary Object Registry Generation chain",),
        "governance_domain_registry_generation_v1.json",
    ),
    (
        "Migration Execution",
        "migration execution gate and batch arming freeze",
        ("Migration Rollback Rehearsal Execution chain", "Main Project Structure Migration chain"),
        "governance_domain_migration_execution_v1.json",
    ),
    (
        "Rollback Rehearsal",
        "rollback rehearsal pre-authorization and execution gate",
        ("Real Rollback Rehearsal Pre-Authorization chain",),
        "governance_domain_rollback_rehearsal_v1.json",
    ),
    (
        "Protected Asset / HR / DnAE",
        "protected asset / human review / permanent block freeze",
        ("Protected Asset and Human Review Resolution chain", "Boundary Object Registry chain"),
        "governance_domain_protected_asset_v1.json",
    ),
    (
        "File Operation",
        "file operation default block",
        ("Main Project Structure Migration chain", "Boundary Object Registry chain"),
        "governance_domain_file_operation_v1.json",
    ),
    (
        "Verifier / Phase Template",
        "verifier baseline and phase template non-modification",
        ("Governance Debt Register chain", "Migration Governance Constraints"),
        "governance_domain_verifier_phase_template_v1.json",
    ),
)

PLANNED_MODULE_ARTIFACTS: Tuple[Tuple[str, str, Tuple[str, ...]], ...] = (
    ("governance_canonical_phase_contract_v1.json", "canonical phase contract", ("CanonicalFrozenFieldExtractionPlan", "PhaseModeLifecycleContractExtractionPlan")),
    ("governance_domain_constraint_registry_v1.json", "domain constraint registry", ("DomainConstraintExtractionPlan",)),
    ("governance_phase_inheritance_matrix_v1.json", "phase inheritance matrix", ("GovernanceConstraintInheritancePolicyPlan",)),
    ("governance_canonical_frozen_fields_v1.json", "canonical frozen fields", ("CanonicalFrozenFieldExtractionPlan",)),
    ("governance_phase_mode_lifecycle_contract_v1.json", "phase mode lifecycle contract", ("PhaseModeLifecycleContractExtractionPlan",)),
    ("governance_constraint_required_fields_v1.json", "required fields manifest", ("GovernanceConstraintInheritancePolicyPlan",)),
    ("governance_constraint_verifier_baseline_v1.json", "verifier baseline", ("DomainConstraintExtractionPlan",)),
    ("governance_constraint_non_claims_library_v1.json", "non-claims library", ("DomainConstraintExtractionPlan",)),
    ("governance_constraint_forbidden_shortcut_library_v1.json", "forbidden shortcut library", ("DomainConstraintExtractionPlan",)),
    ("governance_constraint_extension_rule_v1.json", "extension rule", ("GovernanceConstraintInheritancePolicyPlan",)),
    ("governance_legacy_absorption_policy_v1.json", "legacy absorption policy", ("LegacyAbsorptionPolicyPlan",)),
    ("governance_constraint_module_readiness_decision_v1.json", "module readiness decision", ("GovernanceConstraintModuleOutputPlan",)),
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _planning_meta() -> Dict[str, Any]:
    return {
        "legacy_extraction_planning_only": True,
        "legacy_phase_modified_now": False,
        "legacy_document_rewritten_now": False,
        "legacy_eval_out_modified_now": False,
        "legacy_verifier_rerun_now": False,
        "governance_constraint_module_generated_now": False,
        "canonical_phase_template_generated_now": False,
        "constraint_enforced_now": False,
        "verifier_modified_now": False,
        "phase_template_modified_now": False,
        "automation_implemented_now": False,
        "documentation_auto_sync_executed_now": False,
        "file_operation_executed_now": False,
        "authorization_granted_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "execution_window_opened_now": False,
        "success_claim_allowed": False,
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed": False,
        "runtime_invoked": False,
        "execution_committed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _planning_row(**kwargs: Any) -> Dict[str, Any]:
    return {**kwargs, **_planning_meta()}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _find_eval_out_summary(eval_out_hint: str) -> Dict[str, Any]:
    root = _repo_root() / "_eval_out"
    if not root.is_dir():
        return {}
    matches = sorted(root.glob(f"*{eval_out_hint}*"))
    for match in matches:
        summary = _try_read_json(match / "summary.json")
        if summary:
            return summary
    return {}


def _build_legacy_chain_inventory() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for chain in LEGACY_CHAINS:
        summary = _find_eval_out_summary(chain["eval_out_hint"])
        rows.append(
            _planning_row(
                legacy_chain_id=chain["legacy_chain_id"],
                legacy_chain_name=chain["legacy_chain_name"],
                covered_phases=chain["covered_phases"],
                phase_count=len(chain["covered_phases"]),
                latest_known_verdict=summary.get("final_decision", "GO_observed_from_phase_verdict_table"),
                boundary_ok_observed=summary.get("boundary_ok", True),
                primary_governance_value=chain["primary_governance_value"],
                candidate_constraint_domains=chain["candidate_constraint_domains"],
                legacy_validated_governance_chain=True,
                rewrite_required=False,
                source_for_constraint_extraction=True,
                deprecated=False,
                archival_status="legacy_validated_governance_chain",
            )
        )
    return rows


def _build_phase_to_constraint_matrix() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for domain in CONSTRAINT_DOMAINS:
        source_chains = [
            c["legacy_chain_name"]
            for c in LEGACY_CHAINS
            if domain in c["candidate_constraint_domains"]
        ]
        if domain == "GovernanceCanonicalPhaseContract":
            source_chains.append("Migration Governance Constraints / Anti-Incident Rules")
        rows.append(
            _planning_row(
                legacy_phase_or_chain=domain,
                contributes_to_constraint=domain,
                contribution_type="domain_constraint_source",
                reusable_rules=[
                    "Planning ≠ execution",
                    "DryRun ≠ success",
                    "Post-Review GO ≠ permission release",
                    "Roadmap selected route ≠ real authorization",
                ],
                domain_specific_rules=[f"{domain} specific forbidden shortcuts and required fields"],
                extraction_priority="P0" if domain in ("GovernanceCanonicalPhaseContract", "NonClaimsConstraint") else "P1",
                requires_manual_review=False,
                rewrite_legacy_phase=False,
                source_chains=sorted(set(source_chains)),
            )
        )
    return rows


def _build_frozen_field_plan() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for pattern, default, modes in FROZEN_FIELD_PATTERNS:
        rows.append(
            _planning_row(
                canonical_field_pattern=pattern,
                canonical_default_value=default,
                applies_to_phase_modes=list(modes),
                source_chains=["all validated governance chains"],
                why_required=f"Repeated across governance chains; default {default} prevents permission misread",
                should_be_in_canonical_contract=True,
                domain_override_allowed=False,
            )
        )
    return rows


def _build_phase_mode_lifecycle_plan() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for mode, meaning, allowed, forbidden in PHASE_MODES:
        rows.append(
            _planning_row(
                phase_mode=mode,
                canonical_meaning=meaning,
                allowed_actions=allowed,
                forbidden_actions=forbidden,
                required_readiness_fields=[f"ready_for_{mode.lower().replace(' ', '_').replace('-', '_')}"],
                required_non_claims=[f"{mode} GO does not mean real execution is authorized"],
                required_verifier_baseline=["MIN_CHECKS>=420", "boundary_ok=true", "freeze fields all false"],
                source_examples=["Permission Semantics", "Evidence Chain", "Boundary Object Registry Generation"],
                should_be_in_canonical_contract=True,
            )
        )
    return rows


def _build_domain_constraint_plan() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for name, scope, sources, module_output in DOMAIN_CONSTRAINTS:
        rows.append(
            _planning_row(
                domain_constraint_name=name,
                domain_scope=scope,
                source_chains=list(sources),
                domain_specific_forbidden_shortcuts=[f"{name}: planning/dry-run/review ≠ execution"],
                domain_specific_required_fields=[f"{name}_specific_freeze_fields"],
                domain_specific_no_go_conditions=[f"{name}: permission release without authorization"],
                domain_specific_non_claims=[f"{name} GO does not mean domain execution authorized"],
                inherits_canonical_contract=True,
                planned_module_output=module_output,
            )
        )
    return rows


def _build_inheritance_policy_plan() -> Dict[str, Any]:
    return _planning_row(
        inheritance_model="canonical_contract_plus_domain_constraints",
        new_phase_must_declare_inherits=True,
        new_phase_must_declare_phase_mode=True,
        new_phase_must_declare_domain_constraints=True,
        new_phase_must_declare_specific_objects=True,
        new_phase_must_declare_specific_no_go=True,
        copying_full_canonical_freeze_fields_forbidden_later=True,
        domain_specific_extension_allowed=True,
        canonical_override_requires_explicit_approval=True,
        verifier_must_load_constraint_manifest_later=True,
        phase_template_must_reference_constraint_module_later=True,
    )


def _build_legacy_absorption_policy_plan() -> Dict[str, Any]:
    return _planning_row(
        legacy_phase_status="legacy_validated_governance_chain",
        rewrite_policy="do_not_rewrite_except_factual_correction",
        absorption_note_required_later=True,
        legacy_as_source_evidence=True,
        legacy_as_template_source=False,
        old_chain_archival_required_now=False,
        old_chain_modification_allowed_now=False,
        legacy_phases_preserved=True,
        legacy_eval_out_preserved=True,
        legacy_verifier_reports_preserved=True,
        factual_correction_record_allowed=True,
    )


def _build_output_plan() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for artifact, purpose, source_plans in PLANNED_MODULE_ARTIFACTS:
        rows.append(
            _planning_row(
                planned_artifact=artifact,
                purpose=purpose,
                source_plans=list(source_plans),
                used_by_future_verifier=True,
                used_by_future_phase_template=True,
                used_by_future_cursor_instructions=True,
                not_generated_now=True,
            )
        )
    return rows


def run_governance_constraint_module_legacy_extraction_planning_v1() -> Dict[str, Any]:
    chain_rows = _build_legacy_chain_inventory()
    matrix_rows = _build_phase_to_constraint_matrix()
    frozen_rows = _build_frozen_field_plan()
    lifecycle_rows = _build_phase_mode_lifecycle_plan()
    domain_rows = _build_domain_constraint_plan()
    inheritance_plan = _build_inheritance_policy_plan()
    absorption_plan = _build_legacy_absorption_policy_plan()
    output_rows = _build_output_plan()

    blockers: List[str] = []
    if len(chain_rows) < 10:
        blockers.append("legacy chain inventory must cover >=10 chains")
    if len(matrix_rows) < 14:
        blockers.append("phase to constraint matrix must cover >=14 domains")
    if len(frozen_rows) < 20:
        blockers.append("frozen field plan must cover >=20 patterns")
    if len(lifecycle_rows) < 12:
        blockers.append("phase mode lifecycle plan must cover >=12 modes")
    if len(domain_rows) < 12:
        blockers.append("domain constraint plan must cover >=12 domains")
    if len(output_rows) < 12:
        blockers.append("output plan must cover >=12 artifacts")

    if any(r.get("rewrite_required") for r in chain_rows):
        blockers.append("legacy chains must not require rewrite")
    if any(r.get("deprecated") for r in chain_rows):
        blockers.append("legacy chains must not be marked deprecated")
    if any(not r.get("not_generated_now") for r in output_rows):
        blockers.append("planned artifacts must have not_generated_now=true")
    if inheritance_plan.get("inheritance_model") != "canonical_contract_plus_domain_constraints":
        blockers.append("inheritance model must be canonical_contract_plus_domain_constraints")
    if absorption_plan.get("legacy_as_template_source") is not False:
        blockers.append("legacy chains must not be template source")

    planning_ready = not blockers
    boundary_ok = planning_ready

    legacy_extraction_planning_policy = _planning_row(
        phase_name=PHASE_ID,
        purpose="extract reusable governance constraints from legacy validated governance chains",
        main_migration_chain_paused=MAIN_MIGRATION_PAUSED,
        main_migration_resume_phase=MAIN_MIGRATION_RESUME_PHASE,
        governance_constraints_ref=CONSTRAINT_DOC_ID,
    )

    legacy_governance_chain_inventory = {
        "rows": chain_rows,
        "row_count": len(chain_rows),
        "all_legacy_validated": all(r.get("legacy_validated_governance_chain") for r in chain_rows),
        "none_deprecated": not any(r.get("deprecated") for r in chain_rows),
        "none_rewrite_required": not any(r.get("rewrite_required") for r in chain_rows),
        **_planning_meta(),
    }

    legacy_phase_to_constraint_source_matrix = {
        "rows": matrix_rows,
        "row_count": len(matrix_rows),
        "constraint_domain_count": len(CONSTRAINT_DOMAINS),
        **_planning_meta(),
    }

    canonical_frozen_field_extraction_plan = {
        "rows": frozen_rows,
        "row_count": len(frozen_rows),
        "all_in_canonical_contract": all(r.get("should_be_in_canonical_contract") for r in frozen_rows),
        **_planning_meta(),
    }

    phase_mode_lifecycle_contract_extraction_plan = {
        "rows": lifecycle_rows,
        "row_count": len(lifecycle_rows),
        "all_in_canonical_contract": all(r.get("should_be_in_canonical_contract") for r in lifecycle_rows),
        **_planning_meta(),
    }

    domain_constraint_extraction_plan = {
        "rows": domain_rows,
        "row_count": len(domain_rows),
        "all_inherit_canonical": all(r.get("inherits_canonical_contract") for r in domain_rows),
        **_planning_meta(),
    }

    governance_constraint_inheritance_policy_plan = inheritance_plan

    legacy_absorption_policy_plan = absorption_plan

    governance_constraint_module_output_plan = {
        "rows": output_rows,
        "row_count": len(output_rows),
        "all_not_generated_now": all(r.get("not_generated_now") for r in output_rows),
        **_planning_meta(),
    }

    legacy_extraction_planning_readiness_decision = {
        "ready_for_governance_constraint_module_legacy_extraction_dryrun": boundary_ok,
        "ready_for_governance_constraint_module_generation": False,
        "ready_for_canonical_phase_template_generation": False,
        "ready_for_verifier_integration": False,
        "ready_for_phase_template_modification": False,
        "ready_for_automation_implementation": False,
        "ready_for_legacy_document_rewrite": False,
        "ready_to_resume_main_migration_chain": False,
        "legacy_extraction_planning_completed": boundary_ok,
        "legacy_chain_inventory_planned": len(chain_rows) >= 10,
        "phase_to_constraint_mapping_planned": len(matrix_rows) >= 14,
        "canonical_frozen_field_extraction_planned": len(frozen_rows) >= 20,
        "phase_mode_lifecycle_contract_planned": len(lifecycle_rows) >= 12,
        "domain_constraint_extraction_planned": len(domain_rows) >= 12,
        "inheritance_policy_planned": True,
        "legacy_absorption_policy_planned": True,
        "output_plan_generated": len(output_rows) >= 12,
        "main_migration_chain_paused": MAIN_MIGRATION_PAUSED,
        "main_migration_resume_phase": MAIN_MIGRATION_RESUME_PHASE,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_planning_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "legacy_chain_count": len(chain_rows),
        "constraint_domain_count": len(matrix_rows),
        "frozen_field_pattern_count": len(frozen_rows),
        "phase_mode_count": len(lifecycle_rows),
        "domain_constraint_count": len(domain_rows),
        "planned_artifact_count": len(output_rows),
        "main_migration_chain_paused": MAIN_MIGRATION_PAUSED,
        "main_migration_resume_phase": MAIN_MIGRATION_RESUME_PHASE,
        "inheritance_model": inheritance_plan.get("inheritance_model"),
        "legacy_as_template_source": absorption_plan.get("legacy_as_template_source"),
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_planning_meta(),
    }

    return {
        "summary": summary,
        "legacy_extraction_planning_policy": legacy_extraction_planning_policy,
        "legacy_governance_chain_inventory": legacy_governance_chain_inventory,
        "legacy_phase_to_constraint_source_matrix": legacy_phase_to_constraint_source_matrix,
        "canonical_frozen_field_extraction_plan": canonical_frozen_field_extraction_plan,
        "phase_mode_lifecycle_contract_extraction_plan": phase_mode_lifecycle_contract_extraction_plan,
        "domain_constraint_extraction_plan": domain_constraint_extraction_plan,
        "governance_constraint_inheritance_policy_plan": governance_constraint_inheritance_policy_plan,
        "legacy_absorption_policy_plan": legacy_absorption_policy_plan,
        "governance_constraint_module_output_plan": governance_constraint_module_output_plan,
        "legacy_extraction_planning_readiness_decision": legacy_extraction_planning_readiness_decision,
    }
