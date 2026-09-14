# Luna Field-Centric Layered Architecture Plan v1

## A. Architecture Motivation
- Shift from model- and capability-driven composition to field-centric cognitive structuring.
- Do not replace existing assets wholesale; preserve and reuse prior governance, test, and verification investments.
- Keep existing protocol, admission, boundary, and evidence chain assets as reusable horizontal infrastructure.

## B. Target Top-Level Architecture

### cognition/
- observation_scan
- field_understanding
- situation_goal
- expectation
- attention
- region_intelligence
- role_relation_inference
- evidence_fusion
- decision
- interaction
- feedback_memory

### governance/
- constitution
- cognitive_constitution
- layer_charters
- cross_layer_protocols
- candidate_fact_admission
- model_skill_admission
- runtime_boundary
- evidence_chain
- permission_owner_approval
- negative_guards
- change_control
- rollback_revocation

### evaluation/
- model_test_lens
- layer_test_lens
- case_registry
- verifiers
- human_correction
- diagnostics
- trace_review
- post_review_freeze

### providers/
- vision
- ocr
- audio
- location
- network
- external_models
- local_models
- tools

### runtime/
- controlled_execution
- sandbox
- admission_runtime
- execution_trace
- fallback_abort

## C. Cognitive Vertical Stack

### L0 Observation Scan
- Purpose: collect raw observations and boundary signals.
- Allowed responsibilities: observation intake, signal registration, candidate generation.
- Prohibited responsibilities: fact admission, runtime activation, full-world reconstruction.
- Input ownership: observation channel.
- Output ownership: observation candidate.
- Interpretation ownership: layer-local interpretation only.
- Candidate types: observation_candidate.
- Stop condition: insufficient signal quality for downstream reasoning.
- Abstain condition: no reliable observation signal.
- Next-layer handoff: field_understanding

### L1 Field Understanding
- Purpose: build a minimal field representation.
- Allowed responsibilities: field candidate generation, field-state framing, weak-structure maintenance.
- Prohibited responsibilities: production action, irreversible execution, full scene reconstruction.
- Input ownership: observation scan outputs.
- Output ownership: field candidate.
- Interpretation ownership: field understanding layer.
- Candidate types: field_candidate.
- Stop condition: no stable field candidate.
- Abstain condition: insufficient field evidence.
- Next-layer handoff: expectation generation

### L2 Situation and Goal
- Purpose: frame current situation and goal state.
- Allowed responsibilities: situation and goal candidate generation.
- Prohibited responsibilities: hidden state injection, policy override.
- Input ownership: field understanding outputs.
- Output ownership: situation_goal candidate.
- Interpretation ownership: situation and goal layer.
- Candidate types: situation_goal_candidate.
- Stop condition: incomplete situation context.
- Abstain condition: goal unresolved.
- Next-layer handoff: expectation generation

### L3 Expectation Generation
- Purpose: generate expectation candidates for what should be true or relevant.
- Allowed responsibilities: expectation candidate generation and comparison.
- Prohibited responsibilities: fact admission, runtime policy override.
- Input ownership: situation_goal layer.
- Output ownership: expectation candidate.
- Interpretation ownership: expectation layer.
- Candidate types: expectation_candidate.
- Stop condition: no expectation candidate.
- Abstain condition: expectation unresolved.
- Next-layer handoff: attention allocation

### L4 Attention Allocation
- Purpose: focus processing on the most relevant field regions and cues.
- Allowed responsibilities: salience scoring, attention candidate generation.
- Prohibited responsibilities: autonomous action, over-commitment to weak evidence.
- Input ownership: expectation outputs.
- Output ownership: attention candidate.
- Interpretation ownership: attention layer.
- Candidate types: attention_candidate.
- Stop condition: no actionable attention target.
- Abstain condition: attention remains ambiguous.
- Next-layer handoff: region intelligence

### L5 Region Intelligence
- Purpose: produce region-level evidence candidates.
- Allowed responsibilities: region evidence generation and evidence packaging.
- Prohibited responsibilities: model activation, production execution, full-world reconstruction.
- Input ownership: attention outputs.
- Output ownership: region_evidence candidate.
- Interpretation ownership: region intelligence layer.
- Candidate types: region_evidence_candidate.
- Stop condition: no region evidence candidate.
- Abstain condition: region evidence insufficient.
- Next-layer handoff: role and relation inference

### L6 Role and Relation Inference
- Purpose: infer role and relation candidates.
- Allowed responsibilities: role and relation hypothesis generation.
- Prohibited responsibilities: irreversible intervention, fact promotion.
- Input ownership: region evidence outputs.
- Output ownership: role_candidate and relation_candidate.
- Interpretation ownership: role inference layer.
- Candidate types: role_candidate, relation_candidate.
- Stop condition: no role or relation candidate.
- Abstain condition: role hypothesis unresolved.
- Next-layer handoff: evidence fusion

