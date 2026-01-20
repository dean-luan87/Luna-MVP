# Luna Badge 运营级监控体系使用指南

## 📋 概述

本监控体系提供**生产级**的性能监控、分析和可视化能力，覆盖从数据采集到决策支持的全链路。

## 🏗️ 架构

### 三层架构

1. **采集层**：前端 + 后端全链路埋点
2. **汇总层**：统一 JSONL/CSV 日志 + 自动聚合脚本
3. **展示与决策层**：Dashboard + 瓶颈分析 + 模型对比报告

## 📁 文件结构

```
luna_badge_v1_2/
├── perf_logger.py              # 统一日志记录器
├── realtime_server.py           # 后端服务（已集成埋点）
├── static/
│   └── realtime_client.html     # 前端页面（已集成埋点）
├── scripts/
│   ├── analyze_perf.py          # 性能分析脚本
│   ├── build_dashboard.py       # Dashboard 生成脚本
│   └── compare_models.py       # 模型对比脚本
├── tools/
│   └── run_realtime_op_test.sh  # 一键运营测试脚本
└── perf_logs/                   # 日志输出目录
    ├── run_<run_id>.jsonl      # 原始日志（JSONL 格式）
    ├── run_<run_id>.csv        # CSV 格式（供 Dashboard 使用）
    └── run_<run_id>.html       # 交互式 Dashboard
```

## 🔧 快速开始

### 1. 启动服务

```bash
cd luna_badge_v1_2
python3 realtime_server.py \
  --host 0.0.0.0 \
  --port 8899 \
  --model yolo11n.pt \
  --ssl-keyfile ssl_certs/key.pem \
  --ssl-certfile ssl_certs/cert.pem
```

### 2. 在 iPhone 上测试

1. 打开浏览器访问：`https://<你的Mac IP>:8899/static/realtime_client.html`
2. 点击「开始连续导航（200ms 一帧）」
3. 运行 2-5 分钟真实场景
4. 点击「停止」

**注意**：所有性能数据会自动记录，无需手动操作。

### 3. 运行分析

```bash
bash tools/run_realtime_op_test.sh
```

脚本会自动：
- 查找最新日志文件
- 运行性能分析
- 生成 Dashboard
- 输出统计报告

## 📊 日志格式

### 运行级别（run）

```json
{
  "type": "run",
  "run_id": "2025-12-02T11-30-01Z_iphone_y11t",
  "start_ts": 1733129401.123,
  "end_ts": 1733129463.456,
  "app_version": "1.3.1",
  "server_version": "1.3.1",
  "device": {
    "platform": "iOS",
    "model": "iPhone15,2",
    "os_version": "18.1",
    "browser": "Safari"
  },
  "model": {
    "name": "yolov11-tiny",
    "checkpoint": "yolo11n.pt"
  }
}
```

### 帧级别（frame）

```json
{
  "type": "frame",
  "run_id": "...",
  "frame_id": "183",
  "seq": 183,
  "ts_client_capture": 1733129402.123,
  "ts_client_send": 1733129402.147,
  "ts_server_recv": 1733129402.162,
  "ts_server_det_done": 1733129402.228,
  "ts_server_send": 1733129402.232,
  "ts_client_recv": 1733129402.247,
  "ts_client_render": 1733129402.251,
  "client": {
    "capture_ms": 3.4,
    "encode_ms": 16.2,
    "pack_ms": 1.1
  },
  "network": {
    "upload_ms": 15.0,
    "download_ms": 15.0,
    "rtt_ms": 30.0
  },
  "server": {
    "decode_ms": 2.7,
    "preprocess_ms": 1.9,
    "inference_ms": 41.3,
    "postprocess_ms": 3.6,
    "pack_ms": 0.8
  },
  "end_to_end_ms": 124.6,
  "image_bytes": 48231,
  "det_count": 4,
  "detections": [...]
}
```

### 事件级别（event）

```json
{
  "type": "event",
  "run_id": "...",
  "event_id": "rtt_1733129402.567",
  "ts": 1733129402.567,
  "type": "network_rtt",
  "level": "INFO",
  "meta": {
    "rtt_ms": 23.4
  }
}
```

## 📈 性能分析

### 运行分析脚本

```bash
python3 scripts/analyze_perf.py perf_logs/run_2025-12-02T11-30-01Z_iphone_y11t.jsonl
```

**输出示例**：

