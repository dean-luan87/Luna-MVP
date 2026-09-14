# B2 Trace Viewer (Minimal) - v0.4.3+

## 用途

最小可用、零后端的 Web Trace Viewer：

- ✅ 直接在浏览器打开（本地文件即可）
- ✅ 通过文件选择加载 `*.jsonl` trace
- ✅ 左侧列表（时间轴）+ 右侧详情（单条 trace 展开）
- ✅ 支持过滤：gate.mode / impact.impact / to_c.send / writeback.timeline
- ✅ 支持搜索：按 human_time / t_str / reason / blocked_by 关键词
- ✅ **DCS 红/黄/绿仪表盘**（点击自动过滤）
- ✅ **Gate 状态仪表**（点击自动过滤）
- ✅ **风险解释区**（高亮为什么危险）
- ✅ **跳转到时间/帧**（为视频联动预留）

## 使用方式

### 1️⃣ 打开 Viewer

**macOS：**
```bash
open tools/trace_viewer_min.html
```

或直接双击 `tools/trace_viewer_min.html`

**Windows：**
```bash
start tools/trace_viewer_min.html
```

或直接双击 `tools/trace_viewer_min.html`

**Linux：**
```bash
xdg-open tools/trace_viewer_min.html
```

### 2️⃣ 选择 Trace 文件

1. 点击 "Trace JSONL" 文件选择按钮
2. 选择你的 trace 文件（例如：`traces/b2_trace_v043.jsonl`）
3. 左侧会显示时间轴列表
4. 点击任意一条记录，右侧会显示详细信息

## 功能

### 仪表盘（顶部）

**DCS 仪表盘：**
- 🟢 **DCS GREEN**: 完全合规
- 🟡 **DCS YELLOW**: 边界态 / 提醒但未确认
- 🔴 **DCS RED**: 越权 / 过度预测 / 危险表达
- ⚪ **N/A**: 无 DCS 判定（历史版本）

**Gate 状态仪表：**
- 🟢 **Gate ACTIVE**: 正常运行
- 🟡 **Gate READ_ONLY**: 只读模式
- 🔴 **Gate SUSPENDED**: 已挂起

**点击仪表 → 自动过滤列表**

### 过滤

- **Gate Mode**: 按 ACTIVE / READ_ONLY / SUSPENDED 过滤
- **Impact**: 按 NO_OP / NEED_SLOW_DOWN / PATH_UNCERTAIN / NEED_DETOUR / NEED_STOP 过滤
- **To C**: 只看 `to_c.send=true` 的记录
- **Timeline**: 只看 `writeback.timeline=true` 的记录

### 搜索

支持搜索以下字段：
- `human_time` / `t_str`
- `reason` / `blocked_by`
- `impact` / `dcs_grade` / `main_factor`
- 以及所有 JSON 字段内容

### 统计

左侧控制面板显示：
- Total / Shown（总数 / 过滤后数量）
- Gate A/R/S（ACTIVE / READ_ONLY / SUSPENDED 数量）
- Top impacts（最常见的 impact 类型）

### 风险解释

右侧详情面板新增"⚠️ 风险解释"区域，显示：
- Gate 原因
- Impact 类型
- Advisory only 状态
- DCS 等级
- 风险说明（为什么危险/合规）

### 跳转功能

点击"跳转到该时刻"按钮：
- 显示当前选中 trace 的 frame 和 time
- 为未来视频联动预留接口
- 目前输出到 console 和 alert

## v0.4.3 Trace 字段兼容说明

这个 Viewer 不要求字段完全一致，它会按顺序尝试读取：

- `schema_version` 或 `schema`
- `time.t_str` / `time.human_time` / `time.t_video_s`
- `gate` 或 `gate_eval` / `gate_eval_dict`
- `to_c` 或 `to_c_message`
- `writeback`、`dcs`、`factors`

所以你现在 v0.4.1/0.4.2 的 trace 也能先用起来，不会因为字段小改就崩。

## 颜色编码

### Gate Mode
- 🟢 **ACTIVE**: 绿色
- 🟡 **READ_ONLY**: 黄色
- 🔴 **SUSPENDED**: 红色

### Impact
- 🔴 **NEED_STOP**: 红色
- 🟡 **NEED_DETOUR** / **PATH_UNCERTAIN**: 黄色
- 🔵 **NEED_SLOW_DOWN**: 蓝色
- ⚪ **NO_OP**: 无颜色

### DCS Grade
- 🟢 **GREEN**: 绿色
- 🟡 **YELLOW**: 黄色
- 🔴 **RED**: 红色

## 立即可用

✅ **看 B2 有没有越权**
- 点击 🔴 DCS RED 仪表，查看所有违规记录

✅ **看 Gate 有没有正确阻断**
- 点击 🔴 Gate SUSPENDED 仪表，查看所有被挂起的记录

✅ **看历史版本在什么地方变黄 / 变红**
- 点击 🟡 DCS YELLOW 或 🔴 DCS RED 仪表
- 查看风险解释区，了解为什么

✅ **给任何人看："系统为什么在那一秒说了这句话"**
- 点击任意 trace 记录
- 查看右侧详情和风险解释

## 明确不做（但已留接口）

- ❌ 不绑定视频（但已预留跳转接口）
- ❌ 不自动播放
- ❌ 不在线上传

## 下一步

你可以选一个：
1. 把 v0.1–v0.3 trace 跑进这个 Viewer，出一张"进化曲线截图"
2. 把 DCS RED 项直接在 Viewer 里"锁死高亮"
3. 接视频：点 trace → 跳到视频对应秒
4. 把这个 Viewer 变成 CI artifact（每次跑完自动生成）

---

**版本：** v0.4.3  
**状态：** ✅ 已完成  
**最后更新：** 2025-01-12
