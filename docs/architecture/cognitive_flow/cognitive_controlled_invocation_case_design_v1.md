# Controlled Invocation Case Design v1

## Purpose

These cases define future controlled-invocation validation targets before any model is connected. Each validates the architecture chain, not model accuracy or autonomous cognition.

| Case | Scenario | Primary validation | Required trace |
|---|---|---|---|
| Case 1 — Static scene understanding | Airport-exit image scenario. | Brain Intent → CWO → Provider evidence boundary. | Intent, CWO, requirement, Provider candidate, Evidence, feedback. |
| Case 2 — Visual region focus | Find a specified target/sign region in an image. | Attention/CWO requirement → visual capability organization. | Attention requirement, region evidence scope, coverage/unknown result. |
| Case 3 — Multi-provider complementarity | Text/region evidence requires segmentation-family plus OCR-family candidate. | Middleware capability composition and conflict/partial-coverage reporting. | Composition rationale, each Evidence Candidate, alignment/conflict, fallback. |

## Shared acceptance constraints

- Input is a controlled fixture, not live camera data.
- Provider invocation is deferred until a separately approved implementation phase.
- Brain/Neural cannot name/call a provider directly.
- Provider output must enter Evidence Gateway with uncertainty/provenance.
- Middleware Report cannot state cognitive completion.
- Neural Alignment emits only continue/refine/attention-adjustment/close candidates.
- No Decision, Action, Memory mutation, Reality mutation, or B-route behavior.

## Case 1 example

```text
Brain Intent: establish whether an exit-sign region may be present.
CWO: require visual text, target-region, and current spatial relationship coverage.
Middleware: form visual capability/provider candidates under constraints.
Expected output: trace-linked Evidence Candidates and explicit unknowns—not “exit confirmed”.
```
