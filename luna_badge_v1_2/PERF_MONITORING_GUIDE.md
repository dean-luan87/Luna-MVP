# Luna Badge v1.3.1 性能监控体系使用指南

## 📋 概述

v1.3.1 版本提供了完整的性能监控体系，包括：
- **实时链路 Demo**（交互模式 + 压测模式）
- **自动性能采样**（每帧记录）
- **可视化 Dashboard**（HTML 图表）
- **瓶颈分析工具**（自动识别优化点）

---

## 🚀 快速开始

### 1. 运行压测（推荐）

```bash
# 运行 60 秒压测，关闭 TTS（避免干扰）
python3 demo_realtime_navigation.py \
  --mode stress \
  --tag yolo11tiny_1.3.1 \
  --stress-duration 60 \
  --no-tts
```

**输出文件：**
- `perf_logs/yolo11tiny_1.3.1_stress_YYYYMMDD_HHMMSS_samples.csv`
- `perf_logs/yolo11tiny_1.3.1_stress_YYYYMMDD_HHMMSS_report.json`

### 2. 生成 Dashboard

```bash
python3 generate_perf_dashboard.py
```

**输出文件：**
- `perf_logs/<tag>_<mode>_<timestamp>_dashboard.html`

**查看方式：**
```bash
open perf_logs/*_dashboard.html
```

### 3. 瓶颈分析

```bash
python3 analyze_bottleneck.py
```

**输出：**
- 控制台打印瓶颈分析结果
- `perf_logs/<tag>_<mode>_<timestamp>_bottleneck_report.json`

---

## 📊 功能详解

### demo_realtime_navigation.py

#### 运行模式

**交互模式（默认）：**
```bash
python3 demo_realtime_navigation.py --mode interactive
```
- 实时导航 + 控制台输出
- 每 10 帧输出一次统计信息
- 按 Ctrl+C 退出

**压测模式：**
```bash
python3 demo_realtime_navigation.py --mode stress --stress-duration 60
```
- 持续运行指定时长
- 记录性能热衰减
- 自动生成报告

#### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--mode` | 运行模式：`interactive` 或 `stress` | `interactive` |
| `--device` | 摄像头设备索引 | `0` |
| `--no-tts` | 关闭 TTS 播报 | `False` |
| `--tag` | 测试标签（用于文件命名） | `default` |
| `--stress-duration` | 压测模式：持续秒数 | `60` |
| `--stress-max-frames` | 压测模式：最大帧数 | `None` |

#### 输出文件

**CSV 文件（原始数据）：**
- 字段：`tag`, `mode`, `frame`, `det_ms`, `nav_ms`, `total_ms`, `fps`, `objects`
- 用途：可导入 PowerBI/Tableau 进行深度分析

**JSON 报告（统计指标）：**
- `count`: 总帧数
- `avg_total`, `avg_det`, `avg_nav`: 平均延迟
- `p50`, `p90`, `p95`, `p99`: 百分位数
- `min`, `max`: 最小/最大延迟

---

### generate_perf_dashboard.py

#### 功能

自动读取 `perf_logs/` 中最新的一组采样文件，生成 HTML Dashboard。

#### 图表内容

1. **全链路延迟曲线**
   - total_ms（红色）
   - det_ms（蓝色）
   - nav_ms（绿色）

2. **FPS 曲线**
   - 实时帧率变化

3. **平均耗时拆分**
   - det_ms / nav_ms / overhead / total_ms 的柱状图

#### 使用方式

```bash
python3 generate_perf_dashboard.py
```

会自动找到最新的 `*_samples.csv` 和对应的 `*_report.json`，生成 Dashboard。

---

### analyze_bottleneck.py

#### 功能

自动分析性能瓶颈，识别主瓶颈模块并给出优化建议。

#### 输出内容

1. **延迟占比分析**
   - det_ms 占比
   - nav_ms 占比
   - overhead 占比

2. **瓶颈识别**
   - 主瓶颈模块
   - 次要瓶颈模块

3. **优化建议**
   - 根据瓶颈类型给出具体优化建议

#### 使用方式

```bash
python3 analyze_bottleneck.py
```

---

## 📈 典型工作流

### 场景 1：YOLO11-tiny 性能基线测试

```bash
# 1. 运行压测
python3 demo_realtime_navigation.py \
  --mode stress \
  --tag yolo11tiny_baseline \
  --stress-duration 60 \
  --no-tts

# 2. 生成 Dashboard
python3 generate_perf_dashboard.py

# 3. 瓶颈分析
python3 analyze_bottleneck.py

# 4. 查看 Dashboard
open perf_logs/*_dashboard.html
```

### 场景 2：实时导航体验测试

```bash
# 交互模式，开启 TTS
python3 demo_realtime_navigation.py --mode interactive

# 按 Ctrl+C 退出后自动生成报告
```

### 场景 3：热衰减测试

```bash
# 长时间压测，观察性能衰减
python3 demo_realtime_navigation.py \
  --mode stress \
  --tag heat_test \
  --stress-duration 300 \
  --no-tts
```

---

## 🎯 性能指标解读

### 关键指标

- **avg_total**: 平均全链路延迟（目标 < 250ms）
- **p95**: 95% 请求的延迟（尾部延迟）
- **p99**: 99% 请求的延迟（极端情况）
- **fps**: 平均帧率（目标 > 20 FPS）

### 瓶颈判断

- **det_ms > 80%**: 检测模块是瓶颈，考虑模型优化
- **nav_ms > 20%**: 导航模块是瓶颈，考虑算法优化
- **overhead > 10%**: 系统开销过大，检查预处理/日志

---

## 📁 文件结构

```
luna_badge_v1_2/
├── demo_realtime_navigation.py      # 主脚本（交互/压测）
├── generate_perf_dashboard.py      # Dashboard 生成
├── analyze_bottleneck.py            # 瓶颈分析
└── perf_logs/                       # 性能日志目录
    ├── <tag>_<mode>_<timestamp>_samples.csv
    ├── <tag>_<mode>_<timestamp>_report.json
    ├── <tag>_<mode>_<timestamp>_dashboard.html
    └── <tag>_<mode>_<timestamp>_bottleneck_report.json
```

---

## 💡 最佳实践

1. **压测前准备**
   - 关闭不必要的应用
   - 确保摄像头可用
   - 使用 `--no-tts` 避免音频干扰

2. **标签命名**
   - 使用有意义的标签，如 `yolo11tiny_v1.3.1`
   - 便于后续对比分析

3. **定期运行**
   - 每次代码变更后运行压测
   - 建立性能基线
   - 监控性能回归

4. **Dashboard 分析**
   - 关注延迟趋势（是否稳定）
   - 关注 FPS 曲线（是否有下降）
   - 对比不同版本的 Dashboard

---

## 🔧 故障排查

### 问题：找不到采样文件

**解决：**
```bash
# 先运行一次 demo 生成采样
python3 demo_realtime_navigation.py --mode stress --stress-duration 10 --no-tts
```

### 问题：Dashboard 无法打开

**解决：**
- 检查浏览器是否支持 Chart.js
- 确认 HTML 文件路径正确
- 检查 CSV 文件是否存在

### 问题：摄像头无法打开

**解决：**
```bash
# 尝试不同的设备索引
python3 demo_realtime_navigation.py --device 1
```

---

## 📚 相关文档

- `benchmarks/README.md` - 性能测试套件说明
- `TEST_SCRIPTS_README.md` - 测试脚本说明

---

**版本：** v1.3.1  
**更新日期：** 2025-12-02


