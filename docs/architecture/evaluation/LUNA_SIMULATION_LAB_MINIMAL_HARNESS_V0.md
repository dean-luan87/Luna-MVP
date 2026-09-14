# Luna Simulation Lab — Minimal Harness v0

**Phase**：`Phase-Luna-Simulation-Lab-Minimal-Harness-001`  
**前置**：`Phase-Luna-Simulation-Lab-001` = **GO**  
**定位**：在 **不默认跑模型**、**不接 runtime**、**不改 routing** 的前提下，为 **两个 profile** 提供 **可复现的执行环境骨架**。

---

## 1. 覆盖 profile（仅此两个）

| profile_id | 用途 |
|------------|------|
| `developer_full` | 开发机基线；无人工资源上限 |
| `crash_recovery` | 对接 PaddleOCR **exit 139 / SIGSEGV**、batch recovery、crash sample 记录 |

**暂不纳入本 harness**：`long_run_4h`、`low_memory_2gb`、`stcm_deadline_stress` 等（变量过多，后续 phase 再加）。

---

## 2. 产物与 output_root 规范

每次 **materialize**（默认）在：

`_eval_out/simulation_lab_minimal_harness_v0/<profile_id>/`

至少落盘：

| 文件 | 说明 |
|------|------|
| `simulation_summary.json` | 含 `simulation_profile_id`、`simulation_profile_ref`、`simulation_output_root` 等 |
| `resource_report.json` | 主机资源快照（可选 psutil） |
| `audit_report.json` | 禁止项与「未改 routing」声明 |
| `notes.md` | 人工复现说明；含 **建议** batch recovery 命令（**不自动执行**） |

---

## 3. 人工触发（禁止 CI 默认）

```bash
# 基线环境上下文（不跑模型）
bash scripts/simulation/run_simulation_lab_developer_full_v0.sh

# crash_recovery 上下文（不跑模型；notes 中含建议 batch recovery 命令）
bash scripts/simulation/run_simulation_lab_crash_recovery_v0.sh
```

显式跑子命令（**必须** `--execute-child` + `--child-cmd`）：

```bash
python3 tools/evaluation/simulation/run_luna_simulation_lab_minimal_harness_v0.py \
  --workspace-root /path/to/Luna-Workspace-Min \
  --profile-id crash_recovery \
  --output-root /path/to/_eval_out/simulation_lab_minimal_harness_v0/crash_recovery \
  --execute-child \
  --child-cmd 'echo dry-run'
```

---

## 4. Compose 骨架（可选）

`scripts/simulation/docker-compose.minimal-harness.v0.yml` 为 **占位骨架**，profile `manual`；**不** 默认启动 OCR/模型服务。

---

## 5. 边界（与 Simulation Lab v0 一致）

- **不** 代表真实硬件认证、性能认证、长稳认证  
- **不** 改 CI 默认路径  
- **不** 改 runtime routing  

---

## 6. OCR 联调字段

见：`LUNA_EVALUATION_OCR_SIMULATION_LAB_CONTEXT_SCHEMA_ANNEX_V0.md`

**配置**：`configs/evaluation/simulation/luna_simulation_lab_minimal_harness_v0.example.json`  
**Verifier**：`tools/evaluation/simulation/verify_luna_simulation_lab_minimal_harness_v0.py`

**crash_recovery × PaddleOCR 合同/merge**（不自动跑 heavy）：[LUNA_SIMULATION_LAB_CRASH_RECOVERY_PADDLEOCR_BATCH_RECOVERY_V0.md](./LUNA_SIMULATION_LAB_CRASH_RECOVERY_PADDLEOCR_BATCH_RECOVERY_V0.md)

**System Health Center 治理层**（统一故障分类/恢复/mask）：[LUNA_SYSTEM_HEALTH_CENTER_GOVERNANCE_V0.md](../system_health/LUNA_SYSTEM_HEALTH_CENTER_GOVERNANCE_V0.md)
