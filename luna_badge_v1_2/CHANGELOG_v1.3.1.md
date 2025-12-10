# Luna Badge v1.3.1 版本发布说明

**发布日期**: 2025-12-02  
**Git 标签**: v1.3.1  
**提交哈希**: d9e58ed

## 🎯 版本概述

v1.3.1 是实时推理系统的完整版本，实现了从 iPhone H5 前端到后端 YOLO 推理的完整链路，支持 HTTPS 安全连接和实时性能监控。

## ✨ 主要特性

### 1. HTTPS 实时推理服务器
- ✅ FastAPI + Uvicorn 服务器
- ✅ 自动 SSL 证书生成和管理
- ✅ 支持 iOS Safari 摄像头访问（HTTPS 要求）
- ✅ 健康检查和心跳监控
- ✅ 自动 IP 地址识别（公司/家庭网络）

### 2. H5 前端完整实现
- ✅ 实时摄像头流处理
- ✅ 帧压缩和传输（200ms 间隔）
- ✅ 检测结果可视化（边界框绘制）
- ✅ 性能监控（FPS、延迟、带宽）
- ✅ 自动重连和错误处理
- ✅ 心跳检测和状态显示

### 3. YOLO11-tiny 模型集成
- ✅ 模型管理系统（ModelRegistry）
- ✅ 统一模型加载器（YoloLoader）
- ✅ 支持 PyTorch 和 ONNX 框架
- ✅ 模型健康检查（Smoke Test）
- ✅ 配置文件管理（YAML）

### 4. 性能监控系统
- ✅ 实时延迟统计（端到端、推理、网络）
- ✅ JSONL 日志格式
- ✅ 性能 Dashboard（HTML + ECharts）
- ✅ 瓶颈分析工具
- ✅ 热衰减测试（10 分钟压力测试）

### 5. 协议标准化
- ✅ FrameSpec（前端 → 后端）
- ✅ InferSpec（后端 → 前端）
- ✅ HeartbeatSpec（心跳协议）
- ✅ PerfLogSpec（性能日志）
- ✅ ErrorSpec（错误码规范）

## 📁 新增文件结构

```
luna_badge_v1_2/
├── realtime_server.py          # FastAPI 实时推理服务器
├── web/                        # H5 前端页面
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── core/
│   ├── model_registry.py       # 模型注册表
│   ├── yolo_loader.py          # 统一模型加载器
│   └── yolo_detector.py        # YOLO 检测器
├── configs/
│   └── model_registry.yaml     # 模型配置文件
├── ssl_certs/                  # SSL 证书目录
│   ├── cert.pem
│   └── key.pem
├── generate_ssl_cert.sh        # SSL 证书生成脚本
├── run_realtime_op_test.sh     # 一键运营测试脚本
└── heat_decay_test.py          # 热衰减测试工具
```

## 🔧 技术栈

- **后端**: FastAPI, Uvicorn, YOLO11-tiny (PyTorch)
- **前端**: HTML5, JavaScript, Canvas API, WebSocket/HTTP POST
- **安全**: HTTPS/WSS, 自签名 SSL 证书
- **监控**: JSONL 日志, ECharts Dashboard, 性能分析工具

## 📊 性能指标

- **平均推理延迟**: 43-46ms
- **延迟范围**: 26-103ms
- **帧率**: 5 FPS（200ms 间隔）
- **检测精度**: YOLO11-tiny 标准精度

## 🚀 快速开始

### 1. 启动服务器

```bash
bash run_realtime_op_test.sh
```

### 2. iPhone 访问

- 公司网络: `https://10.183.232.224:5001`
- 家庭网络: `https://192.168.3.57:5001`

### 3. 首次访问步骤

1. Safari 会提示「此连接不是私人连接」
2. 点击「显示详细信息」或「高级」
3. 点击「访问此网站」或「继续访问」
4. 允许摄像头权限
5. 开始实时检测

## 📝 开发分支

- **当前开发分支**: `dev-1.4.0`
- **稳定版本**: `v1.3.1` (标签)

## 🔄 版本历史

- **v1.3.1** (2025-12-02): 实时推理系统完整版
- **v1.0.0**: 初始版本

## 📚 相关文档

- `docs/protocol/`: 协议规范文档
- `docs/OPERATIONAL_MONITORING_GUIDE.md`: 运营监控指南
- `docs/MODEL_SMOKE_TEST.md`: 模型健康检查文档

---

**Luna Badge Team**  
*让 AI 更贴近生活* 🚀





