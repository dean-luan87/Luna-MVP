# Engineering Health Remediation v1

## Phase and authority

- Phase: `Phase-Engineering-Health-Remediation-v1-001`
- Stage: historical engineering debt remediation
- Execution Mode: `Remediation`
- Previous Phase: `Phase-Cognitive-Architecture-Consolidation-and-Dependency-Map-v1-001`
- Previous Phase Decision: `BLOCKED_BEFORE_USER_TERMINAL_VERIFICATION`
- Agent stop point: `WAITING_FOR_USER_TERMINAL_VERIFICATION`

This phase fixes only the confirmed syntax defect and creates governance
registries. It does not create a capability, redesign cognition, implement
Runtime, or connect Model, Provider, Hardware, OCR, SLAM, or VLM.

## Remediation scope

### R1 — Python syntax

The single confirmed blocker was
`capabilities/midplatform/model_test_lens/multi_model_interaction/mobile_sam_ocr_controlled_execution_types_v1.py`.
The affected `RECOMMENDED_NEXT_PHASE` block contained dictionary fields inside
parentheses and had a duplicate definition. The remediation preserves the
field meanings as `BOUNDARY_FLAGS`, restores the string
`RECOMMENDED_NEXT_PHASE`, and changes no protocol or capability behavior.

### R2 — Architecture inventory

The inventory distinguishes `active`, `historical`, `verification_only`, and
`missing_asset_candidate`. Historical assets are retained. Missing assets are
registered only; this phase does not auto-create them.

### R3 — Canonical Schema Registry

New references must use a canonical ID. Existing names remain available as
aliases until a separately approved migration. No file is deleted or moved by
this phase.

### R4 — Large-file governance

Python thresholds are: ≤600 normal, >800 warning, and >1200 blocker
candidate. This phase registers risk and priority only; it does not split
files or perform large-scale refactoring.

## Required checks

V0 Agent checks:

- JSON parse for every phase asset;
- `py_compile` for the phase verifier;
- `python3 -m compileall capabilities/` after the syntax remediation;
- inventory, canonical registry, duplicate map, and large-file registry
  consistency checks;
- static boundary scan for Runtime, Model, Hardware, Provider, Action, and
  automatic Learning introduction.

V1 is not separately authorized. V2 Final Phase Verification is User Terminal
Only. V3 is ChatGPT Only. V0 never grants GO.

## Non-goals and negative guards

No new Capability, Model, Hardware, Provider, Runtime, Action, OCR, SLAM, VLM,
automatic Learning, schema redesign, historical asset deletion, mass rewrite,
check weakening, hardcoded pass, or failure hiding by rename.

Exact negative guards: no Model Runtime; no Hardware Runtime; no Action
execution; no automatic Learning; no schema redesign; no historical asset
deletion; no hardcoded pass.
Exact phrase guards: no Action execution; no historical asset deletion.
