# Luna Voice Piper Engineering Signoff

## 1. 当前结论

`Piper` 已具备当前版本**默认工程主链资格**，本阶段签收通过。

## 2. 通过原因

当前签收依据如下：

- 配置主权已切换到 `Piper`（默认 provider 已切换、provider 顺序已固化）。
- 统一入口链路有效（经 `tts_unified_entry` 真实执行，不是直调 demo）。
- 工程样本 `7/7` 成功，且全部为 `provider_name=piper`。
- latency 区间已有真实记录（约 `585ms~892ms`）。
- fallback / rollback 回归验证通过，链路不退化。
- 日志与音频证据已落地，可追溯复核。

## 3. 当前默认运行口径

- 默认 provider：`piper`
- Fish 状态：`pending`（未接管主链）
- legacy 状态：`rollback safety net`（保留兜底）

## 4. 当前不做的事情

本次签收明确不做：

- 不因 Piper 通过而删除 legacy。
- 不因 Fish 未跑通而阻塞后续白盒流程接入。
- 不在本轮扩展 ASR / UI / 云端链路。

## 5. Fish 接管条件

Fish 仅在满足以下条件时才具备接管默认主链资格：

1. 本机真实出音通过；
2. 统一入口成功路径稳定复现；
3. Fish 失败时 fallback / rollback 不退化；
4. 第一轮 preset 对照评测完成；
5. 在目标场景上达到“明确优于或明确更适配”Piper 的结论。

## 6. 后续下一步

后续进入语音白盒流程接入时，先以 `provider_name=piper` 作为当前主链样本进行观测链组织。  
Fish 的工程恢复与接管评估作为并行后续任务，不影响当前主链推进。

## 7. 证据引用

- `docs/architecture/voice/LUNA_VOICE_PIPER_ENGINEERING_BASELINE.md`
- `docs/architecture/voice/LUNA_VOICE_PIPER_ENGINEERING_GATE_CHECKLIST.md`
- `logs/piper_engineering_pack.json`
- `logs/piper_engineering_pack/*.wav`
- `logs/piper_temp_default_validation.json`
- `logs/piper_temp_default_observations.jsonl`
- `logs/voice_stage22_validation_results.json`

## 8. 主线—白盒—日志一致性检查

- A 主线：Piper 已形成稳定默认工程主链。
- B 白盒：当前链路 observation 可用于后续流程接入，且本轮未越界扩展。
- C 日志：验收证据可回放、可追溯、可复核。
- D 最终判断：**主线通顺，白盒一致，日志已落地**。

