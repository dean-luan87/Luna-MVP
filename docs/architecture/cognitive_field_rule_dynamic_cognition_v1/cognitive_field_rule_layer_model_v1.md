# Cognitive Field Rule Layer Model v1

## Purpose

This phase extends Cognitive Field from a spatial/state container into a
candidate rule-and-dynamic environment model. It describes how a place appears
to operate; it does not decide what Luna should do.

```text
Cognitive Field
├── Physical Layer
├── Entity Layer
├── Spatial Layer
├── Rule Layer
└── Dynamic Layer
```

## Rule layers

- **Physical Rule**: observed physical constraints such as walls, doors,
  obstacles, surfaces, and access geometry.
- **Functional Rule**: candidate use patterns such as a meeting room for
  discussion, a hospital for medical service, or a station for transit.
- **Social Rule**: observed group-conduct convention candidates such as queuing,
  distance, quiet, or flow etiquette. This is not Social Relationship or Role.
- **Legal Rule**: reported or observed restriction candidates such as a
  prohibited area or safety boundary; it is not legal advice.
- **Temporary Rule**: time-bounded construction, event, closure, or crowd
  control candidate.

Rules are not Facts. A Rule Candidate includes Evidence references, confidence,
provenance, validity, scope, and Unknowns. Reality (“people are queued”) is
kept separate from Rule (“a queue norm may apply”).

## Dynamic layer

Dynamic cognition describes observed human flow and environmental change:
Density, Direction, Flow Pattern, entry, exit, queue, gathering, and
evacuation candidates. It does not identify a person's motive, create a Goal,
predict the future, or produce an Action.

## Attention and Capability interfaces

Rules may produce Attention Bias Candidate for relevant exits, signs, flow, and
boundaries. They may produce Capability Requirement Candidate such as OCR,
spatial evidence, or human-flow evidence. Field + Task + Unknown + Attention
determine the requirement; a Model never decides which capability Luna needs.

## Prohibitions

No Role, Emotion, Social Relationship, B Route, Prediction, automatic planning,
Action Runtime, real model, OCR Runtime, SLAM Runtime, Camera, Hardware, or
automatic execution is implemented. Field Rule is a candidate environment
description, not Decision, Value, Goal, or Action authority.

No Emotion, No Social Relationship, No B Route, No Prediction, No automatic
planning, No Action Runtime, No OCR Runtime, No SLAM Runtime, No Camera, and
No Hardware are implemented.

No automatic planning is implemented.
