# Implementation summary

The package loads the planning manifest and referenced JSON artifacts,
validates consistency, classifies declared impact and compatibility, and
provides 20 deterministic governance cases. It never imports phase runners or
executes business/runtime behavior.

The loader preserves source metadata names and normalizes phase boundary
summaries to `candidate_truth_boundary` and `mutation_boundary`. It also
normalizes the planning trace field `required_ref_classes` to the public
`required_reference_classes` view while retaining all six classes.
