# A3 Translation Layer Real Evidence Binding Architecture Plan v1

## Scope

This plan describes the future boundary for binding governed OCR, Vision, Audio, and Spatial Evidence Providers to the frozen Translation Layer. It does not bind a provider, invoke a model, execute Runtime, or alter Fact/Decision/State authority.

```text
Provider-specific raw output
        ↓ stays outside Translation
Governed Evidence Envelope (candidate-only)
        ↓ references + provenance + trace only
Evidence Adapter Binding (future)
        ↓ existing Translation Request
Translation Layer
        ↓ Cognitive Primitive Candidate
```

## Binding Responsibilities

- validate that a Provider has emitted a governed Evidence Envelope before any Translation request is formed;
- map provider identity, Evidence reference, Context reference, provenance, uncertainty, and trace into existing reference fields;
- retain provider-native content behind `evidence_ref`, rather than copying it into Translation;
- select an existing permitted primitive type without semantic finalization; and
- surface missing, stale, revoked, conflicting, or unsupported provider evidence as candidate warnings/block conditions.

## Non-Responsibilities

Binding does not create Fact, decide semantic truth, identify a person, issue navigation or action advice, mutate Context/Snapshot/Field State/Memory, train/update a model, or authorize Runtime. It creates no new governance, Protocol, Permission model, or Registry path.

## Future Provider Onboarding Gate

Before a separately approved binding implementation, each provider must demonstrate compatible Evidence references, source/provider provenance, trace continuity, explicit uncertainty, candidate-only output, and no direct write route. Provider compatibility does not equal provider activation or Runtime authorization.

