# LUNA Voice — Governed Entry RequestTrace Go / No-Go Pack v0（Phase-Voice-Qianwen-003）

---

## GO

1. Phase-002 **online / offline** 根可读，evaluate **产物齐全**。  
2. **request chains**、**provider mode comparison**、**selection / speakability / diff 表** 已生成。  
3. **online**：**accepted → qwen-first** 可观测；**fallback → piper** 可观测。  
4. **offline**：**仅 piper / none**，**永不 qwen**。  
5. **Speakability / diff** 可观测；**provider_caused_rewrite** 恒 **false**；guard 归因 **`guard_v1_speakable_text`**。  
6. **hard_audit** 不变量保持；**trace/replay/whitebox** 非空。  
7. **verifier `ok: true`**；**未改**默认 `voice_tts_config.yaml`；**无真实 Qwen/TTS**。  

---

## CONDITIONAL_GO

- **blocked** 样本 **`spoken_text` 为空**，但 **`entry_block_reason` / governance** 可解释（与设计一致）。

---

## NO_GO

- **offline** 出现 **qwen**；**blocked** 仍选 **qwen**。  
- **expression_provider=true** 或 **model_may_rewrite_text=true**。  
- **provider_caused_rewrite=true**。  
- **缺失** diff / speakability 表或 **hard_audit** 被破坏。  
- **修改默认语音配置**或删除 **Piper fallback**。

---

## 与「主链」关系（口径）

完成 Phase-003 后：**YOLO → OCR → Voice/Qwen** 在 **离线 / shadow / 治理 / 可观测** 维度可视为 **闭合**；**真实 runtime 主链**（真实 provider、播放、连续流回归等）仍 **未闭合**——见主线 readiness 后续 Phase。
