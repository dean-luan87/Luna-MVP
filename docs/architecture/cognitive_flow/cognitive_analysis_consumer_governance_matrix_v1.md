# A3 Cognitive Analysis Result Consumer Governance Matrix v1

| Consumer | Input | Allowed Operation | Forbidden Operation | Authority |
| --- | --- | --- | --- | --- |
| Observation Layer | Result Candidate, Evidence, Uncertainty, Provenance | read and retain candidate signals for future governed observation handling | Fact/Decision/Action/State/Memory operation | read-only; no execution authority |
| Context Layer | Result Candidate, Evidence, Uncertainty, Provenance | read as contextual signal with trace preserved | Context/Snapshot writeback; Fact/Decision/Action/State/Memory operation | read-only; A2 remains Context authority |
| Hypothesis Layer | Result Candidate, Evidence, Uncertainty, Provenance | read as support/contradiction/uncertainty input for a separate candidate process | forced conclusion; Fact/Decision/Action/State/Memory operation | read-only; no Fact authority |
| Decision Support Layer | Result Candidate, Evidence, Uncertainty, Provenance | read as a bounded support signal for a separately governed future domain | Decision creation or execution; Fact/Action/State/Memory operation | read-only; no Decision authority |
| Learning Candidate Layer | Result Candidate, Evidence, Uncertainty, Provenance | read as a candidate input to a future learning review | Memory/Experience update; Fact/Decision/Action/State operation | read-only; no Memory authority |
