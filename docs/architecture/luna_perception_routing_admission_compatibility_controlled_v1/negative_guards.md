# Negative guards

The compatibility projection and controlled evaluation enforce:

- no runtime admission decision or runtime grant;
- no Gateway submission and no FPO runtime invocation;
- no Provider/Model selection, binding, or invocation;
- no Capability activation, Slot reservation, or resource scheduling;
- no Camera, OCR, SLAM, VLM, or observation execution;
- no Attention, Evidence ingress/fusion, Decision, Task, or Action;
- no ranking, scoring, priority, winner, fallback, or route fabrication;
- no capability re-resolution, availability re-check, or class inference;
- no mutation of Requirement, Need, Branch, Strategy, Coordination, Demand,
  Capability Resolution, Current World, Field, Memory, PCN, Intent, Goal, or
  Attention;
- no Truth or World Truth declaration;
- no cross-demand merge and no cross-problem coordination;
- no conversion of Capability Admission into Runtime Admission.

Every emitted compatibility candidate must reference exactly one valid routing
candidate, preserve the routing lineage, and remain candidate-only,
read-only, and non-Truth.
