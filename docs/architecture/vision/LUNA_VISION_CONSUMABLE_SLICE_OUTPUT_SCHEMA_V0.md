# Luna Vision — Consumable Slice Output Schema v0（可消费切片输出规范）

**文件**：`docs/architecture/vision/LUNA_VISION_CONSUMABLE_SLICE_OUTPUT_SCHEMA_V0.md`  
**性质**：视角模块对外输出的统一候选协议 v0（接口规范，可执行/可校验；不展开实现细节）  

---

## 1) 文档定位（写死）

- 这是视角模块对外输出的**统一候选协议 v0**。
- 目标：定义什么样的视觉结果可以作为“**可消费切片（Consumable Slice）**”进入中台，供后续：
  - 中台消费与调度
  - 解释层输出承载
  - 快/慢链分流建议
  - 记忆候选沉淀
- 当前不定义：
  - 具体模型实现
  - 真实视觉识别效果
  - 最终世界模型
- 当前只定义：
  - 输出规范（schema）
  - 分层边界
  - 消费约束（谁能消费什么）

---

## 2) “可消费切片”定义（写死）

**可消费切片（Consumable Slice）**  
是从连续视角底座中提炼出来、可被中台进一步调度消费的**结构化候选单元**。  
它用于“调度与协作”，不用于“直接裁决事实”。

三条边界（写死）：
1. **不是连续视角本体**（不是原始视频流/连续帧流）。  
2. **不是最终事实**（只能是候选与调度输入）。  
3. **不是直接用户播报内容**（不得直接作为可说话输出）。

---

## 3) 统一公共 Envelope（最小公共字段集合）

> 说明：以下字段为“统一公共 Envelope”。字段语义写到“够调度使用”为止，不展开具体策略与阈值。  
> 禁止：在 v0 中引入模块自造的系统级时间/空间锚点细节实现。若需引用，后续必须通过统一时空锚点提供**引用**而非自造事实。

### 3.1 字段列表（必须具备）

- **slice_id**（string）  
  - **用途**：切片唯一标识，用于去重、追踪、回归验证与跨模块引用。

- **slice_type**（string enum）  
  - **用途**：切片类型（见 §4 最小类型集合），用于中台调度与消费权限控制。

- **source_modules**（string[]）  
  - **用途**：产生该切片的模块来源列表（例如 `yolo`/`ocr`/`tracker`/`light_explainer`/`slice_builder`）。  
  - **约束**：只表达来源，不表达“事实成立”。

- **task_relevance**（string enum）  
  - **用途**：与当前任务的相关性等级（调度建议）。  
  - **建议枚举**：`low | medium | high`

- **stability**（string enum）  
  - **用途**：切片稳定性/持续性建议（调度建议：是否需要继续观察）。  
  - **建议枚举**：`low | medium | high`

- **confidence**（number, 0..1）  
  - **用途**：该切片作为候选的置信度（调度建议）。  
  - **边界**：不是最终事实概率，不可直接用作主链裁决依据。

- **needs_rerecognition**（boolean）  
  - **用途**：是否建议触发重识别/复核（例如更高分辨率、二次识别、重新取证）。  
  - **边界**：只是建议，不触发执行；最终由中台决定。

- **needs_confirmation**（boolean）  
  - **用途**：是否需要用户确认/澄清才能推进（例如候选不唯一、意图不明）。  
  - **边界**：这是“阻断/追问建议”，不等于对话策略实现。

- **network_allowed**（boolean）  
  - **用途**：是否允许联网补证（调度建议）。  
  - **边界**：不等于“会联网”；是否联网由中台审批/调度决定。

- **memory_worthy**（boolean）  
  - **用途**：是否具有沉淀为长期候选的价值（调度建议）。  
  - **边界**：不等于直接写记忆事实；记忆消费必须受中台治理与后续规则约束。

- **consume_priority**（string enum）  
  - **用途**：中台消费优先级建议（决定快处理/先处理）。  
  - **建议枚举**：`low | medium | high | critical`

- **lane**（string enum）  
  - **用途**：快链/慢链调度建议（见 §6）。  
  - **枚举**：`fast | slow`

