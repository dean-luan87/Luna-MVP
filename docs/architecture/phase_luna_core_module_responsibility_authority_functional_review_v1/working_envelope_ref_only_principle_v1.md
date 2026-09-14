# Working Envelope Ref-Only Principle v1

The preferred representation is:

`source_ref + source_version + applicability + scope + constraint + provenance`

rather than mutable duplicated source payload. Existing copied values are
classified as follows:

- binding metadata and derived validity markers: REQUIRED_DERIVED_SUMMARY;
- compatibility copies in controlled bridge fixtures: COMPATIBILITY_COPY;
- copied Field/Context/World/Role/Intent/Task payloads: DUPLICATION_RISK;
- source refs, versions, and provenance: REFERENCE_ONLY_TARGET.

No code migration is performed here. The existing bridge's
`authoritative_state_duplicated=False` and `source_owner_preserved=True` flags
are evidence of the target boundary.
