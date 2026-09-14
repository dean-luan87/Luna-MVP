# Action Feasibility Interface v1

## Purpose

This future-facing cognitive interface lets Brain-side reasoning ask whether a
goal is compatible with the represented situation and Self Capability
boundaries without entering an action system.

```text
Goal + Situation Candidate + Self Capability Context
                         ↓
              Feasibility Candidate
```

| Field | Meaning |
|---|---|
| `feasibility_class` | `Possible`, `Possible With Adaptation`, `Currently Impossible`, or `Unknown` |
| `supporting_constraints` | relevant world, capability, and resource constraints |
| `unknowns` | missing information that prevents stronger assessment |
| `adaptation_need_candidate` | non-executing indication that conditions/capabilities may need change |
| `trace_ref` | traceability to inputs and representations |

It does not execute, choose, plan, or generate an Action. It does not invoke a
Provider, bypass Brain authority, or mutate State.
