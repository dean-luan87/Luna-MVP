# Runtime Path

The Runner creates a real OCR observation case and sends it through the shared
Provider Runtime resolution path. It does not use the earlier recorded-result
fixture.

1. Build an observation demand for `OCR_TEXT_EVIDENCE`.
2. Reuse Field Perception Orchestrator and Universal Capability Slot
   resolution.
3. Preserve the canonical FPO capability requirement identity in
   `ProviderRuntimeRequestV1`; retain the separate normalized
   `provider-requirement:*` identity in diagnostics.
4. Resolve `ocr_v1` from the canonical capability/provider/model registries.
5. Invoke the existing RapidOCR adapter once with the local image.
6. Normalize its native candidates into `ProviderRuntimeResultV1`.
7. Adapt the result to `RuntimeObservationEnvelopeV1`.
8. Reuse Observation Gateway, including its LIVE_RUNTIME admission proof.
9. Reuse A-Route and Cognitive State Formation until sufficiency, information
   gap, and stop are produced.

The native text candidate payload is carried as an optional candidate payload
on the runtime envelope and Gateway evidence. It remains referenceable output,
not a fact or semantic interpretation.
