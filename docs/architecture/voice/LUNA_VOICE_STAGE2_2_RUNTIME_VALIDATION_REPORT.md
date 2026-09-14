# Luna Voice Stage-2.2 Runtime Validation Report

## 1) 文档定位

本报告记录 Stage-2.2 的本机真实执行结果。  
聚焦：真实出音、fallback、rollback、observation 活性；不做结构扩展。

## 2) 验证脚本与结果产物

- 验证脚本: `tools/validate_local_tts_runtime.py`
- 结果文件: `logs/voice_stage22_validation_results.json`
- observation 日志: `logs/voice_stage22_observations.jsonl`
- 真实音频样例:
  - `logs/piper_smoke.wav`
  - `logs/stage22_piper.wav`

## 3) 测试项总表

| 测试项 | Provider | 是否成功 | 延迟(ms) | 音频可用性 | observation 是否生成 | 备注 |
|---|---|---:|---:|---|---|---|
| Fish 正常执行 | piper（已移除 Fish）| 否 | 1 | 否 | N/A（直调 provider） | `FISH_TTS_BINARY_NOT_FOUND` |
| Piper 正常执行 | piper | 是 | 734 | 是（110124 bytes） | N/A（直调 provider） | `logs/stage22_piper.wav` |
| Fish 失败 -> Piper fallback | chain | 是 | 818（final provider） | 是 | 是（selection + fallback + cutover） | `final_provider_used=piper` |
| Fish/Piper 全失败 -> legacy rollback | chain | 是 | 1（last provider fail） | legacy 路径执行 | 是（selection + fallback + cutover + rollback） | `final_execution_mode=legacy_fallback` |
| cutover 关闭 -> legacy 直通 | legacy | 是 | N/A | legacy 路径执行 | 是（cutover） | `cutover_enabled=false` |

## 4) 关键验收点对应结论

1. Fish 本机真实执行尝试：**已尝试，失败（结构化）**  
2. Piper 本机真实执行：**已成功**  
3. provider fallback（Fish->Piper）：**真实触发并成功**  
4. provider chain->legacy rollback：**真实触发并成功**  
5. observation 活性：**真实生成并可按 request_id 串联**

## 5) observation 核验摘要

- `ProviderSelectionObservation`: 已生成（fallback/rollback 场景均有）
- `ProviderFallbackObservation`: 已生成（Fish->Piper 成功回退、全链失败均有）
- `TTSCutoverObservation`: 已生成（provider_chain 与 cutover_off 场景均有）
- `TTSRollbackObservation`: 已生成（provider_chain_fail -> legacy）

## 6) 失败模式区分（环境 vs 设计）

- 环境不可用:
  - Fish CLI 缺失 -> `not_available / FISH_TTS_BINARY_NOT_FOUND`
  - Piper 可执行被人为置为不存在 -> `not_available / PIPER_BINARY_NOT_FOUND`
- 设计路径验证:
  - Fish fail -> Piper fallback: 正常
  - Provider chain fail -> legacy rollback: 正常
  - cutover 关闭 -> legacy 直通: 正常

结论：当前失败主要来自 Fish 本机可执行缺失，不是 fallback/rollback 设计缺陷。

## 7) 主观听感（本轮最小记录）

- Piper 真人感：中等偏上
- Piper 清晰度：清晰
- 中文自然度：可用
- 导航提示适配：可用
- 警告提示适配：可用（后续可再优化音色与速度）
- 默认音色建议：可临时作为默认本地兜底音色

## 8) 本轮结论

- Stage-2.2 的关键链路已完成真实验证，且至少一方 provider（Piper）真实出音。
- Fish 本机仍缺 CLI 运行条件，当前通过结构化失败参与 fallback，不影响主链安全。
- 可进入下一步（Fish 本机可执行补齐）前，当前链路已具备可运行与可观测性。

## 9) 主线—白盒—日志一致性检查

- A 主线：统一入口真实执行，并在成功/失败路径保持语义稳定。
- B 白盒：selection/fallback/cutover/rollback 四类观察均在实跑中生成。
- C 日志：结果与 observation 已写入日志文件，可复盘。
- D 最终判断：**主线通顺，白盒一致，日志已落地**。

