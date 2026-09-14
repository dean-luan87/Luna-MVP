# M1.x Baseline Consolidation Review（阶段收束复盘）

**文件**：`docs/M1X_BASELINE_CONSOLIDATION_REVIEW.md`  
**性质**：阶段收束文档（Consolidation Review）  
**本轮声明**：**不是**新能力开发、**不是**规则升级、**不**扩场景、**不**改 benchmark/triage、**不**改主骨架、**不**把 soft-fail/advisory 接入自动 gate/fail。

本文回答：

1. **M1.x 到底完成了什么**（以主线产物为证）；  
2. 哪些模块/能力已经形成**闭环**；  
3. 哪些仍是 **reserve / future**；  
4. 当前是否可认定：**M1.x 主线阶段基本完成（Yes/No）**；  
5. 下一阶段主任务建议（**必须排序**）。

---

## §1. 复盘范围与输入清单（只读）

本轮依据（仅复盘、归纳，不引入新规则）：

- 冻结基线：`docs/MAINLINE_ENGINEERING_BASELINE_FREEZE_M0_6.md`
- 场景压测与 fix sprint：`docs/REAL_SCENARIO_PACK_M1_0_DELIVERY.md`、`docs/TARGETED_FIX_SPRINT_M1_0_X.md`、`docs/REAL_SCENARIO_PACK_M1_1_DELIVERY.md`、`docs/TARGETED_FIX_SPRINT_M1_1_X.md`、`docs/REAL_SCENARIO_PACK_M1_2_DELIVERY.md`、`docs/REAL_SCENARIO_PACK_M1_7_DELIVERY.md`
- tension / severity：`docs/NARRATIVE_EVIDENCE_TENSION_REVIEW_M0.md`、`docs/TENSION_AUDIT_CALIBRATION_REVIEW_M0.md`、`docs/TENSION_REVIEW_TEMPLATE_AND_SOFT_FAIL_SPEC_M0.md`、`docs/TENSION_SEVERITY_PROFILE_SPEC_M0.md`、`docs/SEVERITY_SIGNAL_GAP_REVIEW_M0.md`
- lg / resume-progress：`docs/LOCAL_GLOBAL_PROGRESS_GRADIENT_TIGHTENING_M0.md`、`docs/RESUME_CLOSURE_SIGNAL_ALIGNMENT_REVIEW_M0.md`、`docs/RESUME_PROGRESS_SUMMARY_ALIGNMENT_M0.md`
- critical / soft-fail candidate：`docs/CRITICAL_CANDIDATE_PATTERN_REVIEW_M0.md`、`docs/SOFT_FAIL_CANDIDATE_DRAFT_M0.md`、`docs/SOFT_FAIL_CANDIDATE_VALIDATION_PACK_M0.md`
- advisory 工程接入：`docs/ADVISORY_REVIEW_GATE_DRAFT_M0.md`、`docs/ADVISORY_OBSERVATION_INTEGRATION_M0.md`

---

## §2. M1.x 工程主线复盘（6 大板块）

### A. 冻结基线与主链显式化（M0.6）

**结论**：主线已冻结为 **M0.6 最小工程同链基线**，并明确边界：纳入的是「同帧可追溯的上下文源 + 白盒 + 日志 + summary→后处理入口契约」，不包含图书馆/记忆写入/自治闭环等完整形态能力。

- **已纳入基线（代表对象）**：  
  - `scheduled_source_state`（最小对象）  
  - `mainline_state_snapshot`（四态/六阶段最小显式化）  
  - `task_chain_state_snapshot` + 位置解释（M0.1）  
  - `memory_invocation_explanation`  
  - `run_summary_reference`（Raw/Event/Summary 三层语义分层）  
  - `post_processing_summary_entry`（Summary→后处理边界契约）  
  - `mainline_narrative_alignment`（叙事骨架统一）

**证据**：`docs/MAINLINE_ENGINEERING_BASELINE_FREEZE_M0_6.md`（含“纳入/不纳入”硬句与锚点）。

### B. 场景压测与 fix sprint 闭环（M1.0 → M1.7）

**结论**：M1.x 形成了稳定的“真实场景压测 → triage → 按冻结口径正式分类 → 定点 fix sprint → 回归整包验证”的闭环；且在后续扩包中持续保持“**不改 benchmark/triage**、不提前扩权”的纪律。

