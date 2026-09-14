# Luna Evaluation OCR — Simulation Lab Context Schema Annex v0

**Phase**：`Phase-Luna-Simulation-Lab-Minimal-Harness-001`（附录；适用于 OCR evaluation 子工具与 batch recovery 产物对齐）  
**定位**：在 OCR 评测 / batch recovery 的 `test_summary.json` 或 `simulation_summary.json` 中 **可选挂载** Simulation Lab 上下文字段，便于 Test Board Level 4 与 Simulation Lab profile 联合筛选。

---

## 1. 字段定义

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `simulation_profile_id` | string | 推荐 | 如 `developer_full`、`crash_recovery` |
| `simulation_profile_ref` | string | 推荐 | profiles JSON 路径 + `#profile_id=` |
| `simulation_output_root` | string | 推荐 | 本次 Simulation Lab materialize 根目录 |
| `crash_recovery_enabled` | boolean | 推荐 | 是否启用 crash_recovery 类 fault 注入策略 |
| `exit_code` | int \| null | 可选 | 子进程 / batch 退出码（如 `-11`） |
| `signal` | int \| null | 可选 | Unix signal（如 `11` = SIGSEGV） |
| `rss_mb` | number \| null | 可选 | 峰值 RSS（MB） |
| `batch_size` | int \| null | 可选 | batch recovery 拆批大小 |
| `crash_sample_ref` | string \| null | 可选 | crash report 路径或 `labeled_XXX` 样本 id |

---

## 2. 示例（simulation_summary.json 片段）

```json
{
  "schema": "luna_simulation_lab_run_summary_v0",
  "simulation_profile_id": "crash_recovery",
  "simulation_profile_ref": "configs/evaluation/simulation/luna_simulation_lab_profiles_v0.example.json#profile_id=crash_recovery",
  "simulation_output_root": "/path/to/_eval_out/simulation_lab_minimal_harness_v0/crash_recovery",
  "crash_recovery_enabled": true,
  "exit_code": null,
  "signal": null,
  "rss_mb": null,
  "batch_size": null,
  "crash_sample_ref": null,
  "run_model": false
}
```

子命令跑完后，由 harness **或** batch recovery merge 填入 `exit_code` / `signal` / `batch_size` / `crash_sample_ref`。

---

## 3. 与 batch recovery 的关系

`run_paddleocr_labeled_set_batch_recovery_v0.py` 的 `paddleocr_labeled_set_batch_crash_report.json` 提供 crash 细节；本附录字段用于 **在 Simulation Lab 层** 做索引，**不** 替代 crash report。

---

## 4. 禁止语义

- 不得因挂载 `simulation_profile_id=developer_full` 即宣称 **硬件认证通过**  
- 不得将 **未跑模型** 的 materialize（`run_model: false`）记为 Level 4 **GO**
