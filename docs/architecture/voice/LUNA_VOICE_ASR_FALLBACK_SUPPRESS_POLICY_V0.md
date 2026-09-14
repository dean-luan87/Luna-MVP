# LUNA Voice — ASR Fallback & Suppress Policy v0

## 原则

- **fail-closed**：任何不确定不自动进入对话模型。  
- **本阶段不执行播报**；「ask repeat」等仅指 **产品语义上的用户重试路径占位**，不触发 TTS。

## 策略表

| 条件 | 行为 | Qianwen |
|------|------|---------|
| Provider unavailable | **suppress** 或 **候选 fallback provider**（仅设计；未接线） | 禁止 |
| Low confidence | **confirm / repeat / suppress** 路径 | 禁止直接送全文 |
| No speech | **关闭 utterance** 或 **等待**（策略由 session 定义） | 禁止 |
| Timeout | **关闭 utterance** | 禁止 |
| Cancelled | **取消 utterance** | 禁止 |
| Provider error | **fail-closed** + trace | 禁止 |

## `fallback_reason`（建议枚举，后续实现冻结）

- `provider_unavailable`  
- `switched_provider`  
- `suppressed_by_policy`  
- `low_confidence`  
- `user_cancelled`  
- `timeout`  
- `no_speech`