- **M1.0（第十批回归）**：首次压测暴露 **4 条 `baseline_covered_defect`**（R53/R54/R55/R56），聚焦 `blocked_without_resolution` 与 `recheck_planner` 热点。  
  - 证据：`docs/REAL_SCENARIO_PACK_M1_0_DELIVERY.md`
- **M1.0.x（定点收口）**：对上述 4 条基线内缺陷做最小修复并回归至 **58/58 全绿**。  
  - 证据：`docs/TARGETED_FIX_SPRINT_M1_0_X.md`
- **M1.1（第十一批扩包）**：新增场景再次暴露 **3 条 `baseline_covered_defect`**（R60/R61/R64），热点回到 `recheck_planner`。  
  - 证据：`docs/REAL_SCENARIO_PACK_M1_1_DELIVERY.md`
- **M1.1.x（定点收口）**：对 R60/R61/R64 做最小修复并回归（整包通过、热点清空）。  
  - 证据：`docs/TARGETED_FIX_SPRINT_M1_1_X.md`
- **M1.2（第十二批扩包）**：在两轮 fix sprint 后继续扩压，整包 **70/70** 全通过，未新增 harness 级失败。  
  - 证据：`docs/REAL_SCENARIO_PACK_M1_2_DELIVERY.md`
- **M1.6 / M1.7（第十六/十七批扩包）**：在冻结基线 + tension/severity 上引入 **advisory（SF-1′）只读观察**并进行扩包验证；M1.7 整包 **100/100** 全通过。  
  - 证据：`docs/REAL_SCENARIO_PACK_M1_7_DELIVERY.md`

### C. tension 审计层（只读观察链）

**结论**：已形成 **tension 对象 → 校准 → 使用层级模板 → severity 画像** 的只读观察闭环，且明确“启发式饱和维不可直接升级为失败或 gate”的工程边界。

- **tension 审计对象落地**：`narrative_evidence_tension_review` 挂 frame 顶层，进入聚合链与 Viewer/Console；不改变主链拍板。  
  - 证据：`docs/NARRATIVE_EVIDENCE_TENSION_REVIEW_M0.md`
- **校准与去噪**：解释 M1.3 “中高张力泛化”与区分力问题，给出保留/收紧/配对建议。  
  - 证据：`docs/TENSION_AUDIT_CALIBRATION_REVIEW_M0.md`
- **人工模板与升级边界写死**（L1–L4）：哪类信号只能 observation、哪类可 review、哪类必须配对、soft-fail 仍是 future。  
  - 证据：`docs/TENSION_REVIEW_TEMPLATE_AND_SOFT_FAIL_SPEC_M0.md`
- **severity 画像语义层**：把原始档位翻译为 `watch/review/critical_candidate`（解读层，非 hard-fail）。  
  - 证据：`docs/TENSION_SEVERITY_PROFILE_SPEC_M0.md`
- **信号缺口复盘**：解释为何曾出现 “review 多、critical=0”，并给出工程优先级（排序）。  
  - 证据：`docs/SEVERITY_SIGNAL_GAP_REVIEW_M0.md`

### D. lg / resume-progress 信号链专项（“同帧可消费摘要”闭环）

**结论**：从“信号缺口解释”推进到“摘要链补强落地”，使 **`pc∧lg` 同帧双高**与 **`critical_candidate`** 从 0 变为可复现的非零集合；同时对 `lg` 的梯度做过一次收紧，避免字段名假阳性。

- **`lg` 梯度收紧**：消除 `resume=` 字段名假阳性，引入 `lg=low`，保留 `lg=high` 的保守路径。  
  - 证据：`docs/LOCAL_GLOBAL_PROGRESS_GRADIENT_TIGHTENING_M0.md`
- **resume/closure 对齐复盘**：明确断点在 **ctx → inputs/TCS → run_summary** 的信号透传与压缩损失，而非简单阈值问题。  
  - 证据：`docs/RESUME_CLOSURE_SIGNAL_ALIGNMENT_REVIEW_M0.md`
