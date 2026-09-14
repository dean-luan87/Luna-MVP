# LUNA Evaluation Tools — OCR Test Harness Boundary v0

## Scope

This folder documents **Evaluation Tools / Test Harness** modules. These modules:

- Generate offline datasets (including synthetic datasets)
- Produce ground truth manifests
- Evaluate OCR providers (e.g. RapidOCR) and output quality reports (CER/recall/garbled/failures)

## Hard boundaries

- **Not runtime**: must not be imported or executed by Luna runtime.
- **Not whitebox**: must not be wired into any whitebox backend/UI.
- **No MidPlatform / SceneDelta / WorldContextEvidence**
- **No semantic interpretation**
- **No Qwen / TTS / playback**
- **No world write / hive upload**

## Output contracts

Evaluation tools may write local `trace/replay/whitebox` JSONL files **for evaluation-only auditing**.  
They must **not** reuse runtime RequestTrace pipelines or stage namespaces.

