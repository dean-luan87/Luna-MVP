# Luna Badge v1.1.1 测试指南

> **版本**: v1.1.1  
> **测试日期**: 2025-01-18

---

## 🚀 快速开始

### 1. 启动测试服务器

```bash
cd Luna_Badge
python3 web_test_server.py
```

或者使用启动脚本：

```bash
./start_web_test.sh
```

### 2. 访问测试页面

- **主测试页面**: http://127.0.0.1:9000/
- **测试面板**: http://127.0.0.1:9000/test_panel
- **API状态**: http://127.0.0.1:9000/api/v1/system/status

**注意**: 端口5000和8080不可用，已改为9000

---

## 🧪 v1.1.1 新功能测试

### 测试1: 方向估计（DirectionEstimator）

**功能**: 根据 bbox 横向位置判断方向

**测试代码**:
```javascript
// 在浏览器控制台（F12）执行

// 测试用例1: 左侧
const bbox1 = {x1: 0.1, y1: 0.3, x2: 0.3, y2: 0.7};
console.log("左侧方向:", calcDirection(bbox1)); // 应该输出 "leftFront"

// 测试用例2: 中间
const bbox2 = {x1: 0.4, y1: 0.3, x2: 0.6, y2: 0.7};
console.log("中间方向:", calcDirection(bbox2)); // 应该输出 "front"

// 测试用例3: 右侧
const bbox3 = {x1: 0.7, y1: 0.3, x2: 0.9, y2: 0.7};
console.log("右侧方向:", calcDirection(bbox3)); // 应该输出 "rightFront"
```

**预期结果**:
- ✅ 左侧 bbox → "leftFront"
- ✅ 中间 bbox → "front"
- ✅ 右侧 bbox → "rightFront"

---

### 测试2: 距离估计（DistanceEstimator）

**功能**: 根据 bbox 高度推测粗略距离

**测试代码**:
```javascript
// 测试用例1: 很近（高度大）
const bbox1 = {x1: 0.3, y1: 0.1, x2: 0.7, y2: 0.9};
console.log("很近距离:", calcDistance(bbox1)); // 应该输出 0.3

// 测试用例2: 中等距离
const bbox2 = {x1: 0.3, y1: 0.3, x2: 0.7, y2: 0.6};
console.log("中等距离:", calcDistance(bbox2)); // 应该输出 0.8

// 测试用例3: 较远
const bbox3 = {x1: 0.3, y1: 0.4, x2: 0.7, y2: 0.55};
console.log("较远距离:", calcDistance(bbox3)); // 应该输出 1.2

// 测试用例4: 太远
const bbox4 = {x1: 0.3, y1: 0.5, x2: 0.7, y2: 0.55};
console.log("太远距离:", calcDistance(bbox4)); // 应该输出 null
```

**预期结果**:
- ✅ 高度 > 0.45 → 0.3m
- ✅ 高度 > 0.20 → 0.8m
- ✅ 高度 > 0.10 → 1.2m
- ✅ 高度 ≤ 0.10 → null

---

### 测试3: 拟人化文案生成（SpeechPolicy.getHazardSentence）

**功能**: 根据方向 + 距离 + 类型生成更拟人的提示语句

**测试代码**:
```javascript
// 测试用例1: 左前方半米内有障碍物
const msg1 = SpeechPolicy.getHazardSentence({
  type: "obstacle",
  direction: "leftFront",
  distance: 0.4
});
console.log("文案1:", msg1);
// 预期: "左前方半米内有障碍物，请注意。"

// 测试用例2: 正前方1米内有人接近
const msg2 = SpeechPolicy.getHazardSentence({
  type: "person",
  direction: "front",
  distance: 0.8
});
console.log("文案2:", msg2);
// 预期: "正前方1米内有人接近，请注意。"

// 测试用例3: 右前方1.2米处是下台阶
const msg3 = SpeechPolicy.getHazardSentence({
  type: "stepDown",
  direction: "rightFront",
  distance: 1.2
});
console.log("文案3:", msg3);
// 预期: "右前方 1.2米处是下台阶，请注意。"

// 测试用例4: 无距离信息
const msg4 = SpeechPolicy.getHazardSentence({
  type: "vehicle",
  direction: "front",
  distance: null
});
console.log("文案4:", msg4);
// 预期: "正前方前方有车辆经过，请注意。"
```

**预期结果**:
- ✅ 方向正确翻译（leftFront → "左前方"）
- ✅ 距离正确格式化（0.4 → "半米内", 0.8 → "1米内", 1.2 → "1.2米处"）
- ✅ 类型正确翻译（obstacle → "有障碍物"）

---

### 测试4: 增强危险事件派发（EventDispatcher.emitEnhancedHazardEvent）

**功能**: 支持 bbox + type 的增强危险事件，自动计算方向、距离并生成拟人化文案

