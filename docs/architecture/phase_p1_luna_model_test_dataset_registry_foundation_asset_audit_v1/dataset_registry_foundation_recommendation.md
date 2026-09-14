# Dataset Registry Foundation Recommendation

> Alignment note (Phase-P1-Luna-Field-Cognition-Evaluation-Dual-Test-Plane-Alignment-And-Dataset-Ingress-v1-001): the prior recommendation is preserved and implemented as an evaluation-only foundation. Dataset meaning is now explicitly Evaluation World / Observation Corpus for Plane A first, with Plane B as a consumer rather than the registry's primary purpose.

## Recommendation

**DATASET_REGISTRY_FOUNDATION_REQUIRED**

The repository lacks a generic, durable, cross-modal Dataset Registry. The
existing OCR registry proves the need and provides conventions, but cannot
represent the requested public benchmark, Luna scenario, and future real
observation classes without domain leakage.

## Canonical location recommendation

Future implementation location:

`capabilities/evaluation/dataset_registry/`

This location is proposed only. No implementation is created in this phase.
The registry should be evaluation-only, candidate/metadata oriented, and
forbidden from runtime loading or mainline semantic mutation.

## Three dataset classes

The generic entry should support, without hard-coding any dataset:

- `PUBLIC_BENCHMARK`: external benchmark with declared license, source, split,
  and ground-truth quality.
- `LUNA_SCENARIO`: curated first-person/daily-life/accessibility/navigation-like
  scenario declarations with explicit provenance and review state.
- `FUTURE_REAL_OBSERVATION`: device-generated observations and regression cases,
  subject to consent, privacy, retention, and review gates.

COCO, Open Images, Objects365, LVIS, BDD100K, Mapillary Vistas, Ego4D, and
EPIC-KITCHENS are future declaration examples only. Nothing is downloaded or
registered here.

## Registry relationship map

`Dataset Registry`
→ references `Capability/Slot`, `Model Registry`, `Provider Registry`, and
`Model↔Provider bindings`
→ is consumed by `Model Test Case Manifest` / MUEP / Evaluation Reports
→ produces protected evidence refs in `TestBoard`.

It does not own model selection, provider invocation, Runtime Admission,
Current World, Field, Decision, Task, Action, Memory, or World Truth.

## Source-of-truth rules

- A registry entry must identify its source, version, license/consent status
  where applicable, provenance, and lifecycle.
- A sample must point to a dataset version and an input/media reference.
- Ground truth is evaluation ground truth, not Luna World Truth.
- Human correction remains a review candidate until explicitly accepted under
  data-quality policy.
- `_tmp_eval_out`, `_eval_out`, and Test Lens generated envelopes are evidence
  or run artifacts, never dataset source-of-truth.
- The RF-DETR smoke image is not a dataset member until a future explicit
  registration records its provenance and annotation status.

## Future validation boundary

Validation should detect duplicate IDs, missing owner/version/provenance,
unknown model/capability/provider refs, missing split/sample links, invalid
annotation status, unsupported lifecycle, and runtime-enabled dataset entries.
It must not become Runtime Admission or execute a model.
