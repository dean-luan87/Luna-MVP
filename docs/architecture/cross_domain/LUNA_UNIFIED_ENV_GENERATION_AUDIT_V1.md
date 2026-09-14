# unified env 生成机制审计（V1）

## 1. 当前问题回顾（基于两轮窗口）

两轮窗口（V1 回放、V2 snapshot 真实主线）得到的稳定信号是：

- **candidate 层稳定**：`scene_candidate_match_rate = 1.0`
- **family 层不稳**：`scene_family_match_rate = 0.8`
- **错配不随机**：主要集中在同一类可解释模式（字符串诱导的家族错配）
- **补缺收益暂不强**：V2 `unified_helpful_fill_count = 0`（V1 曾出现 1，但不稳定）

因此当前最值得挖的不是“再跑更多窗口等它变好”，而是：**family 的生成机制是否把弱线索当成强定类依据**。

---

## 2. family 生成路径审计（代码事实）

统一 family 的生成逻辑位于 `capabilities/cross_domain/context/unified_env_summary_v1.py::_classify_scene_family`。

### 2.1 输入

- `raw_scene_candidate`（字符串）：最终会被 `_norm_scene` 归一化为小写、去空格、空值回落 `unknown`
- `raw_family_hint`（可选字符串）：用于补缺的弱提示

### 2.2 强判定（当前实现）

当前实现将 `raw_scene_candidate` 直接做**关键词匹配**，得到：

- `is_retail` 为真条件（任一满足）：
  - candidate 包含 `retail_markers = ("retail_shelf","retail_aisle","retail_shop","retail_store","grocery_aisle")`
  - 或 candidate 含 `"retail"` 且不含 `"walk"` / `"walkway"`
- `is_walkway` 为真条件（任一满足）：
  - candidate 包含 `walkway_markers = ("outdoor_walkway","walkway","sidewalk","pedestrian","path_outdoor")`
  - 或 candidate 等于 `"outdoor"` 且不含 `"retail"`

并据此做强判定：

- `is_retail and is_walkway` → `scene_family="unknown"` + note `family_keyword_conflict`
- `is_retail` → `scene_family="retail"`（**直接定类**）
- `is_walkway` → `scene_family="walkway"`（**直接定类**）
- 否则进入 hint/unknown 逻辑

### 2.3 弱补充（当前实现）

当且仅当 candidate 无法判定为 retail/walkway 时：

- `raw_family_hint in ("walkway","retail")` → `scene_family=hint` + note `family_hint_disambiguation`
- 否则 → `scene_family="unknown"`

### 2.4 unknown 回退（当前实现）

unknown 回退本身是“保守”的：判不出来就 `unknown`。但由于 **retail/walkway 的关键词判定过于直接**，unknown 的有效覆盖面会被压缩。

---

## 3. candidate → family 映射审计（是否过度绑定）

### 3.1 结论：当前映射 **过度绑定**

family 生成完全依赖 `scene_candidate` 字符串（以及候选 hint），且对 retail/walkway 命中采取“**直推定类**”。

这意味着：

- **candidate 可以激进**（它只是候选），但当前实现会把 candidate 的“词命中”直接上升为 **family 定类**。
- 一旦 candidate 字符串被污染（跨域标签、误写、调试注入等），family 会被“过早定类”，形成你观察到的 **P0 字符串诱导错配**。

### 3.2 与两轮错配的对应关系（证据闭环）

两轮错配样本均呈现同一形态：

- `vertical_source=sidewalk`
- `scene_candidate="retail_shelf"`（或等价 retail marker）
- unified 依据 `is_retail=True` 直接定类 `retail`
- 垂直侧的“期望家族”（保守推导）为 `unknown`

该错配不是噪声飘动，而是 **映射规则的确定性触发**。

---

## 4. hint / 关键词 / unknown 回退审计（优先级是否合理）

### 4.1 hint 优先级

当前实现符合“hint 只补缺”的原则：只有在 `is_retail/is_walkway` 均为 false 时才用 hint。

因此，**当前已观察到的 P0 错配，不是 hint 误导导致**，而是关键词强判定过早。

### 4.2 关键词是否被当成强证据

是的。当前 `is_retail/is_walkway` 的判断是 **强证据**（直接决定 family）。

这与“字符串命中不等于 family 成立”的原则冲突，也是当前最需要收紧的点。

### 4.3 unknown 是否吝啬

unknown 分支本身不吝啬；真正的问题是：在当前实现里，**过宽的关键词强判定**让 unknown 回退很难生效。

---

## 5. 审计结论

### 5.1 更像数据问题还是生成机制问题？

**更像生成机制问题（高置信）**：

- 错配模式可重复、可解释、可由规则确定性触发
- candidate 稳但 family 不稳，符合“过早定类/过紧绑定”的典型症状

### 5.2 最优先该收紧哪一层？

优先收紧 **family 的强判定规则**，而不是改 candidate 或继续扩大窗口。

建议的收紧方向（不在本文件实现，作为审计结论给后续路线 A 输入）：

- **把 retail/walkway 的关键词命中从“直接定类”改为“保守建议”**：弱证据不足时回落 `unknown`
- **增加来源域护栏**：当 shadow 输入命中来源为 sidewalk（或未来可见 source 标记为 sidewalk），即便 candidate 带 retail 字符串，也不应直接定类为 retail（至少先回落 unknown / ambiguous）
- **family 比 candidate 更保守**：把“可疑跨域字符串”优先压到 unknown，而不是硬定 family

---

## 一句话收束

两轮窗口的 family 错配更像是 `scene_family` 生成规则“过早定类、过紧绑定”的机制问题；先把 family 的强判定收紧到更保守，再继续双轨观察验证是否显著提升。

