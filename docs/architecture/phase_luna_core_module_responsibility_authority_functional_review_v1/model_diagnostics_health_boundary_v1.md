# Model Diagnostics and Health Boundary v1

Model Governance owns declared model state. Diagnostics owns observed asset
presence, path, checksum, dependency, loadability, and runtime-health evidence.

Registered model + missing asset means registration remains a model-governance
record, diagnostics reports unavailable, and Runtime Admission may block. A
health failure does not silently mutate or unregister the model.
