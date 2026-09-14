# Cognitive Analysis Controlled DryRun Negative Guard v1

## Guard register

All guards are blocker-level unless explicitly classified as an expected
case warning. They must be independently checked rather than inferred from a
single Runner success value.

| # | Guard | Check method | Applies to |
| --- | --- | --- | --- |
| 1 | No real analysis execution | fixed result flag and source boundary | all |
| 2 | No A2 runtime invocation | import/call inspection | all |
| 3 | No Reducer runtime invocation | import/call inspection | all |
| 4 | No model invocation | import/call/result flag | all |
| 5 | No network | import/call/result flag | all |
| 6 | No database | import/call/result flag | all |
| 7 | No camera | import/call inspection | all |
| 8 | No OCR | import/call inspection | all |
| 9 | No SLAM | import/call inspection | all |
| 10 | No system time | AST/source/result determinism check | all |
| 11 | No random | AST/source determinism check | all |
| 12 | No automatic UUID | AST/source determinism check | all |
| 13 | No Hypothesis-to-Fact promotion | object/permission check | all |
| 14 | No confidence-to-Fact promotion | object/permission check | all |
| 15 | No forced dominant hypothesis | Set status/member check | 002 |
| 16 | No Unknown completion | status/warning check | 006 |
| 17 | No Observation execution | request flag/call inspection | 007 |
| 18 | No Decision execution | boundary flag/call inspection | all |
| 19 | No State writeback | result flag/authority check | all, especially 008 |
| 20 | No Context writeback | object immutability/call inspection | all |
| 21 | No Snapshot writeback | object immutability/call inspection | all |
| 22 | No Result-to-Event automatic conversion | output-type and call inspection | all |
| 23 | No fixture mutation | before/after serialized fixture comparison | all |
| 24 | No historical-result deletion | revoked/stale version reference check | 005 |

Expected warnings, including revoked Evidence and temporal unknown, do not
weaken guards. A warning is valid only when it matches the case specification.
