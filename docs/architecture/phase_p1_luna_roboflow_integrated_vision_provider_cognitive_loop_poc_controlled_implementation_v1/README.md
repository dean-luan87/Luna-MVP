# Roboflow Integrated Vision Provider Cognitive-Loop PoC

## Status

`CONTROLLED_IMPLEMENTATION` / `CANDIDATE_ONLY` / `NO_AGENT_EXECUTION`.

The implementation provides separate structural and explicit real-provider
paths. The structural path uses synthetic provider-shaped payloads and must
never be reported as a real Roboflow response. The real path requires an
explicit `--mode real`, user-provided governed input, local image reference,
endpoint and API key.

## Chain

`image ref → governed Provider request → Roboflow Result → Detection/OCR
Evidence → Current World candidate → A-owned evidence-coverage
Hypothesis/Sufficiency → Next Observation candidate or Decision Governance
handoff`.

Task creation, Action admission/execution, Memory, Learning and Brain final
adjudication are outside this PoC.

## Authority boundary

Roboflow is Provider execution only. The Provider client and Evidence
translator do not perform semantic interpretation, hypothesis generation,
sufficiency ownership, re-observation selection, Decision generation, Field
mutation or Current World authoritative writes. The downstream cognitive
adapter may form only A-owned evidence-coverage candidates when real mode
does not receive a user assessment; it never answers the exit question.
