# LUNA Voice — ASR State Machine v0

## 状态集合

| 状态 | 说明 |
|------|------|
| `idle` | 未采集 |
| `listening` | 采集音频窗口内 |
| `partial_transcribing` | 已有 partial，未终结 |
| `finalizing` | 结束采集/等待 provider 定稿 |
| `final_text_ready` | **唯一允许**进入语义 / Qianwen 准备态的 ASR 侧出口（须配合 `asr_status == final`） |
| `no_speech` | 无有效语音 |
| `timeout` | 等稿超时 |
| `cancelled` | 用户或系统取消本 utterance |
| `provider_error` | provider 失败 |
| `low_confidence` | 低于阈值，仅 confirm/repeat/suppress |
| `suppressed` | 被策略抑制，不产生下游文本 |

## 规则（硬）

1. **只有 `final_text_ready`**（且事件 `asr_status == final`、`is_final == true`）才允许进入后续 **语义 / Qianwen**。  
2. **`no_speech` / `timeout` / `cancelled`**：**不得**触发 Qianwen。  
3. **`low_confidence`**：**只能**进入 confirm / repeat / suppress；**不得**将低置信度全文默认送入 Qianwen。  
4. **`provider_error`**：**fail-closed**（不冒进下游；可带错误码入 trace）。  
5. **`suppressed`**：不产生 `final_text` 下游消费；可记 trace。

## 与事件合同的关系

- `final_text_ready` 是 **会话/ASR 编排状态**；`ASRFinalTextEventV0.asr_status == "final"` 是 **事件负载上的终结成功标记**。二者须由 runtime 接线 phase **成对保证**，本阶段仅冻结规则。
