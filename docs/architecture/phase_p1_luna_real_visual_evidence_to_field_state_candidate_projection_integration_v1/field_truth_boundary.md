# Field Truth Boundary

The projection is an evaluation-level candidate projection, not a truth
promotion boundary.

- `provider=REAL_PROVIDER` identifies the source execution mode only.
- `class_label`, `bbox`, confidence, frame dimensions, and region references
  remain visual detection candidates.
- `DETECTION_REGION_CANDIDATE` is an image/runtime region and is not a physical
  Field region.
- `truth_declared=false`, `fact_admitted=false`, and `field_mutation=false`
  remain required at the projection and Reducer output surfaces.
- A missing detection does not imply `TARGET_ABSENT`, `OBJECT_ABSENT`, or Field
  absence. No-detection is an observation limitation unless a separate
  canonical closed-world contract exists.
- The existing Target binding boundary remains unchanged:
  semantic target resolution is not performed here.

