# Luna Evaluation & Test Board — Overview v0

**Phase**：`Phase-Luna-Evaluation-Test-Board-001`  
**名称**：Unified Evaluation Test Board & Tiered Test Plan v0  
**定位**：**Luna 全局** 离线测评与准入治理的 **统一测试板块**；**非 OCR / PaddleOCR 专属**。OCR 为 **首批纳入对象**；后续 Vision、Voice、STCM、OCR Orchestrator、TaskChain、Risk、MidPlatform 等均按 **同一套分级等级（Level 0–9）** 接入与汇报。

**硬边界（本 phase）**：仅 **测试体系设计、文档、schema、示例配置与静态 verifier**。**不**运行 OCR / 视觉 / 语音模型；**不**接 runtime；**不**改 OCR routing；**不**替换 RapidOCR；**不**进入 MidPlatform 实装；**不**执行中台语义解释；**不**做 provider 默认切换。

**治理原则**：任一模块 **不得** 仅以「某条 phase 或某次 benchmark 跑通一次」等同于 **上线许可** 或 **shadow 默认**。**benchmark GO**、**smoke GO** 等仅表示 **该等级、该次运行的工具链或指标结论**；**shadow / release gate** 固定为 **Level 9**，且 **后置**（须先满足 Level 0–8 的必要门槛后再讨论）。

---

## 1. 测试板块要回答的问题（与等级映射）

| # | 问题域 | 说明 |
|---|--------|------|
| 1 | 可运行性 | 能否启动、加载、产出结构化结果 |
| 2 | 正确性 | 与 GT 或规则的一致性 |
| 3 | 性能 | 吞吐、延迟分位、冷/热启动 |
| 4 | 稳定性 | 崩溃、泄漏、性能退化 |
| 5 | 中断与恢复 | 取消、暂停、续跑、拆批、重试 |
| 6 | 长时间工作 | 30min–24h 量级长稳 |
| 7 | 任务类型覆盖 | 多场景、多难度下的速度与稳定性 |
| 8 | 资源治理 | CPU/GPU/内存/网络等预算与告警 |
| 9 | 时空间一致性 | deadline、过期结果丢弃或降级 |
| 10 | 审计与回放 | 失败可定位、产物可复验、trace 完整 |
| 11 | 准入闸门 | 进入 shadow / runtime / release 的条件 |

详细 **Level 0–9** 定义、GO/NO_GO 与 **准入闸门** 见：`LUNA_EVALUATION_TEST_LEVELS_AND_GATE_POLICY_V0.md`。

---

## 2. 统一测试类型矩阵（字段契约）

全 Luna 使用 **同一张逻辑矩阵**（实现上可由 `test_matrix.json` 或 registry 导出），字段至少包括：

`test_level`、`test_name`、`target_module`、`run_model`、`run_runtime`、`requires_ground_truth`、`sample_count_min`、`sample_count_max`、`duration_required`、`interrupt_required`、`recovery_required`、`stcm_required`、`output_artifacts`、`go_condition`、`no_go_condition`。

矩阵 **按模块填行**，不按 OCR 独占。

---

## 3. 文档与工具索引

| 文档 | 作用 |
|------|------|
| `LUNA_EVALUATION_TEST_LEVELS_AND_GATE_POLICY_V0.md` | Level 0–9、闸门与回归策略 |
| `LUNA_EVALUATION_TEST_ARTIFACT_STANDARD_V0.md` | 产物文件名与最小集合 |
| `LUNA_EVALUATION_INTERRUPT_AND_RECOVERY_TEST_POLICY_V0.md` | Level 5 中断/恢复策略 |
| `LUNA_EVALUATION_LONG_RUN_STABILITY_TEST_POLICY_V0.md` | Level 6 长稳策略 |
| `LUNA_EVALUATION_TASK_TYPE_PERFORMANCE_TEST_POLICY_V0.md` | Level 7 任务类型性能 |
| `LUNA_EVALUATION_CROSS_MODAL_STCM_TEST_POLICY_V0.md` | Level 8 跨模态 STCM |
| `LUNA_EVALUATION_MODULE_ADMISSION_TO_TEST_BOARD_V0.md` | 模块接入声明字段与流程 |

**配置示例**：`configs/evaluation/luna_evaluation_test_board_v0.example.json`  
**静态 verifier**：`tools/evaluation/verify_luna_evaluation_test_board_v0.py`

---

## 4. 模块汇报方式（治理语义）

每个模块在 Test Board 上必须明确：

- 当前 **已通过的最高 Level** 与 **证据路径**（verifier / 报告根目录）；  
- **未跑** 或 **阻塞** 的 Level 及原因；  
- **不允许** 用低 Level 的 GO **覆盖** 高 Level 的 NO_GO / PENDING。

---

## 5. 与既有 Evaluation Tools 的关系

本板块 **统摄** 各域已有 evaluation 文档与脚本：在 **不替代** 既有 phase ID 的前提下，为所有模块提供 **同一套等级语言** 与 **产物/准入** 基线。

---

**schema 提示**：overview 对应配置中 `schema_version: luna_evaluation_test_board_v0` 的 **board 元数据**；具体阈值在 v0 中允许 **CONDITIONAL_GO** 后由工程实测补全。
