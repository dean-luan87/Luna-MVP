# LUNA Voice — Qianwen Provider Control Inventory Go / Conditional Go / No-Go Pack v0

**Phase**：Phase-Voice-Qianwen-000（inventory only）。

---

## GO（准许进入下一阶段设计/接线）

以下条件 **全部满足**：

1. **静态扫描**完成，产物齐全：`voice_qianwen_provider_inventory_summary.json`、`voice_qianwen_*_matrix.json`、`voice_qianwen_control_gap_register.json`、`voice_qianwen_search_hits.json`、`inventory_notes.md`。
2. **资产三分法**写清：(a) 代码存在 (b) 文档/模板声明 (c) 默认/激活基线可证明与否。
3. **Qwen 首选 / Piper(TTS) 退路**的状态在「模板 vs 顶层默认基线」层面 **不生搬硬套**——已登记 **S-003**。
4. **source/spoken/generation diff、no_fabrication、rewrite** 与控制面接线状态明确，并已登记至少 **H-002**。
5. **guard/SpeechGate/governance** 与实际 `run_tts_unified_entry`/输出平面的串联状态明确，并已登记 **H-001**。
6. **未改 runtime**、未真实播报、未真实调用 Qwen、未删减 TTS 退路。

---

## CONDITIONAL_GO（带硬缺口条件下的阶段放行）

**推荐结论（针对当前快照）**：**CONDITIONAL_GO**

**理由简述**：

- **Qwen 适配器与「Qwen 优先 + Piper 退路」配置模板**：代码与 YAML **已存在**。  
- **默认签入基线**仍为 **`offline_only` + `[piper]`**，与「口述策略已全部切成 Qwen 首选」**可能不一致**，须按 **S-003** 与运维双层口径对齐。  
- **`VoiceOutputPlaneV1` execute_tts 路径**明示 **不接 SpeechGate**；无法静态证明播报链已吃进完整 **voice_output_governance_v0**（**H-001**）。  
- **结构化 diff audit**缺席（**H-002**）。  

**CONDITIONAL_GO 下的约束**：下一阶段任何「首选 Qwen」推进，须先消解或方案化 **hard blockers**，不得把 Phase-009 的统一查询能力误当成「播报主链已通过 governance」的替身。

---

## NO_GO（本阶段应立即打回）

出现任一即为 **NO_GO**：

1. 在盘点阶段 **修改生产 runtime** 行为以「凑 GO」。
2. 盘点阶段 **真实调用 Qwen** 或执行 **真实 TTS 播报**。  
3. 删除或降级 legacy TTS / Piper 退路。  
4. 将 **文档措辞**误判为「主链已接线完成」。  
5. **未登记** `source/spoken`/diff、`no_fabrication`/`rewrite` 的证据状态与缺口。

---

## Hard blockers（来自 gap_register）

- **QWVoice-INV0-H-001**：unified execute_tts 与 `voice_output_governance_v0` 的证明性串联缺失。  
- **QWVoice-INV0-H-002**：成对文本与 diff_audit schema 缺席。

## Soft follow-ups

- **S-001 / S-002 / S-003**：改写边界、编造策略结构化、三层口径对齐。

## Recommended next phase

**Phase-Voice-Qianwen-001+**：以「不改变默认 policy 语义」为前提，选型 **单一权威入口**，将 `SpeechRequest.text_candidate` **必须**流经 `voice_output_governance_v0`（或可证明等价物），再在 **real_tts_invoked** 仍为硬审计的条件下接通 `run_tts_unified_entry`；并联入 RequestTrace/TRW stage，使 Phase-009 查询可覆盖 Qwen+Piper fallback 全路径。
