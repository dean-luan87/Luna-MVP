# Luna Vision — Visual Interpretation & Correction Output v0（解释/纠偏层输出协议）

**文件**：`docs/architecture/vision/LUNA_VISUAL_INTERPRETATION_AND_CORRECTION_OUTPUT_V0.md`  
**性质**：P2-1 解释/纠偏层一期输出协议 v0（可执行接口规范）  

---

## 0. 文档定位（写死）

- 这是 **视角解释/纠偏层（Light Explanation & Correction）** 的一期**输出协议 v0**。
- 目标：定义“解释/纠偏层对中台输出什么候选（candidates）”的统一接口基线。
- 当前不定义：
  - 具体轻量模型选型与落地
  - 模型内部推理细节与算法实现
  - 中台裁决/路由策略
- 当前只定义：
  - **输入边界**、**输出边界**
  - 纠偏循环的能力占位（闭环位置与候选类型）
  - 消费约束（谁能消费什么、谁不能直接消费什么）

---

## 1. 系统角色与职责边界（写死）

### 1.1 解释/纠偏层处于哪里

解释/纠偏层不是检测层，也不是主链裁决层。它位于：
- **YOLO / OCR / 其他前端感知之后**
- **中台消费之前**

### 1.2 解释/纠偏层负责什么

它的职责是（只做候选层）：
1. 融合和解释前端候选（候选合并/对齐/解释性聚合）
2. 检测冲突和不一致（同一对象/文本的冲突、跨源矛盾）
3. 触发重识别/延迟消费/补证候选（以候选形式输出）
4. 输出“更可信的候选”，供中台进一步调度（仍然是候选，不是事实）

### 1.3 解释/纠偏层不负责什么（写死）

- 不直接对用户说话
- 不直接写记忆
- 不直接触发导航
- 不直接写主链正式事实
- 不充当中台裁决器

---

## 2. 输入边界（只定义接口位，不展开实现）

> 说明：以下输入仅是接口位；不等于已经实现。解释/纠偏层未来可消费，但本轮不落代码。

### 2.1 感知输入（Perception Inputs）

- YOLO 候选（对象检测候选，占位）
- OCR 候选（文本候选，占位）
- 其他前端感知候选（深度/分割/跟踪等，占位）

### 2.2 主链/任务输入（Mainline / Task Context）

- 当前任务语境（占位）
- 当前 `proposal.task_action` 或同等级任务上下文（占位）
- 当前中台/主链状态摘要（占位，仅说明存在，不定义结构）

### 2.3 记忆/联网补证输入（占位）

- 记忆摘要（占位）
- 联网补证摘要（占位）

---

## 3. 统一公共 Envelope（解释/纠偏层候选公共包络 v0）

解释/纠偏层对外输出的**所有候选**必须共用一个最小 envelope。  
可部分对齐 P1 的 Consumable Slice 风格，但本 envelope 体现解释/纠偏层特有关注点：**冲突、纠偏、复核建议、上游引用**。

### 3.1 字段列表（v0）

- **candidate_id**：候选唯一标识（字符串）。用于去重、跟踪、回归对比；不代表“事实成立”。
- **candidate_type**：候选类型（见第 4 节最小集合）。用于中台分发与策略归类。
- **source_modules**：产生该候选的模块链路标识数组（字符串列表）。用于可审计与问题定位。
- **upstream_slice_refs**：上游引用（字符串列表），用于指向 P1 可消费切片/原始候选的“引用 id/handle”。  
  - 写死：本字段只做引用，不要求本期定义引用格式。
- **task_relevance**：与当前任务的相关性标记（例如 `unknown|low|high`，v0 只要求字符串）。不等于裁决。
- **stability**：候选稳定性（例如 `unstable|stable`，v0 只要求字符串）。用于提示是否应延迟消费/重识别。
- **confidence**：候选置信度（0~1 浮点）。不用于直接裁决，只供中台策略参考。
- **conflict_detected**：是否检测到冲突（bool）。冲突不等于失败，意味着需要纠偏/复核候选链路。
- **needs_rerecognition**：是否建议重识别/再看/再读（bool）。用于闭环触发占位。
- **needs_confirmation**：是否需要用户确认（bool）。只能被中台用于后续“追问候选”生成；解释层不直接驱动语音。
- **network_verify_recommended**：是否建议联网补证（bool）。写死：不能默认触发，必须中台批准。
- **memory_candidate**：是否作为记忆候选（bool）。写死：不等于写入记忆；必须中台批准后才能进入慢链。
- **consume_priority**：消费优先级（字符串，例如 `low|normal|high`）。供中台排序，不代表抢占主链。
- **lane**：快/慢链建议（字符串，例如 `fast|slow`）。供中台决定是否延迟消费。
- **can_enter_mid_platform**：是否允许进入中台消费面（bool）。v0 默认为候选层入口许可，不代表可直接入主链事实。