- **can_enter_mainline**（boolean）  
  - **用途**：该切片是否满足“可进入主链被中台消费”的最低条件。  
  - **边界**：`true` 只表示“可被中台消费”，不表示“可裁决为事实/可执行”。

---

## 4) 最小切片类型集合（一期收敛为 5 类）

> v0 禁止扩太多类型；新增类型必须走专题与 freeze。

### 4.1 risk_slice

- **表示什么**：风险相关候选（安全/碰撞/危险环境/行为纠偏相关）。
- **典型来源**：连续观察 + 跟踪 + 前端感知（YOLO/深度/运动）+ 轻量纠偏候选（仍是候选）。
- **可被谁消费**：中台（必需）；语音（仅在中台裁决后生成语音候选）；联网补证（默认不触发）。
- **当前不允许它直接做什么**：不允许直接触发任务执行/导航启动；不允许直接生成用户播报结论。

### 4.2 task_target_slice

- **表示什么**：当前任务关键目标候选（例如“正在找的目标/需要对齐的目标/关键证据候选”）。
- **典型来源**：解释/纠偏层候选重排；连续观察的稳定目标；前端感知候选聚合。
- **可被谁消费**：中台；语音（经中台裁决后触发追问/提示候选）；慢链复核（可选）。
- **当前不允许它直接做什么**：不允许单独成为主链事实；不允许直接写记忆事实。

### 4.3 ocr_related_slice

- **表示什么**：与文字识别相关的候选（需要 OCR、OCR 结果需复核、或文字证据是关键）。
- **典型来源**：OCR 候选（非原始块）；解释层对 OCR 的“需要/复核”建议；连续观察发现文字相关触发。
- **可被谁消费**：中台；慢链（高精复核/补证）；语音（经中台裁决后生成“请对准/请放大/请再拍”的候选）。
- **当前不允许它直接做什么**：不允许 OCR 原始块直接入主链；不允许 OCR 文本直接当作最终事实播报。

### 4.4 environment_fragment_slice

- **表示什么**：环境碎片候选（可沉淀、可复用的环境片段候选，面向长期建模/记忆候选）。
- **典型来源**：连续观察的稳定环境限制变量；解释层对环境碎片的候选总结；慢链沉淀候选生成。
- **可被谁消费**：中台；记忆（仅允许这一类及其受限子集）；慢链建模更新。
- **当前不允许它直接做什么**：不允许直接写为记忆事实；只能作为候选进入后续升格规则。

### 4.5 navigation_need_candidate

- **表示什么**：导航需求候选（“可能需要导航/方向指引”的候选信号，用于中台分流建议）。
- **典型来源**：任务上下文 + 视角候选（例如道路/入口/路径相关线索）；解释层输出的“需要导航”候选。
- **可被谁消费**：中台（用于 Need-Navigation Routing 的观测层）；语音（经中台裁决后生成澄清/引导候选）。
- **当前不允许它直接做什么**：不允许直接启动导航；不允许绕过语音侧的目标绑定事实链。

---

## 5) 谁能消费什么（边界写死）

### 5.1 中台（Mid-Platform）

- **可消费**：全部切片类型（本 schema 内定义的所有 `slice_type`）。
- **职责**：最终调度与路由（唯一消费路由器）。
- **写死**：中台是唯一消费调度器；其他模块不得绕过中台直接消费切片并驱动行为。

### 5.2 语音（Voice）

- **禁止**：语音链不得直接消费原始视觉切片（不得把切片当作“可说话事实”）。
- **允许**：语音只能消费**经中台裁决后的语音候选**（例如“需要追问/需要提醒”的候选），而不是直接消费切片本体。

### 5.3 记忆（Memory）

- **禁止**：记忆不能直接吃所有切片。
- **允许**：只允许消费 `environment_fragment_slice` 等“可沉淀候选”子集，并必须遵守后续“候选→升格→事实”的规则与治理。

### 5.4 联网补证（Network Evidence）

- **禁止**：不能默认触发联网补证。
- **允许**：只允许消费中台批准的“高价值不确定候选”，并受 `network_allowed` 与后续审批/预算/超时规则约束。

---

## 6) 快链 / 慢链分工口径（lane 字段语义）