### L7 Evidence Fusion
- Purpose: integrate evidence candidates into a coherent candidate state.
- Allowed responsibilities: evidence fusion, uncertainty packaging, evidence conflict marking.
- Prohibited responsibilities: production action, fact promotion without admission.
- Input ownership: role and relation outputs.
- Output ownership: fused evidence candidate.
- Interpretation ownership: evidence fusion layer.
- Candidate types: evidence_candidate.
- Stop condition: evidence remains incoherent.
- Abstain condition: insufficient evidence coherence.
- Next-layer handoff: decision and interaction

### L8 Decision and Interaction
- Purpose: decide whether interaction is necessary and what form it should take.
- Allowed responsibilities: interaction decision candidates, communication actions, pause or request confirmation.
- Prohibited responsibilities: autonomous irreversible action, production execution.
- Input ownership: fused evidence outputs.
- Output ownership: interaction decision candidate.
- Interpretation ownership: decision and interaction layer.
- Candidate types: interaction_decision_candidate.
- Stop condition: no interaction necessary.
- Abstain condition: interaction decision unresolved.
- Next-layer handoff: feedback and memory

### L9 Feedback and Memory
- Purpose: record feedback, memory candidates, and unresolved state for future correction.
- Allowed responsibilities: memory candidate generation, correction candidate generation.
- Prohibited responsibilities: production action, implicit fact promotion.
- Input ownership: interaction decision outputs.
- Output ownership: feedback_candidate and memory_candidate.
- Interpretation ownership: feedback and memory layer.
- Candidate types: feedback_candidate, memory_candidate.
- Stop condition: no memory update required.
- Abstain condition: no durable memory candidate.
- Next-layer handoff: none

## D. Normative Hierarchy
- L0 Survival and Safety Constitution
  → L1 Field-Centric Cognitive Constitution
  → L2 Cognitive Layer Charters
  → L3 Cross-Layer and Layer-Internal Protocols
  → L4 Model / Skill / Provider Contracts
  → L5 Runtime Execution Rules
- Lower layers may not override higher-layer constitutional rules.
- Field rules may not override the life-and-safety constitution.
- Providers may not decide cognitive structure.
- Runtime may not promote a candidate to fact.

## E. Horizontal Governance Reuse
- Reuse the existing Model Test Lens as a layer-agnostic evaluation primitive.
- Reuse the Model / Skill Admission Contract across layers.
- Reuse the Runtime Boundary Contract as the execution guardrail.
- Reuse Candidate / Fact Admission for all candidate promotion decisions.
- Reuse the Evidence Chain as the common evidence path.
- Reuse Input / Output Symmetry for all layer boundaries.
- Reuse Negative Guards for non-executing safety boundaries.
- Reuse Verifier, Human Correction, Trace and Diagnostics, Change Control, Post-Review / Freeze, Rollback / Revocation, and Owner Approval as shared governance services.
- The governance stack serves all layers horizontally rather than being reimplemented per layer.

## F. Interaction Loop
- Enter Field
  → Field Candidate
  → Expectation
  → Attention
  → Region Evidence
  → Role / Relation Candidate
  → Interaction Necessity
  → Interaction Decision
  → Feedback Observation
  → Field Correction
  → Memory Candidate
- Allowed interaction actions include speak, ask, remind, observe, stay silent, query external knowledge, request confirmation, pause task, and record unresolved candidate.

## G. Minimum Vertical Slice
- Field Candidate
  → Expectation Candidate
  → Attention Candidate
  → Region Evidence Candidate
  → Role Candidate
  → Interaction Decision Candidate
  → Feedback Candidate
- This slice remains candidate-only, not_fact, without production activation, without autonomous irreversible action, and without full-world reconstruction.

## H. Migration Strategy
### Wave 0
- Architecture freeze only.

### Wave 1
- Logical ownership mapping; no file movement.

### Wave 2
- Compatibility aliases and adapters only.

### Wave 3
- Controlled directory migration planning.

### Wave 4
- Controlled migration dry-run.

### Wave 5
- Real migration only after owner approval.

This phase does not execute any migration.

## I. Stop Conditions
- Do not implement all cognitive layers at once.
- Do not rewrite existing Model Admission.
- Do not rewrite Runtime Boundary.
- Do not rebuild the test center.
- Do not batch-move files.
- Do not batch-change imports.
- Do not delete old directories.
- Do not train models.
- Do not activate runtime.
- Do not enter production.
- Stop immediately after planning artifacts are complete.
