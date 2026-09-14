# Model Asset Onboarding Governance Standard V1

**Standard ID:** `ModelAssetOnboardingGovernanceStandardV1`  
**Phase Reference:** `Phase-P1-Controlled-Install-Governance-Standardization-v1-001`  
**Case Basis:** MobileSAM P1 controlled install → weight → model-load → inference trial chain  
**Template Ref:** `ControlledTrialGovernanceLifecycleTemplateV1`  
**Test Board Ref:** `TestBoardProtectedArtifactRuleV1`

---

## 1. Purpose / 定位

本标准将 MobileSAM P1 完整资产接入闭环抽象为**通用模型资产接入治理规范**，供后续新模型 onboarding 复用。

- **做什么：** 规范化生命周期、readiness 状态机、审批 gate、安装策略、源码/权重/依赖修复/试载/推理试跑/registry patch/失败语义/负向 guard/test board 保护产物要求。
- **不做什么：** 本标准文档本身不执行安装、不下载权重、不 import、不 model load、不 inference、不 runtime、不写 registry overlay、不写 fact、不进入 output adapter / 语义层。

---

## 2. Scope / 适用范围

适用于 Luna P1 受控模型资产接入全链：

1. Package / source install planning & execution  
2. Repository verification / commit pin / license / dependency review  
3. Code-only source install  
4. Weight download / hash / storage governance  
5. Dependency gap repair  
6. Model-load trial  
7. Inference trial (candidate-only)  
8. Registry overlay patch  
9. Runtime / output adapter / semantic / fact / navigation 边界排除  

---

## 3. Non-goals / 非目标

- 不授予 `runtime_ready`、`output_adapter_ready`、`semantic_layer_ready`、`commercial_runtime_approved`
- 不把 `model_load_verified` 解释为 `inference_ready`
- 不把 `inference_trial_verified` 解释为 broad `inference_ready` 或 `runtime_ready`
- 不允许 candidate output 进入 fact / runtime / output adapter / semantic / navigation
- 不在标准化阶段执行任何真实安装、下载、加载或推理

---

## 4. Lifecycle State Machine

```
registry_planned
  → probe_observed
  → install_required
  → [package_install_partial | source_install_required]
  → code_only_ready
  → weight_download_ready
  → code_and_weight_ready
  → model_load_requested
  → model_load_verified
  → inference_trial_requested
  → inference_trial_verified
  → runtime_boundary_planned
  → (reserved: runtime_ready / output_adapter_ready / semantic_layer_ready / commercial_runtime_approved)
```

**27 lifecycle stages（抽象阶段）：**

asset_registry_planning → local_availability_probe → package_install_planning → package_install_execution → source_install_planning → repository_verification → commit_pin → license_review → dependency_review → code_only_source_install → registry_patch_code_only_readiness → weight_download_request_approval_readiness → weight_download_execution → weight_registry_patch → model_load_request_approval_readiness → model_load_execution → dependency_gap_repair → dependency_install_request_approval_execution → model_load_retry → model_load_registry_patch → inference_trial_request_approval_readiness → inference_trial_execution → inference_trial_registry_patch → runtime_boundary_planning → output_adapter_boundary_planning → semantic_fact_navigation_exclusion → commercial_runtime_exclusion

---

## 5. Readiness Levels

