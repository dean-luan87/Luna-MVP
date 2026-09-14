# Diagnostics Cross-Source Conflict v1

Conflicting sources are preserved as a conflict finding with each source,
version, observed time, and provenance. Examples include filesystem/model
registry mismatch, Provider available versus device unavailable, or dependency
verified versus runtime import failure.

Diagnostics must not silently choose a universal Truth or rewrite a source. A
consumer may conservatively block or request governance review; Diagnostics
only reports the conflict and uncertainty.
