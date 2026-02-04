# Luna Badge 一期测试验收指南

> 生成时间: 2025-01-18
> 
> 本文档提供一期功能的测试验收方法，包括最小闭环验收、真机测试和问题排查。

---

## 📋 目录

1. [最小闭环验收](#最小闭环验收)
2. [真机/手机端测试](#真机手机端测试)
3. [二期预留点说明](#二期预留点说明)
4. [快速检查清单](#快速检查清单)

---

## 1️⃣ 最小闭环验收

### 目标

验证核心链路是否真正打通：
```
YOLO → VisionBridge → SceneGraph/NavigationHook → TTS → TestPanel → 日志上传
```

### 步骤 A：确认模块都挂在 window 上

**在浏览器 DevTools 控制台输入（检查是否有 undefined）：**

```javascript
// 检查所有关键模块
console.log("ParameterHub:", typeof window.ParameterHub);
console.log("ErrorCode:", typeof window.ErrorCode);
console.log("LogUploader:", typeof window.LogUploader);
console.log("VisionBridge:", typeof window.VisionBridge);
console.log("NavigationHook:", typeof window.NavigationHook);
console.log("TestPanel:", typeof window.TestPanel);
console.log("testFullChain:", typeof window.testFullChain);
```

**✅ 要求：**
- 所有模块都不是 `undefined`
- 至少是 `object` 或 `function`
- 如果出现 `undefined`，说明模块未正确加载

**预期输出：**
```
ParameterHub: object
ErrorCode: object
LogUploader: object
VisionBridge: object
NavigationHook: function
TestPanel: function
testFullChain: function
```

---

### 步骤 B：运行全链路测试脚本

**在控制台输入：**

```javascript
window.testFullChain();
```

**预期结果：**

1. **TTS 播报**
   - 会听到一条测试语音
   - 内容类似："测试播报：导航系统已启动"
   - 或："前方有危险，请注意避让"（如果检测到危险）

2. **TestPanel 显示**
   - 页面右侧出现绿色调试面板
   - 面板内容包含：
     ```json
     {
       "yolo": [
         { "label": "person", "conf": 0.71, ... },
         { "label": "stairs", "conf": 0.82, ... }
       ],
       "navState": {
         "state": "IDLE" 或 "NAVIGATING",
         "currentStep": ...
       },
       "taskState": {
         "queueLength": 0,
         "currentTask": null,
         "running": false
       },
       "timestamp": "2025-01-18T..."
     }
     ```

3. **后端日志**
   - Flask 端 `/api/v1/log/client` 收到日志
   - 日志包含：
     - `level`: "info" / "alert" / "warning"
     - `code`: "VISION_UPDATE" / "NAV_DANGER" 等
     - `message`: 描述信息
     - `source`: "VisionBridge" / "NavigationHook" 等
     - `timestamp`: 时间戳

**✅ 验收标准：**
- ✅ TTS 能播报
- ✅ TestPanel 能显示数据
- ✅ 日志能上传到后端
- ✅ VisionBridge 能处理 YOLO 数据
- ✅ NavigationHook 能响应场景变化

**如果这一步跑通，说明"一期最小生命体"已经建立！**

---

## 2️⃣ 真机/手机端测试

### 目标

验证三个关键问题：
1. 导航播报「只说一句就没了」
2. 危险误报太多
3. 日志不够完整

---

### 2.1 导航播报「只说一句就没了」——测试方法

#### 问题描述
开启导航后，只说一句"我是Luna语音助手……"就停止播报了。

#### 测试步骤

**步骤 1：创建模拟导航测试按钮**

在测试页面添加一个按钮（或直接在控制台执行）：

```javascript
// 创建测试按钮
const btn = document.createElement('button');
btn.textContent = '开始模拟导航';
btn.style.cssText = 'position:fixed;top:10px;left:10px;z-index:99999;padding:10px;background:#00ff00;';
btn.onclick = function() {
    let frameCount = 0;
    const interval = setInterval(() => {
        frameCount++;
        
        // 生成模拟YOLO数据（距离逐渐变化）
        const fakeDetections = [
            {
                label: "person",
                conf: 0.71,
                x: 120 + frameCount * 5,
                y: 200,
                w: 80,
                h: 140,
                confidence: 0.71,
                class: "person"
            },
            {
                label: "stairs",
                conf: 0.82,
                x: 260,
                y: 180 - frameCount * 3,
                w: 90,
                h: 110,
                confidence: 0.82,
                class: "stairs"
            }
        ];
        
        // 调用VisionBridge处理
        if (window.VisionBridge) {
            window.VisionBridge.ingestYolo(fakeDetections);
        }
        
        // 更新TestPanel
        if (window.TestPanel) {
            const panel = new window.TestPanel();
            panel.append(`frame_${frameCount}`, {
                detections: fakeDetections.length,
                navState: window.NavigationFSM ? window.NavigationFSM.getState() : "IDLE"
            });
        }
        
        console.log(`[测试] 第 ${frameCount} 帧已处理`);
        
        // 运行30秒后停止
        if (frameCount >= 30) {
            clearInterval(interval);
            console.log('[测试] 模拟导航测试完成');
        }
    }, 1000); // 每秒一帧
};
document.body.appendChild(btn);
```

**步骤 2：观察以下指标**

1. **TTS 播报情况**
   - ✅ 是否在开始时播报提示
   - ✅ 是否在后续继续有播报（如"继续直走"、"前方有台阶"等）
   - ❌ 是否只播一句就停止

2. **TestPanel 状态更新**
   - ✅ 导航状态是否实时更新
   - ✅ 场景状态是否变化
   - ❌ 状态是否卡在某个值不动

3. **后端日志**
   - ✅ 是否持续收到 `VISION_UPDATE` 日志
   - ✅ 是否收到 `NAV_DANGER` 或其他导航相关日志
   - ❌ 日志是否在某一点停止

**步骤 3：问题定位**

如果出现「只说一句就没了」，检查：

```javascript
// 1. 检查NavigationFSM状态
console.log("NavigationFSM状态:", window.NavigationFSM ? window.NavigationFSM.getState() : "不存在");

// 2. 检查TTS队列
console.log("TTS队列:", window.PriorityTTSQueue ? window.PriorityTTSQueue.queue : "不存在");

// 3. 检查VisionBridge是否持续接收数据
console.log("VisionBridge:", window.VisionBridge);

// 4. 检查任务链状态
console.log("任务链状态:", window.taskChain ? {
    queueLength: window.taskChain.queue ? window.taskChain.queue.length : 0,
    running: window.taskChain.running,
    currentTask: window.taskChain.currentTask
} : "不存在");
```

**可能的原因：**
- ❌ VisionBridge 不再接收 YOLO 数据 → 检查 YOLO 服务是否正常
- ❌ NavigationFSM 状态变为 IDLE/ERROR → 检查导航状态机逻辑
- ❌ TTS 队列锁死 → 检查 TTS 队列处理逻辑
- ❌ 任务链停止执行 → 检查任务链状态机

---

### 2.2 危险误报太多——逐步优化方法

#### 问题描述
明明没危险，却一直说危险。

#### 测试步骤

**步骤 1：记录当前误报情况**

1. 找一个安全场景（家里客厅、办公室等）
2. 开启完整产品模式 + 摄像头
3. 运行 1 分钟，记录：
   - 危险提示出现的次数
   - 每次触发危险的对象（label / 距离 / score）
   - TestPanel / 日志中的详细信息

**步骤 2：在线调整参数（无需改代码）**

在浏览器控制台直接调整：

```javascript
// 1. 提高危险检测置信度（默认0.45）
window.ParameterHub.set("yolo.dangerThreshold", 0.6);
console.log("危险阈值已调整为:", window.ParameterHub.get("yolo.dangerThreshold"));

// 2. 提高危险判定的距离门槛（默认1.2米）
window.ParameterHub.set("yolo.distanceDangerMeters", 0.8);
console.log("危险距离已调整为:", window.ParameterHub.get("yolo.distanceDangerMeters"));

// 3. 提高一般检测置信度（默认0.30）
window.ParameterHub.set("yolo.generalThreshold", 0.40);
console.log("一般检测阈值已调整为:", window.ParameterHub.get("yolo.generalThreshold"));

// 4. 提高行人检测置信度（默认0.50）
window.ParameterHub.set("yolo.personThreshold", 0.65);
console.log("行人检测阈值已调整为:", window.ParameterHub.get("yolo.personThreshold"));
```

**步骤 3：重新测试并记录**

1. 调整参数后，重新运行 1 分钟
2. 记录新的误报次数
3. 对比调整前后的差异

**步骤 4：找到最佳参数组合**

建议测试以下参数组合：

| 组合 | dangerThreshold | distanceDangerMeters | generalThreshold | 预期效果 |
|------|----------------|---------------------|-----------------|---------|
| 保守 | 0.7 | 0.6 | 0.5 | 误报最少，但可能漏报 |
| 平衡 | 0.6 | 0.8 | 0.4 | 平衡误报和漏报 |
| 敏感 | 0.5 | 1.0 | 0.35 | 误报较多，但漏报少 |

**步骤 5：记录最佳配置**

找到最佳参数后，记录到文档：

```javascript
// 最佳配置（示例）
const bestConfig = {
    dangerThreshold: 0.6,
    distanceDangerMeters: 0.8,
    generalThreshold: 0.4,
    personThreshold: 0.65
};

// 应用最佳配置
Object.keys(bestConfig).forEach(key => {
    window.ParameterHub.set(`yolo.${key}`, bestConfig[key]);
});
```

---

### 2.3 日志是否够用——快速判断方法

#### 问题描述
日志不够完整，看不清问题出在哪。

#### 测试步骤

**步骤 1：触发典型行为**

1. **启动完整模式**
   ```javascript
   // 手动触发启动
   if (window.initProductMode) {
       window.initProductMode();
   }
   ```

2. **触发危险提示**
   ```javascript
   // 模拟危险检测
   window.VisionBridge.ingestYolo([
       { label: "car", conf: 0.8, x: 100, y: 200, dangerLevel: 3 }
   ]);
   ```

3. **人为制造错误**
   ```javascript
   // 手动抛异常测试日志记录
   try {
       throw new Error("测试错误");
   } catch (e) {
       window.LogUploader.push({
           level: "error",
           code: window.ErrorCode.SYS_MODULE_CRASH,
           message: "测试错误",
           error: e.toString(),
           source: "ManualTest"
       });
   }
   ```

**步骤 2：检查后端日志**

在后端查看 `/api/v1/log/client` 接收到的日志，检查是否包含：

1. **行为类型**
   - ✅ `VISION_UPDATE` - 视觉更新
   - ✅ `NAV_DANGER` - 导航危险
   - ✅ `SYS_FORCE_RECOVER` - 系统恢复
   - ✅ `TASK_ENQUEUED` - 任务入队
   - ✅ `NAV_STEP_COMPLETE` - 导航步骤完成

2. **上下文信息**
   - ✅ YOLO 识别结果（label / confidence / position）
   - ✅ 导航状态（state / currentStep / routeLength）
   - ✅ 错误码和错误信息
   - ✅ 时间戳

3. **关键字段**
   ```json
   {
     "level": "info|warning|error|alert|critical",
     "code": "VISION_UPDATE|NAV_DANGER|...",
     "message": "描述信息",
     "source": "VisionBridge|NavigationHook|...",
     "timestamp": 1705564800000,
     "details": {
       "detections": [...],
       "navState": {...},
       "error": "..."
     }
   }
   ```

**步骤 3：验证日志完整性**

针对"危险提示相关"的日志，检查是否能回答：

1. ✅ **是哪一帧触发了危险？**
   - 日志中是否有 `timestamp` 或 `frameId`？

2. ✅ **触发危险时，前方检测到的是什么？**
   - 日志中是否有 `details.detections` 或 `node.label`？

3. ✅ **当时导航状态是什么？**
   - 日志中是否有 `details.navState` 或 `navState`？

4. ✅ **播报是否有"被打断"或"被队列挡住"的记录？**
   - 日志中是否有 `TTS_QUEUE_FULL` 或 `TTS_INTERRUPTED`？

**步骤 4：日志完整性评分**

如果以上问题都能从日志中找到答案，说明日志系统已经足够支撑调试和优化。

**如果日志不够完整，可以：**
- 在关键位置添加更多日志点
- 增加更多上下文信息
- 使用 `LogUploader.push()` 记录更多细节

---

## 3️⃣ 二期预留点说明

### 说明

以下内容是二期的规划方向，**当前不需要实现**，只是帮助理解未来的发展方向。

### 3.1 场景节点多层记忆结构

**设计思路：**
- **场景节点层**：物理环境节点（电梯、楼梯、门等）
- **社会节点层**：社会功能节点（挂号窗口、收银台、服务台等）
- **用户节点层**：用户自定义节点（家、办公室、常去地点等）

**实现方向：**
```javascript
// 二期实现（示例）
class MultiLayerMemory {
    sceneLayer: SceneNodeLayer;      // 场景节点层
    socialLayer: SocialNodeLayer;    // 社会节点层
    userLayer: UserNodeLayer;        // 用户节点层
    
    // 跨层查询
    findNode(query) {
        return this.userLayer.find(query) ||
               this.socialLayer.find(query) ||
               this.sceneLayer.find(query);
    }
}
```

**当前状态：**
- ✅ 已有 `SceneNodes` 模块（场景节点层）
- ⏳ 社会节点层（二期）
- ⏳ 用户节点层（二期）

---

### 3.2 区域逻辑共存

**设计思路：**
- A 城市的医院有一套规则
- B 城市的医院是另一套
- Luna 记在不同 zone 里，不互相覆盖

**实现方向：**
```javascript
// 二期实现（示例）
class ZoneManager {
    zones: {
        "hospital_A_city": { rules: {...}, nodes: [...] },
        "hospital_B_city": { rules: {...}, nodes: [...] },
        "mall_C_city": { rules: {...}, nodes: [...] }
    };
    
    switchZone(zoneName) {
        // 切换区域，加载对应的规则和节点
    }
}
```

**当前状态：**
- ✅ 已有 `ZoneManager` 模块（基础区域管理）
- ✅ 已有 `ZoneAutoDetector` 模块（自动区域识别）
- ⏳ 区域规则系统（二期）
- ⏳ 区域间规则隔离（二期）

---

### 3.3 地图 × 视角 × 记忆一体化

**设计思路：**
- "去某个地方"时：调用历史场景 + 本地地图 + 实时视觉
- 走的过程中不断更新"这条路现在还有没有变动"

**实现方向：**
```javascript
// 二期实现（示例）
class IntegratedNavigation {
    planRoute(destination) {
        // 1. 查询历史场景记忆
        const history = this.memoryLayer.findRoute(destination);
        
        // 2. 查询本地地图
        const mapData = this.mapLayer.getRoute(destination);
        
        // 3. 结合实时视觉
        const realtime = this.visionLayer.getCurrentState();
        
        // 4. 综合规划路线
        return this.merge(history, mapData, realtime);
    }
}
```

**当前状态：**
- ✅ 已有 `MapMemory` 模块（地图记忆）
- ✅ 已有 `SceneNodes` 模块（场景记忆）
- ✅ 已有 `VisionBridge` 模块（实时视觉）
- ⏳ 一体化导航规划（二期）

---

## 4️⃣ 快速检查清单

### Mini Checklist（最简单的事）

完成以下4步，即可确认一期功能是否正常工作：

- [ ] **步骤 1：控制台检查 window.xxx 是否都存在**
  ```javascript
  // 在控制台执行
  ['ParameterHub', 'ErrorCode', 'LogUploader', 'VisionBridge', 
   'NavigationHook', 'TestPanel', 'testFullChain'].forEach(name => {
      console.log(name + ':', typeof window[name]);
  });
  ```
  **预期：** 所有都是 `object` 或 `function`，没有 `undefined`

- [ ] **步骤 2：运行全链路测试**
  ```javascript
  window.testFullChain();
  ```
  **预期：** 
  - ✅ TTS 播报测试语音
  - ✅ TestPanel 显示数据
  - ✅ 控制台无错误

- [ ] **步骤 3：检查 TestPanel 是否出现**
  ```javascript
  // 检查TestPanel
  const panel = document.getElementById('luna_test_panel');
  console.log('TestPanel存在:', !!panel);
  ```
  **预期：** TestPanel 出现在页面右侧

- [ ] **步骤 4：检查后端是否收到日志**
  ```javascript
  // 手动上传日志测试
  window.LogUploader.push({
      level: "test",
      code: "TEST_CHECK",
      message: "测试日志上传",
      source: "ManualTest"
  });
  
  // 等待5秒后检查后端日志文件
  // 或查看 Flask 控制台输出
  ```
  **预期：** 后端 `/api/v1/log/client` 收到日志

---

### 问题反馈模板

如果测试过程中发现问题，请提供以下信息：

```
1. 问题描述：
   [描述具体问题]

2. 复现步骤：
   [列出复现步骤]

3. 预期行为：
   [描述预期行为]

4. 实际行为：
   [描述实际行为]

5. 控制台输出：
   [粘贴控制台错误信息]

6. 后端日志：
   [粘贴相关后端日志]

7. 测试环境：
   - 浏览器：[Chrome/Safari/其他]
   - 设备：[PC/手机]
   - 系统版本：[macOS/iOS/Android/其他]
```

---

## 📝 总结

### 当前重点

**不要急于做二期功能，先把一期验证到可信 & 好用。**

### 验证目标

1. ✅ **最小闭环验收** - 确认链路真的通了
2. ✅ **真机测试** - 解决三个关键问题
3. ✅ **日志完整性** - 确保能看清问题

### 下一步

完成快速检查清单后，根据测试结果决定：
- 🔧 **针对误报做规则优化** - 如果误报太多
- 🔧 **针对"只播一句就停"做状态机修复** - 如果播报中断
- 🔧 **增强日志记录** - 如果日志不够用

---

*文档生成时间: 2025-01-18*
*最后更新: 2025-01-18*



