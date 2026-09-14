# Cognitive Flow Existing Asset Mapping v1

## Mapping Scope

This mapping is read-only. It records available modules and planning assets for Route A; it does not change code, registries, lifecycles, or ownership.

| Existing asset | Observed current role | Cognitive Flow placement | Classification | Route A handling |
| --- | --- | --- | --- | --- |
| Field Event Admission | Deterministic candidate admission with source/evidence/trace/time preservation | Perception Admission → Field Kernel gate | directly reusable | retain as the sole input eligibility boundary for Reducer candidates |
| Temporal Validity | Timezone-aware assessment, expiry, ordering and deferral rules | Field Kernel temporal boundary | directly reusable | extend only through later protocol alignment, not parallel time logic |
| Field State Reducer | Consumes admitted events and owns candidate Field State reduction | Field Kernel | directly reusable | preserve singular mutation authority |
| Field State Read Model | Read-only query/projection surface | Field Kernel → Cognitive Analysis read surface | directly reusable | use as analysis input; do not add write paths |
| Task Manager | Task lifecycle, safety/confirmation/owner gates, guidance candidates | Cognitive Delivery execution boundary | directly reusable | consume delivery candidates only through explicit contract work |
| Observation Attention | Region priority and follow-up model-route candidates | Perception Admission attachment | directly reusable | keep as observation scheduling, not interpretation/fact authority |
| Model Manager | Provider/capability governance and model-output boundary | external capability attachment | directly reusable | route bounded requests; never fact or decision authority |
| Human Correction Layer | Correction/review/training-signal candidates, no direct overwrite | Perception Admission / review evidence input | directly reusable | retain human correction as evidence and review, not ground truth |
| Situation Understanding Model | Situation, uncertainty, missing-information and capability hints | Cognitive Analysis attachment | needs upgrade | refactor future outputs into explicit hypothesis/difference/gap protocols; retain candidate-only boundary |
| Case Library | Deterministic situation-case records with provenance and review gating | early Experience System substrate | needs upgrade | evolve records into Experience Episode candidates; remove UUID/non-deterministic assumptions in a later authorized phase |
| Evidence Chain | Source-chain, lifecycle, acceptance and non-substitution governance | shared lineage substrate | directly reusable | reuse reference/lifecycle rules; evidence still does not establish fact |
| OCR / SLAM / TTS/ASR | perception or expression capability modules | external organs / capability attachments | future replacement in core flow | retain as providers; replace any core-logic role with protocols and cognitive domains |
| Legacy scene/model test-lens UI assets | visualization and testing surfaces | diagnostics / interface attachments | temporarily unused | do not make them cognitive authority; revisit after A3 delivery contracts |

## Source Evidence Read

- Field State Reducer module types declare `admitted_events` as input and candidate-only/no-fact output flags.
- Field State Read Model documents read-only, no mutation, no event reduction, and no runtime-loop ownership.
- Task Manager contract grants task lifecycle submission/governance rather than factual world ownership.
- Observation Attention explicitly emits attention and route candidates, not facts or actions.
- Human Correction explicitly produces correction/review candidates and prohibits direct overwrite or automatic ground truth.
- Situation Understanding exposes uncertainty, missing-information and case-reference schemas suitable for later protocol decomposition.
- Situation Case Library retains candidate-only and provenance fields but is not yet an Experience System.
- Evidence Chain governance preserves source-chain and non-substitution rules.

## Mapping Decisions

1. The Field Kernel is not replaced; it is the current cognitive-flow anchor.
2. Perception attachments remain replaceable and must enter through admission/evidence boundaries.
3. Situation Understanding and Case Library are inputs to future Cognitive Analysis and Experience System work, not their final architecture.
4. No existing asset is authorized to define Hive, individual values, or a central decision mechanism.

