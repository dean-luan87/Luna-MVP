# Field Kernel Skeleton Contract v1

Required fields are Field View identity, a base `field_state_reference`, candidate overlay, Context/Temporal/Spatial/Task/Attention references, uncertainty, provenance, and trace. The view fixes `candidate_only=true`, `field_state_source=false`, `state_mutation=false`, `not_state=true`, and `not_fact=true`.

Raw model/provider input, Memory, Fact, Decision, Action, and Reducer commands are rejected. Overlay cannot become State, Snapshot, or History.
