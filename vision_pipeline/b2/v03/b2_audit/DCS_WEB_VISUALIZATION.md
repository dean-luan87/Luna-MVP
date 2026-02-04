# B2 v0.5 DCS Web 可视化设计文档

## 📊 定位

**这是 B2 的"道德心电图"，不是性能监控。**

DCS Web 可视化是一个面向未来的控制面板，用于实时监控 B2 的设计一致性。

## 🎨 页面结构（三层）

### 1. 顶部：一眼判生死（红黄绿）

**DCS 状态灯（强制）**

| 分数区间 | 状态 | 颜色 | 含义 |
|---------|------|------|------|
| ≥ 90 | EXCELLENT | 🟢 绿 | 设计高度一致 |
| 85–89 | PASS | 🟡 黄 | 可接受但需注意 |
| 70–84 | WARNING | 🟠 橙 | 设计开始偏移 |
| < 70 | FAIL | 🔴 红 | 禁止合并 / 回滚 |

**顶部卡片示例**

```
Design Consistency Score: 92 🟢
Status: PASS
Fatal Violations: 0
Warnings: 1
```

**❗ 红灯 = 不允许任何"但是"**

### 2. 中部：六大维度可视化（责任归因）

**六大维度条形 / 雷达图**
- Gate
- Evidence
- Trigger
- Impact
- Trace
- Timeline

**每一项必须支持：**
- 得分
- 扣分原因 hover
- 对应 Cursor 自检条目编号（B.x）

**📌 这是为了防止甩锅**
不是"系统问题"，而是"哪一条设计被破坏"。

### 3. 底部：违规 → 证据 → 帧

**违规时间线（Timeline Drill-down）**

点击某一扣分项，展开：

```
Violation: Trigger without behavior impact (-15)
Time: 00:02:31
Frame: 4512
Impact: NO_OP
Decision: CONDITION_CHANGE
Gate: ACTIVE
Human Explanation:
"B 在此帧认为有变化，但该变化不会影响 C 的行为"
```

**这一步的意义只有一个：让工程师"羞于犯错"**

## 📊 数据来源

| 数据 | 来源 |
|------|------|
| DCS 总分 | 自动化验收规则 A |
| 维度扣分 | A + B 映射 |
| 人类解释 | trace.human_readable |
| 时间定位 | trace.time |

## 🔧 技术实现

### 数据生成

使用 `dcs_web_generator.py` 生成 Web 数据：

```bash
python vision_pipeline/b2/v03/b2_audit/dcs_web_generator.py \
    traces/b2_runtime_trace_v05.jsonl \
    timeline.jsonl
```

输出：`b2_dcs_web_data.json`

### 数据 Schema

参考 `dcs_web_schema.json` 了解完整的数据结构。

### Web 前端（待实现）

前端可以使用任何框架（React / Vue / 原生 JS），只需要：
1. 读取 `b2_dcs_web_data.json`
2. 按照三层结构渲染
3. 实现交互（hover、点击展开等）

## 🎯 使用场景

1. **PR Review**: 查看本次改动的 DCS 评分
2. **持续监控**: 跟踪 DCS 趋势
3. **问题定位**: 通过违规时间线定位问题
4. **团队对齐**: 可视化展示设计一致性

## 💡 设计原则

1. **一眼判生死**: 顶部状态灯必须清晰
2. **责任归因**: 每个扣分都要能追溯到具体规则
3. **证据链完整**: 违规 → 证据 → 帧，完整可追溯
4. **防甩锅**: 明确标注对应的 Cursor 自检条目
