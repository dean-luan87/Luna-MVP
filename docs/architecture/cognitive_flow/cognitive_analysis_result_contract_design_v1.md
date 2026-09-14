# A3 Cognitive Analysis Result Contract Design v1

## Position

`Analysis Result Candidate` is a structured A3 cognitive signal. It records a possible analysis output with references, uncertainty, provenance, confidence, and warnings. It is neither a Fact, a Field State change, a Decision Candidate, an Action instruction, nor a Memory update.

`runtime_authorized=false` is unchanged. This design does not implement Runtime or generate analysis.

## Required Contract Fields

| field | meaning | boundary |
| --- | --- | --- |
| `analysis_id` | stable candidate identity supplied by a governed producer | no automatic ID generation in this contract |
| `input_reference` | Context/Question reference that scoped the result | reference only; no Context or Snapshot writeback |
| `evidence_reference` | one or more supplied Evidence references | no evidence fetch, replacement, mutation, or Fact claim |
| `analysis_type` | one declared candidate analysis category | context interpretation, evidence relationship, hypothesis, uncertainty, or semantic explanation only |
| `candidate_output` | structured possible output | candidate meaning only; no asserted conclusion |
| `uncertainty` | explicit unresolved, coverage, conflict, or limitation information | must not be silently removed |
| `provenance` | source, trace, contract/version, and producer lineage | mandatory; no untraceable result |
| `confidence` | optional `[0,1]` candidate attribute | never Fact authority or admission authority |
| `warning` | stable warning/reason codes | limitation signal, not an authorization override |

## Explicit Authority Flags

Every result declares the following as `false`: Fact creation/mutation, Decision creation, Action execution, State mutation, Memory update, Runtime execution, model invocation, and inference execution. The contract is structural: it validates a declared candidate but performs none of these operations.

## Result Handoff

A future consumer may read a valid result only as a candidate cognitive signal under separate governance. It may not treat validation as Fact admission, Decision authority, Action permission, or permission to write Field State. Any future Decision Candidate handoff remains a separate domain contract.
