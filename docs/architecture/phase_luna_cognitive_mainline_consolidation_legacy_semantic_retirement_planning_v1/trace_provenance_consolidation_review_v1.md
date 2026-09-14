# Trace / provenance consolidation review

Current patterns are repeated but not owned by a new Trace Manager:

- Dynamic Flow builds `trace:{scenario}:state/transition` and evidence-derived provenance refs;
- A semantic bridge builds decision validation traces and provenance;
- A/B bridge carries request/result traces;
- Working Envelope bridge builds envelope, Need and evidence-return refs;
- Loop stores local trace/provenance refs and closure history;
- A Route builds stage/handoff traces;
- Capability and Observation own their own candidate trace fields.

Disposition: KEEP source ownership and reverse-linkability. P2 consolidation may introduce a shared protocol/helper only if an existing trace primitive is extended without changing ownership. Do not normalize identifiers or merge histories in this phase.

