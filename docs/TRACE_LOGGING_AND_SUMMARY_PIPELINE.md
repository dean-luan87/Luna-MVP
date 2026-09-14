# 日志落地与总结分层（Trace, Logging & Summary Pipeline）— M0

**文件**：`docs/TRACE_LOGGING_AND_SUMMARY_PIPELINE.md`  
**版本**：M0（日志/总结专题定稿）  
**上位文档**：`docs/LUNA_MAINLINE_SHAPE_BLUEPRINT.md`  
**运行约束**：`docs/DECISION_MAINLINE_ARCHITECTURE.md`、`docs/WHITEBOX_OBSERVATION_ARCHITECTURE.md`  
**工程串联**：`docs/MAINLINE_WHITEBOX_LOG_CHAIN_RULE.md`

**本文不写**：JSON schema、API、日志文件格式、Console UI、benchmark/triage 代码细节、图书馆正式接入实现、真实场景扩包。

**最小工程接入状态（M0）**：`scheduled_source_state` 已进入 frame/JSONL/聚合链可见摘要（见 `docs/SCHEDULED_SOURCE_STATE_MINIMAL_INSERT_M0.md`）。

**Trace × Summary 工程分层（M0.2）**：已增加 `run_summary_reference`（含 `raw_trace_layer_snapshot` / `structured_event_layer_snapshot`）与聚合层三层 one-liner，形成最小 **运行总结入口**（派生自 trace，非替代黑匣子）。交付见 `docs/TRACE_SUMMARY_SEPARATION_M0_2.md`。

**任务链进度摘要增强（M0.1）**：`task_chain_progress_summary` 与 `task_position_*` 字段随 frame 落地；`summary_brief` 中 `task=` 片段可区分主任务推进提示、局部成功风险、恢复/插入语义（见 `docs/TASK_CHAIN_POSITION_EXPLANATION_ALIGNMENT_M0_1.md`）。

**记忆调用解释（M0.3）**：`memory_invocation_explanation` 与增强后的 `memory_usage_summary`（`build_memory_usage_summary_line`）随 frame 落日志；`summary_brief` 叙事骨架含 `mem=` 段（见 `docs/MEMORY_INVOCATION_EXPLANATION_M0_3.md`）。

**主链状态/阶段显式化（M0.4）**：`mainline_state_snapshot` 随 frame/JSONL 落地；`run_summary_reference` 含 `mainline_state_summary`，见 `docs/MAINLINE_STATE_PHASE_EXPLICITNESS_M0_4.md`。

**Summary × 后处理边界契约（M0.5）**：`post_processing_summary_entry` 由 `run_summary_reference` 只读派生，定义后处理合法入口与回溯提示；**不**内含 Raw/Structured 原件全文，见 `docs/SUMMARY_POST_PROCESSING_BOUNDARY_CONTRACT_M0_5.md`。

**主线叙事口径对齐（M0.6）**：`summary_brief` / `mainline_narrative_brief` 对齐统一骨架 `ctx→source→task→mem→mainline→closure→risk`，并与 `post_processing_summary_entry.narrative_readable` 同口径（见 `docs/MAINLINE_NARRATIVE_ALIGNMENT_M0_6.md`）。

---

## §1. 文档目标与适用范围

### 1.1 解决的问题

- **日志链**不是普通打点，而是**黑匣子**体系：原样、可追溯、不可被总结篡改。  
- **运行总结链**不是日志替代品，而是**轻提炼层**（summary feed）。  
- **原始运行记录**、**结构化事件**、**摘要引用入口**、**总结链产出**须**分层**；图书馆与记忆**不得**直接吞原始运行流。

### 1.2 讨论范围

| 在范围内 | 不在范围内 |
|----------|------------|
| 日志链语义与三层结构 | 具体 JSON schema / 文件格式 |
| 总结链与 summary-first | 图书馆内部存储与检索实现 |
| 后处理如何接 summary 与 trace | 后处理归因算法 |
| 主线—白盒—日志同链（日志视角） | 白盒 UI |
| 对象语义：Trace / Event / Summary | API 设计与字段表 |

### 1.3 约束效力

后续日志落地、总结生成、后处理与图书馆接入须以本文为约束；与总纲冲突以**总纲**为准。

---

## §2. 日志落地链的正式定义

**日志落地链** = 对**决策运行主链**全过程进行**原样落地**、**可追溯**、**不可被总结层篡改**的黑匣子记录体系。

**只负责**：

- **记录**；**保留证据**；**支持回溯**；  
- 支撑 **benchmark / triage / rebaseline / 后处理** 等读**同一套**落地事实的需求。

**不负责**：

- **解释**、**归纳结论**、**美化**；  
- **干预**主链运行或控制流；  
- **代替**总结链产出摘要产品。

### 写死

# 日志链是证据链，不是解释链

---

## §3. 日志链的三层结构

三层均属**日志链语义**；实现可映射为多种载体（如 frame / JSONL / trace 文件），**不得**在语义上混为「总结结论」。

### 3.1 原始运行日志层（Raw Trace Layer）

**记录**（与主链、总纲一致）：

- 主链**真实过程**；**数据源状态**（整理后的调度事实）；  
- **记忆片段调用**相关事实；**收口与恢复**；**结果回流**。

**不做解释**。

**强调**：本层为**黑匣子原件**承载面；**不允许**被总结层**污染或覆盖语义**。

### 3.2 结构化事件层（Structured Event Layer）

将黑匣子中的关键事实整理为**事件**（主链事件、源调度事件、记忆调用事件、收口事件、治理 reserve 事件等，语义见 `WHITEBOX_OBSERVATION_ARCHITECTURE.md` §9）。

**强调**：

