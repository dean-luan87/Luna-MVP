# Luna — Controlled Frame File Existence Check Guarded Planning v1

**Phase**：`Phase-Controlled-Frame-File-Existence-Check-Guarded-Planning-v1-001`  
**性质**：planning-only（只定义未来“文件存在性检查”如何被门控与审计；本阶段不执行存在性检查）  
**输出目录**：`_eval_out/controlled_frame_file_existence_check_guarded_planning_v1_smoke_v0/`

## 阶段定位

这是从 “manifest/declared metadata 世界” 迈向 “真实文件系统世界” 的第一层门控，但仍然是 **门的规划**，不是执行。

本阶段用于回答：

1. 文件存在性检查未来是否允许（允许：**候选**；当前：**不允许**）
2. 文件存在性检查与 `file stat / file open / content read` 的边界是什么（当前全部 **blocked**）
3. 哪些路径范围未来可作为 guarded existence check 候选（repo/eval_out/显式登记/受控测试资产）
4. 哪些路径必须阻断（外部绝对路径、traversal、未知路径、系统敏感目录、home 任意路径、网络挂载等）
5. user upload / symlink / traversal 的处理原则
6. existence check 需要哪些 gate / 授权源 / 审计 trace
7. existence check 输出是否能成为事实（答案：**不能**，永远 `not_fact`）
8. 检查失败时如何处理（缺失/权限/不可信路径/缺少 source_chain/隐私标签等 → 保守回退）
9. 是否需要 audit trace 与 source_chain（答案：必须）
10. 下一阶段是否可以进入 `Guarded DryRun`（答案：可以，但仍必须 simulation-only，不调用真实 exists/stat）

## 强边界（必须冻结）

本阶段严格禁止：

- 不执行文件存在性检查；不调用 `os.path.exists` / `pathlib.Path.exists`
- 不 `stat` 文件；不 `open` 文件；不读取任何目标文件内容（尤其 image/video）
- 不解析 EXIF；不 probe 视频；不抽帧；不计算真实 hash / perceptual hash
- 不进入任何 runtime：camera / vision model / OCR / map / tracking / crossing / speech
- 不写 `WorldModel / Memory / Fact / Library`；不生成 Scene Delta；不触发 Task/Navigation action

## 核心对象（v1）

- `ControlledFrameFileExistenceCheckGuardedPlanningPolicy`
  - `planning_only=true`
  - `existence_check_allowed_now=false`
  - `exists_call_allowed_now=false`
  - `stat_allowed_now=false`
  - `open_allowed_now=false`
  - `content_read_allowed_now=false`
  - `hash_allowed_now=false`
- `FileExistenceCheckGatePolicy`
  - gate 类型：`CapabilityRuntimePreGate`
  - 当前 gate 必须关闭：`current_phase_gate_open=false`
  - 必须要求：授权源 + 路径分类 + 隐私 precheck + 必要时 manual review + audit trace + source_chain
- `AllowedPathScopePolicy` / `BlockedPathScopePolicy`
  - 允许候选：repo fixture / eval_out fixture / 显式登记 fixture / 受控测试资产（均 `allowed_now=false`）
  - 阻断：外部绝对路径 / traversal / 未知路径 / 系统敏感 / home 任意 / network mount / live stream 等
  - restricted：symlink / user upload（默认不允许，仅在未来以更强 gate+review 才可能候选）
- `FileExistenceAuthorizationPolicy`
  - 明确：只有路径字符串不能授权 existence check
- `FileExistenceAuditTracePolicy` / `FailureModePolicy` / `RollbackPolicy`
  - 审计必须可追溯、可复跑；失败必须保守回退；rollback 必须无持久副作用
- `FileExistenceDecisionCandidateSchema`
  - `existence_status=not_checked`
  - `file_exists_verified=false`
  - `fact_status=not_fact`

## 场景矩阵（planning-only）

runner 必须生成 `controlled_frame_file_existence_check_guarded_planning_scenario_matrix.json`，覆盖 ≥18 个规划场景：

- allowed future candidate：repo / eval_out / registered fixture / controlled test asset
- restricted：user upload、symlink
- blocked：external absolute / traversal / unknown / system sensitive / home arbitrary / network mount
- governance blockers：missing source_chain / missing privacy tags / missing fixture registry ref
- authorized but not invoked（本阶段仍不执行）
- failure modes：gate denied / permission denied

## 通过条件（概念级）

当 verifier=GO 时：

- `final_decision=CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_PLANNING_READY_FOR_DRYRUN`
- `recommended_next_phase=Phase-Controlled-Frame-File-Existence-Check-Guarded-DryRun-v1-001`

## 实施状态

`Phase-Controlled-Frame-File-Existence-Check-Guarded-DryRun-v1-001` 已以 **dry-run-only（simulation-only）** 形式落地：只模拟 gate/授权/路径范围/审计/失败与回滚决策，不调用 `exists/stat/open/read`，并保持 no-runtime/no-write 边界。

`Phase-Controlled-Frame-File-Existence-Check-Guarded-Post-DryRun-Review-v1-001` 将对上述 dry-run 产物做 **review-only** 审计，重点检查：`exists/stat/open/read/hash` 全未发生，且 gate 决策符合规划合同；通过后才允许进入 closure（closure 仍不意味着真实存在性检查已启用）。

`Phase-Controlled-Frame-File-Existence-Check-Guarded-Closure-v1-001` 将对 planning+dryrun+review 做阶段性关账：冻结 no-exists/no-stat/no-open/no-read/no-hash，明确真实文件系统访问仍不可用，并将后续路线移交给 roadmap decision。