- **摘要链补强落地**：把 `scenario_task_resume_target` 与 expected flags 透传进 `InputsLayer`，合并到 `task_chain_state_snapshot`，并通过 `resume_main_align` 等 token 让 “resume 脆弱 + 主未推进”在同帧可被 rsr/tcp 消费，从而支撑 `lg=high` 与 `critical_candidate` 的可复现集合。  
  - 证据：`docs/RESUME_PROGRESS_SUMMARY_ALIGNMENT_M0.md`

### E. critical / soft-fail candidate 线（条款化 + 验证）

**结论**：已把 `critical_candidate` 样本从“集合”提升为“可命名主模式”，并将其条款化为 **SF-1′**，再用验证包证明边界稳定；但**仍明确保持为观察/人审提示**，不升级为自动失败。

- **模式复盘**：m15 的 `critical_candidate` 7 例同族，主模式命名为 `resume_fragility_with_global_main_stall`。  
  - 证据：`docs/CRITICAL_CANDIDATE_PATTERN_REVIEW_M0.md`
- **条款草案（SF-1′）**：把 `pc∧lg` raw high + `rsr` + `tcp` token 写成可引用条款，并列出近邻/健康排除条件。  
  - 证据：`docs/SOFT_FAIL_CANDIDATE_DRAFT_M0.md`
- **验证包（边界）**：正样本 7/7 命中，近邻/健康/轻量变体 0 误伤；产物可复现。  
  - 证据：`docs/SOFT_FAIL_CANDIDATE_VALIDATION_PACK_M0.md`

### F. advisory / review 候选工程接入（只读可见性闭环）

**结论**：SF-1′ 已从“文档条款”推进到 **frame 顶层可读对象**（JSONL/聚合/Console/Viewer 可见），并在 M1.6/M1.7 真实扩包中验证其与 `critical_candidate` 的持续一致性；仍为 **advisory-only**（提示权，无裁决权）。

- **使用草案（权限边界）**：明确 SF-1′ 的角色、禁止落点、接入顺序（排序）。  
  - 证据：`docs/ADVISORY_REVIEW_GATE_DRAFT_M0.md`
- **工程接入（可见性）**：`advisory_review_observation` 进入 frame 顶层 + JSONL + 聚合链 + Console/Viewer；不参与判定。  
  - 证据：`docs/ADVISORY_OBSERVATION_INTEGRATION_M0.md`
- **真实扩包验证**：M1.7 显示 advisory 与 `critical_candidate` 仍同集合（本批 11=11），近邻与健康样本稳定排除。  
  - 证据：`docs/REAL_SCENARIO_PACK_M1_7_DELIVERY.md`

---

## §3. 已闭环能力清单（表格）

> “闭环”在本文的含义：**有工程落地对象/字段 + 有可复现产物（log/doc/test）+ 有真实场景或定点回归验证 + 边界清楚（不扩权）**。

