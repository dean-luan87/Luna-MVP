# Multi-loop coexistence, priority, and preemption

## Coexistence

Each loop has an independent identity, state-version chain, current minimum
Need, sufficiency status, pending candidates, lifecycle state, and provenance
namespace. Loops may share read-only Context, Field, Current World, capability,
priority, and resource references. Shared references do not merge loop state.

No complex arbitration algorithm is introduced. A `priority_ref` and an
`arbitration_ref` are evidence of governance input, not a local winner
selection algorithm. Any later arbitration owner must preserve loop-local
state and scope decisions to the selected loop.

Global governance remains with Brain capabilities and existing owners:
Attention, Safety, Resource, Intent, Task, Field / Current World, and
Capability Governance. A Loop may carry their references but cannot become a
global scheduler or arbitration authority.

## Safety preemption

The planned sequence is:

```text
Normal Loop ACTIVE
  -> Safety-relevant Loop priority candidate
  -> Normal Loop PAUSED candidate
  -> Safety Loop ACTIVE candidate
  -> safety disposition complete
  -> Normal Loop Resume Assessment
```

Safety priority can change urgency and pause a normal loop. It cannot:

- bypass Capability Scope or Resolution
- promote candidate evidence to Truth
- bypass Action or Permission governance
- automatically resume a stale Requirement
- terminate unrelated loops by implication

The Safety / Survival owner remains authoritative for safety disposition. The
Cognitive Flow owner records references and candidate transitions only.

## Resource pressure

Resource pressure may pause or defer an optional loop, or leave a loop waiting
for recovery. Inactive Loops preserve minimum resumable state and references;
they do not imply full runtime resource retention. Resource release or
reallocation remains owned by Resource Governance and must be visible in the
next Resume Assessment. Pressure does not delete candidates, mutate Intent,
release all capability history, or mark the loop's Task as failed. Shared
resource refs are preserved on every loop snapshot; allocation and utility
scoring are deferred.

## Brain non-duplication rule

When Brain materializes a local concern as a Loop, the same local concern must
not also remain as an independently progressing Brain path. Brain may observe,
govern, pause, preempt, reassess, and assimilate the Loop outcome, but it does
not run a duplicate local solution.
