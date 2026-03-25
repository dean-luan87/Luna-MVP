# Post-Processing Intelligence Reserve M0（后置信息处理板块占位层）交付

**上位总纲**：`docs/LUNA_MAINLINE_SHAPE_BLUEPRINT.md` §9、§12（后置链与 reserve 在完整形态中的位置）。

## 1. 定位（写死）

在 **Runtime 主线之后**、**图书馆 / 记忆系统之前**，预留独立板块：**后置信息处理**（当前仅 **reserve / 占位**）。

- **不是记忆系统的一部分**；与图书馆/记忆接口分离。
- **原始历史处理信息不得直接进入记忆**；记忆系统只接收经该板块筛选、优化后的结果（当前仅字段与原则占位，无真实写库）。
- **本轮不做**：真实归类/归因/策略效果分析/记忆筛选/图书馆与记忆正式写入/自动提炼/去噪压缩。

## 2. 交付件

| 组件 | 路径 |
|------|------|
| 占位层 | `decision_monitor/post_processing_intelligence_reserve.py` |
| Frame 字段 | `post_processing_intelligence_reserve`（`PostProcessingIntelligenceReserveResult`） |
| Runtime 摘要（占位） | `runtime/context.py`：`post_processing_summary`、`post_processing_routing_hint`、`memory_write_reserved`、`library_link_reserved` |
| 时间轴 | 事件类型 `post_processing_reserved`（`append_post_processing_reserved_event`） |
| 结构树 | `tree_summary` 追加 `post_processing_reserved=true`（当 reserve_applied） |
| Console | `tools/reasoning_console_aggregator.py` + `tools/reasoning_console_server.py` 轻量区块 |
| Viewer | `tools/decision_monitor_viewer.py` 卡片 + 专家展开 |
| 单测 | `tests/test_post_processing_intelligence_reserve.py` |
| smoke | `tools/smoke_post_processing_intelligence_reserve.py` |

## 3. 数据结构（摘要）

- `PostProcessRecordCandidate`：`record_source_type`（reasoning_trace / whitebox_summary / optimization_feedback / scenario_benchmark / real_case_result / user_feedback / strategy_shadow / …）、`record_summary`、`record_candidate_ready`
- `PostProcessAnalysisReserve`：`analysis_type`（classification / failure_mode_analysis / strategy_effectiveness_analysis / contamination_observation / …）、`analysis_reserved_only=True`
- `PostProcessRoutingReserve`：`routing_target`（library_candidate_pool / memory_candidate_pool / risk_observation_pool / contamination_observation_pool / discard_candidate / …）
- `PostProcessingIntelligenceReserveResult`：`library_link_reserved`、`memory_write_reserved`、`post_processing_reserve_applied`

## 4. 最小生成规则（M0）

只读现有 frame 粗映射：结构树/时间轴/白盒 → 记录候选与分类/模式占位；optimization_feedback_loop → 策略效果占位与图书馆候选去向；`trace_anchor_id` 含 benchmark/bench/scenario_pack 或 `R数字_` 等 → 场景/真实 case 与 failure_mode 占位；用户确认桥 → user_feedback；strategy_injection_shadow → strategy_shadow；污染占位存在 → contamination 分析与污染观察池；空帧 → discard 候选。

可选：`frame["post_processing_hints"]` 字典（`scenario_benchmark` / `real_case_result`）供脚本显式标注。

## 5. 原则（写入 CONTRACT）

见 `decision_monitor/CONTRACT.md` § Post-Processing Intelligence Reserve M0。

## 6. 结论（M0）

占位层已接入 frame / Console / Viewer / 时间轴 / 结构树摘要；**不**实现真实后处理管线或写库。