- **仍属于日志链** — 是**结构化记录**，不是「总结结论」或「归纳判断」。  
- 事件用于检索、对齐、回放与链间校验，**不**等同于后处理的归类结论。

### 3.3 摘要引用层（Summary Reference Layer）

提供供**总结链**、**后处理链**、**图书馆**读取的**摘要入口与引用关系**：**引用而不替代**黑匣子；支持快速浏览、定位、下钻。

**强调**：

- **不是**运行总结链本体；**不是**最终 summary 产品定义的全部。  
- **必须**能回溯到**原始日志**（黑匣子）。

---

## §4. 运行总结链的正式定义

**运行总结链** = 对**一次运行**（或约定周期）结果的**轻提炼层**。

**面向**：后置信息处理链；图书馆的**读入口**；归类与分析入口。

**产出形态**（概念，非 schema）：

- 记忆使用总结；行为逻辑总结；问题摘要；归类入口摘要。

**硬规则**：

- **不能替代黑匣子**；**不能**跳过日志链从「脑补解释」直接生成；  
- **是**后处理与图书馆的**入口层之一**，**不是**证据本体。

---

## §5. 日志链与总结链的严格分离

1. **日志链只记录，不解释。**  
2. **总结链只提炼，不冒充原始证据。**  
3. **总结链必须基于日志链**（及允许的引用层），**不得**无锚编造。  
4. **总结不能反写、污染日志**原件语义。  
5. **日志不能**为「好总结」而**干预**主链（见总纲：日志不干预运行）。

### 写死

# 日志链 = 黑匣子

# 总结链 = 提炼层

# 二者严格分离

---

## §6. summary-first 原则（图书馆读序）

- **图书馆默认先读 summary feed**（运行总结链产出的摘要面）。  
- **图书馆不直接吞原始黑匣子**全量。  
- 需要时，按摘要入口**回溯**：结构化事件 → 白盒解释素材 → 原始日志。

### 写死

# 图书馆默认先吃总结，再按需回溯详细过程

**理由（架构）**：防止图书馆沦为**原始日志垃圾场**；提高归类效率；**降低噪声扩散与信息污染**；保持**外部器官**的可治理性（总纲 §E）。

---

## §7. 后处理链如何接 summary 与 trace

- **后处理链优先**接收 **summary feed** 作为**归类与分析入口**。  
- **必要时下钻**读取：**structured event**、**raw trace**、**白盒解释**（白盒不是证据本体，但可辅助下钻）。  
- 后处理负责：**分类、归因、模式提炼、去向决策**（算法不在本文）。

**硬规则**：

- **不能**跳过已落地日志链，直接拿**未落地瞬时残影**当作唯一依据。

### 写死

# 后处理链读的是「已落地可复盘信息」，不是瞬时运行残影

---

## §8. 记忆片段调用在日志与总结中的双重要求

### 8.1 日志链中须记录（概念清单）

- 是否调用记忆片段；**哪个/哪类**；**调用时机**；  
- **选中依据**；**实际采用的内容**；**使用逻辑**；  
- **未选其他片段的原因**（若可叙述）。

### 8.2 总结链中至少须有

- 本次**记忆使用摘要**；  
- 记忆是**帮助**主链还是**偏移风险**；  
- 是否**值得进入**后处理分析（入口标记，非结论）。

### 写死

# 记忆调用既要进黑匣子，也要进入总结摘要

（与白盒 `WHITEBOX_OBSERVATION_ARCHITECTURE.md` §8 可解释要求同链。）

---

## §9. 主线—白盒—日志的一致性要求（日志视角）

### 9.1 对主链

- 日志须**原样**记录主链关键步骤；**不能**「记录一套、运行一套」。

### 9.2 对白盒

- 白盒须能**回指**日志证据；日志须能**校验**白盒是否忠实于主链事实；**白盒不能替代**日志原件。

### 9.3 对 benchmark / triage / rebaseline

- 须读取**同一套**真实落地结果；**禁止**从「仅 Console 摘要」直接构建工程判断。

### 写死

# 主线真实运行

# 白盒真实解释

# 日志真实落地

---

## §10. 日志链与总结链的对象分层（仅概念，无 schema）

| 对象类型 | 语义 | 备注 |
|----------|------|------|
| **Trace / Record** | 原始记录（黑匣子） | 证据本体 |
| **Event** | 结构化事件 | 仍属日志链，非总结结论 |
| **Summary / Digest** | 摘要提炼 | 运行总结链产出；入口用 |

**说明**：

- **后处理**接收 **summary + trace** 的组合（按授权与下钻策略）。  
- **图书馆**默认先接 **summary**。  
- **记忆**：**不**直接接 raw trace（总纲）；**须经**代谢后的路径。

---

## §11. 与其他专题文档的关系

| 文档 | 关系 |
|------|------|
| `LUNA_MAINLINE_SHAPE_BLUEPRINT.md` | 上位总纲；日志/总结/图书馆分离 |
| `DECISION_MAINLINE_ARCHITECTURE.md` | 日志观察对象的**主链**基础 |
| `WHITEBOX_OBSERVATION_ARCHITECTURE.md` | 白盒与日志**边界**；白盒不替代证据 |
| `LIBRARY_MEMORY_AND_GOVERNANCE_ARCHITECTURE.md` | summary/trace/后处理/图书馆/记忆**去向** |

---

## §12. 当前 reserve 与未来扩展位

下列方向**保留**、**本文不展开实现**：

- 更细的 trace 粒度；更丰富的结构化事件类型；  
- summary 的多层压缩策略；  
- 图书馆与后处理的**更细权限**分层；  
- 污染抵抗 / 线程观察的**专门日志通道**；  
- Whitebox Plus 对日志链的**深度利用**。

---

## 修订记录

- **M0**：按 §1–§12 正式定稿日志落地与总结分层；取代原章节骨架。
