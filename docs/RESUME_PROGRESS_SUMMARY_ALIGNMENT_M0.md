# Resume Progress Summary Alignment M0

**文件**：`docs/RESUME_PROGRESS_SUMMARY_ALIGNMENT_M0.md`

## 一、文档定位

1. **不是**新推理能力模块、**不是**主链拍板 / recheck 行为改写、**不是** benchmark / triage 规则修改、**不是** `lg`/`nt` 启发式再调；**是** **`ctx → inputs → TCS → run_summary → narrative`** 的 **摘要链最小工程补强**（派生字段与透传，**不**发明主链事实）。  
2. **把** **`恢复已声明 / resume 目标 / 主任务未真正推进`** **稳定写入同帧可消费摘要**（与 `run_summary_builder` 既有契约一致）。  
3. **目标**是提升 **信号可见性与同帧共现**，**不**以制造 harness 新 fail 为目的（整包仍 **acceptable / issue none**）。

---

## 二、问题复盘（承接 `RESUME_CLOSURE_SIGNAL_ALIGNMENT_REVIEW_M0`）

1. **ctx** 中已有 **`task_resume_target`**、**`recovery_declared_but_resume_chain_fragile_expected`** 等，但 **未进入 `frame.inputs`** → **`run_summary_builder._build_process_observation`** 无法打 **`m11x_ctx_observed`**，**`resume_chain_fragility_summary`** 常为 **`none`**。  
2. **`task_chain_state_snapshot.task_resume_target`** 仅由 **OSI** 推导，**未合并** 场景 **resume 字符串** → 与 **ctx** 不一致。  
3. **`task_chain_progress_summary`** 缺一条 **显式、可匹配** 的 **「全局主任务未收口 / 未 terminal」** 对齐句。  

---

## 三、本轮补强（实现摘要）

| 位置 | 变更 |
|------|------|
| **`decision_monitor/schema.py` `InputsLayer`** | 增加 **`scenario_task_resume_target`** 与三类 **expected** 布尔（从 ctx 只读透传）。 |
| **`decision_monitor/builder.py` `_build_inputs`** | 从 **ctx** 填充上述字段（**不改**主链决策）。 |
| **`decision_monitor/task_chain_state_snapshot.py`** | **合并** `scenario_task_resume_target` 到 **`task_resume_target`**（当 OSI 未给出时）；新增 **`build_resume_main_progress_alignment_summary`** → 写入 **`resume_main_progress_alignment_summary`**；**`build_task_chain_progress_summary`** 追加 **`resume_main_align=...`**。 |
| **`run_summary_reference`（既有逻辑）** | **`inputs`** 现含 expected flag → **`process_observation_summary`** 可出现 **`m11x_ctx_observed`**；**TCS `task_resume_target` 非空** 时 **`resume_chain_fragility_summary`** 可按原规则升为 **`resume_declared_but_main_not_progressed`**。 |

**未改**：`narrative_evidence_tension_review` 规则文件；**未改** `tools/tension_severity_profile_map.py` 映射公式（**`critical_candidate`** 仍 **`pc∧lg` 同帧 high**，随 **raw** 自然变化）。

---

## 四、对齐前后（代表 case）

### 4.1 `R60_recovery_declared_but_resume_chain_fragile_real`

| 项 | 对齐前 | 对齐后 |
|----|--------|--------|
| **`inputs.scenario_task_resume_target`** | 无 | **`resume_main_search_route`** |
| **`inputs.recovery_declared_but_resume_chain_fragile_expected`** | 无 / 不可见 | **`true`** |
| **TCS `task_resume_target`** | **`null`** | **`resume_main_search_route`** |
| **`resume_chain_fragility_summary`** | **`none`** | **`resume_declared_but_main_not_progressed`** |
| **`process_observation`** | 无 m11x | **`m11x_ctx_observed; resume_frag=resume_declared_but_main_not_progressed; ...`** |
| **`task_chain_progress_summary`** | 无 `resume_main_align` | 含 **`resume_main_align=resume_chain_fragile_expected; resume_target_traced; global_main_progress_not_terminal_complete`** |
| **`pc` / `lg`（tension）** | high / medium | **high / high** |

