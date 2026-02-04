# Luna Badge 一键运营测试系统使用指南

## 📋 概述

一键运营测试系统提供**完整自动化**的性能测试、分析和报告生成能力，只需一个命令即可完成从测试到报告的整个流程。

## 🚀 快速开始

### 基本使用

```bash
bash tools/run_realtime_op_test.sh
```

脚本会自动：
1. ✅ 检查服务状态（如未运行会提示启动）
2. ✅ 引导你在 iPhone 上完成测试
3. ✅ 自动分析性能数据
4. ✅ 生成交互式 Dashboard
5. ✅ 进行模型对比（如有多个测试）
6. ✅ 生成 Markdown 运营报告

## 📁 生成的文件

运行测试后，会在 `perf_logs/` 目录下生成：

```
perf_logs/
├── run_20251202_143022.jsonl      # 原始性能日志
├── run_20251202_143022.csv        # CSV 格式数据
├── run_20251202_143022.html       # 交互式 Dashboard
└── report_run_20251202_143022.md  # Markdown 运营报告
```

## 📊 运营报告内容

自动生成的 Markdown 报告包含：

1. **测试目的** - 验证清单
2. **测试环境** - 设备、模型、配置信息
3. **性能结果摘要** - 关键指标和 KPI 达成情况
4. **模型对比结果** - 多模型性能对比（如有）
5. **瓶颈分析** - 性能瓶颈识别和优化建议
6. **总结 & 建议** - 性能评估和优化建议

## 🛠️ 辅助工具

### 1. 日志收集工具

收集指定 run_id 的所有相关文件并打包：

```bash
bash tools/collect_logs.sh run_20251202_143022
```

**输出：**
- 复制所有相关文件到临时目录
- 生成 tar.gz 压缩包
- 创建 README.txt 说明文件

### 2. 清理旧测试工具

清理指定天数之前的测试日志：

```bash
# 预览模式（不会实际删除）
bash tools/clean_old_runs.sh

# 删除 7 天前的日志，保留最新 5 个
bash tools/clean_old_runs.sh -d 7 -k 5

# 实际执行删除
bash tools/clean_old_runs.sh -d 7 -k 5 -f
```

**选项：**
- `-d, --days N`: 删除 N 天前的日志（默认: 30）
- `-k, --keep N`: 保留最新的 N 个测试（默认: 10）
- `-f, --force`: 实际执行删除（默认: 仅预览）

## 📈 测试流程

### 步骤 1: 启动服务

确保服务正在运行：

```bash
python3 realtime_server.py \
  --host 0.0.0.0 \
  --port 8899 \
  --model yolo11n.pt \
  --ssl-keyfile ssl_certs/key.pem \
  --ssl-certfile ssl_certs/cert.pem
```

如果服务未运行，脚本会提示是否启动。

### 步骤 2: 在 iPhone 上测试

1. 打开浏览器访问：`https://<你的Mac IP>:8899/static/realtime_client.html`
2. 点击「开始连续导航（200ms 一帧）」
3. 进行实际导航场景测试（建议 30-120 秒）
4. 点击「停止」

**注意：** 所有性能数据会自动记录，无需手动操作。

### 步骤 3: 运行一键测试

```bash
bash tools/run_realtime_op_test.sh
```

脚本会：
- 等待你完成测试
- 自动查找最新日志文件
- 运行所有分析脚本
- 生成完整报告

### 步骤 4: 查看结果

```bash
# 打开 Dashboard
open perf_logs/run_*.html

# 查看报告
cat perf_logs/report_*.md

# 或使用编辑器
code perf_logs/report_*.md
```

## 📊 报告解读

### 性能指标

- **总帧数**: 测试期间处理的帧数
- **平均延迟**: 所有帧的平均端到端延迟
- **P95 延迟**: 95% 的帧延迟低于此值
- **P99 延迟**: 99% 的帧延迟低于此值

### KPI 达成情况

- **目标**: < 250ms
- **平均延迟**: ✅/❌ 达成情况
- **P95 延迟**: ✅/❌ 达成情况

### 瓶颈分析

报告会自动识别性能瓶颈，按平均耗时排序：
1. 主要瓶颈（占比最高）
2. 次要瓶颈
3. 优化建议

## 🔍 模型对比

如果有多个测试日志，脚本会自动进行模型对比：

```bash
# 运行多个测试
bash tools/run_realtime_op_test.sh  # 第一次测试
# ... 更换模型后 ...
bash tools/run_realtime_op_test.sh  # 第二次测试

# 对比所有模型
python3 scripts/compare_models.py perf_logs/run_*.jsonl
```

**对比指标：**
- 端到端延迟（平均、P95、P99）
- 推理速度（平均、P95）
- 自动识别最佳模型

## 💡 最佳实践

### 1. 测试时长

- **最短**: 30 秒（约 150 帧）
- **推荐**: 60-120 秒（约 300-600 帧）
- **深度测试**: 5-10 分钟（约 1500-3000 帧）

### 2. 测试场景

建议在不同场景下测试：
- 室内走廊
- 室外街道
- 不同光照条件
- 不同网络环境

### 3. 模型对比

确保对比的公平性：
- 相同测试场景
- 相同测试时长
- 相同网络环境

### 4. 定期清理

定期清理旧日志，节省磁盘空间：

```bash
# 每月清理一次（保留最新 10 个）
bash tools/clean_old_runs.sh -d 30 -k 10 -f
```

## 🐛 故障排查

### 问题 1: 未找到日志文件

**原因**: 测试未完成或日志未生成

**解决**:
1. 确认在 iPhone 上完成了测试
2. 检查 `perf_logs/` 目录权限
3. 查看服务器日志：`tail -f realtime_server.log`

### 问题 2: 分析脚本失败

**原因**: 日志格式不正确或缺少必要字段

**解决**:
1. 检查 JSONL 文件格式
2. 确认包含 `type: "frame"` 的记录
3. 查看脚本错误信息

### 问题 3: Dashboard 无法打开

**原因**: CSV 文件未生成或格式错误

**解决**:
1. 确保先运行 `analyze_perf.py`
2. 检查 CSV 文件是否存在
3. 查看浏览器控制台错误

## 📚 相关文档

- [运营监控指南](./OPERATIONAL_MONITORING_GUIDE.md)
- [性能监控指南](./PERF_MONITORING_GUIDE.md)
- [自愈系统手册](./self_heal_book.md)

## 🆘 支持

如有问题，请查看：
- 服务器日志：`realtime_server.log`
- 脚本输出：终端错误信息
- 日志文件：`perf_logs/run_*.jsonl`

---

**最后更新**: 2025-12-02

















