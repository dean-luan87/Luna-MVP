# Phase-Voice-OutputGovernance-004
# Voice Output TRW Adapter Test Matrix v0（测试矩阵）

**目的**：保证 adapter 能从 Phase-002 产物生成 TRW records、stage timeline、mapping report，并保持硬审计不变量。

---

## 1. 输入根目录

- `logs/voice_output_governance_002_test_run`

---

## 2. 覆盖点

- records 生成：每个 request 至少生成一组 stage records（按固定 stage_names 顺序）
- timeline 生成：每个 request 有 ordered timeline
- mapping report 生成：包含 sources、field_mapping、missing_fields_expected_future
- whitebox extension 生成：包含 why_* 字段

---

## 3. 全局不变量（必须）

- hard audit fields 可观测且满足：
  - `real_tts_invoked=false`
  - `playback_invoked=false`
  - `provider_invoked=false`
  - `downstream_invocation_count=0`
  - `navigation_action=null`
- adapter trace/replay/whitebox JSONL 非空
- 本阶段不接入真实 submit、不真实播报、不执行真实 TTS

