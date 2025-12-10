# Luna Badge 统一数据规范体系

**版本**: 1.0.0  
**最后更新**: 2025-12-02  
**适用范围**: 前端（iPhone/Android/Web）× 后端（WS + HTTP）× 工具链（压测、热衰减、分析器）

---

## 📋 目录

1. [FrameSpec - 前端到后端帧数据规范](./framespec.md)
2. [InferSpec - 后端到前端推理结果规范](./inferspec.md)
3. [HeartbeatSpec - WebSocket 心跳规范](./heartbeatspec.md)
4. [PerfLogSpec - 性能日志 JSONL 规范](./perflogspec.md)
5. [HeatDecaySpec - 热衰减测试规范](./heatdecayspec.md)
6. [EventBusSpec - 标准事件类型](./eventbusspec.md)
7. [ErrorSpec - 标准错误码规范](./errorspec.md)
8. [版本管理](./versioning.md)

---

## 🎯 规范目标

1. **统一格式**：所有前后端严格统一格式，避免字段不一致
2. **工具兼容**：所有工具（压测、实时测试、Dashboard、热衰减）自动识别字段
3. **可扩展性**：支持未来模块扩展（深度估计、BEV、SLAM）
4. **多设备支持**：支持多形态设备（Badge、眼镜、玩具、电视）统一协议层
5. **专业 QA**：为 Luna Badge 的"专业级 QA 体系"奠基

---

## 📦 规范文件结构

```
docs/protocol/
├── README.md              # 本文件
├── framespec.md           # 帧数据规范
├── inferspec.md           # 推理结果规范
├── heartbeatspec.md       # 心跳规范
├── perflogspec.md         # 性能日志规范
├── heatdecayspec.md       # 热衰减规范
├── eventbusspec.md        # 事件类型规范
├── errorspec.md           # 错误码规范
└── versioning.md          # 版本管理
```

---

## 🔧 使用方式

### 前端使用

```javascript
// 发送帧数据
const frameData = {
  type: "frame",
  frame_id: 12345,
  client_ts: performance.now(),
  width: 1280,
  height: 720,
  image_base64: "...",
  meta: { platform: "ios", auto_mode: true }
};
ws.send(JSON.stringify(frameData));
```

### 后端使用

```python
# 解析帧数据
from protocol.framespec import FrameSpec
frame = FrameSpec.parse(json_data)

# 返回推理结果
from protocol.inferspec import InferSpec
result = InferSpec.create(
    frame_id=frame.frame_id,
    client_ts=frame.client_ts,
    objects=detections,
    nav=nav_result
)
```

### 工具链使用

```python
# 分析性能日志
from protocol.perflogspec import PerfLogSpec
for line in open("perf_logs/run_*.jsonl"):
    log = PerfLogSpec.parse(line)
    print(f"延迟: {log.infer.total_ms}ms")
```

---

## 📝 版本历史

- **1.0.0** (2025-12-02): 初始版本，定义核心规范

---

## 🔗 相关文档

- [运营监控指南](../OPERATIONAL_MONITORING_GUIDE.md)
- [一键运营测试指南](../ONE_CLICK_OPERATIONAL_TEST.md)
- [性能监控指南](../PERF_MONITORING_GUIDE.md)






