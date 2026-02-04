# Luna Badge H5 实时推理测试系统

**版本**: 1.0.0  
**最后更新**: 2025-12-02

---

## 📋 概述

这是一个完整的 H5 实时推理测试系统，支持在 iPhone Safari 上运行 Luna Badge 的端到端测试。

### 功能特点

- ✅ **实时摄像头流**: 使用 iPhone 后置摄像头实时捕获画面
- ✅ **YOLOv11-tiny 推理**: 服务器端真实模型推理
- ✅ **协议规范**: 完全符合 Luna Badge 协议规范（FrameSpec, InferSpec, HeartbeatSpec）
- ✅ **自动重连**: WebSocket 自动重连机制
- ✅ **性能监控**: 实时显示 FPS、延迟、推理时间、网络 RTT
- ✅ **可视化**: 实时绘制检测框和标签
- ✅ **热衰减测试**: 10 分钟系统资源监控工具

---

## 🚀 快速开始

### 方式 1: 一键启动（推荐）

```bash
cd h5_realtime
bash run_all.sh
```

脚本会自动：
1. 创建虚拟环境
2. 安装依赖（Flask, Flask-Sock, ultralytics, Pillow）
3. 启动后端服务器（端口 5000）
4. 显示 iPhone 访问地址

### 方式 2: 手动启动

```bash
# 1. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 2. 安装依赖
pip install flask flask-sock ultralytics pillow

# 3. 启动服务器
python3 server.py
```

---

## 📱 iPhone 访问

1. 确保 iPhone 和电脑在同一 WiFi 网络
2. 在 iPhone Safari 中打开显示的地址（例如：`http://10.183.232.224:5000`）
3. 允许相机权限
4. 点击"连接服务器"开始测试

---

## 📊 性能指标说明

- **FPS**: 每秒发送的帧数
- **端到端延迟**: 从捕获帧到收到结果的完整延迟
- **推理时间**: YOLO 模型推理耗时
- **导航时间**: 导航决策耗时
- **网络 RTT**: 网络往返延迟
- **上行/下行流量**: 网络带宽使用情况

---

## 🔧 配置

### 修改服务器地址

编辑 `ws_client.js`:

```javascript
const SERVER_HOST = "10.183.232.224";  // 修改为你的服务器 IP
const SERVER_PORT = "5000";            // 修改为你的服务器端口
```

### 修改帧发送间隔

编辑 `app.js`:

```javascript
const FRAME_INTERVAL_MS = 200;  // 修改为需要的间隔（毫秒）
```

---

## 🧪 热衰减测试

运行 10 分钟系统资源监控：

```bash
cd h5_realtime
python3 heat_test.py
```

测试会：
- 每秒记录 CPU/内存使用率
- 每秒记录 GPU 温度（如果可用）
- 生成 JSON 和 CSV 报告

输出文件：
- `perf_logs/heat_YYYYMMDD_HHMMSS.json`
- `perf_logs/heat_YYYYMMDD_HHMMSS.csv`

---

## 📁 文件结构

```
h5_realtime/
├── index.html          # 主页面
├── styles.css          # 样式文件
├── camera.js           # 相机控制模块
├── overlay.js          # 检测框绘制模块
├── metrics.js          # 性能监控模块
├── ws_client.js        # WebSocket 客户端（协议规范）
├── app.js              # 主应用逻辑
├── server.py           # Flask + WebSocket 服务器
├── run_all.sh          # 一键启动脚本
├── heat_test.py        # 热衰减测试工具
└── README.md           # 本文件
```

---

## 🔌 协议规范

本系统完全符合 Luna Badge 协议规范：

- **FrameSpec**: 前端发送的帧数据格式
- **InferSpec**: 后端返回的推理结果格式
- **HeartbeatSpec**: WebSocket 心跳机制
- **ErrorSpec**: 错误处理格式

详细规范见：`../docs/protocol/`

---

## 🐛 故障排查

### 问题 1: 相机无法启动

**原因**: iOS Safari 需要 HTTPS 或 localhost

**解决**: 
- 使用 HTTPS（需要 SSL 证书）
- 或使用 `localhost` 访问（仅限本机）

### 问题 2: WebSocket 连接失败

**原因**: 防火墙或网络问题

**解决**:
- 检查防火墙设置
- 确保 iPhone 和电脑在同一 WiFi
- 检查服务器 IP 地址是否正确

### 问题 3: 模型加载失败

**原因**: ultralytics 未安装或模型文件不存在

**解决**:
```bash
pip install ultralytics
# 模型会自动下载到 ~/.ultralytics/models/
```

---

## 📚 相关文档

- [协议规范文档](../docs/protocol/)
- [运营测试指南](../docs/ONE_CLICK_OPERATIONAL_TEST.md)

---

**最后更新**: 2025-12-02
















