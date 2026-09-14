# Post-Observation Semantics

An executing state consumes the existing real OCR result path:

`ProviderRuntimeResult → RuntimeObservationEnvelope → Observation Gateway`
`→ Evidence Candidate → A-Route → Cognitive State → Sufficiency / Gap / Stop`.

The regulation state records the returned Provider Result, RuntimeObservation,
Gateway, Evidence, A-Route/CState, Sufficiency, Information Gap, and Stop
references. It does not reinterpret OCR text as Truth or mutate Field state.

When the existing cognition result is sufficient, the regulation status is
`INFORMATION_SUFFICIENT` and the finite case ends. The phase does not create an
autonomous re-observation loop.