### 3.2 时空关联（写死约束）

- 本协议 **不引入任何模块自造的时间/空间字段**。
- 如候选未来需要时空关联，只能通过“引用统一时空锚点”的方式表达（本期不展开锚点结构）。

---

## 4. 最小候选类型集合（一期收敛为 5 类）

> 写死：本期只定义以下 5 类，不扩张更多类型。

### 4.1 stable_object_candidate

- **表示什么**：一个相对稳定、跨帧一致性较好的对象候选（仍为候选，不是事实）。
- **通常由什么输入组合而来**：YOLO/跟踪候选 + 稳定性评估（占位）。
- **能被谁消费**：中台（可消费）；其他模块必须经中台裁决后再获得派发。
- **当前不允许它直接做什么**：不允许直接触发语音/记忆/导航；不允许直接材料化主链事实。

### 4.2 ocr_bound_candidate

- **表示什么**：OCR 文本候选与其“绑定对象/区域/上下文”的候选关系（例如牌子文字↔实体/区域），仍是候选。
- **通常由什么输入组合而来**：OCR 候选 + 目标区域/对象候选对齐（占位）。
- **能被谁消费**：中台（可消费）；联网补证/记忆沉淀需中台批准后进入慢链。
- **当前不允许它直接做什么**：不允许直接播报“确定读到了什么”；不允许直接写记忆事实。

### 4.3 needs_rerecognition_candidate（纠偏闭环关键类型）

- **表示什么**：当前结果“高价值但不够稳”，建议再看/再读/再验证的候选。  
  - 写死：它**不代表失败**；它代表“值得投入一次重识别/补证/延迟消费”的信号。
- **通常由什么输入组合而来**：YOLO↔OCR 冲突、跨帧不一致、低稳但任务相关性高（占位）。
- **能被谁消费**：中台（可消费，且是未来闭环调度的主要触发输入）。
- **当前不允许它直接做什么**：不允许解释层直接触发重识别执行；只能输出候选，由中台决定是否调度。

### 4.4 task_relevant_candidate

- **表示什么**：与当前任务强相关的候选（对象/文本/区域/风险提示等的“任务相关聚合候选”）。
- **通常由什么输入组合而来**：前端候选 + 任务上下文（proposal/task state，占位）对齐。
- **能被谁消费**：中台（可消费）。
- **当前不允许它直接做什么**：不允许直接生成语音文本；不允许直接启动导航/执行。

### 4.5 environment_fragment_candidate

- **表示什么**：可进入慢链“沉淀/建模”评估的环境碎片候选（可撤销、可复核的候选层输入）。
- **通常由什么输入组合而来**：多源候选聚合出的环境片段（占位），或稳定对象/区域候选的聚合。
- **能被谁消费**：中台（可消费）；记忆系统只能在中台批准后接收进入慢链。
- **当前不允许它直接做什么**：不允许直接写记忆事实；不允许越过中台治理。

---

## 5. Recognition → Correction → Re-recognition Loop（占位）

> 本节将“识别→纠偏→重识别”的闭环写成正式能力占位，只定义位置与作用，不展开调度策略。

最小闭环逻辑（v0）：
1. 前端识别给出原始候选（YOLO/OCR/跟踪等，占位输入）
2. 解释/纠偏层发现：冲突 / 低稳 / 高价值不确定
3. 解释/纠偏层不直接下结论，而是产出候选：
   - `needs_rerecognition_candidate`（建议重识别/再看/再读）
   - `network_verify_recommended == true` 的候选（若适用，仅建议，不触发）
4. 中台未来决定：是否重识别、是否补证、是否延迟消费、是否转入慢链

写死：
- 闭环的“执行权”在中台，不在解释/纠偏层。

---

## 6. 谁能消费什么（写死）

### 6.1 中台（Mid-Platform）

- **可消费**：全部解释/纠偏层候选（本协议输出）。
- **写死**：中台是唯一调度路由器。

### 6.2 语音（Voice）

