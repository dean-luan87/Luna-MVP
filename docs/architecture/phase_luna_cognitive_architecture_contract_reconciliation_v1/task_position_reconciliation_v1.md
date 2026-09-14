# Task Position Reconciliation

## Target position

Task is:

- a goal and behavior constraint input;
- an execution organization structure after Decision where appropriate;
- a source of completion conditions and behavioral constraints.

Task is not:

- the cognitive subject;
- the Loop owner;
- the reasoning owner;
- a Brain-wide cognitive operating system;
- an independent controller of Loop cognition.

## Current assets\n\nThe Task Manager currently owns lifecycle, readiness, dependency waiting,\npause/resume, cancel/terminate, completion and failure recovery. B3 maps\nDecision candidates into Task candidates. B4 preserves Task Manager as the sole\nTask lifecycle owner.\n+\n+The Task Manager capability router can produce capability request candidates\n+from task capability requirements. This is a candidate route, not Provider\n+execution and not proof that Task owns Capability resolution.\n+\n+## Required boundary\n+\n+Task enters A/B through the Semantic Working Outline and Context working\n+environment. Task may contribute:\n+\n+- target;\n+- behavior constraints;\n+- completion conditions;\n+- resource and permission references;\n+- observation dependency references.\n+\n+No canonical direct Task → Loop cognition-control path should remain. A/B may\n+read Task refs and may submit candidate Task feedback through Task Manager, but\n+Task does not issue reasoning commands to Loop.\n+\n+## Current conflicting appearance\n+\n+The A Route Product Loop stages Task after Decision and before Action. The Loop\n+identity also stores task/behavior refs. These are handoff/reference surfaces,\n+not Task ownership of cognitive direction. The distinction must remain explicit\n+during migration.\n*** Add File: /Users/luanlei/Desktop/Luna-Core/docs/architecture/phase_luna_cognitive_architecture_contract_reconciliation_v1/experience_short_path_filter_boundary_v1.md
# Experience / Short-Path Filter Boundary

## Status\n+
This is a contract boundary only. No filter runtime, retrieval, mutation or
semantic compression is implemented in this phase.

## Target boundary

Semantic Working Outline
→ Experience collision / retrieval
→ information match, confidence and validity evaluation
→ DIRECT_RESOLUTION
  or SHORT_CAPABILITY_RESOLUTION
  or A_REASONING_REQUIRED

## Reuse candidates\n\nExisting composable assets include:\n\n- ExperienceCandidateV1;\n- MemoryCandidateV1;\n- Cognitive Memory & Experience Governance;\n- Attention relevance and uncertainty candidates;\n- Current World and evidence refs;\n- Capability Requirement, Scope, Resolution and Invocation candidates;\n- Observation Gateway admission boundaries.\n+\n+No new Filter owner should be introduced if these existing governance owners\n+can compose the function.\n+\n+## Authority rules\n+\n+- Experience result is not automatically truth.\n+- Historical Experience cannot override Current Reality.\n+- A short Capability result may expose a remaining cognitive gap and enter A.\n+- The filter does not decide general cognitive sufficiency.\n+- The filter does not choose Provider identity outside Capability Governance.\n+- The filter does not control Loop lifecycle.\n+- The filter does not mutate Memory or Experience.\n+- The filter is not another Brain or reasoning owner.\n+\n+## Resolution outcomes\n+\n+DIRECT_RESOLUTION returns a bounded candidate to Brain without Loop\n+materialization. SHORT_CAPABILITY_RESOLUTION forms only a bounded Requirement\n+through existing Capability Governance. A_REASONING_REQUIRED transfers the\n+remaining concern to A, optionally with a Loop materialization request.\n*** Add File: /Users/luanlei/Desktop/Luna-Core/docs/architecture/phase_luna_cognitive_architecture_contract_reconciliation_v1/cognitive_architecture_overlap_inventory_v1.md
# Cognitive Architecture Overlap Inventory

| Overlap | Current evidence | Classification | Reconciliation direction |
|---|---|---|---|
| Brain vs A Route | Brain goal/final authority docs; A Route canonical caller planning | semantic authority duplication risk | Brain owns concern; A owns active reasoning |
| A Route vs Cognitive Flow | A Route stages Cognitive State/Flow; Flow owns Dynamic transitions | orchestration overlap | A consumes Flow mechanics; no dual owner |
| A Route vs Loop transitions | A Route lifecycle states and Loop lifecycle/next-step candidates | lifecycle duplication | A reasons; shared Loop Engine stores mechanics |
| Dynamic Flow vs Loop Engine | Dynamic Flow selects Need/sufficiency/reconsideration; Loop stores same refs | semantic authority overlap | Move judgment to A/B; retain state storage |
| A/B environment construction | A Route includes Context/Field/Observation stages | orchestration overlap | Context/Field/Observation remain external owners |
| Brain direct Loop governance | Loop materialization candidate references Brain | intentional governance reference, no concrete API | Keep candidate boundary; define API later |
| Task / Intent / Role / Field refs | A/B/Loop envelopes carry shared refs | intentional shared reference | Preserve read-only refs, no copies |
| Hypothesis ownership | Hypothesis Governance plus Flow/Loop lineage | semantic authority overlap | A/B judges; Hypothesis owner governs representation |
| Sufficiency ownership | Dynamic Flow and Loop local sufficiency | semantic authority duplication risk | A local judgment; Brain global adjudication |
| Need / Observation Need | Dynamic Flow Need and B4/FPO observation need | semantic overlap | Separate cognitive gap from observation admission |
| Capability path | Dynamic Flow path and Task capability router | orchestration overlap | Capability Governance owns resolution |
| Experience / Memory | Loop package refs and Experience/Memory candidates | intentional boundary reference | No mutation; future filter composes existing owners |
| B Route naming | future simulation and perception Route B | unnecessary parallel naming | Fix namespace before B implementation |

## Findings

No confirmed external authoritative state duplication was found in Loop. The
main issue is authority declared by candidate behavior, not mutable data
duplication. Existing negative guards should remain.

## Non-goals

This inventory does not authorize code deletion, type changes, enum changes or
owner replacement. It only identifies later reconciliation boundaries.
