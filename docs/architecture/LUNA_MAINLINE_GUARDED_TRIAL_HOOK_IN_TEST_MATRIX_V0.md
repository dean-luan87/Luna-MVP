# LUNA Guarded Trial Hook-In 测试矩阵 v0

**Phase**：Phase-Mainline-RuntimeReadiness-004

---

## 自动化静态验证

| 检查项 | 工具 |
|--------|------|
| 产物存在、三 hook、默认 no-op、global kill 生效、invalid mode 阻断、side effect 全 false、trace/replay/whitebox 非空 | `tools/verify_mainline_guarded_trial_hook_in_v0.py` |

---

## 必测场景（本 Phase 不触发 provider）

1. **default env**：所有 trial `disabled`，hook 全 `no_op=true`  
2. **global kill**：`LUNA_DISABLE_ALL_GUARDED_TRIALS=1` → `forced_disabled_by_global_kill`  
3. **invalid mode**：例如 `LUNA_YOLO_TRIAL_MODE=not_a_real_mode` → `blocked_invalid_mode`  

运行：

```bash
cd /path/to/Luna-Core
python3 tools/evaluate_mainline_guarded_trial_hook_in_v0.py \
  --output-root logs/mainline_guarded_trial_hook_in_004_<timestamp>
python3 tools/verify_mainline_guarded_trial_hook_in_v0.py \
  --output-root logs/mainline_guarded_trial_hook_in_004_<timestamp>
```

