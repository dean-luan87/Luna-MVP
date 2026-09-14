# Condition Derivation Semantics

The existing `situated_state_perception_engine_v1.derive()` remains the
condition owner. The new source projection supplies candidate-valued inputs;
it does not directly populate `satisfied_condition_refs`.

| Condition | Real visual basis | v1 status rule |
|---|---|---|
| `condition:target-visible:v1` | At least one native detection candidate | `VISIBLE` may yield `SATISFIED`; no detection yields `UNKNOWN`, not proof of absence |
| `condition:target-complete:v1` | Native bbox and frame width/height | A valid bbox fully inside frame bounds yields a frame-completeness candidate |
| `condition:target-scale-adequate:v1` | bbox/frame width, height and area ratios | Ratios are emitted; no canonical threshold was found, so status is `UNKNOWN` |
| `condition:stable-relation:v1` | No legal single-frame temporal source | Always `UNKNOWN` in this phase |

The canonical minimum requirement for
`information:primary-transit-sign-text:v1` requires all four condition
references. Therefore the current real visual projection is expected to fail
closed at feasibility while scale and stability remain unknown. This is
intentional and does not trigger OCR.
