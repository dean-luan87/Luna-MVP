# LUNA Guarded Trial Wiring Path 测试矩阵 v0

**Phase**：Phase-Mainline-RuntimeReadiness-003

---

## 自动化静态校验

| ID | 检查项 | 工具 |
|----|--------|------|
| A–N | 产物文件、三 trial、global kill、默认关、禁止 downstream/world、无效模式、TRW/hooks/wiring、NO_GO verdict | `tools/verify_mainline_guarded_trial_wiring_path_v0.py` |

运行示例：

```bash
cd /path/to/Luna-Core
python3 tools/evaluate_mainline_guarded_trial_wiring_path_v0.py \
  --output-root logs/mainline_guarded_trial_wiring_path_003_<timestamp>
python3 tools/verify_mainline_guarded_trial_wiring_path_v0.py \
  --output-root logs/mainline_guarded_trial_wiring_path_003_<timestamp> \
  --repo-root /path/to/Luna-Core
```

---

## 手动 / 后续集成测试（本 Phase 不执行）

| 场景 | 期望 |
|------|------|
| 默认 env | 三 trial `disabled`，无 provider/playback/downstream |
| `LUNA_DISABLE_ALL_GUARDED_TRIALS=1` + 分项全开 | 仍 `forced_disabled_by_global_kill` |
| 无效 `LUNA_YOLO_TRIAL_MODE` | `blocked_invalid_mode` |
| TRW 缺 `request_id` | validator `valid=false` |

探测结果已写入 `mainline_guarded_trial_gate_decisions.json` 的 `invalid_mode_probe` / `global_kill_probe`。
