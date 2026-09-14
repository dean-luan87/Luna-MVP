# Field Event Validation Matrix v1

| Area | Required future evidence | Blocker |
| --- | --- | --- |
| Schema | Required identity/type/source/before/after/change/time/trace fields | Missing or authority-bearing field |
| Input lineage | Field View/Primitive/Concept/Context/Temporal references retained | Raw external input or broken provenance |
| Candidate lifecycle | Candidate-only/not-fact/not-state | Fact/admitted/reduced status asserted |
| Temporal | Explicit time/unknown/conflict/stale scope | Temporal rewrite or invented chronology |
| Admission boundary | Event does not enter Reducer directly | Bypass of Admission/Temporal Validity |
| Reducer boundary | No State/History mutation operation | Event/Kernel/attention writes State |
| Confidence/attention | Metadata only | Admission or trigger authority |

Planning Only: no Event Runtime, Admission/Reducer integration, runner, verifier, or State modification is created.
