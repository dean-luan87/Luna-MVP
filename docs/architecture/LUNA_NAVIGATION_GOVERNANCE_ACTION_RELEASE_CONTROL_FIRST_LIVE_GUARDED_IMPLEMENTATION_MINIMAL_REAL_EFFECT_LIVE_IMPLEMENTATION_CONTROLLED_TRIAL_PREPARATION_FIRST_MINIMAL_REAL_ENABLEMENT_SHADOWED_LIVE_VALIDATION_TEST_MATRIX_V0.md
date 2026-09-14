# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation First Minimal Real Enablement Shadowed Live Validation Test Matrix v0（验证矩阵冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_MINIMAL_REAL_ENABLEMENT_SHADOWED_LIVE_VALIDATION_TEST_MATRIX_V0.md`  
**性质**：Phase-Next-153：把验证场景、预期 started/release/closure 行为与失败判定矩阵化（无代码）

---

## 验证场景矩阵（写死口径）

| 场景 | 输入特征 | 预期 started | 预期 release(window) | 预期 closure | 失败判定 |
|---|---|---:|---:|---:|---|
| A.not_ready | readiness 不足 | 否 | 否 | 不要求（但不得异常） | 任意 started/release 即 fail |
| B.preparation_go_only | 只有 preparation_go | 否 | 否 | 不要求 | started/release 即 fail |
| C.dry_run_only | dry_run_executed；无 intent | 否 | 否 | 不要求 | started/release 即 fail |
| D.admitted_but_no_start_event | admission/评估通过；但无 start_event（通过缺 intent/不调用入口模拟） | 否 | 否 | 不要求 | started/release 即 fail |
| E.legal_started_success | start gate 满足；观测 start_event；写 state+result 成功 | 是 | 短时允许且最终回落 | 是（最终 se=false） | closure 缺失 / se 不回落 即 fail |
| F.legal_started_failure | start gate 满足；观测 start_event；写入阶段受控失败 | 是 | 短时允许且最终回落 | 是（rollback_completed；最终 se=false） | 无 closure / se 不回落 / 未收口 即 fail |
| G.illegal_release_attempt | started 前 release（合成非法观测） | N/A | N/A | N/A | 必须被捕获为 illegal_release_without_started |
| H.illegal_started_without_event | 无 start_event 却 started（合成非法观测） | N/A | N/A | N/A | 必须被捕获为 illegal_started_without_start_event |
| I.unclosed_path_probe | started 后未 closure（合成非法观测） | N/A | N/A | N/A | 必须被捕获为 illegal_started_without_closure |

