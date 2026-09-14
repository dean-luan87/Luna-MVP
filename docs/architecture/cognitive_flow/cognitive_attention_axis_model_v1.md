# Cognitive Attention Axis Model v1

## Axis structure

```text
Attention Axis Candidate
├── Direction
├── Region
├── Entity
├── Attribute
├── Relationship
└── trace_ref
```

| Axis | Observation question | Example |
|---|---|---|
| Direction | what orientation or context should be understood? | forward safety context |
| Region | what possible area warrants evidence? | road intersection |
| Entity | what possible entity matters? | vehicle or pedestrian |
| Attribute | what property is relevant? | speed, distance, opening status |
| Relationship | what relation should be understood? | vehicle approaching pedestrian |

Attention Axis Candidate scopes information need; it does not assert that an entity exists, control a camera/body, choose a model, or determine what the evidence means.
