# Luna Voice Stage-2.1：唯一入口收敛与 Cutover 最小桥接方案

## 1. 为什么需要唯一入口

Stage-2 完成了 Fish/Piper provider 链，但若外部可直接调用 Fish/Piper/fallback manager，会形成并行入口、不可审计与治理漂移。  
因此 Stage-2.1 强制收敛为：

- provider chain 唯一公开入口：`tts_provider_selector.execute_provider_chain`
- fallback manager：内部机制，不作为外部调用入口

## 2. selector 为什么必须收敛

- 主权一致：provider 选择与 fallback 必须由系统统一控制
- 可观察：selection/fallback/rollback 需要统一留痕
- 可回滚：统一入口才有可靠 rollback 策略

## 3. cutover 只改一处原则

本轮主链桥接只改一处集中入口：`main.py` 的统一提交函数 `_submit_tts_via_unified_entry()`。  
其余逻辑（`_speak_safely`、`_handle_immediate_risk`）都通过该函数间接提交，避免散点接线。

## 4. rollback 策略

配置化开关（`voice_tts_config.yaml`）：

- `cutover.enabled`
- `cutover.rollback_to_legacy_on_failure`
- `cutover.rollback_on_selector_failure`
- `cutover.rollback_on_provider_chain_failure`
- `legacy_fallback.enabled`

触发后行为：
- selector/provider chain 失败 → 按配置回滚 legacy 提交
- rollback 必须记录 observation，不允许静默切换

## 5. 旧底座不动原则

`core/speech_gate.py` 与 `core/audio_worker.py` 语义保持不变：

- speech_gate 继续负责 gate（占用/冷却/去重）
- audio_worker 继续负责异步执行底座

Stage-2.1 不把它们改成 provider 控制器。

## 6. 为什么本轮不删 legacy

Cutover 的正确顺序是：
1) 唯一入口  
2) 最小桥接  
3) rollback 可观察  
4) 再进入 legacy 清理  

因此本轮保留 legacy 模块，优先保证可运行与可回滚。

