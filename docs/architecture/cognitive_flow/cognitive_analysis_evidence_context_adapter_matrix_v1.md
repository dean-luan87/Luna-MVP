# A3 Cognitive Analysis Evidence Context Adapter Matrix v1

| input source | accepted adapter input | normalization allowed | provenance requirement | prohibited outcome |
| --- | --- | --- | --- | --- |
| OCR Evidence Governance | candidate Evidence references only | reference-name/order mapping | source refs and trace retained | OCR execution, Fact promotion, text semantic finalization |
| Vision Evidence | read-only candidate Evidence references only | reference-name/order mapping | source-chain and trace retained | Vision execution, Fact/World Model write, Decision output |
| Observation Attention | candidate attention/observation references only | reference-name/order mapping | source and candidate trace retained | follow-up Runtime/model route execution, Fact/semantic write |
| Current Cognitive Context | derived/read-only Context reference only | Context reference mapping | Context provenance and trace retained | Context/Snapshot/Field State mutation |
| A3 Runtime | receives normalized references only | none performed by Runtime through this Adapter | Adapter provenance carried forward | Runtime authorization, State writeback, Fact/Decision/Action/Memory operation |

All rows remain subject to L1 Input Candidate, Output Candidate, Symmetry, Traceability, and Permission/Admission governance.
