# Cognitive Attention Persistence Model v1

## Persistence profiles

```text
Attention Persistence
├── Persistent
├── Temporary
└── Interruptive
```

Persistent attention supports a continuing task such as navigation. Temporary
attention supports a one-off observation such as a door sign. Interruptive
attention supports a short high-priority anomaly such as a sudden sound.

Each profile has a start condition, maintenance candidate, decay signal,
release condition, resource cap, and restoration candidate. Persistence is not
permanent allocation and does not imply importance forever.

## Boundary

Persistence cannot directly request hardware frequency, call a Provider, make
a Decision, or execute an Action. When the resource budget is exhausted, the
request may be Decayed, Released, or Suspended and its Unknown remains visible.

Persistence cannot make a Decision and cannot execute an Action.
