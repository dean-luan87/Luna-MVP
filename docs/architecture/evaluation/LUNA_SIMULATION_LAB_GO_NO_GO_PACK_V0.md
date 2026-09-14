# Luna Simulation Lab — GO / NO-GO Pack v0

**Phase**：`Phase-Luna-Simulation-Lab-001`

---

## GO（本 phase 静态范围）

- Overview、profile standard、resource、input、fault、STCM 文档 **齐全**。  
- `luna_simulation_lab_profiles_v0.example.json` **存在**，`profiles.length >= 10`，且覆盖 **developer_full、low_memory、low_cpu、offline、network_unstable、long_run、crash_recovery、stcm_deadline_stress** 等 **必选 profile 族**。  
- 每个 profile 含 **`resource_limits`、`expected_degradation`、`required_artifacts`**。  
- `README.md` 含 **Simulation Lab 索引**。  
- 文档 **明确** Mac Lab **不等同真实硬件**；**真实硬件验证仍为后置必须环节**。  
- 静态 **`verify_luna_simulation_lab_v0.py` verdict = GO**。

---

## CONDITIONAL_GO

- 主体文档与 profile **齐全**，但 **Dockerfile / compose / harness 脚本** 尚未合入（允许在后续仓库变更中补齐）。  
- 部分 profile 的 **数值阈值**（如延迟 ms、丢包率）标为 **TBD**，已在 `luna_simulation_lab_gap_report.json` 登记。

---

## NO_GO

- **缺** 资源模拟、故障/中断模拟、STCM 模拟或 **long-run** profile **族** 的 **设计与配置**。  
- 文档将 **Mac 模拟** 表述为 **真实硬件等价** 或 **可替代认证**。  
- **README 缺索引**。  
- 将 **默认 routing / 默认 provider** 的 **非法变更** 写为允许项。

---

## System Health Center

故障分类与恢复决策统一契约见 [LUNA_SYSTEM_HEALTH_CENTER_GOVERNANCE_V0.md](../system_health/LUNA_SYSTEM_HEALTH_CENTER_GOVERNANCE_V0.md)（Simulation Lab 制造故障 → Health Center 分类决策 → Benchmark 记录）。

---

## 与 Evaluation Test Board 的一句话关系

**Test Board = 测什么；Simulation Lab = 在什么模拟环境下测。**
