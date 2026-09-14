# Protocol Fingerprint and Lifecycle v1

Distinguish declared protocol fingerprint, observed artifact fingerprint,
comparison result, and drift finding. No fingerprint is calculated in this
phase.

Conceptual lifecycle:

`Draft → Review → Approved → Active → Frozen → Deprecated → Retired`

Deprecated may remain valid for existing compatible bindings during an explicit
compatibility window. Superseded versions retain lineage; Retired versions are
history/replay references only unless explicit policy permits historical use.
