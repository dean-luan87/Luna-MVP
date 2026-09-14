# Field Event and Temporal Validity Protocol Architecture Diagram v1

```mermaid
flowchart TD
  raw_event[Raw FieldEvent]
  intake[Field Event Intake]
  validate[Event Validator]
  evidence[Evidence Normalizer]
  anchor[Space and Time Anchor Resolver]
  candidate[Field Candidate Builder]
  admission[Field Event Admission]
  temporal[Temporal Validity Evaluator]
  overlay[Temporary Overlay Manager]
  revision[Revision and Revocation Manager]
  replay[Replay Protocol]
  projection[Active Field Projection Eligibility]

  raw_event --> intake --> validate --> evidence --> anchor --> candidate --> admission --> temporal --> overlay --> projection
  admission --> revision
  revision --> replay --> projection
  temporal --> replay
```

## Notes
- 该图展示了协议中事件从 Intake 到 Admission，再到 Temporal、Overlay、Revision 与 Projection 的路径。
- Replay 与 Revision 使用相同事件历史轨迹注意力。
- Overlay 管理不改变基础 substrate 定义。
