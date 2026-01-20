# Cursor 指令包：可审判闭环（Trace Viewer + DCS + CI 执行器）

**目标：** 在仓库里新增一个"可审判闭环"  
**输入：** trace.jsonl（任意版本，只要每行是 JSON）  
**输出：** viewer/trace_viewer_v043.html + tools/run_arch_guard.py + tools/dcs_rules_v1.json + tools/dcs_eval.py + CI 示例

---

## 执行步骤

你在当前 repo 内实现"可审判闭环：Trace Viewer + DCS + CI 执行器"，严格按下面步骤创建文件与内容，不要改动既有业务逻辑。

### === A. 新增目录结构 ===

创建目录：
- viewer/
- tools/
- artifacts/ (用于CI落盘产物，允许空)

### === B. 新增 DCS 规则（硬判定项，红黄绿） ===

创建文件 `tools/dcs_rules_v1.json`

规则最小集：
1) authority_violation (RED)：B 在 2m 内输出 NEED_STOP/NEED_DETOUR/INTERRUPT
2) env_overreach (RED)：ENV 触发 CONDITION_CHANGE 或 INTERRUPT
3) no_op_timeline (YELLOW)：impact=NO_OP 仍写入 timeline/decision
4) missing_advisory (RED)：缺少 advisory_only=true（若字段存在则必须为 true）
5) missing_core_fields (YELLOW)：缺少 engine_version/time/frame_id/impact 任一字段
6) over_prediction_language (YELLOW)：human_interpretation 或 reasons 包含 "一定/必然/确认/已发生" 等确认性词（B 不允许确认风险）

### === C. 新增 DCS 评估器（读取 trace.jsonl -> 输出 dcs_report.json，同时把 grade 写回事件用于Viewer展示） ===

创建 `tools/dcs_eval.py`

要求：
- 输入：trace.jsonl 路径（默认 trace.jsonl）
- 输出：
  - artifacts/dcs_report.json
  - artifacts/trace_enriched.jsonl（每行在原 event 上追加 dcs 字段）
- 兼容旧 trace：字段不存在时按 missing_core_fields 记 YELLOW
- DCS 分级：任意 RED -> event.grade=RED；否则任意 YELLOW -> YELLOW；否则 GREEN
- dcs_report.json 要包含：total, red_count, yellow_count, green_count, top_violations(按次数排序), sample_red_events(最多10条，含 human_time/frame_id/violation)

### === D. 新增 CI 执行器（run_arch_guard.py） ===

创建 `tools/run_arch_guard.py`

要求：
- 调用 dcs_eval.py 生成 artifacts
- 若 red_count>0 则 exit(1)，否则 exit(0)
- 无论是否失败，都保留 artifacts 下的 report 和 enriched trace

### === E. 新增 v0.4.3 Demo Viewer（单文件 HTML） ===

创建 `viewer/trace_viewer_v043.html`

要求：
- 可通过 query 参数指定数据源：
  - ?src=../artifacts/trace_enriched.jsonl
  - 默认 src=../artifacts/trace_enriched.jsonl
- 页面结构：
  1) 顶部仪表盘：GREEN/YELLOW/RED 数量 + 总数（显著显示）
  2) Filter：Grade 下拉（ALL/GREEN/YELLOW/RED）+ 搜索框（按字符串搜索整行 JSON）
  3) 列表：每条显示 [engine_version] human_time | impact | main_factor | grade
  4) 详情面板：点击某条展开完整 JSON（pretty print）
  5) 点击某条时 console.log 输出 jump_request：{t_video_s, frame_id, human_time}
- UI 约束：
  - RED 行背景深红 + 白字；YELLOW 黄底；GREEN 绿底（可浅色）
  - RED 默认置顶（排序规则：RED->YELLOW->GREEN，再按 t_video_s 或 frame_id）
  - 不依赖任何外部库/CDN（纯原生 JS）

### === F. 提供最小运行说明 ===

创建 `README_DCS_VIEWER.md`

说明：
1) 把 trace.jsonl 放仓库根目录
2) python3 tools/dcs_eval.py trace.jsonl
3) 用浏览器打开 viewer/trace_viewer_v043.html?src=../artifacts/trace_enriched.jsonl

### === G. 自检 ===

在实现后，创建 `tools/_selftest_make_sample_trace.py`

生成一个 10 行 trace.jsonl（含 2 条 RED、2 条 YELLOW、其余 GREEN）用于演示。

运行：`python3 tools/_selftest_make_sample_trace.py && python3 tools/dcs_eval.py trace.jsonl`

确保 viewer 能显示仪表盘与列表。

---

## 全部完成后，给我输出：

- 新增文件清单
- 如何运行 selftest
- dcs_report.json 的示例输出（节选）
