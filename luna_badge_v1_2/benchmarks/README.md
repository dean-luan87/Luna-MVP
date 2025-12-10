# Luna Badge 性能测试套件

## 📋 概述

本目录包含 Luna Badge 1.3.0 的性能测试工具，用于：
- YOLO 多模型对比
- 链路压测（并发 + 热衰减）
- 自动可视化 Dashboard

所有结果输出到 `perf_logs/` 目录，便于后台回传和 Dashboard 展示。

---

## 🚀 快速开始

### 一键运行所有测试

```bash
bash benchmarks/run_perf_suite.sh
```

### 单独运行

```bash
# 1. YOLO 模型对比
python3 benchmarks/benchmark_yolo_models.py

# 2. 链路压测（60秒，并发4）
python3 benchmarks/stress_realtime_pipeline.py --duration 60 --concurrency 4

# 3. 生成 Dashboard
python3 benchmarks/perf_dashboard.py
```

---

## 📊 脚本说明

### 1. benchmark_yolo_models.py

**功能**: 对比 yolov8, yolov11, yolov11-tiny 三种模型的检测耗时

**输出**:
- `perf_logs/yolo_model_benchmark.json` - 详细报告（JSON）
- `perf_logs/yolo_model_benchmark.csv` - 表格数据（CSV）

**统计指标**:
- avg, p50, p90, p95, p99, min, max

---

### 2. stress_realtime_pipeline.py

**功能**: 链路压测，观察并发下的性能衰减和错误率

**参数**:
- `--duration`: 压测持续时间（秒），默认 60
- `--concurrency`: 并发线程数，默认 4

**输出**:
- `perf_logs/stress_realtime_result.json` - 压测结果报告
- `perf_logs/stress_realtime_samples.csv` - 样本数据（用于可视化）

**统计指标**:
- 总请求数、成功数、失败数、错误率
- 延迟统计（avg, p50, p90, p95, p99）

---

### 3. perf_dashboard.py

**功能**: 自动生成可视化 Dashboard（HTML + Chart.js）

**输出**:
- `perf_logs/perf_dashboard.html` - 可视化 Dashboard

**图表内容**:
- YOLO 模型对比（柱状图）
- 链路压测延迟曲线（折线图）
- 全链路各段耗时分布（饼图）

**查看方式**:
用浏览器打开 `perf_logs/perf_dashboard.html`

---

## 📁 输出文件结构

```
perf_logs/
├── yolo_model_benchmark.json      # YOLO 模型对比报告
├── yolo_model_benchmark.csv        # YOLO 模型对比 CSV
├── stress_realtime_result.json     # 压测结果报告
├── stress_realtime_samples.csv     # 压测样本数据
└── perf_dashboard.html             # 可视化 Dashboard
```

---

## 🔧 配置说明

### 模块适配

所有脚本都支持自动容错：
- 优先使用真实模块
- 模块不可用时自动降级到 Mock
- 不影响整体测试流程

### 自定义参数

```bash
# 压测参数
python3 benchmarks/stress_realtime_pipeline.py --duration 120 --concurrency 8

# YOLO 测试次数（修改脚本中的 runs 参数）
# 默认 30 次，可在 benchmark_yolo_models.py 中调整
```

---

## 📈 使用场景

### 1. 模型选型

运行 YOLO 模型对比，选择最适合当前环境的模型：
- 性能最优（延迟最低）
- 准确率满足要求
- 资源占用合理

### 2. 性能基线

运行链路压测，建立性能基线：
- 平均延迟
- P95/P99 延迟
- 错误率
- 热衰减情况

### 3. 性能监控

定期运行测试套件，监控性能趋势：
- 性能是否退化
- 新版本是否优化
- 瓶颈模块识别

---

## 🎯 下一步

1. **运行完整测试套件**
   ```bash
   bash benchmarks/run_perf_suite.sh
   ```

2. **查看 Dashboard**
   ```bash
   open perf_logs/perf_dashboard.html  # macOS
   # 或直接用浏览器打开
   ```

3. **分析结果**
   - 查看哪个 YOLO 模型最适合
   - 观察压测下的延迟分布
   - 检查 Dashboard 曲线

4. **优化建议**
   - 根据结果优化瓶颈模块
   - 调整模型配置
   - 优化并发策略

---

**版本**: 1.3.0  
**最后更新**: 2025-12-02