| Level | 含义 | 不得等同于 |
|-------|------|-----------|
| `registry_planned` | 资产登记规划完成 | install ready |
| `probe_observed` | 本地探测完成 | install success |
| `install_required` | 需安装 | code ready |
| `package_install_partial` | PyPI 部分可用 | source ready |
| `source_install_required` | 需源码安装 | weight ready |
| `code_only_ready` | 代码可 import root 就绪 | weight ready |
| `weight_download_ready` | 权重下载审批就绪 | model load ready |
| `code_and_weight_ready` | 代码+权重就绪 | model load verified |
| `model_load_requested` | 已请求 model-load trial | model load verified |
| `model_load_verified` | checkpoint 加载验证通过 | inference ready |
| `inference_trial_requested` | 已请求 inference trial | inference verified |
| `inference_trial_verified` | 单次受控推理试跑通过 | broad inference_ready / runtime_ready |
| `runtime_boundary_planned` | runtime 边界已规划 | runtime_ready |
| `runtime_ready` | **仅预留** | 本标准不得直接授予 |
| `output_adapter_ready` | **仅预留** | 本标准不得直接授予 |
| `semantic_layer_ready` | **仅预留** | 本标准不得直接授予 |
| `commercial_runtime_approved` | **仅预留** | 本标准不得直接授予 |

**关键不等式：**

- `code_only_ready` ≠ weight ready  
- `code_and_weight_ready` ≠ model load ready  
- `model_load_verified` ≠ inference ready  
- `inference_trial_verified` ≠ broad `inference_ready`  
- `inference_trial_verified` ≠ `runtime_ready`  
- 单次 inference trial **不得**自动授予 `runtime_ready`

---

## 6. Approval Gates

### 6.1 install_request_gate

| 维度 | 规则 |
|------|------|
| 输入 | 资产 ID、安装路由候选（package / source）、owner 上下文 |
| 允许 | 记录 install intent、选择路由、生成 planning artifact |
| 禁止 | 直接 pip install / git clone / 下载权重 |
| GO | request 记录完整、路由明确、无 blocker |
| FAILED_NO_BOUNDARY_VIOLATION | request 被拒或路由不可行，但无越界执行 |
| BLOCKED | 未授权 install、跳过 review、伪造路由 |
| 下游 | owner_approval_gate |

### 6.2 owner_approval_gate

| 维度 | 规则 |
|------|------|
| 输入 | install_request + 风险摘要 |
| 允许 | owner 显式 GO / NO-GO |
| 禁止 | 默认批准、隐式批准 |
| GO | `owner_approved=true` |
| FAILED_NO_BOUNDARY_VIOLATION | owner 拒绝，边界干净 |
| BLOCKED | 无 owner 记录却进入 execution |
| 下游 | execution_readiness_gate |

### 6.3 execution_readiness_gate

| 维度 | 规则 |
|------|------|
| 输入 | 上游 GO、snapshot、rollback plan、negative guard 清单 |
| 允许 | 标记 execution 可进入 |
| 禁止 | 在 planning 阶段执行真实 install |
| GO | readiness checklist 全绿 |
| FAILED_NO_BOUNDARY_VIOLATION | readiness 不足，可 repair planning |
| BLOCKED | planning 阶段偷偷 execution |
| 下游 | execution_gate |

### 6.4 execution_gate

| 维度 | 规则 |
|------|------|
| 输入 | execution_readiness GO、scoped target |
| 允许 | 受控 pip/source install、受控 weight download、受控 model-load/inference（各阶段独立 flag） |
| 禁止 | 越 scope 资产、越 flag 行为 |
| GO | 执行目标成功 |
| FAILED_NO_BOUNDARY_VIOLATION | 执行失败但边界干净 |
| BLOCKED | 越界下载/runtime/registry/semantic |
| 下游 | post_review_gate |

### 6.5 post_review_gate

| 维度 | 规则 |
|------|------|
| 输入 | execution 产物、audit log、test board draft |
| 允许 | 写 post-review、更新 readiness 建议（非直接 broad ready） |
| 禁止 | 跳过 post-review、伪造成功 |
| GO | post-review 完整、test board 达标 |
| FAILED_NO_BOUNDARY_VIOLATION | 执行失败复盘完成 |
| BLOCKED | 缺 post-review 或 test board 失败 |
| 下游 | registry_patch_gate 或 repair planning |

### 6.6 registry_patch_gate

