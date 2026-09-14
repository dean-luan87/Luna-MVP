# OCR Synthetic Eval Metrics v0 (Evaluation Tools)

## Metrics

- **CER**: character error rate \(edit\_distance / max(1, truth\_len)\)
- **Chinese character recall**: set-based recall over Chinese characters in truth
- **Garbled score**: heuristic ratio of unusual glyphs outside common ranges

## Quality classes (v0)

- **pass**: cer \(\le 0.15\) and garbled\_score \(\le 0.10\)
- **weak_pass**: cer \(\le 0.35\) and garbled\_score \(\le 0.20\)
- **fail**: pred empty, or cer \(> 0.50\), or garbled\_score high
- **review_pending**: otherwise

## Notes

This is evaluation-only and must not drive runtime provider selection directly.

