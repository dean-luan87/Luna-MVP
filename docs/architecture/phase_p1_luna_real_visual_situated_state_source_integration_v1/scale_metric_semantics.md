# Scale Metric Semantics

The source projection emits only geometry-derived candidate metrics:

- `width_ratio = (x2 - x1) / frame_width`
- `height_ratio = (y2 - y1) / frame_height`
- `area_ratio = ((x2 - x1) * (y2 - y1)) / (frame_width * frame_height)`

Static audit found no canonical minimum target-scale threshold for this
condition. The Runner therefore does not invent one and sets
`target_scale_condition_status = UNKNOWN`. The existing Situated State
Perception engine consequently produces an `UNKNOWN` scale condition, which
the existing feasibility evaluator treats as insufficient for a required
condition.
