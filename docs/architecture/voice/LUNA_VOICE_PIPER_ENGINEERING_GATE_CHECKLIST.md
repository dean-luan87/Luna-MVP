# Luna Voice Piper Engineering Gate Checklist

## 1. 文档定位

本文件是当前 `Piper` 工程基线的阶段验收清单（Gate Checklist）。  
用途：作为后续白盒接入、Fish 恢复、ASR 预案前的统一 gate 判定依据。

## 2. 当前验收范围

本次仅覆盖以下范围：

- `Piper` 作为当前默认工程主链
- 统一入口链路（`tts_unified_entry -> selector -> provider chain`）
- preset 工程化参数落地
- fallback / rollback 不退化

明确不包含：

- Fish 本机跑通
- 白盒后台实现
- ASR 接入

## 3. 验收项表格

| 验收项 | 状态 | 证据 | 备注 |
|---|---|---|---|
| 正式配置切到 Piper | 通过 | `capabilities/voice/config/voice_tts_config.yaml` | `active_provider=piper` |
| provider_order 正确 | 通过 | `capabilities/voice/config/voice_tts_config.yaml` | `[piper]` |
| Fish 已移除 | 通过 | `capabilities/voice/config/voice_tts_config.yaml` | `local_runtime.piper.enabled=false` |
| preset 已工程化 | 通过 | `capabilities/voice/config/voice_presets.yaml` | 四个 preset 已映射到 Piper 参数 |
| 统一入口真实可调用 | 通过 | `tools/run_piper_engineering_pack.py` + `logs/piper_engineering_pack.json` | 非直调 provider demo |
| 7 条工程样本成功 | 通过 | `logs/piper_engineering_pack.json` | `success=7/7` |
| latency 已记录 | 通过 | `logs/piper_engineering_pack.json` | 约 `585ms~892ms` |
| provider_name = piper | 通过 | `logs/piper_engineering_pack.json` | 全部样本 `provider_name=piper` |
| fallback 回归通过 | 通过 | `logs/voice_stage22_validation_results.json`（fallback 场景） | 链路未退化 |
| rollback 回归通过 | 通过 | `logs/voice_stage22_validation_results.json`（rollback 场景） | 链路未退化 |
| 旧主链未被破坏 | 通过 | 当前变更范围与回归结果 | 未对 `main.py`/`core/audio_worker.py`/`core/speech_gate.py` 做语义改造 |
| 当前局限已记录 | 通过 | `docs/architecture/voice/LUNA_VOICE_PIPER_ENGINEERING_BASELINE.md` | 局限与交接条件已声明 |

## 4. 当前局限

- 真人感和情绪层次仍有限，当前以“稳定播报”优先。
- Fish 尚未本机跑通，当前不参与主链质量对照。
- 警告强度仍受本地 TTS 表达上限约束。
- 当前口径仍是本地 TTS 主链，不涉及云端增强。

## 5. 结论

当前 Gate 结论：**通过**。  
`Piper` 可作为当前阶段默认工程主链继续推进。

## 6. 证据索引

- `docs/architecture/voice/LUNA_VOICE_PIPER_ENGINEERING_BASELINE.md`
- `logs/piper_engineering_pack.json`
- `logs/piper_engineering_pack/*.wav`
- `logs/piper_temp_default_validation.json`
- `logs/piper_temp_default_observations.jsonl`
- `logs/voice_stage22_validation_results.json`

## 7. 主线—白盒—日志一致性检查

- A 主线：Piper 主链已稳定可执行。
- B 白盒：本轮不扩白盒实现，仅保留现有 observation 链路可用。
- C 日志：工程验证结果与音频证据已落地可复核。
- D 最终判断：**主线通顺，白盒一致，日志已落地**。

