# A3 Evidence Context Translation Layer Mapping Matrix v1

| External Evidence candidate | Translation primitive candidate | preserved boundary |
| --- | --- | --- |
| OCR `text_candidate` | `semantic_candidate` | text remains a candidate with OCR source/provenance; it is not a Fact or final semantic meaning |
| Vision `object_candidate` | `entity_candidate` | object remains a candidate; provider identity is provenance, not the Entity |
| SLAM `location_reference` | `spatial_candidate` | location reference remains candidate spatial input; no Field/State update |
| Audio `speech_candidate` | `semantic_candidate` or `entity_candidate` only when separately governed | speaker/audio signal remains candidate-only; no identity Fact or action |
| Temporal source reference | `temporal_candidate` | temporal signal retains uncertainty and trace; no lifecycle or State transition |

No mapping produces a Fact, Decision, Action, State, Memory update, Learning Candidate admission, or Runtime authority.
