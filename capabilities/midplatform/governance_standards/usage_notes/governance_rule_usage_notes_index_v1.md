# Governance Rule Usage Notes Index V1

**Library:** `capabilities/midplatform/governance_standards/`  
**Phase:** `Phase-P1-Midplatform-Governance-Standards-Packaging-Planning-v1-001`  
**Status:** Planning — per-rule usage notes required before packaging execution

---

## 1. How to Select a Governance Rule

1. Identify phase type: planning / request / execution / post-review / registry patch / closure  
2. Search `legacy_rules/legacy_reusable_governance_rules_inventory_v1.json` by `category` or `when_to_use`  
3. Prefer existing `rule_id` over creating new rules  
4. Confirm `forbidden_usage` does not apply to your scenario  
5. Cite `canonical_target_path` (after packaging) or `current_source_refs` (during transition)

---

## 2. Rule Categories

| Category | Examples |
|----------|----------|
| test_board_governance | TestBoardProtectedArtifactRuleV1 |
| controlled_trial_governance | ControlledTrialGovernanceLifecycleTemplateV1 |
| owner_approval | OwnerApprovalGovernanceStandardV1 |
| negative_guards | NegativeGuardPatternV1 |
| failure_semantics | GO / FAILED_NO_BOUNDARY / BLOCKED |
| registry_patch | snapshot, diff, scoped mutation |
| model_onboarding | ModelAssetOnboardingGovernanceStandardV1 |
| runtime_boundary | admission gate, exclusion |
| input_output_symmetry | traceability, evidence refs |
| protocol_governance | canonical path, version, owner |
| file_governance | file size, module split |
| validation_rules | validate-once reference |
| evidence_candidate | fact admission |
| rollback | snapshot, rollback readiness |
| artifact_protection | cleanup forbidden scope |
| main_program_separation | policy not execution |

---

## 3. Common Phase Patterns

| Pattern | Required Rules |
|---------|----------------|
| Planning only | test_board, negative_guards, controlled_trial template |
| Request/Approval/Readiness | owner_approval, controlled_trial, test_board |
| Execution/Post-Review | failure_semantics, negative_guards, rollback, artifact_protection |
| Registry patch | registry_patch, rollback, owner_approval |
| Model onboarding | model_onboarding + all sub-rules |
| Runtime admission | runtime_boundary + exclusion + owner_approval |

---

## 4. When to Reuse Existing Rule Instead of Creating a New One

- Same gate semantics (install approval, registry patch, test board)  
- Same failure semantics (FAILED_NO_BOUNDARY vs BLOCKED)  
- Same lifecycle template (planning → execution → post-review)  
- Same exclusion boundary (runtime, semantic, fact, navigation)

**Reuse first.** Duplication is forbidden unless inventory has no match.

---

## 5. How to Cite a Standard in a Phase Instruction

```
Must reference:
- rule_id: ModelAssetOnboardingGovernanceStandardV1
- canonical_path: capabilities/midplatform/governance_standards/model_onboarding/...
- usage_note: see governance_rule_usage_notes_index_v1.md
```

Do not paste full rule text into phase instructions — cite `rule_id` and path.

---

## 6. How to Handle Similar Workflows

1. Map workflow to existing categories  
2. If ≥80% overlap with existing rule → **must reuse**  
3. If gap is narrow → **standard patch phase** (extend, do not fork)  
4. If genuinely new domain → new standardization phase with usage note

---

## 7. When a New Rule Is Allowed

- No inventory rule covers the governance concern  
- After explicit standardization phase with usage note + negative guards  
- With canonical path, owner_layer, test board record

---

## 8. When Rule Duplication Is Forbidden

- Reimplementing test board rules per phase  
- Re-defining GO/FAILED_NO_BOUNDARY/BLOCKED per module  
- Per-model onboarding lifecycle redesign  
- Inline governance in runtime main program

---

## 9. How to Update a Standard

1. Open **standard patch phase** (not silent edit)  
2. Bump version in manifest  
3. Preserve historical evidence (original files non-deletable)  
4. Update usage note if behavior changes  
5. Re-run negative guards

---

## 10. How to Deprecate a Standard

1. Mark `lifecycle_status = deprecated` in manifest  
2. Add successor `rule_id` reference  
3. Keep deprecated artifact for audit  
4. Update usage notes index with migration path

---

## 11. How to Preserve Historical Evidence

- Never delete original phase review artifacts  
- Packaging execution copies, does not move  
- `source_path` retained in manifest alongside `canonical_path`

---

## 12. How to Keep Main Program Separated

- Main program imports admission **results**, not governance executors  
- governance_standards has no model calls, no downloads, no fact writes  
- Runtime cannot bypass admission gate  
- Business code cites `rule_id`, not duplicated policy text

---

## Per-Rule Usage Notes

Full per-rule `when_to_use`, `how_to_use`, `forbidden_usage` fields are in:

`legacy_rules/legacy_reusable_governance_rules_inventory_v1.json`

---

*End of Usage Notes Index V1 (Planning)*