| 维度 | 规则 |
|------|------|
| 输入 | registry patch planning、scoped diff |
| 允许 | planning；execution 前 snapshot |
| 禁止 | 无 planning 写 overlay；窄 trial 提升 broad ready |
| GO | snapshot + diff + scoped write + post-review |
| FAILED_NO_BOUNDARY_VIOLATION | patch 未执行但 planning 完整 |
| BLOCKED | out-of-scope mutation、无 snapshot |
| 下游 | rollback_readiness_gate |

### 6.7 rollback_readiness_gate

| 维度 | 规则 |
|------|------|
| 输入 | pre-patch snapshot、install snapshot |
| 允许 | 定义 rollback 路径 |
| 禁止 | 无 snapshot 的 destructive write |
| GO | rollback artifact 可解析 |
| FAILED_NO_BOUNDARY_VIOLATION | rollback 未测但 plan 存在 |
| BLOCKED | 缺 rollback readiness 却执行 patch |
| 下游 | 下一阶段 planning / execution |

### 6.8 test_board_protection_gate

| 维度 | 规则 |
|------|------|
| 输入 | review result、phase_id、test_mode |
| 允许 | 写 protected / non-deletable 记录 |
| 禁止 | 跳过 test board；cleanup 删除 board |
| GO | ≥6 protected 记录 + manifest |
| FAILED_NO_BOUNDARY_VIOLATION | review 失败但 board 仍写入 |
| BLOCKED | 未标 protected / cleanup 删 board |
| 下游 | 链 closure / 下一 phase |

---

## 7. Install Strategy Rules

### 7.1 Package install route

- clean PyPI package 可用  
- import root 可 `find_spec` 验证  
- 无 source ambiguity  
- 无 license blocker  

### 7.2 Source install route

- PyPI 不可靠或不存在  
- canonical repo 必须验证（含 redirect/rename 记录）  
- commit pin 必须记录  
- license / dependency 必须审查  
- source checkout **不得**偷偷下载权重  
- code-only install ≠ model load  

### 7.3 no-deps dependency repair route

- 适用于已有 torch/torchvision 等大依赖可复用、仅缺轻量 import root（如 timm）  
- 必须防止全局污染（isolated target、`find_spec` only）  
- 成功 ≠ model load 成功  

---

## 8. Source Repository Rules

- canonical repository verification required  
- redirect / rename must be recorded  
- commit pin required  
- default branch observed  
- license observed  
- dependency files observed (`requirements.txt`, `setup.py`, `pyproject.toml`)  
- build risk recorded  
- C++ extension risk recorded  
- LFS / committed weight risk recorded  
- full clone may equal weight download → 需 weight-exclusion checkout  
- sparse checkout / archive filtering may be required  
- **repo verification success ≠ install success**

---

## 9. Weight Governance Rules

- weight download requires separate request / approval / readiness  
- weight source must be pinned or source reviewed  
- storage path must be controlled (`capabilities/model_weights/...`)  
- sha256 required  
- size required  
- no overwrite without snapshot  
- weight registry patch separate from model load  
- weight downloaded ≠ model ready  
- committed weight inside repo requires weight-exclusion checkout unless approved  

---

## 10. Dependency Repair Rules

（MobileSAM timm 案例）

- missing dependency during model-load = `dependency_gap`，非 model corruption  
- dependency repair requires request / approval / readiness / execution / post-review  
- full isolated install may timeout（transitive heavy deps）  
- no-deps controlled install valid if torch/torchvision reuse explicitly bounded  
- no-deps success = dependency available only  
- dependency repair success ≠ model-load success  
- dependency repair success does not grant inference / runtime  

---

## 11. Model-load Trial Rules

- requires model_load request / approval / readiness  
- sha256 recheck required  
- real import allowed **only in execution phase**  
- model object creation allowed  
- checkpoint load allowed  
- image input **prohibited**  
- inference **prohibited**  
- success = `model_load_verified` only  
- model-load success ≠ inference approval  
- model-load registry patch separate from model-load execution  

---

## 12. Inference Trial Rules

