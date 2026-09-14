# Reusable Governance Standard Packaging Plan V1

**Phase:** `Phase-P1-Midplatform-Governance-Standards-Packaging-Planning-v1-001`  
**Mode:** Planning only — no file move, no copy, no delete

---

## 1. Objective

将当前已沉淀的 **Model Asset Onboarding Governance Standard V1** 及关联模板、案例映射，规划打包进集中式中台治理标准库：

`capabilities/midplatform/governance_standards/`

---

## 2. Library Positioning

`governance_standards/` 是 **Luna 中台可复用治理标准库（制度库）**，不是某个模型的规则包。

| 存放 | 不存放 |
|------|--------|
| 可复用治理规则 | 模型代码 |
| 生命周期流程 | runtime 主程序 |
| approval gate 模板 | output adapter 实现 |
| negative guard 模板 | 业务逻辑 / 推理脚本 |
| readiness / registry patch 标准 | 权重 / dataset / 用户数据 |
| test board / rollback / failure semantics | 临时 eval / fact 记录 |

---

## 3. Planned Subdirectories

1. `index/` — 统一索引、版本、引用关系  
2. `model_onboarding/` — Model Asset Onboarding Standard V1  
3. `runtime_boundary/` — runtime admission gate  
4. `registry_patch/` — overlay patch pattern  
5. `test_board/` — protected artifact 规范  
6. `approval_gates/` — gate 模板库  
7. `negative_guards/` — guard pattern 库  
8. `rollback/` — snapshot / rollback  
9. `failure_semantics/` — GO / FAILED_NO_BOUNDARY / BLOCKED  
10. `templates/` — reusable phase templates  
11. `case_mappings/` — MobileSAM 等案例映射  
12. `usage_notes/` — 规则 usage note 索引  
13. `legacy_rules/` — 历史可复用规则 inventory  
14. `protocol_governance/` — 协议 canonical 治理  
15. `file_governance/` — 文件大小与拆分  
16. `input_output_symmetry/` — 输入输出对称  
17. `owner_approval/` — owner approval scope  
18. `validation_rules/` — validate-once reference  

---

## 3b. Legacy Reusable Rules Inclusion

17 类历史可复用规则已登记至 `legacy_rules/legacy_reusable_governance_rules_inventory_v1.json`，每条含 `when_to_use` / `how_to_use` / `forbidden_usage`。

Reuse policy: 先查制度库 → 有则引用 → 无则 standardization → 扩展则 standard patch。

---

## 4. Planned Migrations (copy in execution phase)

| # | Source | Canonical Target |
|---|--------|------------------|
| 1 | `model_asset_onboarding_governance_standard/model_asset_onboarding_governance_standard_v1.md` | `governance_standards/model_onboarding/...` |
| 2 | `.../model_asset_onboarding_governance_standard_types_v1.py` | `governance_standards/model_onboarding/...` |
| 3 | `.../model_asset_onboarding_governance_standard_registry_v1.py` | `governance_standards/model_onboarding/...` |
| 4 | `.../review_model_asset_onboarding_governance_standard_v1.py` | `governance_standards/model_onboarding/...` |
| 5 | `_tmp_eval_out/.../reusable_phase_template_map_v1.json` | `governance_standards/templates/...` |
| 6 | `_tmp_eval_out/.../mobile_sam_case_mapping_v1.json` | `governance_standards/case_mappings/...` |

**本阶段不执行复制。** 原始路径保留为历史证据。

---

## 5. Manifest & Index

- `governance_standards_manifest_v1.json` — 标准清单（planning 版）
- `governance_standards_index_v1.md` — 人类可读索引

---

## 6. Main Program Separation

- governance_standards **不得** import 主程序 runtime  
- 主程序 runtime **不得**依赖 governance test executor  
- runtime 只读 admission gate 输出  
- governance 不调用模型、不下载权重、不写 fact、不触发 navigation/speech  

---

## 7. Reference Handoff

后续所有 phase 应：

```python
# Prefer canonical path after packaging execution:
# capabilities/midplatform/governance_standards/<category>/<standard>
```

Planning 阶段可继续引用原始路径 + manifest 中的 `source_path`。

---

## 8. Next Phase

**`Phase-P1-Midplatform-Governance-Standards-Packaging-Execution-And-Post-Review-v1-001`**

- 创建子目录  
- 复制/迁移 6 项标准产物  
- 生成 path mapping + post-review  
- 不修改主程序、不 runtime、不删证据  

---

*End of Packaging Plan V1*
