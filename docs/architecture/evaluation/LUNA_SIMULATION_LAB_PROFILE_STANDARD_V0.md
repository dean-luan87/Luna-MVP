# Luna Simulation Lab — Profile Standard v0

**Phase**：`Phase-Luna-Simulation-Lab-001`  
**定位**：定义 **simulation profile** 的 **冻结字段**；适用于 OCR、Vision、Voice、STCM、TaskChain 等模块在 Lab 中的 **一次运行上下文**。

**非真实硬件等价**：profile 仅描述 **模拟意图** 与 **期望退化**；**不** 宣称与某款量产机 1:1 一致。

---

## 1. 每个 profile 必须包含的字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `profile_id` | string | 唯一标识，如 `low_memory_4gb` |
| `description` | string | 人可读目标与边界 |
| `resource_limits` | object | `cpu_cores`、`memory_mb`、`gpu_available`、可选 `disk_io_class` 等 |
| `network_policy` | object | `mode`：`online` / `offline` / `unstable`；可选 `latency_ms`、`packet_loss` |
| `input_sources` | object | 图像序列、视频、OCR manifest、音频 manifest、GPS/anchor trace 等 **引用或 null** |
| `fault_injection` | object | 布尔开关：provider timeout、subprocess kill、stale result、exit 139 模拟等 |
| `stcm_policy` | object | `deadline_class`、`expired_outputs_cannot_drive_action` 等 |
| `expected_degradation` | array | 允许的退化形态（如 async-only、cache 优先） |
| `forbidden_runtime_changes` | array | **禁止** 在 profile 下做的变更（如改默认 routing、替换默认 provider） |
| `required_artifacts` | array | 本 profile 运行结束后 **最少** 应落盘的文件名 |

---

## 2. 与 Test Board 产物的对齐

若某次运行声明 `simulation_profile_id`，则应在 `test_summary.json`（或别名映射）中 **并列** `test_board_level` 与 `simulation_profile_id`，便于矩阵筛选。

---

## 3. 最小 `required_artifacts`（全 profile 基线）

建议至少包含：

- `simulation_summary.json`  
- `resource_report.json`  
- `audit_report.json`  
- `verifier_report.json`  

涉及 STCM 应力时，应 **追加** `stcm_event_trace.jsonl`（或与 Test Board STCM 产物对齐的别名映射）。

---

## 4. 禁止项（写入 `forbidden_runtime_changes` 的推荐默认值）

- 修改主线 **默认** OCR routing 或替换 **默认** RapidOCR。  
- 静默打开 **未授权** 的网络 OCR / VLM。  
- 将 **模拟通过** 写为 **真实硬件认证通过**。

**不等同真实硬件；真实硬件验证仍为后置必须环节。**
