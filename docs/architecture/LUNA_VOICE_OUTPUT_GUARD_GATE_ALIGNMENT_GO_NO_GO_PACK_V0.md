# Phase-Voice-OutputGovernance-001-Fix
# Voice Output Guard/Gate Alignment Go/No-Go Pack v0（对齐补丁决策包）

**目标**：把两项硬风险（`guard_v1_speakable_text` 命名/实现不一致、SpeechGate 主链接线不明）在“合同 + 静态验证”层面钉死，避免后续 skeleton 在错误假设上继续演进。  
**硬边界**：不改 runtime、不真实播报、不执行真实 TTS、不接新 provider、不删 legacy voice、不改现有 env 开关语义、不接导航/SceneTask/Fusion/Output 新链路。

---

## 1. In scope

- Guard/Gate 现状复盘（代码/文档证据）
- 主链 gate contract（必须经过 guard + gate 的接线顺序与可观测要求）
- 静态 verifier（扫描资产、引用、接线痕迹、合同标记）
- `docs/architecture/README.md` 索引更新

## 2. Out of scope（禁止）

- 任何真实播报行为改变
- 任何真实 TTS 执行/新 provider 接入
- 任何 env 开关语义/默认值改变
- 删除或重构 legacy voice 代码

---

## 3. GO 条件

满足以下全部条件判定 **GO**：

- **guard 当前状态明确**：
  - `guard_v1_speakable_text` 若缺失，必须被明确记录为缺口/替代策略，而不是继续假设存在
- **SpeechGate 主链接线要求明确**：
  - 无论当前是否已接线，都必须在合同中写清“应在哪个点生效（submit helper 或 output plane）”
- **后续 skeleton hard gate 条件明确**：
  - candidate → guard → gate → expiry/priority/cancel → output plane → provider health → tts/playback
- **静态 verifier 通过**：
  - 输出 `verification_result.json`
  - 识别并报告 guard 缺失/接线缺失为 blocker/required（而非 silent pass）
- **边界未破坏**：本阶段只新增文档与静态工具，不改 runtime 行为

---

## 4. CONDITIONAL_GO（条件通过）

允许在以下情况下判定 **CONDITIONAL_GO**：

- SpeechGate 接线未检测到，但合同已明确 `SPEECH_GATE_MAINLINE_WIRING_REQUIRED: true`，且 verifier 输出中将其标记为 required，并把它作为 Phase-002 的 hard gate。

---

## 5. NO-GO 条件

出现任一情况判定 **NO-GO**：

- 文档继续假设 `guard_v1_speakable_text` 存在但代码不可定位（即“假 guard”）
- SpeechGate 是否应生效/在哪生效未说明（即“空 gate”）
- 盘点/对齐阶段出现真实播报、真实 TTS 执行、新 provider 接入、或删除 legacy voice

---

## 6. 验收输出（本阶段）

1. 实际新增/修改文件路径
2. 每个文件一句话作用说明
3. `guard_v1_speakable_text` 定位结果（present/missing + evidence）
4. SpeechGate 主链定位结果（detected/not_detected + contract required）
5. mainline gate contract 摘要
6. verifier 结果摘要（pass/blockers/required）
7. go / conditional_go / no_go 结论
8. hard blockers
9. soft follow-ups
10. recommended next phase
11. 明确声明：本阶段只做 guard/gate 对齐，不改 runtime、不真实播报、不接新 provider、不删 legacy voice

