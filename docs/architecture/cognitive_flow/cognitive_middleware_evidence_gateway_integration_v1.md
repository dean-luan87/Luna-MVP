# Middleware Evidence Gateway Integration v1

## Purpose

The Evidence Gateway is the only Cognitive Middleware return boundary that makes Provider output available to Neural Governance. It packages provenance, scope, reliability, status, and conflicts while leaving world understanding and truth outside Middleware authority.

```mermaid
flowchart LR
    P[Provider Output] --> A[Provider / Evidence Adapter]
    A --> C[Evidence Candidate]
    C --> G[Evidence Gateway]
    G --> R[Middleware Report]
    R --> N[Neural Feedback Package]
    N --> B[Brain Update Candidate]
```

## Existing asset mapping

| Existing asset class | Reintegrated Gateway role | Status |
|---|---|---|
| `model_manager/.../document_surface_detector_evidence_normalizer_v1.py` | Provider-output normalization evidence. | MIGRATE / adapt |
| `model_manager/.../mixed_region/context_evidence_builder_v1.py` | Context/provenance-oriented evidence construction support. | MIGRATE / adapt |
| `model_manager/collaboration/evidence_fusion_processor_v1.py` and dry-run equivalents | Structural aggregation/conflict-support input. | MIGRATE / authority-restrict |
| Field Perception handoff output/diagnostics/trace assets | Candidate-only perception handoff provenance. | MIGRATE / adapt |
| Model Manager output builder and health diagnostics | Provider status, lifecycle, resource, and trace metadata. | KEEP / project |

## Gateway contract

An Evidence Candidate must include source/provider references, capability and CWO/session references, timestamp/scope, confidence/reliability metadata, uncertainty, status/failure/degradation information, and trace provenance.

## Prohibitions

- Provider Output ≠ Reality.
- Evidence Candidate ≠ Truth.
- Evidence Gateway does not decide cognitive completion, select a Goal, allocate Attention, mutate state, or execute Action.
- Evidence fusion cannot erase disagreement; conflict remains a Conflict Candidate for Neural/Brain handling.

The phase only maps existing normalizer/fusion assets into this boundary. It creates no new gateway implementation.
