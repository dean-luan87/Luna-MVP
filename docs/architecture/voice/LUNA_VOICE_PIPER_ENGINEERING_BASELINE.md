# Luna Voice Piper Engineering Baseline

## 1. 定位

在 Fish 未本机跑通期间，Piper 作为当前可执行语音主链。  
本基线文档用于固化工程状态，保证后续迭代有统一口径。

## 2. 当前正式工程配置

- `active_provider: piper`
- `provider_order: [piper]`
- `fallback_provider: piper`（仅 Piper）
- `local_runtime.piper.enabled: false`
- `local_runtime.piper.enabled: true`

说明：保持统一入口与链路结构不变，仅将当前可执行 provider 切到 Piper。

## 3. preset 工程化落点

已将现有四个 preset 参数映射到 Piper 参数（模型、语速、句停、音量）：

- `calm_female_v1`
- `navigation_clear_v1`
- `warning_strong_v1`
- `gentle_companion_v1`

参数落点文件：`capabilities/voice/config/voice_presets.yaml`  
（保留文件名以避免影响既有引用，内容已切换为 Piper 当前工程参数）

## 4. 一键工程验证

脚本：`tools/run_piper_engineering_pack.py`

覆盖场景：
- 导航（2条）
- 警告（2条）
- 普通反馈（3条）

输出：
- 结构化结果：`logs/piper_engineering_pack.json`
- 音频产物：`logs/piper_engineering_pack/*.wav`

## 5. 已知限制

- 当前仍以单一 Piper 音色为主，情绪层次上限有限。
- Fish 尚未进入可执行成功态，不参与主链质量对照。
- 输出治理细粒度白盒接线仍在后续阶段。

## 6. Fish 交接条件（保持）

当且仅当以下条件满足才切回 Fish 主链：

1. Fish 本机真实出音通过；
2. Fish 统一入口成功链可复现；
3. Fish 失败 -> Piper fallback 不退化；
4. Fish/Piper 全失败 -> legacy rollback 不退化。

## 7. 主线—白盒—日志一致性检查

- A 主线：Piper 主链已可稳定执行。
- B 白盒：当前 observation 链持续可用（selection/cutover/fallback/rollback）。
- C 日志：工程验证结果与音频产物已落地。
- D 最终判断：**主线通顺，白盒一致，日志已落地**。

