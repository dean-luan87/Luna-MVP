# Canonical Flow Contract Inventory v1

## Reuse-first inventory

| Existing family | Needed use | Classification | Closure action |
|---|---|---|---|
| `CapabilityResolutionCandidateV1` | logical capability resolution | REUSE | retain Capability authority |
| `RuntimeAdmissionAssessmentCandidateV1` | executable eligibility assessment | REUSE | carry binding/constraint refs |
| `ExecutableCapabilityCandidateV1` | admitted executable candidate | REUSE | does not imply invocation |
| `ModelAssetContractV1` / model repository | model identity/declaration | REUSE | extend by binding ref, not duplicate model type |
| loader/model/provider mapping assets | compatibility declarations | EXTEND / ADAPTER | add single binding lifecycle metadata |
| Provider Admission contracts | provider admission/invocation | REUSE | consume provider binding |
| Observation Request contracts | acquisition request | REUSE | add source-version/trace linkage where needed |
| Evidence Candidate / Gateway contracts | normalization/admission | REUSE / EXTEND | attach source-state handoff refs |
| Field Event contracts | operational event candidate | REUSE | preserve Field admission |
| Current World candidate contracts | cognitive world representation | EXTEND | add handoff lineage/version refs |
| Outcome Candidate contracts | multi-source evaluation | EXTEND | add Brain adjudication input refs |
| Brain governance/adjudication records | final consequence | EXTEND | separate input/output records |
| Working Envelope version/invalidation | admitted binding set | EXTEND | reuse version/invalidation lineage |
| existing trace/provenance structures | reverse-linkable flow | REUSE | normalize edge observability semantics |

## Contract surface conclusion

No duplicate canonical ontology is required. The six closure targets are cross-boundary contract profiles over existing owner-specific types, not a universal runtime object.

