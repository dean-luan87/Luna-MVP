# 主线 2 第二阶段：骨架过滤 M0 交付说明

**依据**：SPATIAL_SKELETON_SYSTEM_CONSTITUTION.md v1.0 + Skeleton Mix M0  
**目标**：在 Skeleton Mix 基础上增加最小骨架感知过滤层，使当前骨架配比影响“哪些空间信息保留、哪些降权”；仅作用于空间结构保留策略，不直接控制 detector/OCR。

---

## 1. 修改文件清单

| 文件 | 变更摘要 |
|------|----------|
| `decision_monitor/skeleton_filter.py` | **新建**。SkeletonFilterResult（keep_region_types、suppress_region_types、keep_anchor_priority、suppress_detail_level、granularity_bias、filter_reason）；build_skeleton_filter(mix) 按 dominant_skeleton 与权重规则生成。 |
| `decision_monitor/schema.py` | 引入 SkeletonFilterResult；DecisionMonitorFrame 新增 skeleton_filter。 |
| `decision_monitor/builder.py` | 引入 skeleton_filter；build 中在 mix 之后调用 build_skeleton_filter(mix)，写入 frame.skeleton_filter。 |
| `runtime/context.py` | 新增 skeleton_filter_reason、skeleton_filter_keep、skeleton_filter_suppress、skeleton_filter_granularity。 |
| `main.py` | 决策显示器块内，将 frame.skeleton_filter 写入 runtime_ctx（keep/suppress 为逗号分隔字符串）。 |
| `tools/decision_monitor_viewer.py` | 新增「骨架过滤 / Skeleton Filter (M0)」卡片：保留/压低、粒度、锚点优先、原因；sections 增加 skeleton_filter。 |
| `decision_monitor/CONTRACT.md` | 补充 skeleton_filter（骨架过滤 M0）说明与预留边界。 |

---

## 2. Skeleton Filter 数据结构说明

| 字段 | 类型 | 含义 |
|------|------|------|
| keep_region_types | List[str] | 建议保留的区域/结构类型（如 traversable_region、risk_region、anchor、portal、segment 等） |
| suppress_region_types | List[str] | 建议压低的类型（如 fine_interaction_detail、far_decoration、long_path_detail 等） |
| keep_anchor_priority | str | 锚点保留优先级：path_anchor / interaction_anchor / overview_anchor / safety_anchor |
| suppress_detail_level | str | 压低的信息粒度：coarse / mid / fine / object |
| granularity_bias | str | 当前粒度偏向：coarse / mid / fine / safety_first |
| filter_reason | str | 本帧过滤策略原因（规则型短句） |

---

## 3. 最小规则型过滤规则说明

- **输入**：SkeletonMix（dominant_skeleton、四类 weight）。
- **Navigation 主导**：保留 traversable/risk/confirm/focus/anchor/portal/segment；压低 fine_interaction_detail、far_decoration、low_value_local_object；粒度 coarse；锚点 path_anchor。
- **Fine Interaction 主导**：保留 focus/confirm/interaction_region/object_cluster/occlusion/reachability/height_depth；压低 long_path_detail、far_navigation_anchor；粒度 fine；锚点 interaction_anchor。
- **Observation 主导**：保留 focus/container/major_region/anchor/state_summary；压低 object_level_detail；粒度 mid；锚点 overview_anchor。
- **Safety 主导**：保留 risk_region/blocking/clearance/anomaly/confirm/traversable；suppress 为空（其他降级不抹掉）；粒度 safety_first；锚点 safety_anchor。
- **Safety 权重大时**：无论主导是谁，若 safe_w ≥ 0.3 则保证 risk_region 在 keep；≥ 0.35 则保证 clearance 在 keep。

---

## 4. Viewer 展示说明

- **卡片标题**：骨架过滤 / Skeleton Filter (M0)。
- **第一行**：保留：&lt;keep_region_types 逗号分隔&gt; · 压低：&lt;suppress_region_types 逗号分隔&gt;。
- **第二行**：粒度：&lt;granularity_bias&gt; · 锚点优先：&lt;keep_anchor_priority&gt; · &lt;filter_reason&gt;。
- 专家折叠面板可展开 skeleton_filter 查看全部字段。

---

## 5. 样本运行结果（测试）

- 见验收：frame.skeleton_filter 存在；不同 dominant 下 keep/suppress/granularity_bias 与 filter_reason 变化；Navigation/Fine Interaction/Observation/Safety 四类主导时过滤策略区分明显；与 M0/M1/M1.5/M2/Skeleton Mix M0 链路无破坏。

---

## 6. 当前哪些过滤字段已真实化，哪些仍规则型占位

| 项目 | 状态 |
|------|------|
| keep_region_types、suppress_region_types、keep_anchor_priority、suppress_detail_level、granularity_bias、filter_reason | **真实化**：每帧由 build_skeleton_filter(mix) 产出并写入 frame、runtime_ctx、Viewer。 |
| 过滤策略数值与 reason 文案 | **规则型占位**：由 dominant + 四权重规则推导，未接真实检测器/OCR 调度。 |
| 对象级复杂过滤、广告专项、记忆/遗忘/假设层联动、detector/OCR 调度 | **预留**，未实现。 |

---

## 7. 本轮是否通过

- **是**。验收满足：运行时存在可读的 Skeleton Filter 结果；Decision Monitor / Viewer 能显示；不同 dominant 下过滤策略会变化；四类骨架保留偏好可区分；不破坏既有链路。
