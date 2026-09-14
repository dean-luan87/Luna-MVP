# Cognitive Neural Signal Taxonomy v1

## Signal envelope rule

Every Neural Signal is candidate-shaped and carries at least a signal reference, type, source, destination, direction, context reference when applicable, priority/urgency when applicable, lifecycle status, provenance, and trace reference. The taxonomy describes categories; it does not implement a schema or authorize State mutation.

| Signal Type | Typical source | Typical destination | Purpose | Authority / lifecycle | May modify? |
|---|---|---|---|---|---|
| Attention Signal | Brain Attention Controller | Neural Layer → Middleware | Focus target, priority, duration, depth, direction | Candidate only; create/update/reduce/suspend/close | No; cannot call a capability or allocate State |
| Capability Signal | Brain through Cognitive Neural Path; Middleware feasibility response | Middleware / Brain | Information need, capability class, provider/bundle feasibility | Request/admission/bind/degrade/close candidate | No; cannot select goal or execute provider |
| Evidence Signal | Evidence Gateway after provider/hardware result | Neural Layer → Brain | Source-scoped observation/evidence | Return/update/expire/conflict candidate | No; cannot become truth or update Context directly |
| State Signal | Hardware, provider, Resource Manager, Diagnostics | Neural Layer → Self State / Brain / Middleware | Capability, reliability, battery, compute, storage, network, load condition | Health/change/degrade/recover candidate | No; cannot mutate Self State or Goal |
| Reflex Signal | Hardware local protection / safety observation | Middleware and Brain feedback path | Emergency protection, hardware safety, resource protection | Trigger/protect/report/resolve candidate | Only future device-local protection within embodiment boundary; never World Action |
| Adaptation Signal | Feedback / Experience / validation processes | Brain evolution boundary / Protocol Manager proposal input | Pattern adjustment, routing preference, signal payload evolution proposal | Candidate/validation/adoption; slow loop | No runtime protocol rewrite, no direct learning mutation |

## Classification constraints

- `Attention Signal` priority does not mean importance truth.
- `Capability Signal` availability does not mean execution.
- `Evidence Signal` confidence does not mean fact.
- `State Signal` reliability does not mean Cognitive Evaluation result.
- `Reflex Signal` urgency does not mean action authority.
- `Adaptation Signal` frequency does not mean adoption value.

## Signal lifecycle vocabulary

| Phase | Meaning |
|---|---|
| Create | A source emits a candidate signal. |
| Transport | Neural Layer verifies classification, boundary, compatibility, and trace envelope. |
| Receive | Destination consumes signal as an input candidate. |
| Update | A new candidate supersedes or refines current relevance; no in-place truth mutation. |
| Reduce / Suspend | Relevance, feasibility, or safety constraint decreases use. |
| Close | Signal/session relevance ends; trace remains observable. |
| Evolution proposal | Compatibility/payload/routing preference improvement enters validation, not runtime rewrite. |

## Status

`COGNITIVE_NEURAL_SIGNAL_TAXONOMY_READY_WITH_NOTES`

`WAITING_FOR_USER_TERMINAL_VERIFICATION`
