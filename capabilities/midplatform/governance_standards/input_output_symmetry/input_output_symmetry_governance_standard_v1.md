# Input / Output Symmetry Governance Standard V1

## Principle

Any input candidate that becomes output, record, or fact-layer input must preserve full traceability.

## Required Chain Elements

- `candidate → output/result/record` traceability  
- `evidence_refs`  
- `protocol_refs`  
- `error_namespace`  
- `whitebox_candidate_ref`

## When to Use

Before promoting any candidate to output adapter, record, registry field, or fact admission input.

## Forbidden

- Output without input evidence chain  
- Silent drop of protocol or candidate refs  
- Fact write without admission record

## Usage Note

Symmetry applies to OCR, vision, inference, runtime candidates, and external API outputs equally.
