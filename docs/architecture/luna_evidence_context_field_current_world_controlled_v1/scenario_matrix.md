# Controlled scenario matrix

The evaluation contains 100 deterministic cases covering:

| Family | Coverage |
| --- | --- |
| Formation | valid, malformed, stale, insufficient, context mismatch |
| Admission | required, admitted, temporal expiry, duplicate replay |
| Reduction | single authority, deterministic replay, unknown, conflict, correction, overlay, expiry, refresh, reopen |
| Representation | Field State candidate, Current World candidate, read-only context and provenance |
| Governance | valid pairing, authority without responsibility, responsibility without authority, preflight hard-stop and postflight guards |
| Boundaries | no provider/model/runtime recall, no Memory/Experience/Decision/Task/Action, no truth/world mutation |
| Scenario 12 | independent abstract signage and human-flow paths, opaque payloads, no auto-merge, no exit truth |

Scenario 12 creates separate event/state candidates for its two abstract
provider paths. It does not infer OCR, VLM, camera, SLAM, YOLO, text, people,
exits, directions, or any other world semantic.
