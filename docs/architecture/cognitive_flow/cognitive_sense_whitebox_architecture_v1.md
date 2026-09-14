# Sense Whitebox Architecture v1

## Purpose

Sense Whitebox makes software perception governance inspectable. It presents the chain from cognitive reason to evidence return rather than a flat list of model invocations.

```mermaid
flowchart LR
    goal[Goal] --> attention[Attention]
    attention --> request[Sense Capability Request]
    request --> composition[Capability Composition]
    composition --> provider[Provider Candidate]
    provider --> evidence[Evidence Candidate]
    evidence --> update[Cognitive Update]
```

## Required views

| View | Displays | Never displays as authority |
|---|---|---|
| Goal / Attention | information need, priority, depth, duration, suppression reason | final decision or model command |
| Sense Capability Request | domain, capability, evidence requirement, resource constraint | provider selection as cognitive answer |
| Capability Composition | provider roles, input requirements, fallback/degradation, resource limits | hidden result stitching |
| Provider Candidate | model/algorithm/service traits, lifecycle/admission/reliability state | automatic execution |
| Evidence | source/scope/time/confidence/uncertainty/conflict/composition trace | fact confirmation |
| Cognitive Update | Workspace/Context/Evaluation/Self State candidate references | State mutation/action |

## UI boundary

Future local Whitebox is read-only. It cannot invoke providers, change composition, edit attention, create goals, approve evidence, or mutate State. Existing Model Test Lens is a candidate trace-rendering base only after separate authorization.

## Status

`COGNITIVE_SENSE_WHITEBOX_ARCHITECTURE_READY_WITH_NOTES`

`WAITING_FOR_USER_TERMINAL_VERIFICATION`
