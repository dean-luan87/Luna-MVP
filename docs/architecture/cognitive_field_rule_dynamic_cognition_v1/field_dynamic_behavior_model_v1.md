# Field Dynamic Behavior Model v1

## Observed dynamics

Dynamic Layer maintains candidates for:

- **Density**: sparse, normal, dense, or unknown;
- **Direction**: entering, leaving, crossing, stationary, or unknown;
- **Flow Pattern**: queue, gathering, dispersal, evacuation, circulation, or
  unknown;
- **Change**: opening, closing, obstruction, temporary control, or unknown.

These are group/environment patterns, not person identification, intention,
emotion, Role, or Social Relationship.

## Update path

```text
Evidence Frames
      ↓
Entity / Flow Assembly
      ↓
Dynamic Candidate
      ↓
Rule Candidate / Confidence
      ↓
Field Update Candidate
      ↓
Attention / Capability Requirement Candidate
```

Dynamic candidates preserve timestamps, provenance, uncertainty, and conflict.
They do not directly update Reality, Goal, Situation, Decision, or Action.

## Human flow constraints

Crowd following is a low-information risk-reduction strategy, not blind
imitation. When Unknown is high, Luna may seek an information source, observe
crowd flow, estimate a low-risk route candidate, and acquire more Evidence.
It must keep alternatives and Unknowns visible and must not execute a route.

No prediction, automatic planning, Action Runtime, Role, Emotion, Social
Relationship, B, or real model is implemented.

Motive is not inferred. Information Source Candidate remains a candidate. No
automatic planning, No Action Runtime, and No real model are included.

Motive remains unknown. No automatic planning is included.

The motive is unknown and is not inferred.
