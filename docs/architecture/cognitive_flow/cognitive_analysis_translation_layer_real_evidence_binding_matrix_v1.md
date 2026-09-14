# A3 Translation Layer Real Evidence Binding Matrix v1

| provider family | governed Evidence Envelope input | existing Translation Request mapping | permitted primitive candidate | prohibited escalation |
| --- | --- | --- | --- | --- |
| OCR | `evidence_ref` for text candidate; `source_capability_ref`; confidence/uncertainty; provenance/trace | `evidence_refs`, `source_capability_refs`, `provenance_refs`, `trace_ref`, read-only `context_refs` | `semantic_candidate` | text → Fact, final meaning, instruction, Decision/Action |
| Vision | `evidence_ref` for object/scene candidate; provider/source provenance; uncertainty/trace | same reference mapping; provider remains provenance only | `entity_candidate` or `relation_candidate` | object → confirmed Entity/identity; provider identity → Entity |
| Audio | `evidence_ref` for speech/sound/speaker candidate; source/trace and uncertainty | same reference mapping; no raw audio payload | `semantic_candidate` or separately governed `entity_candidate` | identity/relationship confirmation; command/action |
| Spatial | `evidence_ref` for location/spatial candidate; coordinate/context provenance and trace | same reference mapping; retain temporal/uncertainty limits | `spatial_candidate` or `temporal_candidate` | navigation decision, route action, Field/State update |

## Required Provider Mapping Evidence

Every row requires non-empty source/provider reference, Evidence reference, Context reference, provenance reference, trace reference, declared requested primitive type, uncertainty retention, and a candidate-only status. Unsupported mapping, missing provenance, hidden provider identity, or a raw payload substitution blocks the binding request.

## Mapping Invariants

- Provider-native output remains external Evidence content and is not copied as Translation input.
- Translation can only use the already frozen primitive vocabulary: Entity, Relation, Semantic, Spatial, or Temporal Candidate.
- Multiple provider contributions remain separate evidence references unless a future governed composition contract is approved.

