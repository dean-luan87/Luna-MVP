# Self / Field / Target / Relation Boundary

- Self is represented by the existing `SelfPerceptualViewpointStateV1`; it
  describes orientation, motion, stability, current view, visible regions,
  and sensor availability for Self.
- Field and Target remain referenced as candidate state/observation inputs.
- The existing `RelativeObservationStateV1` expresses the time-bounded
  Self↔Target↔Field relationship, including visibility, completeness, scale,
  motion, stability, orientation, and occlusion candidates.
- Situated State composes these references for one capability requirement.

Self does not own capability necessity, feasibility, eligibility, or action
decisions.  No second Self State or Field State owner was introduced.
