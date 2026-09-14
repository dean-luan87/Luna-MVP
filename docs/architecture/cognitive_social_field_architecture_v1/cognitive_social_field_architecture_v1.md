# Cognitive Social Field Architecture v1

## Position

Social Field is the social operating environment within a Cognitive Field. It
is formed by Participants, Role Context, Relationship Context, Social Rules,
Interaction Patterns, and Social Position. It is not a Contacts List, Social
Network, Face Recognition Runtime, or Relationship Database.

```text
Cognitive Field
├── Physical Field
│   Reality / Entity / Spatial / Rule / Dynamic / Behavior
└── Social Field
    Participants / Role / Relationship / Social Rule / Interaction Pattern
```

Social Field describes a context; it does not make a Social Decision, judge a
Relationship, infer Emotion, confirm Human Identity, or execute Action.

## Participants

A Participant is an observed social presence with Identity Candidate,
Observation Evidence, Confidence, Field Presence, and Interaction History. An
Identity Candidate is not a confirmed identity. Automatic identity
confirmation, Face Recognition Runtime, and permanent individual tracking are
out of scope.

## Role Context

Role belongs to Field, not Identity. The same Self may be Employee in an Office
Field, Family Member in a Home Field, and Resident in a Community Field. Role
Context contains Field Context, Permission Boundary, Responsibility, Expected
Behavior, and Confidence. A Role cannot modify Self Identity.

## Relationship Context

Relationship is a contextual, temporal candidate between Participant A and
Participant B. It includes Context, History, Confidence, and Boundary. A
Colleague candidate may be valid in a Work Field while a Friend candidate is
scoped to a Private Field. Relationship Context cannot directly infer Emotion,
make a Decision, or become a permanent identity label.

## Social Rule Layer

Social Rules are candidates supported by Evidence, Confidence, and Unknown:
Norm Rule, Authority Rule, Interaction Rule, Cultural Rule, and Temporary Rule.
“People are queued” is Evidence; “a queue norm may apply” is a Social Rule
Candidate. Social Rules do not overwrite Reality or become unconditional law.

## Interaction Patterns

Interaction Pattern Candidate records observed historical patterns such as who
usually hosts a meeting or which step receives a report. It is not Prediction
and cannot predict a person's behavior. It may support Attention Candidate,
Behavior Candidate, or Memory Candidate after validation.

## Self and interfaces

Social Field + Self produces Role Context, Social Position Candidate, Attention
Candidate, and Behavior Candidate while preserving Identity Continuity. Social
Field may provide Social Field Memory Candidate. Memory does not override
Reality. An Emotion State Candidate is a placeholder only:

```text
Social Field + Role + Relationship + Memory → Emotion State Candidate
```

No Emotion Runtime is implemented.

## Explicit non-goals

No Personality Switching, Social Decision, Relationship Judgment, Human
Identity Confirmation, Face Recognition Runtime, Multi-Agent, Hive, B Route,
Prediction, Action Runtime, or Social Runtime is implemented.

Social Network is out of scope. Automatic identity confirmation is forbidden.
Expected Behavior is contextual. Social Rule Candidate is not absolute Reality.
No Social Decision. No Relationship Judgment. No Human Identity Confirmation.
No Face Recognition Runtime. No Multi-Agent. No Hive. No B Route. No Prediction.
No Action Runtime. No Social Runtime.
