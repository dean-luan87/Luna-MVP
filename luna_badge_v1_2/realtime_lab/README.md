# Luna Realtime H5 Lab

独立的 H5 + WebSocket 实时推理实验模块，用于：

- 在 iPhone 上做真实摄像头测试
- 验证 YOLOv11-tiny 延迟
- 做 10 分钟热衰减测试

## 一键运行

```bash
cd realtime_lab
bash scripts/run_all_realtime.sh
```

然后在手机 Safari 访问：

```
http://<你的电脑IP>:8081
```

**注意**: 如果端口 8080 被占用，脚本会自动使用 8081。WebSocket 使用端口 5001（避免与 macOS AirPlay 冲突）。

即可看到实时画面 + 检测框 + FPS + 延迟 + 带宽。

---

## 目录结构

```
realtime_lab/
├── backend/
│   ├── server.py          # WebSocket 推理服务器
│   └── requirements.txt   # Python 依赖
├── frontend/
│   ├── index.html         # H5 主页面
│   ├── styles.css         # 样式
│   ├── camera.js          # 相机控制
│   ├── overlay.js         # 检测框绘制
│   ├── metrics.js         # 性能统计
│   ├── ws_client.js       # WebSocket 客户端
│   └── app.js             # 主应用逻辑
├── scripts/
│   ├── run_all_realtime.sh    # 一键启动脚本
│   ├── heat_stress_10min.py   # 热衰减测试
│   └── analyze_heat.py        # 热衰减分析
├── logs/
│   └── .gitkeep           # 日志目录
└── README.md              # 本文件
```

---

## 使用说明

### 1. 启动服务

```bash
cd realtime_lab
bash scripts/run_all_realtime.sh
```

脚本会自动：
- 创建虚拟环境（`.venv_realtime`）
- 安装依赖
- 启动后端服务器（端口 5000）
- 启动前端静态服务器（端口 8080）

### 2. iPhone 访问

1. 确保 iPhone 和电脑在同一 WiFi
2. 在 iPhone Safari 打开显示的地址（例如：`http://10.183.232.224:8080`）
3. 允许相机权限
4. 自动开始实时检测

### 3. 热衰减测试

```bash
cd realtime_lab/scripts
python3 heat_stress_10min.py  # 运行 10 分钟监控
python3 analyze_heat.py        # 分析结果
```

---

## 功能特点

- ✅ **实时摄像头流**: iPhone 后置摄像头实时捕获
- ✅ **YOLOv11-tiny 推理**: 服务器端真实模型推理
- ✅ **自动重连**: WebSocket 自动重连机制
- ✅ **性能监控**: FPS、延迟、带宽统计
- ✅ **可视化**: 实时绘制检测框和标签
- ✅ **热衰减测试**: 10 分钟系统资源监控

---

## 技术栈

- **前端**: HTML5 + JavaScript (ES6+)
- **后端**: Python + Flask + Flask-Sock
- **模型**: YOLOv11-tiny (ultralytics)
- **协议**: 简单 WebSocket JSON 协议

---

## 健康检查

后端提供 HTTP 健康检查接口：

```bash
curl http://localhost:5000/health
```

返回：
```json
{
  "status": "ok",
  "model": "yolov11n.pt",
  "total_frames": 1234,
  "avg_latency_ms": 45.2,
  "last_latency_ms": 43.1,
  "last_error": null
}
```

---

## 故障排查

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

## 独立使用

这个模块是完全独立的，可以：

1. **在当前工程中使用**: 直接运行 `bash scripts/run_all_realtime.sh`
2. **拆分成独立 repo**: 将 `realtime_lab/` 目录复制出去即可
3. **集成到测试体系**: 使用 `tests/realtime/test_realtime_smoke.py`

---

**最后更新**: 2025-12-02