| 模块/能力 | 当前状态 | 证据文档/产物 | 结论 |
|---|---|---|---|
| **M0.6 冻结基线**（主线/白盒/日志/summary→entry 同链） | 冻结完成 | `docs/MAINLINE_ENGINEERING_BASELINE_FREEZE_M0_6.md` | **闭环**：工程基线与边界硬句成立 |
| **真实场景压测 → triage → 正式三类分类** | 稳定执行 | `docs/REAL_SCENARIO_PACK_M1_0_DELIVERY.md`、`docs/REAL_SCENARIO_PACK_M1_1_DELIVERY.md`、`docs/REAL_SCENARIO_PACK_M1_2_DELIVERY.md`、`docs/REAL_SCENARIO_PACK_M1_7_DELIVERY.md` | **闭环**：不靠“感觉”，有固定流程与产物 |
| **Targeted Fix Sprint（基线内缺陷定点收口）** | 两轮闭环 | `docs/TARGETED_FIX_SPRINT_M1_0_X.md`、`docs/TARGETED_FIX_SPRINT_M1_1_X.md` | **闭环**：`blocked_without_resolution` 清零且回归验证 |
| **tension 审计对象（五维）** | 工程落地 | `docs/NARRATIVE_EVIDENCE_TENSION_REVIEW_M0.md` | **闭环**：只读观察进入 frame/聚合/展示 |
| **tension 校准与使用层级模板** | 文档化收束 | `docs/TENSION_AUDIT_CALIBRATION_REVIEW_M0.md`、`docs/TENSION_REVIEW_TEMPLATE_AND_SOFT_FAIL_SPEC_M0.md` | **闭环**：饱和维/区分力/配对规则已写死 |
| **severity 画像层（watch/review/critical_candidate）** | 工程可读 + 场景验证 | `docs/TENSION_SEVERITY_PROFILE_SPEC_M0.md`、`docs/SEVERITY_SIGNAL_GAP_REVIEW_M0.md` | **闭环**：画像语义明确；缺口解释与优先级给出 |
| **lg 梯度收紧（去假阳性）** | 完成一轮收口 | `docs/LOCAL_GLOBAL_PROGRESS_GRADIENT_TIGHTENING_M0.md` | **闭环**：`lg=low` 出现、`resume=` 假阳性去除 |
| **resume-progress 摘要链对齐（ctx→inputs→TCS→rsr）** | 工程落地 + 整包验证 | `docs/RESUME_PROGRESS_SUMMARY_ALIGNMENT_M0.md` | **闭环**：同帧可消费 token 形成，支撑 `pc∧lg` 非零 |
| **critical_candidate 主模式复盘** | 模式固化 | `docs/CRITICAL_CANDIDATE_PATTERN_REVIEW_M0.md` | **闭环**：7/7 同族，边界与对照写清 |
| **SF-1′ 条款 + 验证包** | 条款化 + 边界验证 | `docs/SOFT_FAIL_CANDIDATE_DRAFT_M0.md`、`docs/SOFT_FAIL_CANDIDATE_VALIDATION_PACK_M0.md` | **闭环**：正样本命中、近邻/健康排除可复现 |
| **advisory 工程观察接入（advisory-only）** | 工程可见 + 真实扩包复验 | `docs/ADVISORY_REVIEW_GATE_DRAFT_M0.md`、`docs/ADVISORY_OBSERVATION_INTEGRATION_M0.md`、`docs/REAL_SCENARIO_PACK_M1_7_DELIVERY.md` | **闭环**：提示权落地且不扩权；与 critical 持续一致 |

---

## §4. 未闭环 / reserve / future 清单（表格）

> “未闭环”在本文的含义：尚未形成“工程对象 + 真实验证 + 边界稳定”的闭环，或明确被冻结文档列为 **not_included / reserved_only**。

| 能力/方向 | 为什么不算完成 | 建议属于哪一阶段以后再做 |
|---|---|---|
| **`nt` 启发式专项（叙事顺滑但证据薄）** | `nt` 长期“区分力塌缩”，多轮复盘已指出需 **收紧启发式** 才能把产品关切落为可观测信号；当前仍主要停在 observation | **下一阶段优先级靠前**（见 §6-1） |
| **advisory 自动 gate / block** | 已明确“提示权无裁决权”；自动 gate 会改变运行态与评测语义，属于 90% 后的自治系统设计 | **M2+ / 军工级阶段** |
| **soft-fail 正式接入（写入规则/CI）** | 目前条款与验证已具备，但“接入规则”属于评测哲学与治理升级，违反本阶段约束 | **M2+（规则升级阶段）** |
| **图书馆正式接入 / 记忆写入** | 冻结文档明确不在基线；当前仅解释/占位与边界契约，不具备写入治理闭环 | **M2+（数据治理与长期记忆阶段）** |
| **任务链深机制**（终止/熔断/归因/稳定状态机） | 当前仅快照与位置解释（M0/M0.1），并非完整任务引擎/执行器；深机制会牵动主链与评测 | **M2+（任务引擎阶段）** |
| **语音/对话承接层** | 当前主线聚焦“主线—白盒—日志—summary/entry”的可追溯闭环；语音/对话会引入输入形态与多轮对齐新变量 | **独立大阶段（产品输入形态扩展）** |
| **语义转译层**（多模态/用户意图→任务结构） | 需要更完整的任务语义、工具/执行器边界与长期记忆配合；当前阶段不具备依赖栈 | **在任务引擎/记忆治理之后** |
| **军工级自治闭环**（运行态切换、退化态验证、fail-safe） | 明确属于 90% 之后的系统性工程；当前阶段只做“观察层三件套”验证 | **M2+（自治系统阶段）** |

