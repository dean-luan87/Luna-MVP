# LUNA Qwen Voice Governed Entry Trial 定义 v0

**Phase**：Phase-Mainline-RuntimeReadiness-002  
**Trial id**：`qwen_voice_governed_entry_trial_v1`  
**入口**：`LUNA_ENABLE_QWEN_VOICE_GUARDED_TRIAL_V1`（默认 **false**）

---

## 目标

验证 **governance → GovernedVoiceProviderEntry → `run_tts_unified_entry` 前闸门**，且 **默认** 不真实播放、不真实默认 Qwen/TTS。

---

## 允许

- 读取 voice output governance decision  
- 运行 governed entry  
- provider selection **dry-run**  
- 仅在 **显式** 子闸下可选 **受控** provider 调用  
- 写 diff audit  
- 写 RequestTrace stage  
- 记录 fallback 决策  

---

## 禁止

- 默认真实 Qwen（无 flag）  
- 默认真实 TTS（无 flag）  
- 默认真实播放（无 flag）  
- 绕过 governance  
- 不经闸门直接进入 `run_tts_unified_entry`  
- 删除 Piper fallback  
- 修改默认 provider policy（本 Phase **禁止改代码/默认**）  
- 导航 / 世界模型 / SceneTask 等  

---

## 建议 env（与生成矩阵一致）

| Flag | 典型默认值 | 说明 |
|------|------------|------|
| `LUNA_DISABLE_ALL_GUARDED_TRIALS` | false | Global kill |
| `LUNA_ENABLE_QWEN_VOICE_GUARDED_TRIAL_V1` | false | Trial 总入口 |
| `LUNA_QWEN_VOICE_TRIAL_MODE` | shadow_only | `shadow_only` \| `governed_entry` \| `provider_dry_run` \| `controlled_provider` |
| `LUNA_ENABLE_GOVERNED_QWEN_ENTRY_V1` | false | governed entry 真路径筹备闸 |
| `LUNA_ENABLE_QWEN_PRIMARY_VOICE_MODE_V1` | false | 与 yaml 默认解耦的 trial 闸 |
| `LUNA_QWEN_VOICE_TRIAL_ALLOW_PROVIDER_INVOCATION` | false | 真实 provider |
| `LUNA_QWEN_VOICE_TRIAL_ALLOW_PLAYBACK` | false | 真实扬声器 |
| `LUNA_QWEN_VOICE_TRIAL_ABORT_ON_DIFF_AUDIT_MISSING` | true | 缺 audit 则 abort |
| `LUNA_QWEN_VOICE_TRIAL_WRITE_REQUEST_TRACE` | true | 关闭则不作为验收 |

---

## Acceptance（摘要）

- `voice_output_governance_decision` 存在  
- 合同要求处 Guard / SpeechGate 通过  
- GovernedVoiceProviderEntry 决策已发出  
- `source_text` / `spoken_text` / diff_audit 齐备（按模式）  
- Qwen 仅在 `online_prefer_qwen` 或显式允许模式选中  
- `offline_only` **永不** 选 Qwen  
- blocked 请求 `selected_provider=none`  
- RequestTrace stage 已发出  
- hard audit 合法；默认路径 `real_*` 仍为 false  

---

## Abort（摘要）

- governance 决策缺失  
- 必需路径上 SpeechGate 缺失  
- diff_audit 缺失（模式要求时）  
- blocked 仍选 provider  
- offline_only 选 Qwen  
- 无 allow flag 调用 provider  
- 无 allow flag 调用 playback  
- 非预期的 `real_tts_invoked`  
- global disable 与分项 enable **语义冲突**  

---

## Rollback（摘要）

- 关闭 `LUNA_ENABLE_QWEN_VOICE_GUARDED_TRIAL_V1`  
- `provider_mode=offline_only`  
- 不确定时 `selected_provider=none`  
- **保留** trial 日志  

机器可读完整表：`mainline_guarded_trial_matrix.json`（capability=`qwen_voice`）。
