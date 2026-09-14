# Cross-Binding Consistency v1

An executable chain is represented only when the Capability ↔ Model and Model
↔ Provider candidates refer to the same Model asset, model version and
weights version.

The consistency adapter rejects model ref mismatch, version mismatch, stale
upstream/downstream bindings and superseded bindings. It does not correct
either binding and does not create Runtime Admission.

