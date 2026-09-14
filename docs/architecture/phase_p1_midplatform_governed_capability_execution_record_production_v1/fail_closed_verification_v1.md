# Fail-Closed Verification

The controlled Runner reports:

- `status = BLOCKED_BY_MISSING_CANONICAL_DECLARATION`;
- `record_bundle_produced = false`;
- explicit missing declaration names;
- `no_success_synthesized = true`;
- model loading, Provider invocation, Observation execution, Action
  execution, source mutation, and World Truth declaration all false.

The Verifier checks repository source references and confirms that the
YOLO11n Model Contract candidate is not treated as a canonical registry
entry, that the Provider Registry gap is detected, and that no synthetic
bundle is accepted.

The Verifier's fail-closed checks may pass while production availability
remains blocked.  This is safety verification, not a GO declaration.

