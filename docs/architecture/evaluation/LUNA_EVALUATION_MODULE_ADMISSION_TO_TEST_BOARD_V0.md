# Luna Evaluation & Test Board — Module Admission v0

**Phase**：`Phase-Luna-Evaluation-Test-Board-001`  
**定位**：模块进入 **Luna Evaluation & Test Board** 前的 **接入声明**；**Luna 全局**；**非 OCR 专属**。

---

## 1. 必须声明的字段（与 example JSON 对齐）

每个模块提交一份 **admission 记录**（可 JSON 或注册表中的一行），至少包含：

| 字段 | 说明 |
|------|------|
| `module_name` | 模块唯一名 |
| `capability_type` | 能力类型（ocr / vision / voice / stcm / taskchain / …） |
| `provider_name` | 若适用（如某 OCR provider） |
| `test_levels_supported` | 声明计划支持的 Level 子集 |
| `input_contract` | 输入合同路径或 schema id |
| `output_contract` | 输出合同路径或 schema id |
| `audit_contract` | 审计字段与禁止项 |
| `resource_budget` | CPU/内存/GPU/时长上限 |
| `timeout_policy` | 与 STCM / 本地超时的关系 |
| `interrupt_policy` | Level 5 语义对齐声明 |
| `recovery_policy` | Level 4/5 续跑与幂等声明 |
| `verifier_path` | 静态或运行后置 verifier 脚本路径 |
| `release_gate_required` | 是否 **强制** 经过 Level 9（默认 true） |

配置中 `module_admission_required_fields` 列出 **最小键集合**；`release_gate_required` 可在扩展表中单独要求。

---

## 2. 接入流程（摘要）

1. 补齐 Level 0 合同与静态 verifier。  
2. 在 `test_matrix.json` 注册首批用例行。  
3. 逐级提升 Level，**每级** 保留 `output_root` 与 verifier 报告。  
4. 未达标 Level **阻塞** shadow/release（Level 9）讨论。

---

## 3. OCR 首批（叙述）

OCR（含 PaddleOCR 受控试验线）作为 **首个** 完整走通 0–4 映射的候选；**不** 授予「其他模块可省略低 Level」的豁免。

---

**非 OCR 专属声明**：Vision、Voice、STCM 等须 **独立** 提交 admission 记录。
