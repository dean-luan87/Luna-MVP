# Cognitive Contract Alignment Review v1

## Candidate alignment

`cognitive/contracts/candidate.py` matches Candidate First at the object level:

- immutable object and nested payload/provenance values;
- required identifier, type, origin, and context reference;
- evidence, confidence, constraints, uncertainty, validation state, provenance, and trace fields;
- documentation explicitly excludes fact, command, decision, permission, action, memory write, and State mutation.

### Alignment gap

The generic payload currently permits an arbitrary caller to describe authority-like metadata. A future contract-admission validator should reject or quarantine prohibited authority fields and reserved candidate types without making Candidate itself a decision engine.

## Signal alignment

`CognitiveSignal` provides source, target, timestamp, context reference, candidate type, payload, confidence, provenance, and trace. This supports decoupled candidate communication.

### Alignment gap

The current contract does not yet define first-class signal envelopes for Evidence, Context, Goal, Attention, Feedback, and Interrupt. Future extension should be additive and versioned.

## Snapshot alignment

`CognitiveSnapshot` is an immutable current-cycle view rather than Field State or Reducer State. It has situation, context, goal, attention, unknowns, and active candidates.

### Alignment gap

Evidence, feedback, interrupt, resource, and self-state references are currently represented only through `active_candidates`, not typed snapshot fields. This is sufficient for synthetic validation, not yet a complete runtime view.

## Tick alignment

`CognitiveTick` is a declared request, not a scheduler/executor/state transition. It currently supports field change, goal change, risk change, and information-gap triggers.

### Alignment gap

Future additive trigger types are needed for new evidence, context change, self-state change, and attention expiration candidates.