```
======================================================================
Luna Badge 性能分析报告
======================================================================
日志文件: run_2025-12-02T11-30-01Z_iphone_y11t.jsonl
总帧数: 1500

端到端延迟统计:
  平均: 124.6ms
  中位数 (P50): 118.3ms
  P90: 156.2ms
  P95: 178.9ms
  P99: 234.5ms
  最小: 89.2ms
  最大: 456.7ms

分段耗时统计:
  server_infer        41.3ms  ( 33.1%)
  client_encode       16.2ms  ( 13.0%)
  net_upload          15.0ms  ( 12.0%)
  net_download        15.0ms  ( 12.0%)
  server_decode        2.7ms  (  2.2%)

⚠️  瓶颈分析（按平均耗时排序）:
  1. server_infer        41.3ms  ( 33.1%)
  2. client_encode       16.2ms  ( 13.0%)
  3. net_upload          15.0ms  ( 12.0%)

建议优先优化: server_infer
```

## 📊 Dashboard

### 生成 Dashboard

```bash
python3 scripts/build_dashboard.py perf_logs/run_2025-12-02T11-30-01Z_iphone_y11t.jsonl
```

### 打开 Dashboard

```bash
open perf_logs/run_2025-12-02T11-30-01Z_iphone_y11t.html
```

**Dashboard 包含**：
- 总帧数、平均延迟、P95/P99 延迟统计卡片
- 端到端延迟分布图（折线图）
- 各阶段平均耗时（柱状图）
- 延迟趋势图（最近 100 帧）

## 🔍 模型对比

### 对比多个运行

```bash
python3 scripts/compare_models.py \
  perf_logs/run_2025-12-02_y8.jsonl \
  perf_logs/run_2025-12-02_y11.jsonl \
  perf_logs/run_2025-12-02_y11t.jsonl
```

**输出示例**：

```
====================================================================================================
模型对比结果
====================================================================================================

Run ID                          Frames   Lat Avg    Lat P95    Lat P99    Inf Avg    Inf P95
----------------------------------------------------------------------------------------------------
2025-12-02_y8                   1500     156.3      198.5      234.5      78.2       95.3
2025-12-02_y11                  1500     142.1      178.9      212.3      65.4       82.1
2025-12-02_y11t                 1500     124.6      156.2      189.7      41.3       58.9

🏆 最佳端到端延迟: 2025-12-02_y11t (124.6ms)
🏆 最佳推理速度: 2025-12-02_y11t (41.3ms)
```

## 🚀 一键运营测试

### 使用一键脚本

```bash
bash tools/run_realtime_op_test.sh
```

脚本会：
1. 检查服务是否运行
2. 提示你在 iPhone 上测试
3. 等待测试完成
4. 自动运行分析和 Dashboard 生成
5. 输出完整报告

### 对比多个模型

```bash
bash tools/run_realtime_op_test.sh run_id_1 perf_logs/run_model1.jsonl perf_logs/run_model2.jsonl
```

## 📝 API 接口

### POST /perf_log

接收前端批量日志。

**请求体**：

```json
{
  "run_id": "2025-12-02T11-30-01Z_iphone_y11t",
  "records": [
    {"type": "frame", ...},
    {"type": "event", ...}
  ]
}
```

**响应**：

```json
{
  "ok": true,
  "received": 2
}
```

## 🎯 最佳实践

### 1. 测试时长

建议每次测试运行 **2-5 分钟**，确保有足够的数据样本（约 600-1500 帧）。

### 2. 测试场景

- 室内走廊
- 室外街道
- 不同光照条件
- 不同网络环境

### 3. 模型对比

在相同场景下测试不同模型，确保对比的公平性。

### 4. 定期分析

建议每周运行一次完整分析，跟踪性能趋势。

## 🔧 故障排查

### 日志文件未生成

1. 检查 `perf_logs/` 目录权限
2. 检查前端是否成功发送日志到 `/perf_log`
3. 查看服务器日志：`tail -f realtime_server.log`

### Dashboard 无法打开

1. 确保已运行 `analyze_perf.py` 生成 CSV
2. 检查 CSV 文件是否存在
3. 检查浏览器控制台错误

### 性能数据异常

1. 检查网络延迟是否正常
2. 检查服务器负载
3. 查看详细日志定位问题

## 📚 相关文档

- [性能监控指南](./PERF_MONITORING_GUIDE.md)
- [自愈系统手册](./self_heal_book.md)

## 🆘 支持

如有问题，请查看：
- 服务器日志：`realtime_server.log`
- 前端控制台：浏览器开发者工具
- 日志文件：`perf_logs/run_*.jsonl`

















