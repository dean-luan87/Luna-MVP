# LUNA Voice Prefilter Routing M3.5.6b Model-Chain Proof（最小观测补证）

## 补证目标

对 M3.5.6 中那 12 条 **day 段 model routes 非绿样本**做最小观测补证，确认结论是否可从 **B（暂定）**升级为 **B（确认）**。

本轮只回答两个问题：

1. 失败时模型有没有返回 payload / JSON？
2. 若返回了，为什么没有被识别为 `model_chain` 成功（`used_model_chain=true`）？

## 原则与边界（冻结项）

- 只加观测，不改逻辑
- 不修复、不扩灰
- 不改骨架
- 不改 prefilter / prompt / schema / validator / builder / fallback

## 专项开关（默认关闭）

- `LUNA_VOICE_ENABLE_MODEL_CHAIN_AUDIT_DEBUG=1`

要求：

- 未开启：当前行为完全不变
- 开启：仅额外写入观测字段，不改变业务结果

## 允许新增的最小观测字段（仅 5 项）

- `raw_model_payload_present`
- `raw_json_present`
- `raw_json_top_level_keys`
- `model_chain_detection_reason`
- `model_chain_detection_failed_reason`

建议观测落点（语义上）：

1. provider 返回后
2. parse 前 / parse 后
3. `used_model_chain` 判定前 / 判定后
4. fallback 决策前

## 复现实验方式（建议）

环境变量：

```bash
export LUNA_EXTERNAL_LLM_PROVIDER=qwen
export DASHSCOPE_API_KEY=...
export LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1
export LUNA_QWEN_MODEL_TIMEOUT_MS=120000
export LUNA_VOICE_ENABLE_MODEL_CHAIN_AUDIT_DEBUG=1
```

范围：

- 使用 M3.5.6 同类样本集（`m3_5_3` case 集）
- 轮数不需要很大；目标复现至少 1～2 条失败样本，并抓到若干成功对照样本

## 脚本

- `tools/repro_model_chain_failures_m3_5_6b.py`

运行示例：

```bash
python3 tools/repro_model_chain_failures_m3_5_6b.py --rounds 6 --time-slot day
```

输出：

- `logs/repro_model_chain_failures_m3_5_6b_<UTC>.json`
- `logs/repro_model_chain_failures_m3_5_6b_<UTC>.md`

## 结果填写区（已执行）

### 已跑 repro 产物（工作区 `logs/`）

| 实验 | 产物 JSON | 产物 MD | failure_rows |
|------|-------------|---------|--------------|
| day / 6 轮 | `logs/repro_model_chain_failures_m3_5_6b_20260407T034448Z.json` | `logs/repro_model_chain_failures_m3_5_6b_20260407T034448Z.md` | **0** |
| day / 10 轮 | `logs/repro_model_chain_failures_m3_5_6b_20260407T040044Z.json` | `logs/repro_model_chain_failures_m3_5_6b_20260407T040044Z.md` | **0** |

### 观测事实

- **补证链路已打通**：成功样本可稳定输出全部 5 个审计字段（`raw_model_payload_present`、`raw_json_present`、`raw_json_top_level_keys`、`model_chain_detection_reason`、`model_chain_detection_failed_reason`）。
- **失败样本未复现**：上述两次小规模 repro 中 **`failure_rows` 均为 0**，未再次捕获与 M3.5.6 同型的 `used_model_chain=false` 失败行。

## M3.5.6b 结论（收口）

**证据不足以完成归因确认；M3.5.5/M3.5.6a 中的「B」维持「暂定」，不能升级为「确认」。**

说明：

- 既不能据此写死「模型真失败」（A），也不能写死「success tagging / detection 未命中」（B 确认）。
- 结合 M3.5.6 全量跑批曾出现 12 条 day 段非绿、而后续 day/6 与 day/10 均未复现，更符合 **低频、偶发、当前条件下难以稳定复现** 的边缘事件，而非稳定故障。

**M3.5.6b 结果（可直接写入状态说明）：**

补证链路已完成，成功样本可正常输出全部审计字段；但在 day/6 与 day/10 的复现实验中未再次捕获失败样本，因此当前仍无法将 B 从「暂定」升级为「确认」。现阶段不建议继续为复现而扩大专项轮数；建议保留该审计链作为后续同类问题再次出现时的定点归因工具。

## 最终结论（三选一）与下一步

本轮 **不满足**在 repro 中给出 A/B/C 单选结论的前提（无失败样本可对照）。建议：

1. **不再继续追 M3.5.6b 复现**（避免无限提轮数「钓鱼」）。
2. **不改任何逻辑**；**维持当前灰度范围，不继续扩大**。
3. **暂不修 detection，也不修 provider**；将本套开关 + `repro_model_chain_failures_m3_5_6b.py` 作为 **应急审计能力**，仅在复发时再启用。

若未来复发且 repro 中抓到失败样本，再按下方「最关键的判断标准」在 A / B / C 中单选，并决定下一层修复方向。

## 最关键的判断标准（用于确认 B）

若补证后出现：

- `raw_model_payload_present=true`
- `raw_json_present=true`
- `raw_json_top_level_keys` 合理
- 但 `used_model_chain=false`

则基本可确认：

**B. success tagging / detection 口径问题为主**。

若补证后发现：

- 根本没有 payload
- 或根本没有 JSON
- 或 provider 路径没有形成有效结构化结果

再考虑 **A / C**。

