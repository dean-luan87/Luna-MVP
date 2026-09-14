# Same-Evidence Invariance

每个 contrast 的左右 side 固定同一 source path，并要求以下 native projection 相同：

- provider/model identity
- OCR runtime mode
- `raw_text_candidates` 的 text、normalized text、bbox、confidence、line order
- joined text 与 native runtime status
- empty/error semantics

projection 去除 per-execution sample/frame identity 与 latency，仅用于证明物理 observation
content 等价；原始 native result 仍分别保存在 Runner 输出中。`native_observation_fingerprint`
不是 cognition 语义，也不能单独构成对照通过条件。

Verifier 同时要求 side 的 source、capability/provider/model identity 不变，并拒绝
physical mutation、Truth promotion、Fact admission 和 identity-only fake difference。
