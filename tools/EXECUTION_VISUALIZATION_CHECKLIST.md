# 执行可视化·必须四件套 - 完整执行 Checklist

**版本：** v0.4.3+  
**状态：** ✅ 执行中  
**日期：** 2025-01-12

---

## 🎯 目标冻结（不可变）

1. ✅ v0.1–v0.3 trace → Viewer → 形成"进化曲线证据"
2. ✅ DCS = RED 的记录必须被 Viewer 强制高亮 / 锁定
3. ✅ Trace ↔ 视频时间轴联动（点击即跳）
4. ✅ Viewer 作为 CI Artifact 自动产出（系统自证）

**核心一句话：**
不是给人看热闹，而是给系统"留法庭证据"。

---

## 🧱 执行顺序（必须按此顺序，避免返工）

**正确顺序：** 1 → 2 → 3 → 4

**为什么不能反过来：**
- ❌ 没进化曲线 → 不知道红黄绿是否合理
- ❌ 没 RED 锁死 → 视频联动会掩盖越权
- ❌ 没 Viewer Artifact → CI 没有"证据输出"

---

## ① v0.1–v0.3 Trace → 进化曲线（先做）

### ✅ 要做什么

- [x] 同一个 Viewer
- [ ] 加一个 Version Selector
- [ ] 同一时间窗口（例如 30 秒）
- [ ] 同一类事件
- [ ] 并排对比 v0.1 / v0.2 / v0.3 / v0.4.3

### Viewer 新增字段（Schema 层）

```json
{
  "engine_version": "v0.3",
  "dcs": {
    "grade": "RED | YELLOW | GREEN",
    "violations": ["over_prediction", "authority_violation"]
  }
}
```

### UI 表现（语义冻结）

- 时间轴纵向不变
- 横向增加版本切换
- 同一 timestamp：
  - v0.1：🔴
  - v0.3：🟡
  - v0.4：🟢

👉 **这是你"系统进化证明图"**

### 实现步骤

1. [ ] 在 Viewer 顶部添加 Version Selector
2. [ ] 支持加载多个 trace 文件（v0.1, v0.2, v0.3, v0.4.3）
3. [ ] 按时间对齐显示
4. [ ] 颜色编码：RED/YELLOW/GREEN
5. [ ] 生成对比视图

---

## ② DCS = RED 强制高亮 & 锁死（不能被过滤）

### ❗ 这是"法务级规则"

### 冻结规则（必须写进 Guard）

- ❌ RED 不能被隐藏
- ❌ RED 不能被 collapse
- ❌ RED 不能被 filter 掉
- ✅ RED 永远置顶
- ✅ RED 必须展开显示 violation 原因

### Viewer 行为冻结

```javascript
if dcs.grade == RED:
  - 强制高亮背景（深红）
  - 强制显示 violation_reason
  - 禁用隐藏 / 搜索过滤
```

**意义：**
防止"漂亮 Demo 把问题遮住"
系统不允许自己掩盖犯罪现场

### 实现步骤

1. [ ] 在 CSS 中添加 RED 强制高亮样式
2. [ ] 修改 `applyFilters()` 函数，RED 记录永远显示
3. [ ] 修改 `renderList()` 函数，RED 记录置顶
4. [ ] 在 `renderDetail()` 中强制显示 violation_reason
5. [ ] 禁用 RED 记录的隐藏/过滤功能

---

## ③ Trace ↔ 视频联动（点击即跳）

### 冻结原则（非常重要）

- Viewer 不负责播放
- Viewer 只负责精确定位
- 播放权交给 Video Player

### Trace 必须包含（你已经有 80%）

```json
{
  "frame_id": 4821,
  "t_video_s": 160.77,
  "fps": 29.99
}
```

### Viewer 行为

```
点击 trace →
  emit jump_request {
    video_time: 160.77
    frame_id: 4821
  }
```

### 第一阶段（你现在做）

- [x] alert / console.log 即可

### 第二阶段（后续）

- [ ] iframe / video.js / 外部播放器接管

### 实现步骤

1. [x] 实现 `jumpTo()` 函数（已完成）
2. [ ] 优化 `jumpTo()` 输出格式
3. [ ] 添加视频播放器接口预留
4. [ ] 文档说明如何接入视频播放器

---

## ④ Viewer 作为 CI Artifact（系统自证）

### 这是"工程上最值钱的一步"

### CI 每次必须产出

```
/artifacts/
  ├── trace.jsonl
  ├── dcs_report.json
  └── trace_viewer.html   ← 打开即看
```

### CI 判死规则（必须冻结）

```
if dcs.RED > 0:
  - CI FAIL
  - Viewer 仍然生成
  - 用于事后审判
```

**作用：**
- ❌ 不允许"测试过了但不知道发生了什么"
- ✅ 每一次失败都有可视证据

### 实现步骤

1. [ ] 创建 CI 脚本生成 Viewer HTML
2. [ ] 在 CI 中集成 Viewer 生成
3. [ ] 将 Viewer 作为 Artifact 上传
4. [ ] 添加 CI 判死规则（RED > 0 → FAIL）

---

## 🧠 你现在拥有的能力（总结）

到这一步，你的系统已经具备：
- ✅ 自我审判能力
- ✅ 进化证据链
- ✅ 越权不可掩盖
- ✅ 人能理解的执行轨迹
- ✅ 机器也能回看自己犯的错

这已经不是普通 AI 项目了，这是可被监管、可被审计、可被追责的系统。

---

**版本：** v0.4.3+  
**最后更新：** 2025-01-12  
**状态：** ✅ 执行中
