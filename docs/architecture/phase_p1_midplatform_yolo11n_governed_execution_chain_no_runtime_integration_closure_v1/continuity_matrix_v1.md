# Continuity matrix

The closure checks preserve:

- Capability and Slot identity;
- Model asset, model version and weights version;
- Provider binding identity and version;
- Runtime Admission ref/version;
- Grant and constraint refs;
- trace and provenance refs;
- source-version refs;
- empty/current invalidation state.

The Provider Admission candidate receives the binding and Runtime Admission
refs from the context; it does not reconstruct them.
