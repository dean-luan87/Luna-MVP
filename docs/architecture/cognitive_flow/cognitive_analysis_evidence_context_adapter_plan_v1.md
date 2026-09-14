# A3 Cognitive Analysis Evidence Context Adapter Plan v1

## Position

The Evidence Context Adapter is a reference-only boundary between governed external Evidence/Context inputs and A3 Cognitive Analysis Runtime.

```text
External Evidence / Current Cognitive Context
                ↓
      Evidence Context Adapter Candidate
                ↓
      Cognitive Analysis Runtime input boundary
                ↓
        Analysis Result Candidate
```

It accepts only governed reference identities and provenance. It does not fetch raw observations, execute OCR/Vision/Attention, invoke Runtime, or produce an Analysis Result.

## Responsibilities

- map Evidence references without changing evidence content;
- map a derived, read-only Context reference;
- normalize reference field names and ordering only;
- attach retained source/trace provenance.

## Direct Asset Alignment

- OCR evidence envelopes are candidate-only and expose provenance/trace references.
- Vision read-only ingest candidates preserve `not_fact` and source-chain summaries.
- Observation Attention is candidate-only and explicitly disallows Runtime and Fact writes.
- `CurrentCognitiveContextV1` is derived/read-only and preserves provenance/trace.

## Non-Goals

No Fact creation, semantic finalization, Decision generation, Action execution, State update, Memory update, model invocation, Runtime execution, network access, or persistence is allowed.
