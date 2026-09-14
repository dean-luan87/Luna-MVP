# Recommended Next Implementation Scope

## One coherent module

Recommended next module: **Level-1 Cognitive Evaluation Run Boundary and Durable Archive Bridge** under `capabilities/evaluation/`, extending the existing `dataset_registry`, `level1_field_cognition_suite`, `a_route_cognitive_whitebox_foundation`, and common evaluation result contracts.

This is one evaluation-owned integration module, not a new runtime owner. Its purpose is to move one explicit registered World Sample through one Level-1 case, accept actual A-Route/candidate refs, project the existing V1 White-box Trace/Profile/Gap contracts, emit separate Plane A and Plane B result refs, and append an immutable versioned evaluation record for future baseline comparison.

## MUST IMPLEMENT NOW in the next phase

- explicit dataset/sample registration persistence and registry-membership validation;
- one real Level-1 case manifest referencing registered sample and layered GT refs;
- a bounded ingress from the actual A-Route evidence/cognition path, with unavailable nodes remaining unavailable;
- reuse of `CognitiveWhiteBoxTraceV1`, `LunaCognitiveExecutionProfileV1`, and `CognitiveFailureGapRefV1`;
- dual-plane result and evidence-backed failure attribution;
- append-only archive identity for run, Luna/code/config, dataset/sample/case, trace/profile, versions, environment, outcome, and TestBoard refs;
- structural protection against treating evaluation result, GT, human correction, or provider output as World Truth.

## REUSE AS-IS

- Dataset Registry types and explicit-registration guard;
- Level-1 category/assertion/perturbation vocabulary and sample-to-case composer;
- White-box V1 trace/profile/gap contracts and availability semantics;
- existing Observation/Evidence/Gateway candidates;
- Model Test Lens envelope/TestBoard references as auxiliary evidence surfaces;
- Capability/Model/Provider governance and RF-DETR evidence precedent.

## DEFER

- large-scale ingestion and public dataset download;
- broad model/provider comparison and model-fit scoring;
- Knowledge/Experience extraction and promotion workflow;
- White-box UI;
- Level 2 Role cognition, Memory, B-Route, Learning, Emotion;
- semantic compression and resource metrics that are not observable.

## DO NOT BUILD

- Dataset Manager or parallel registry;
- new Test Case, Trace, Profile, Result Envelope, or TestBoard system;
- Model Selector, runtime binding mutation, training infrastructure, automatic annotation, data lake, or runtime cognition owner.

