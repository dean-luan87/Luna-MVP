# Self / Social Self Engineering Migration Whitebox v1

## Required engineering questions

| Question | Required answer |
|---|---|
| What is the module? | Self, Social Self, Cognitive Core, Capability, Action, or Governance |
| Where is the asset? | Repository path recorded in impact inventory |
| What object does it manage? | Explicit state/object contract |
| Who owns it? | One canonical owner in the ownership registry |
| What can it write? | Explicit permission contract |
| Who consumes it? | Explicit interface contract |
| How does it migrate? | Mapping and risk plan before implementation |

## Current findings

- Existing architecture and capability assets are present and must be mapped,
  not rebuilt.
- `capabilities/emotion/` is treated as a boundary/skeleton candidate and does
  not justify an Emotion Runtime.
- Role and Relationship architecture assets become Social Self references.
- Self Model, Self Regulation, and Self Evolution remain Self Layer assets.
- Runtime assets require future context-contract review, not immediate changes.

## Safety rails

P0 risks (duplicate ownership, Emotion authority leakage, premature file move)
must be resolved before any implementation phase. This phase only registers the
risk and mitigation.
