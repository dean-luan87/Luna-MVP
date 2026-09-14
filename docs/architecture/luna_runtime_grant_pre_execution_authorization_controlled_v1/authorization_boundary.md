# Authorization boundary

The phase distinguishes four decisions:

1. FPO semantic continuation: whether more observation is semantically useful.
2. Provider binding: whether a governed provider can be associated with a
   preparation candidate.
3. Runtime execution grant: whether this complete request may proceed into a
   future execution boundary.
4. Gateway ingress admission: whether an already-produced runtime observation
   may enter the observation system.

Only item 3 is formed here. A grant decision is authoritative for the
permission boundary but has no runtime authority and no truth authority. It
contains no concrete execution instance identity. `GRANTED` preserves
`runtime_allocated=false`, `execution_instance_created=false`,
`provider_session_started=false`, and `gateway_submission=false`.

The grant cannot select a provider, select a model, rewrite a demand, or
replace a denied provider with a fallback. It consumes explicit upstream
references and explicit controlled status inputs.
