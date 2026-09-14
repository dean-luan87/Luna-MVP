# Intent / Semantic Module / Cognitive State Boundary v1

The Semantic Module represents Intent relations inside the Semantic Working
Outline. It may expand, normalize or fold the representation, but cannot
admit, activate, supersede or terminate Intent.

Cognitive State Formation carries Intent refs and versions in a candidate
snapshot and aligns them with other source versions. It does not copy or own
the authoritative Intent payload. Working Envelope carries the read-only
Intent refs needed by A/B.

The target path is:

`Intent Governance → Intent ref/version → Working Envelope and candidate
snapshot → Semantic representation and/or A reasoning`.

Any local semantic relation is derived representation. It is not an alternate
Intent record and cannot be written back without Intent Governance.
