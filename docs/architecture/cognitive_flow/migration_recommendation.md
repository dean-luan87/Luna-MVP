# Cognitive Architecture Migration Recommendation v1

## Status vocabulary

| Status | Meaning in this review |
|---|---|
| `KEEP` | Retain the asset in its current responsibility boundary. |
| `MIGRATE` | Retain the asset but introduce an approved adapter, contract mapping, or ownership shift before A-route use. |
| `REPLACE` | Replace the asset's **role in the A-route path**; this is not deletion. |
| `DEPRECATE` | Do not use the asset directly in the A-route path; retain legacy use only until an approved retirement plan exists. |

## Recommended disposition

| Asset group | Status | Recommendation |
|---|---|---|
| Root `cognitive/` Candidate, Signal, Snapshot, Reducer boundary | `KEEP` | Treat as the A-route controlled-skeleton foundation. Preserve immutability and Candidate-only rules. |
| Root cognitive Kernel / Attention / Organization / Process / Runtime Instance skeletons | `KEEP` | Continue only through controlled skeleton validation; do not upgrade implicitly into scheduler, decision engine, or executor. |
| `cognitive/validation/` traces, replay, and stress assets | `KEEP` | Use as regression assets when later adapters are proposed. |
| Model Test Lens UI and diagnostics | `MIGRATE` | Develop into a read-only Cognitive Whitebox consuming trace/evidence/allocation data. Keep local runner bridge test-only. |
| Model Manager and capability registries | `MIGRATE` | Keep provider inventory and policy metadata; expose them to capability composition as candidates, not cognitive authority. |
| Task Manager | `MIGRATE` | Constrain it to external task/workflow management. New cognitive processes are described by Process Composer and governed by Kernel/Attention. |
| OCR, detection, segmentation, VLM, SLAM, ASR adapters | `MIGRATE` | Wrap each output as `EvidenceCandidate`, including source, time, scope, uncertainty, confidence, and trace. Start with one controlled adapter per approved phase. |
| Legacy evidence packs | `MIGRATE` | Map to one Evidence Field contract and eliminate parallel truth/evidence semantics before live use. |
| Legacy candidate-style field/context/simulation modules | `MIGRATE` | Reuse only after one-to-one contract mapping. Prevent duplicate Context, Simulation, or Attention runtimes. |
| Model Router as cognitive selector | `REPLACE` | Attention Governance + Kernel decide whether a capability should be considered; Model Router only resolves providers for an admitted capability need. |
| Fixed `runtime/main_loop.py` direct decision/execution path | `REPLACE` | Do not use as the A-route runtime. A future runtime must be event-driven, candidate-first, and separated from decision/execution. |
| Legacy direct Decision role | `REPLACE` | In A-route, retain Evaluation and Decision Support Candidate only; external human/permission authority remains beyond the boundary. |
| Direct Action / execution-intent use from cognition | `DEPRECATE` | Prohibit A-route direct use. Preserve external action/governance assets only as future permission-controlled executor integrations. |

## Ordered migration candidates (not approved implementation work)

1. Establish an adapter mapping review for one perception source, beginning with its output contract—not model invocation.
2. Define Evidence Field admission and conflict semantics against `cognitive.evidence.EvidenceCandidate`.
3. Connect Model Test Lens in read-only mode to existing cognitive traces.
4. Align Model Manager/Capability Registry as capability metadata inputs to a future Capability Composition candidate.
5. Maintain isolation from `runtime/main_loop.py` and all direct execution paths.
6. Only after a separate approved phase: introduce a single controlled real-input adapter with V0/V1 evidence and trace regression.

## Risks requiring human confirmation

- The repository has two architectural generations: legacy operational routing/decision paths and the new controlled A-route skeleton. A formal ownership boundary is required before integration.
- `capabilities/cognitive_flow/` contains concepts overlapping the root `cognitive/` foundation. Reuse without contract mapping risks two competing cognitive authorities.
- Existing Model Test Lens is valuable, but its model/runner controls must remain observability and test tooling rather than attention or decision authority.
- Real camera/OCR/VLM/SLAM/ASR wiring must be approved as a new execution phase; this review performed none.

## Final reassessment

| Domain | CURRENT_ARCHITECTURE_STATUS |
|---|---|
| Controlled Cognitive Foundation skeleton | `KEEP` |
| Legacy capability and evidence estate | `MIGRATE` |
| Legacy direct cognitive-selection / decision role | `REPLACE` |
| Direct action use in A-route cognition | `DEPRECATE` |

**Overall status: `MIGRATE` — architecture alignment is adequate for a separately authorized controlled adapter or skeleton phase, but no live integration is approved by this review.**

`WAITING_FOR_USER_TERMINAL_VERIFICATION`
