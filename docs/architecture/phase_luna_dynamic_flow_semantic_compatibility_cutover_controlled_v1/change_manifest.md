# Change manifest

## Created

- Candidate-only Dynamic Flow compatibility package with output type, adapter, fixture, Runner, and Verifier.
- Focused architecture and scenario documentation for the compatibility cutover.

## Modified

- Real Input controlled integration result envelope now carries compatibility/A decision references and derives downstream semantic fields from A.
- Real Capability single-invocation trial adapter now records compatibility/A decision references only.

## Intentionally untouched

- DynamicCognitiveFlowEngineV1 and all legacy helpers/fields.
- Provider/model/YOLO/B1/B2/evidence admission behavior.
- Canonical enums, canonical owners, Loop semantic cutover, Multi-loop and closure scenario corpora.

## Verification ownership

User terminal owns Runner and Verifier execution. This phase has not been verified in this environment.
