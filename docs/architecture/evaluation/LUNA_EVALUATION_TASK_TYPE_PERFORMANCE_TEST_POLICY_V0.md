# Luna Evaluation & Test Board — Task-Type & Scenario Performance Policy v0

**Phase**：`Phase-Luna-Evaluation-Test-Board-001`  
**Level**：7  
**定位**：**Luna 全局** 分任务类型/场景的性能与成功率矩阵；**非 OCR 专属**。

---

## 1. 产出（必须可计算）

| 产物 | 说明 |
|------|------|
| `task_type_matrix.json` | 任务类型 × 运行结果 × 资源快照索引 |
| `latency_by_task_type` | 聚合在 `metrics.json` 或独立切片 |
| `success_rate_by_task_type` | 同上 |
| `resource_by_task_type` | CPU/GPU/内存峰值或积分 |
| `failure_type_by_task_type` | 与 `error_report.json` 对齐的分类 |

---

## 2. OCR 任务类型（示例，非穷尽）

`plain_text`、`signboard`、`product_label`、`medicine_label`、`poster`、`multi_region_notice`、`artistic_text`、`small_text`、`low_light`、`moving_camera` 等；与既有 OCR taxonomy 文档 **对齐引用**，不在此重复冻结字段。

---

## 3. Vision 任务类型（示例）

`obstacle_detection`、`pedestrian_approach`、`stair_detection`、`traffic_light`、`doorway`、`elevator_button`、`sign_detection` 等。

---

## 4. Voice 任务类型（示例）

`immediate_safety_notice`、`delayed_task_notice`、`long_explanation`、`interruptible_speech`、`expired_notice_drop` 等。

---

## 5. GO 条件（摘要）

各声明的任务类型 **均有** 可计算指标行；**缺口** 须在 `notes.md` 与 `test_matrix.json` 中显式标为 `not_run` 或 `deferred`，不得伪称为全量 GO。

---

**非 OCR 专属声明**：本 Level 为 **跨模态** 性能治理基线；OCR 仅为其中一行来源。
