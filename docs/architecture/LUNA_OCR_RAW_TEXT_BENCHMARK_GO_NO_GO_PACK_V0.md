# LUNA — OCR Raw Text Benchmark Go/No-Go Pack v0

## Phase

- **Phase-ModelOCR-005**
- Subject: GT dataset + 3-provider raw text benchmark pipeline validity.

## GO

- dataset manifest + GT schema valid.
- small GT dataset runnable.
- provider outputs legal (or honest not_available).
- accuracy/latency/governance/observability metrics generated.
- semantic/navigation leakage = 0.
- verifier A-L passes.

## CONDITIONAL_GO

- sample set is small.
- some provider not_available but honestly reported.
- Paddle orientation-sensitive cases excluded/not-claimed.
- pipeline can proceed to dataset expansion.

## NO_GO

- GT includes semantic/navigation labels.
- GT fabricated from OCR outputs.
- downstream invocation exists.
- semantic/navigation leakage > 0.
- trace/replay/whitebox missing.
- metrics incomplete.
- provider failure faked as success.