### fast

适合：
- 风险相关（risk_slice）
- 行为纠偏相关
- 当前任务关键候选（task_target_slice）
- 需要快速追问的候选

### slow

适合：
- OCR 高精复核
- 联网补证
- 环境碎片沉淀
- 建模更新
- 二次解释/纠偏

写死：
- `lane` 是**调度建议**，不等于最终裁决；最终进入快链/慢链由中台决定。

---

## 7) 哪些不能进入主链（写死：不属于 Consumable Slice）

以下内容不属于 Consumable Slice，禁止以切片形式进入主链：
- 原始连续视频流
- YOLO 原始检测框结果
- OCR 原始文本块结果
- 未经筛选的解释层原始输出
- 视觉直接生成的自然语言结论（“最终答案句”）

---

## 8) 最小 JSON 样例（仅示例，不含实现逻辑）

### 8.1 公共 envelope 示例（risk_slice）

```json
{
  "slice_id": "slice_001",
  "slice_type": "risk_slice",
  "source_modules": ["yolo", "tracker"],
  "task_relevance": "high",
  "stability": "medium",
  "confidence": 0.82,
  "needs_rerecognition": false,
  "needs_confirmation": false,
  "network_allowed": false,
  "memory_worthy": false,
  "consume_priority": "high",
  "lane": "fast",
  "can_enter_mainline": true
}
```

### 8.2 ocr_related_slice 示例

```json
{
  "slice_id": "slice_101",
  "slice_type": "ocr_related_slice",
  "source_modules": ["ocr", "slice_builder"],
  "task_relevance": "high",
  "stability": "low",
  "confidence": 0.55,
  "needs_rerecognition": true,
  "needs_confirmation": false,
  "network_allowed": false,
  "memory_worthy": false,
  "consume_priority": "medium",
  "lane": "slow",
  "can_enter_mainline": true
}
```

### 8.3 environment_fragment_slice 示例

```json
{
  "slice_id": "slice_201",
  "slice_type": "environment_fragment_slice",
  "source_modules": ["continuous_observer", "slice_builder"],
  "task_relevance": "medium",
  "stability": "high",
  "confidence": 0.66,
  "needs_rerecognition": false,
  "needs_confirmation": true,
  "network_allowed": false,
  "memory_worthy": true,
  "consume_priority": "low",
  "lane": "slow",
  "can_enter_mainline": true
}
```

### 8.4 navigation_need_candidate 示例

```json
{
  "slice_id": "slice_301",
  "slice_type": "navigation_need_candidate",
  "source_modules": ["light_explainer", "slice_builder"],
  "task_relevance": "high",
  "stability": "medium",
  "confidence": 0.6,
  "needs_rerecognition": false,
  "needs_confirmation": true,
  "network_allowed": false,
  "memory_worthy": false,
  "consume_priority": "medium",
  "lane": "fast",
  "can_enter_mainline": true
}
```

---

## 9) 当前不做（写死）

- 不做视觉直接裁决
- 不做视觉直接驱动语音
- 不做视觉直接写记忆
- 不做连续视角全量进入主链
- 不做完整 3D 建模 schema
- 不做真实地图接入协议
- 不做最终事实层 schema

---

## 10) 模块打标标准（占位）

- **定位**：为切片类型、候选分级、风险级、任务相关性、可消费等级建立统一打标标准。
- **覆盖范围**：slice_type 扩展纪律、字段分级口径、跨模块一致性。
- **当前未展开**：本 v0 不提供具体打标表与阈值策略。

---

## 11) 信息处理超时方案（占位）

- **定位**：为切片生成/复核/补证定义超时与过期处理口径，避免主链被拖死。
- **覆盖范围**：fast/slow lane 超时、补证超时、过期切片丢弃纪律。
- **当前未展开**：本 v0 不提供具体超时参数与实现策略。

---

## 12) 模块报错处理方案（占位）

- **定位**：定义切片生成链各层报错与降级处理口径（可观测、可回退）。
- **覆盖范围**：前端感知异常、OCR 失败、解释层异常、切片构建异常、中台接口异常。
- **当前未展开**：本 v0 不提供具体错误分级与降级路径。

