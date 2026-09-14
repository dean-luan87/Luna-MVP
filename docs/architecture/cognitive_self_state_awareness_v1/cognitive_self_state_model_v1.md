# Cognitive Self State Model v1

## Purpose

Self State Awareness represents Luna's current condition without redefining
who Luna is or what Luna can permanently do. It complements Self Capability
Awareness:

```text
Self Identity       = who Luna is
Self Capability     = what Luna can do / its capability boundary
Self State          = how Luna is currently doing
```

Self State is dynamic and time-bounded. Self State is not Self Identity, not
Personality, not Personality, not Emotion, not a Goal, not a Decision, and not Reality. A low
battery state does not mean that Luna is a weaker subject; it is a current
Resource State constraint.

## State domains

```text
Self State
├── Physical State
│   ├── battery
│   ├── temperature
│   ├── sensor health
│   ├── storage
│   └── network
├── Cognitive State
│   ├── current load
│   ├── active Field count
│   ├── Attention consumption
│   └── Unknown accumulation
├── Capability State
│   └── Self Capability Awareness reference
└── Resource State
    ├── compute
    ├── memory
    └── time
```

Each domain supplies evidence for a Self State Update Candidate. `Available`,
`Degraded`, `Limited`, `Unavailable`, and `Unknown` retain the Capability
State vocabulary but do not replace Self State domains.

## Feedback boundary

```text
Runtime / Diagnostics
        ↓
Self State Update Candidate
        ↓
Reducer validation
        ↓
Self Awareness Context
        ↓
Attention Adjustment Candidate
        ↓
Brain Awareness Candidate
```

Self State may constrain Attention, Field context, and confidence. It may
produce a Resource Protection Candidate, Alternative Observation Candidate, or
Brain Awareness Candidate. It cannot directly modify Reality, Goal, Decision,
Action, Self Identity, Capability Identity, Personality, or Emotion. The
Reducer remains the sole State mutation authority.

## Recovery and continuity

State recovery may restore Attention capacity or confidence when new evidence
supports recovery. A transient state must not become a permanent capability
rewrite. State history is an Experience reference only; it is not automatic
learning and it cannot replace current Runtime evidence.

No Emotion Runtime, No Role Runtime, No Social Runtime, No B Runtime, and No
Action Runtime are included in this architecture-only phase. No Action Runtime
is enabled.
