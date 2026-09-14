# Attention Requirement Model v1

## Role

Attention Requirement translates an abstract Attention Intent into an
evidence-oriented observation need. It describes what information is required,
not what model should detect or execute.

```text
Attention Requirement Candidate
├── Target Domain
├── Observation Scope
├── Region Candidate
├── Object Candidate
├── Information Need
├── Evidence Type
├── Unknown Requirement
└── trace_ref
```

| Field | Question answered |
|---|---|
| Target Domain | which reality domain may contain relevant information? |
| Observation Scope | what bounded context is relevant? |
| Region Candidate | what possible region merits evidence? |
| Object Candidate | what possible entity class/relation may matter? |
| Information Need | what must be understood rather than merely detected? |
| Evidence Type | visual, audio, spatial, environment, or another governed evidence type |
| Unknown Requirement | which ambiguity should remain visible or be reduced? |

## Boundary

Attention Requirement Candidate is not a detection specification, model name,
Provider selection, Capability Session, Truth claim, Decision, Action, or
automatic frequency adjustment.

