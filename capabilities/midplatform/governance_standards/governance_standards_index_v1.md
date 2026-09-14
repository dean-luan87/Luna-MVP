# Midplatform Governance Standards Index V1

**Library Root:** `capabilities/midplatform/governance_standards/`  
**Phase:** `Phase-P1-Midplatform-Governance-Standards-Packaging-Planning-v1-001`  
**Status:** Planning only — `migration_mode = planned_only`

---

## 1. Purpose

`capabilities/midplatform/governance_standards/` 是中台治理标准库（Midplatform Governance Standards Library）。

它集中管理**怎么准入、怎么审批、怎么测试、怎么回滚、怎么写 registry、怎么判断失败**，供后续模型、能力、runtime、输出链路的统一治理复用。

它不是模型实现、不是 runtime 主程序、不是业务执行逻辑。

---

## 2. Directory Layout

```
capabilities/midplatform/governance_standards/
├── index/                  # 统一索引与版本清单
├── model_onboarding/       # 模型资产接入标准
├── runtime_boundary/       # runtime 准入与边界
├── registry_patch/         # registry overlay patch 标准
├── test_board/             # test board protected artifact 标准
├── approval_gates/         # approval gate 模板
├── negative_guards/        # negative guard 模板库
├── rollback/               # rollback / snapshot 标准
├── failure_semantics/      # GO / FAILED_NO_BOUNDARY / BLOCKED
├── templates/              # reusable phase 模板
└── case_mappings/          # 案例映射（MobileSAM 等）
├── usage_notes/              # 每条规则的 usage note 索引
├── legacy_rules/             # 历史可复用规则 inventory + mapping
├── protocol_governance/      # 协议 canonical 治理
├── file_governance/          # 文件大小与模块拆分
├── input_output_symmetry/    # 输入输出对称与 traceability
├── owner_approval/         # owner approval 独立 scope
└── validation_rules/         # validate-once reference 治理
```

---

## Legacy Reusable Rules (17 Categories)

Full inventory: `legacy_rules/legacy_reusable_governance_rules_inventory_v1.json`  
Usage notes index: `usage_notes/governance_rule_usage_notes_index_v1.md`

Categories include: test board, controlled trial, owner approval, negative guards, failure semantics, registry patch, model onboarding, runtime boundary, input/output symmetry, protocol, file governance, validate-once, evidence/candidate, rollback, artifact protection, main program separation.

**Policy:** Reuse before create. Duplicate rule creation forbidden. Standard patch required for extensions.

---

## 3. Standard Categories

| Category | 内容 |
|----------|------|
| `model_onboarding` | install lifecycle, weight, dependency repair, model-load, inference trial |
| `runtime_boundary` | runtime admission, candidate→runtime, execution prohibition |
| `registry_patch` | snapshot, diff, post-review, scoped mutation |
| `test_board` | protected artifact, process/conclusion, non-deletable |
| `approval_gates` | request/approval/readiness/execution/post-review |
| `negative_guards` | BLOCKED templates, FAILED_NO_BOUNDARY distinction |
| `rollback` | pre-snapshot, rollback readiness, cleanup forbidden scope |
| `failure_semantics` | GO, FAILED_NO_BOUNDARY_VIOLATION, BLOCKED |
| `templates` | planning, execution, registry patch, failure repair templates |
| `case_mappings` | MobileSAM and future model mappings |

---

## 4. Canonical Standard Paths

| Standard ID | Canonical Path (planned) |
|-------------|--------------------------|
| ModelAssetOnboardingGovernanceStandardV1 | `model_onboarding/model_asset_onboarding_governance_standard_v1.md` |
| ReusablePhaseTemplateMapV1 | `templates/reusable_phase_template_map_v1.json` |
| MobileSAMCaseMappingV1 | `case_mappings/mobile_sam_case_mapping_v1.json` |

完整清单见 `governance_standards_manifest_v1.json`。

---

## 5. Versioning Policy

- 标准文件版本后缀 `_v1`、`_v2` …
- Manifest `version` 字段记录库级版本
- Planning 阶段：`lifecycle_status = planned_migration`
- Execution 阶段后：`lifecycle_status = canonical`
- 历史阶段产物保留，不删除

---

## 6. Reference Policy

1. 后续阶段引用治理规则时，**优先引用** `capabilities/midplatform/governance_standards/`
2. 原始阶段产物保留为历史证据
3. 打包后的文件成为 **canonical standard**
4. 主程序不得内嵌治理规则全文，只能引用 standard id / path
5. runtime / output adapter / semantic 不得自行解释 readiness
6. registry patch 必须引用 `registry_patch/` 标准
7. test board 必须引用 `test_board/` 标准

---

## 7. Do Not Mix With Main Program

**禁止混入：**

- 模型代码、runtime 主程序、output adapter 实现
- 业务逻辑、推理脚本
- 权重文件、dataset、用户数据
- 临时 eval 输出、fact 层记录

**governance_standards 是 policy / protocol / template，不是 execution logic。**

---

## 8. Runtime Separation Policy

- runtime 只能通过 **admission gate** 读取准入结果
- 不得绕过 governance standards 自行授予 `runtime_ready`
- output adapter 不得直接消费 candidate output（须 admission）
- semantic / fact / navigation 不得直接消费 inference trial output

---

## 9. Registry Patch Standard

- planning before execution
- pre-patch snapshot required
- scoped asset only, diff required
- post-review required, rollback readiness required
- narrow trial must not promote broad readiness

（详见 `registry_patch/` 与 Model Asset Onboarding Standard）

---

## 10. Test Board Standard

- 引用 `TestBoardProtectedArtifactRuleV1`
- 每阶段 ≥6 protected 记录
- `protected / non_deletable / deletion_forbidden`
- cleanup 不得删除 test board artifact

---

## 11. Approval Gate Standard

Gate 类型：install_request, owner_approval, execution_readiness, execution, post_review, registry_patch, rollback_readiness, test_board_protection.

每 gate 定义：输入、允许、禁止、GO、FAILED_NO_BOUNDARY、BLOCKED、下游路由。

---

## 12. Failure Semantics Standard

| Decision | 含义 |
|----------|------|
| GO | 目标成功，边界干净，test board 完整 |
| FAILED_NO_BOUNDARY_VIOLATION | 目标失败但边界干净，可 repair planning |
| BLOCKED | 边界违规或关键治理失败 |

---

## 13. Reusable Phase Templates

模板类型：Planning, Request/Approval/Readiness, Execution/Post-Review, Failure Review/Repair, Registry Patch Planning/Execution, Runtime Boundary Planning.

详见 `templates/reusable_phase_template_map_v1.json`（planned canonical path）。

---

## 14. Case Mappings

- `case_mappings/mobile_sam_case_mapping_v1.json` — MobileSAM P1 全链事实映射
- 未来模型 onboarding 可追加同类 mapping

---

## 15. Future Migration / Packaging Execution Route

**Recommended next phase:**

`Phase-P1-Midplatform-Governance-Standards-Packaging-Execution-And-Post-Review-v1-001`

允许：创建子目录、复制/迁移标准文件、生成 manifest/index/path mapping、post-review。  
禁止：修改主程序、执行 runtime、删除原始证据。

---

*End of Governance Standards Index V1 (Planning)*