- **不可直接消费**：解释/纠偏层原始候选。
- **只能消费**：中台裁决后的“语音候选/语音输出候选”（本协议不定义语音候选结构）。

### 6.3 记忆（Memory）

- **不能直接吃全部候选**。
- **只应接收**：如 `environment_fragment_candidate` 等，经中台批准的可沉淀候选进入慢链。

### 6.4 联网补证（Network Evidence）

- **不能默认触发**。
- **只应在中台批准后**处理 `network_verify_recommended == true` 的候选。

### 6.5 导航链（Navigation）

- **不能直接消费**：解释/纠偏层原始候选。
- **必须经过**：中台与主链事实层过滤后，才能进入导航相关链路。

---

## 7. 当前不做（写死）

- 不做解释层直接裁决
- 不做解释层直接驱动语音
- 不做解释层直接写记忆
- 不做解释层直接启动导航
- 不做轻量模型直接替代 YOLO/OCR
- 不做完整在线多模态世界理解
- 不做解释层直接材料化主链事实

---

## 8. JSON 样例（仅服务 schema 说明）

### 8.1 stable_object_candidate（样例）

```json
{
  "candidate_id": "cand_obj_001",
  "candidate_type": "stable_object_candidate",
  "source_modules": ["vision.explain_correct_v0"],
  "upstream_slice_refs": ["slice_obj_track_42"],
  "task_relevance": "unknown",
  "stability": "stable",
  "confidence": 0.78,
  "conflict_detected": false,
  "needs_rerecognition": false,
  "needs_confirmation": false,
  "network_verify_recommended": false,
  "memory_candidate": false,
  "consume_priority": "normal",
  "lane": "fast",
  "can_enter_mid_platform": true,
  "payload": {
    "object_label_candidate": "unknown",
    "track_candidate_id": "track_42"
  }
}
```

### 8.2 needs_rerecognition_candidate（样例）

```json
{
  "candidate_id": "cand_rerec_001",
  "candidate_type": "needs_rerecognition_candidate",
  "source_modules": ["vision.explain_correct_v0"],
  "upstream_slice_refs": ["slice_ocr_7", "slice_yolo_12"],
  "task_relevance": "high",
  "stability": "unstable",
  "confidence": 0.42,
  "conflict_detected": true,
  "needs_rerecognition": true,
  "needs_confirmation": false,
  "network_verify_recommended": false,
  "memory_candidate": false,
  "consume_priority": "high",
  "lane": "fast",
  "can_enter_mid_platform": true,
  "payload": {
    "conflict_summary": "ocr_vs_object_label_mismatch",
    "rerecognition_hint": "recheck_text_region_or_wait_more_frames"
  }
}
```

### 8.3 environment_fragment_candidate（样例）

```json
{
  "candidate_id": "cand_env_frag_001",
  "candidate_type": "environment_fragment_candidate",
  "source_modules": ["vision.explain_correct_v0"],
  "upstream_slice_refs": ["slice_env_003"],
  "task_relevance": "unknown",
  "stability": "unstable",
  "confidence": 0.55,
  "conflict_detected": false,
  "needs_rerecognition": false,
  "needs_confirmation": true,
  "network_verify_recommended": false,
  "memory_candidate": true,
  "consume_priority": "low",
  "lane": "slow",
  "can_enter_mid_platform": true,
  "payload": {
    "fragment_kind": "place_feature_candidate",
    "fragment_note": "needs_mid_platform_approval_before_memory_write"
  }
}
```

---

## 9. 模块打标标准（占位）

- **定位**：定义解释/纠偏层候选的统一打标口径（candidate_type、conflict、stability、lane、priority 等）。
- **覆盖范围**：解释/纠偏层对外输出的所有候选 envelope 字段语义与允许值范围。
- **当前状态**：占位；本期不展开具体策略与枚举全集。

## 10. 信息处理超时方案（占位）

- **定位**：定义解释/纠偏层在快/慢链下的超时处理接口面（降级为候选、延迟消费建议、重识别建议等）。
- **覆盖范围**：候选产出超时、上游候选到达延迟、跨帧等待窗口等。
- **当前状态**：占位；本期不展开具体超时策略。

## 11. 模块报错处理方案（占位）

- **定位**：定义解释/纠偏层错误的对外可观测面（错误类型、严重性、是否影响候选产出）。
- **覆盖范围**：上游输入缺失/格式错误、内部处理异常、输出候选失败等。
- **当前状态**：占位；本期不展开具体错误码与恢复策略。

