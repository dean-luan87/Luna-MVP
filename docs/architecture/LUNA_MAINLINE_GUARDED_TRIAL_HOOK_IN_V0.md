# LUNA Guarded Trial Hook-In v0（主线候选路径挂接，默认关闭）

**Phase**：Phase-Mainline-RuntimeReadiness-004  \n
**目标**：允许将 Phase-003 的 `guarded_trial_gate_v0` / `trw_validator` / `abort_rollback_hooks` 以 **wrapper hook** 形式挂到候选主线路径，但只允许 **默认关闭短路（no-op）**。  \n
**禁止**：真实调用 Qwen/OCR provider、真实播报/播放、真实 TTS、进入下游 SceneTask/Fusion/Output、导航动作、世界模型写入、修改默认 provider 策略、修改 env 语义、删除 legacy fallback。

---

## 1. 交付物

- Hook wrapper：
  - `capabilities/runtime_readiness/yolo_guarded_trial_hook_v0.py`
  - `capabilities/runtime_readiness/ocr_guarded_trial_hook_v0.py`
  - `capabilities/runtime_readiness/qwen_voice_guarded_trial_hook_v0.py`
- Hook-in evaluation：
  - `tools/evaluate_mainline_guarded_trial_hook_in_v0.py`
  - `tools/verify_mainline_guarded_trial_hook_in_v0.py`

输出目录：`logs/mainline_guarded_trial_hook_in_004_<timestamp>/`。

---

## 2. HookResult schema（统一）

三条线统一返回：

- `enabled=false`
- `no_op=true`
- `provider_invoked=false`
- `playback_invoked=false`
- `downstream_invocation_count=0`
- `world_write_invoked=false`
- `navigation_action=null`
- `default_behavior_changed=false`

并包含 `gate_decision_ref` 与 `reason`（如 `trial_disabled` / `global_kill_switch` / `invalid_mode` / `missing_trw`）。

---

## 3. 主线挂接点（候选）

- YOLO：`capabilities/model_perception/yolo_shadow_adapter_v0.py`（shadow adapter 入口；hook 评估结果不影响逻辑）
- OCR：`capabilities/model_ocr/offline_source_policy_v0.py`（selector；hook 评估结果不影响选择）
- Qwen Voice：`capabilities/voice/output/voice_output_plane_v1.py`（submit；hook 仅作为 debug metadata 附着）

---

## 4. 测试/验证

脚本覆盖三种情形（不调用 provider）：

1. default env：全部 `disabled` → no-op  
2. global kill：`forced_disabled_by_global_kill` → no-op  
3. invalid mode：`blocked_invalid_mode` → no-op  

并产出非空 `trace/replay/whitebox` jsonl。

