# Controlled scenario matrix

The evaluation contains more than 75 controlled cases covering completed and non-completed invocation outcomes, model-null and explicit-model carry-through, every required lineage reference, malformed and mismatched Gateway inputs, replay/idempotency, authority/responsibility guards, no-effect guards, and the synthetic Scenario 12 paths.

Scenario 12 keeps two independent abstract paths:

- signage → controlled provider → opaque Runtime Observation → Gateway admission → opaque Evidence;
- human-flow → controlled provider → opaque Runtime Observation → Gateway admission → opaque Evidence.

The paths retain distinct observation, admission, and evidence identities. No semantic content is assigned to either path and no model is inferred.