### 4.2 `R82` / `R53` 等（仅有部分 ctx 线索）

- **无** `task_resume_target` 字符串时：**`resume_chain_fragility_summary`** 仍可能为 **`none`**，但 **`resume_main_align`** 可含 **`resume_chain_fragile_expected`**、**`closure_semantics_misaligned_expected`**、**`global_main_progress_not_terminal_complete`**，**显式度仍提升**。  
- **`R53`/`R59`/`R60`** 等：在 **整包**中可出现 **`pc=high ∧ lg=high`**（与 **TCS + OSI + ctx** 组合一致）。

---

## 五、整包 `m14` 结果摘要（对齐后）

命令：`python3 tools/real_scenario_pack.py --out logs/real_scenario_pack_m14.json`

- **`pc=high ∧ lg=high`**：**3** 例（如 **`R53`、`R59`、`R60`**，以日志为准）。  
- **`overall_severity_profile`**：**`critical_candidate` = 3**（**59 review** / **19 watch**，与 **`map_severity_profile_m14`** 一致）。  
- **harness**：**不改变** benchmark 判定逻辑；**仍** **82 passed**、**acceptable**。

---

## 六、风险评估

- **误报**：仅在 **ctx 显式提供** resume/frag 或 **OSI 已给出 resume 语义** 时强化摘要；**R1** 等无 flag 场景 **`recovery_*` 为 False**，**不会**凭空注入。  
- **噪声**：**`task_chain_progress_summary`** 略长，但 **token 化**、**可 grep**。  
- **本质**：把 **原先只在 ctx 或隐式结构里** 的语义 **显式化**，**不是**发明新故障。

---

## 七、测试与产物

- **单测**：`tests/test_resume_progress_summary_alignment.py`  
- **Smoke**：`tools/smoke_resume_progress_summary_alignment.py` → `logs/smoke_resume_progress_summary_alignment.jsonl`  
- **分析**：`tools/analyze_resume_progress_summary_alignment.py` → `logs/resume_progress_summary_alignment_analysis.json`  

---

## 八、最终问题（必须回答）

1. **resume / main progress 是否更易同帧共现？** **是**：**`resume_main_align`**、**`m11x`**、**`resume_chain_fragility_summary`** 与 **TCS `task_resume_target`** 对齐。  
2. **是否更有利于 `lg` 与 `pc` 配对？** **是**：整包出现 **非零 `pc∧lg` high** 与 **`critical_candidate`**。  
3. **是否还要再做一轮信号对齐？** **可选**：若需 **100% ctx resume** 均进 **rf**，可再审 **无 `task_resume_target` 字符串** 仅 **frag flag** 的 case（如部分 **R82**）。  
4. **是否适合第十五批扩包？** **可以**：摘要链已更能支撑 **severity / tension** 阅读。  
5. **`nt` 是否仍第二优先级？** **是**，本轮未动。  

---

## 九、本轮是否适合作为 resume-progress 信号对齐收口

**适合。** 有 **代码路径、代表 before/after、整包统计、测试与风险**。

---

## 十、M1.5 场景验证（第十五批）

- 已用 **`logs/real_scenario_pack_m15.json`**（`R83–R88`）做 **resume-progress 摘要链** 下的整包回归；交付见 **`docs/REAL_SCENARIO_PACK_M1_5_DELIVERY.md`**：观察 **`pc∧lg` 同帧 high** 与 **`critical_candidate`** 是否从「偶发」变为更可重复模式（**severity 仍不接入 hard-fail**）。

---

## 十一、（M0 摘要链补强）是否通过

**通过。** 摘要链已补强；**未**改 benchmark / recheck 拍板 / 主骨架重构。

---

## 主线—白盒—日志

- **主线**：仅 **inputs/TCS/run_summary** 派生字段，**不**改决策拍板。  
- **白盒**：与 **task_chain / process_observation** 同链。  
- **日志**：`logs/real_scenario_pack_m14.json`、`logs/resume_progress_summary_alignment_analysis.json`。  
- **最终判断**：**主线通顺，白盒一致，日志已落地**。