- requires registry `model_load_verified`  
- request / approval / readiness required  
- test image manifest required  
- local synthetic / tiny / scoped test image only  
- live camera **prohibited**  
- personal image **prohibited**  
- external URL **prohibited**  
- uncontrolled dataset **prohibited**  
- output **candidate-only**  
- candidate must not enter fact / runtime / output adapter / semantic / navigation  
- success = `inference_trial_verified` only  
- broad `inference_ready` must remain false unless separately defined  
- runtime requires separate governance  

---

## 13. Registry Overlay Patch Rules

- registry patch requires planning stage first  
- execution must snapshot before write  
- only scoped asset may change  
- diff required  
- post-review required  
- rollback readiness required  
- broad readiness fields must not be promoted by narrow trial  
- out-of-scope asset change = **blocker**

---

## 14. Candidate-only Output Rules

- inference trial output is **candidate-only**  
- candidate eval artifacts live under `_tmp_eval_out`  
- candidate must not be promoted to fact / runtime / output adapter / semantic / navigation  
- candidate requires separate review before any runtime use  

---

## 15. Runtime Boundary Rules

- `runtime_ready` reserved; not granted by asset onboarding standard alone  
- runtime requires separate request / owner approval / execution phase  
- inference_trial_verified does not imply runtime_ready  
- commercial_runtime_approved requires separate governance  

---

## 16. Output Adapter Boundary Rules

- `output_adapter_ready` reserved  
- output adapter requires separate review  
- candidate → output mapping requires failure mode review  
- user-visible output policy review required  

---

## 17. Semantic / Fact / Navigation Exclusion Rules

- semantic_layer_ready reserved  
- fact_write requires separate governance  
- navigation / action / speech requires separate governance  
- candidate result must not enter fact layer or trigger navigation/speech  

---

## 18. Failure Semantics

### GO

- 执行目标成功  
- 无边界违规  
- test board 完整  

### FAILED_NO_BOUNDARY_VIOLATION

- 执行目标失败  
- 边界保持干净  
- 无 unauthorized download  
- 无 runtime / output / semantic / fact / navigation  
- 无 out-of-scope registry mutation  
- **可进入 repair planning**  

### BLOCKED

- 边界违规  
- test board failure  
- registry 越界  
- sha256 / size mismatch  
- 非授权下载 / runtime / output / semantic / fact / navigation  
- 伪造 version / pin / license / readiness  

---

## 19. Negative Guard Pattern

标准化阶段与标准定义必须 blocker 以下 Invalid 场景：

| ID | 场景 | 预期 |
|----|------|------|
| A | 标准化阶段 pip / source install | blocker |
| B | 下载权重 / 模型 / checkpoint / dataset | blocker |
| C | 真实 import / model load / inference | blocker |
| D | 写 registry overlay | blocker |
| E | model_load_verified → inference_ready | blocker |
| F | inference_trial_verified → runtime_ready | blocker |
| G | candidate → fact/runtime/output/semantic | blocker |
| H | live camera / personal image / external URL 默认试跑输入 | blocker |
| I | 跳过 test board protected artifact | blocker |
| J | 缺少 FAILED_NO_BOUNDARY_VIOLATION | blocker |
| K | 缺少 rollback readiness | blocker |
| L | 缺少 registry diff / post-review | blocker |
| M | 缺少 source repo / commit pin / license / dependency | blocker |
| N | 缺少 weight governance | blocker |
| O | 缺少 dependency repair | blocker |
| P | 缺少 runtime/output/semantic/fact/navigation exclusion | blocker |
| Q | 测试过程/结论未写 test board | blocker |
| R | artifact 未标 protected / non-deletable | blocker |
| S | cleanup 删除 test board artifact | blocker |

---

## 20. Test Board Protected Artifact Requirements

每阶段必须：

