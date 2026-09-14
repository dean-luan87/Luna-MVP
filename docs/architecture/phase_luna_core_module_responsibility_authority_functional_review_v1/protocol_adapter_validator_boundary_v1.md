# Protocol Adapter and Validator Boundary v1

An Adapter translates explicitly supported contracts, preserves provenance and
version lineage, and owns translation errors. It does not become source owner,
protocol owner, or semantic authority.

Validators check conformance. Static validator output is evidence; runtime
validation is boundary-local admission evidence. Validators do not mutate
protocol or source state and do not replace Protocol Governance.
