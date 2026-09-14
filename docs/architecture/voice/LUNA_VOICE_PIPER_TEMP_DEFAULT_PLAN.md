# Luna Voice Piper Temp Default Plan

## 1. 当前定位

当前阶段 Fish 尚未完成本机可用链路收口（模型下载/运行环境仍在进行），因此本轮将 `Piper` 作为**临时正式本地 TTS 主链**。  
该方案用于保证 Luna 在 Stage-2.3 前半段具备稳定可用、可观察、可回退的语音输出能力。

## 2. 当前调用方式（统一入口）

- 入口：`capabilities/voice/runtime/tts_unified_entry.py`
- 选择层：`tts_provider_selector`
- provider chain：`piper only`（本轮受控临时配置）
- 验证方式：通过 `tools/validate_piper_temp_default_plan.py` 走统一入口触发，不直调 provider 作为正式路径
- observation：
  - `ProviderSelectionObservation` 正常
  - `TTSCutoverObservation` 正常
  - 在本轮主路径下 `fallback/rollback` 未触发（因为 Piper 主选成功）

相关结果：
- `logs/piper_temp_default_validation.json`
- `logs/piper_temp_default_observations.jsonl`

## 3. 当前临时默认方案（最小可用）

### 3.1 运行参数基线（Piper）

- executable: `/Users/luanlei/Library/Python/3.9/bin/piper`
- model: `capabilities/voice/models/piper/zh_CN-huayan-medium.onnx`
- timeout: `6000ms`
- provider order: `["piper"]`
- active provider: `piper`
- fallback: enabled（保留）

### 3.2 preset 参数（首轮）

- `calm_female_v1`：
  - `length_scale=1.00`
  - `sentence_silence=0.15`
  - `noise_scale=0.667`
  - `noise_w_scale=0.8`
  - `volume=1.0`
- `navigation_clear_v1`：
  - `length_scale=0.92`
  - `sentence_silence=0.12`
  - `volume=1.05`
- `warning_strong_v1`：
  - `length_scale=0.86`
  - `sentence_silence=0.08`
  - `volume=1.12`
- `gentle_companion_v1`：
  - `length_scale=1.05`
  - `sentence_silence=0.18`
  - `volume=0.98`

## 4. 场景化建议（临时）

- 导航提示：优先 `navigation_clear_v1`（更短促、清晰）
- 安全警告：优先 `warning_strong_v1`（节奏更紧、响度更高）
- 普通反馈：优先 `calm_female_v1`，必要时 `gentle_companion_v1`

## 5. 三类文本验证摘要（真实出音）

- 导航：
  - “前方十米右转。”
  - “请沿当前方向继续前进。”
- 警告：
  - “前方靠近水边，请停一下。”
  - “前面人多，请减速靠右。”
- 反馈：
  - “已开始导航。”
  - “我没听清，请再说一次。”
  - “已暂停当前任务。”

结果：
- 7/7 成功，均为 `provider_chain` 路径，provider 为 `piper`
- 典型延迟范围约 `613ms ~ 1203ms`
- 音频文件落地于：`logs/piper_temp_plan/`

## 6. 当前已知局限

- 真人感和情绪层次有限，仍偏“稳定播报音”
- 警告力度主要依赖节奏/音量参数，表达上限有限
- 目前为临时阶段参数，不是最终音色工程定稿

## 7. Fish 交接条件（后续）

Fish 仅在满足以下条件后接管默认主链：

1. 本机 Fish 真实出音可复现；
2. Fish 成功路径可通过统一入口稳定命中；
3. Fish 失败时 `Fish->Piper fallback` 不退化；
4. `provider chain->legacy rollback` 不退化；
5. 首轮 Fish/Piper 对照听感结论确认 Fish 在默认场景不劣于 Piper。

## 8. 主线—白盒—日志一致性检查

- A 主线：统一入口 `tts_unified_entry` 路径可用，Piper 已可作为临时主链。
- B 白盒：selection/cutover observation 在实跑中生成；fallback/rollback 由回归脚本验证未退化。
- C 日志：结果与音频产物落地在 `logs/piper_temp_default_validation.json` 与 `logs/piper_temp_plan/`。
- D 最终判断：**主线通顺，白盒一致，日志已落地**。