1. 写 `_tmp_eval_out` 评审产物  
2. 同步写 `capabilities/test_board/<module>/phase_<slug>/`  
3. `test_mode` = `planning` 或 `real_test`（按阶段）  
4. 至少 6 条 protected 记录：`test_process_record`, `test_result_summary`, `test_conclusion_record`, `test_artifact_refs`, `protected_marker`, `non_deletable_notice`, `manifest`  
5. 标注 `protected=true`, `non_deletable=true`, `deletion_forbidden=true`  
6. cleanup **不得**删除 test board 记录  

本标准化阶段额外记录：lifecycle / install strategy / source repo / weight / dependency repair / model-load trial / inference trial / registry patch / failure semantics / test board artifact / reusable template route。

---

## 21. Reusable Phase Template Map

| Template | Required Flags | Required Records | Negative Guards | GO Criteria | Output Path | Test Board |
|----------|----------------|------------------|-----------------|-------------|-------------|------------|
| Planning | `planning_only=true`, execution flags false | profile, stage_refs, planning records | no execution | blocker_count=0 | `_tmp_eval_out/<phase>_smoke_v0/*_review_v1.json` | `test_mode=planning` |
| Request/Approval/Readiness | upstream GO, `owner_approved` | request, approval, readiness | no execution | readiness checklist | 同上 | planning |
| Execution/Post-Review | execution flags true (scoped) | execution audit, post-review | boundary guards | target success or FAILED_NO_BOUNDARY | 同上 + execution artifacts | real_test |
| Failure Review/Repair Planning | upstream FAILED_NO_BOUNDARY | failure audit, repair plan | no blind retry | repair route defined | 同上 | planning |
| Registry Patch Planning | `registry_mutation_allowed=false` | patch plan, diff plan | no write | plan complete | 同上 | planning |
| Registry Patch Execution | `registry_mutation_allowed=true` (scoped) | snapshot, diff, write audit | scoped only | patch success | overlay + review | real_test |
| Runtime Boundary Planning | runtime flags false | runtime/output/semantic exclusion | no runtime | boundaries defined | 同上 | planning |

---

## 22. MobileSAM Case Mapping

| 事实 | 值 |
|------|-----|
| Install route | source component, code-only, weight-excluding checkout |
| Committed weight risk | true（repo 内含权重风险） |
| Weight sha256 | `6dbb90523a35330fedd7f1d3dfc66f995213d81b29a5ca8108dbcdd4e37d6c2f` |
| Weight size | 40728226 bytes |
| Readiness progression | code_only_ready → code_and_weight_ready → model_load_verified → inference_trial_verified |
| Model-load failure | missing `timm` dependency |
| timm full install | timeout (transitive heavy deps) → FAILED_NO_BOUNDARY_VIOLATION |
| timm no-deps install | GO (v1.0.27) |
| Model-load retry | GO (Sam checkpoint load) |
| Inference trial | GO (synthetic 128×128, candidate-only) |
| Registry patches | code_and_weight_ready → model_load_verified → inference_trial_verified |
| Runtime / broad inference | remain false |

---

## 23. Future Model Onboarding Checklist

- [ ] Asset registry planning + probe  
- [ ] Choose package vs source route  
- [ ] If source: repo verification + commit pin + license + dependency review  
- [ ] Code-only install + registry patch (`code_only_ready`)  
- [ ] Weight request / approval / download / hash verify + registry patch (`code_and_weight_ready`)  
- [ ] Model-load request / approval / execution (+ dependency repair if needed) + registry patch (`model_load_verified`)  
- [ ] Inference trial request / approval / execution (candidate-only) + registry patch (`inference_trial_verified`)  
- [ ] Runtime boundary planning (separate phase)  
- [ ] Output adapter review (separate)  
- [ ] Semantic / fact / navigation governance (separate)  
- [ ] Commercial runtime approval (separate)  
- [ ] Test board protected artifacts at every phase  
- [ ] Preserve FAILED_NO_BOUNDARY_VIOLATION vs BLOCKED semantics  

---

*End of Model Asset Onboarding Governance Standard V1*
