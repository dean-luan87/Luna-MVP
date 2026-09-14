# Phase-Voice-OutputGovernance-004
# Voice Output TRW Adapter & Extractor Mapping Go/No-Go Pack v0

**目标**：让语音治理结果进入统一可观察面（通过 adapter records + timeline + mapping report），但仍不触碰真实播放链。

---

## 1. GO 条件

- input root 可读：`logs/voice_output_governance_002_test_run`
- TRW records 生成且非空
- stage namespace 完整（`voice_output_governance_v0`）且 stage_order 存在
- request-level timeline 生成
- extractor mapping report 生成且覆盖关键映射
- hard audit fields 全部可观测且满足不变量
- adapter trace/replay/whitebox 非空
- verifier 通过
- 未接真实 submit、未真实播报、未执行真实 TTS

---

## 2. CONDITIONAL_GO

- `trace_id/session_id` 为空，但：
  - `request_id` 完整可用
  - mapping report 中明确记录为 future mapping（主链注入）

---

## 3. NO_GO 条件

- hard audit fields 缺失或不满足不变量（任一为 true/非 null）
- 无 request-level timeline
- mapping report 缺失或不完整
- 本阶段接入真实 submit / 真实播报 / 执行真实 TTS
- 删除 legacy voice 或修改 env 语义

