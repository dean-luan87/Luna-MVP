# LUNA — YOLO × OCR Offline Bridge Boundary Register v0

## Prohibited (must not)

- 连接真实 runtime（不允许接入真实系统调用链）
- 接中台（MidPlatform wiring not allowed）
- 进入下游（SceneTask / Fusion / Output not allowed）
- 语义提炼（semantic interpretation disabled）
- 导航动作建议与执行
- 真实播报与 real TTS 触发
- controlled_live_stream 进入
- 修改 `YOLO closed_v0` 或 `OCR closed_v0`（离线证据只读）

## Must Preserve (must preserve)

- `raw-text-only`
- `candidate-only`
- Proposal/result/attribution 字段契约（YOLO→OCR evidence 链）
- crop padding + clamp 的边界约束
- trace / replay / whitebox 证据文件的完整性
- `candidate_only=true`、`semantic_interpretation_enabled=false`、`allows_execute_now=false`、`real_tts_invoked=false`、`downstream_invocation_count=0`

## Governance Assertion

- governance leakage 必须为 0。
- verifier 通过才允许将 offline bridge 状态登记为 closed_v0（但允许在 closure 中记录证据样本规模限制作为 future branch）。