---

## §5. 阶段判断（重点：必须 Yes/No）

### 5.1 当前 M1.x 主线是否可认定为“阶段基本完成”？

**结论：Yes。**

### 5.2 “基本完成”的边界是什么（包含/不包含）

- **包含（M1.x 的完成边界）**：
  - **M0.6 冻结基线**成立（主线/白盒/日志/summary→entry 同链 + 边界硬句）；
  - **真实场景压测 + 两轮 fix sprint 收口**完成闭环；
  - **tension / severity / advisory（SF-1′）**三层观察链在真实扩包（至 M1.7）中持续稳定：**不误伤近邻/健康样本**、且 **不接自动 fail/gate**；
  - 正式问题判断仍严格服从三类：`baseline_covered_defect` / `baseline_excluded_requirement` / `reserve_only_finding`。

- **不包含（仍为 reserve/future）**：
  - advisory 自动 gate、soft-fail 正式接入、图书馆/记忆写入、任务链深机制、语音/对话承接、语义转译层、军工级自治闭环。

### 5.3 若反证（为何不是 No）

在 M1.0 与 M1.1 两次真实场景中，确实暴露了基线内缺陷，但均通过 **Targeted Fix Sprint** 做了 **可复现的定点收口 + 整包回归**，后续批次在同冻结口径下未出现新的 harness 级失败；因此从“阶段闭环”角度，M1.x 的主线目标已达成。

---

## §6. 下一阶段优先级建议（必须排序）

> 目标：在不提前进入“军工级自治闭环”的前提下，选择**最能提升后续阶段质量与确定性**的主任务。

### 6.1 建议排序（1 → 5）

1. **`nt` 启发式专项（叙事—证据支持张力的可观测性修复）**  
   - **为什么优先**：多份复盘一致指出 `nt` 长期“区分力塌缩”，与产品关切（故事顺但证据薄）不对齐；不修复 `nt`，后续更高阶 gate/soft-fail 很容易继续建立在“不可分层信号”上。  
   - **为什么不是别的**：相比直接推进自治/记忆写入，`nt` 修复更小、更贴近现有观测链，不需要改变 benchmark/主链边界即可先把信号质量抬起来。
2. **图书馆/记忆正式接入的前置工程（边界契约 → 可落地写入链）**  
   - **为什么第二**：当前 backfill/entry 已形成契约，但仍停在“入口与解释”；若进入下一阶段，最容易产生真实收益的是把长期知识与记忆治理真正落地（否则很多张力只能停在观察）。  
   - **为什么不是第三**：任务链深机制与语义转译需要记忆/治理/工具边界支撑，依赖栈更深。
3. **任务链深机制（退出/熔断/归因/稳态）**  
   - **为什么第三**：M1.x 已做“快照 + 位置解释”；下一阶段若要提升自治与可执行性，必须补齐任务链深语义，但它会牵动主链与评测，应放在记忆治理之后推进。
4. **语义转译层（用户输入→任务结构）**  
   - **为什么第四**：依赖更完整的任务引擎与长期记忆，且会引入更复杂的评测与治理边界。
5. **语音 / 对话承接层**  
   - **为什么第五**：输入形态扩展会显著增加变量；在任务/记忆/信号仍需升级前，先扩语音容易稀释主线收口与可复现性。

**明确不建议本阶段直接进入**：advisory 自动 gate / soft-fail 自动接入 / 军工级自治闭环（均会改变裁决权限与运行态，属于后续大阶段）。

---

## §7. 建议最小同步更新

- `docs/PHASE2_STATUS_MATRIX.md`：新增本收束文档条目。  
- （可选）在 `docs/REAL_SCENARIO_PACK_M1_7_DELIVERY.md` 增加一句：**已进入 M1.x consolidation review**（仅状态标注，不改结论口径）。

---

## §8. 本轮是否适合作为 M1.x 阶段收束文档

**适合。** 理由：

- 覆盖你指定的 6 大板块，并用“文档 + 产物”作为证据锚点；  
- 给出了“已闭环/未闭环”表格化清单；  
- 给出了 **Yes/No** 阶段判断与边界；  
- 给出了下一阶段建议的**排序**与“为何不是别的”。

---

## §9. 本轮是否通过

**通过。**

