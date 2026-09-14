# Luna Voice Stage-2.1 变更清单（唯一入口 + 最小桥接 + rollback）

## 1) 新增 runtime / observation 文件

- `capabilities/voice/runtime/tts_unified_entry.py`
- `capabilities/voice/runtime/tts_cutover_state.py`
- `capabilities/voice/observations/tts_cutover_observation.py`
- `capabilities/voice/observations/tts_rollback_observation.py`

## 2) 配置新增 cutover 字段

更新：
- `capabilities/voice/config/voice_tts_config.yaml`

新增：
- `cutover.enabled`
- `cutover.mode`
- `cutover.rollback_to_legacy_on_failure`
- `cutover.rollback_on_selector_failure`
- `cutover.rollback_on_provider_chain_failure`
- `cutover.observe_rollbacks`
- `legacy_fallback.enabled`
- `legacy_fallback.mode`
- `legacy_fallback.reason_tag`

## 3) selector / fallback 收敛关系

- `tts_provider_selector.py`：
  - 新增 `execute_provider_chain()` 作为唯一公开入口
- `tts_fallback_manager.py`：
  - 标注 internal，仅作为 selector 的内部机制
  - 保留兼容别名供既有测试使用

## 4) 唯一桥接点

主链仅新增一个集中桥接提交函数：
- `main.py`：`_submit_tts_via_unified_entry()`

`_speak_safely` 与 `_handle_immediate_risk` 均通过该函数提交，避免散点改造。

## 5) 哪些旧文件没动

- `core/speech_gate.py`（语义未改）
- `core/audio_worker.py`（语义未改）

## 6) 为什么本轮不进一步重构

本轮目标是最小桥接，不是全链重构：
- 不改 gate/execution 底座语义
- 不删 legacy
- 不扩展 provider 参数体系
- 不接云端模型

## 7) 最小测试新增

- `tests/test_tts_unified_entry.py`
  - 新链成功
  - provider chain 失败回滚 legacy
  - cutover 关闭走 legacy