**测试代码**:
```javascript
// 测试用例1: 障碍物检测
const bbox1 = {x1: 0.2, y1: 0.2, x2: 0.4, y2: 0.8};
EventDispatcher.emitEnhancedHazardEvent(bbox1, "obstacle");

// 预期行为:
// 1. 自动计算方向（leftFront）
// 2. 自动计算距离（0.3m）
// 3. 生成拟人化文案并TTS播报
// 4. 触发钩子（onHazard + onActionSuggest）
// 5. 记录日志
// 6. 更新调试面板

// 测试用例2: 人员检测
const bbox2 = {x1: 0.5, y1: 0.3, x2: 0.7, y2: 0.6};
EventDispatcher.emitEnhancedHazardEvent(bbox2, "person");

// 测试用例3: 台阶检测
const bbox3 = {x1: 0.6, y1: 0.4, x2: 0.8, y2: 0.55};
EventDispatcher.emitEnhancedHazardEvent(bbox3, "stepDown");
```

**预期结果**:
- ✅ 自动计算方向和距离
- ✅ 生成并播报拟人化文案
- ✅ 触发所有钩子
- ✅ 记录日志到 LogUploader
- ✅ 更新调试面板（如果有）

---

### 测试5: 动作建议钩子（Hooks.onActionSuggest）

**功能**: 为 v1.2.0 的动作建议模块预留接口

**测试代码**:
```javascript
// 注册动作建议钩子
Hooks.on("onActionSuggest", (data) => {
  console.log("🎯 动作建议数据:", data);
  console.log("  类型:", data.type);
  console.log("  方向:", data.direction);
  console.log("  距离:", data.distance);
  console.log("  宽度:", data.width);
  console.log("  高度:", data.height);
  console.log("  bbox:", data.bbox);
  
  // 未来可以在这里接入动作建议模块
  // 例如: 向右横走一步、减速、停止等
});

// 触发增强危险事件，应该会调用上面的钩子
const bbox = {x1: 0.2, y1: 0.3, x2: 0.4, y2: 0.7};
EventDispatcher.emitEnhancedHazardEvent(bbox, "obstacle");
```

**预期结果**:
- ✅ 钩子被正确注册
- ✅ 触发事件时钩子被调用
- ✅ 数据格式正确（包含 type, direction, distance, width, height, bbox）

---

## 🔄 向后兼容性测试

### 测试6: 旧API仍然可用

**测试代码**:
```javascript
// 测试旧的 emitHazardEvent API
EventDispatcher.emitHazardEvent({
  type: "obstacle",
  msg: "前方有障碍物，请注意安全。",
  level: "warning"
});

// 测试旧的 getHazardMessage API
const oldMsg = SpeechPolicy.getHazardMessage("obstacle");
console.log("旧文案:", oldMsg);
// 预期: "前方有障碍物，请注意安全。"
```

**预期结果**:
- ✅ 旧API仍然可用
- ✅ 新旧API可以并存
- ✅ 不破坏现有功能

---

## 📊 完整测试流程

### 步骤1: 环境检查
```bash
# 检查Python版本
python3 --version

# 检查依赖
pip list | grep -i flask

# 检查端口
lsof -i:5000
```

### 步骤2: 启动服务器
```bash
cd Luna_Badge
python3 web_test_server.py
```

### 步骤3: 打开浏览器
1. 访问 http://127.0.0.1:9000/ （注意：端口已改为9000，5000和8080不可用）
2. 按 F12 打开开发者工具
3. 切换到 Console 标签

### 步骤4: 执行测试代码
复制上面的测试代码到控制台执行

### 步骤5: 检查结果
- ✅ 控制台输出正确
- ✅ TTS播报正常（如果有speakText函数）
- ✅ 日志记录正常（检查LogUploader）
- ✅ 调试面板更新正常（如果有TestPanel）

---

## 🐛 常见问题

### Q1: 端口被占用
**解决方案**:
```bash
# 查找占用端口的进程
lsof -ti:9000

# 杀死进程（替换PID）
kill -9 <PID>

# 或使用其他端口（注意：5000和8080不可用）
PORT=9999 python3 web_test_server.py
```

**重要**: 端口5000和8080不可用，默认使用9000端口

### Q2: 模块未加载
**解决方案**:
- 检查浏览器控制台是否有错误
- 确认所有JS文件都已内联到web_test_server.py
- 刷新页面重新加载

### Q3: TTS不播报
**解决方案**:
- 检查是否有speakText函数
- 检查浏览器是否允许音频播放
- 检查控制台是否有错误信息

---

## ✅ 测试检查清单

- [ ] 方向估计功能正常
- [ ] 距离估计功能正常
- [ ] 拟人化文案生成正常
- [ ] 增强危险事件派发正常
- [ ] 动作建议钩子正常
- [ ] 向后兼容性正常
- [ ] 日志记录正常
- [ ] 调试面板更新正常

---

## 📝 测试报告模板

```
测试日期: 2025-01-18
测试版本: v1.1.1
测试环境: Chrome/Safari/Firefox

测试结果:
- [ ] 方向估计: ✅/❌
- [ ] 距离估计: ✅/❌
- [ ] 拟人化文案: ✅/❌
- [ ] 增强事件: ✅/❌
- [ ] 动作建议钩子: ✅/❌
- [ ] 向后兼容: ✅/❌

问题记录:
1. ...
2. ...

建议:
1. ...
2. ...
```

---

**祝测试顺利！** 🎉

