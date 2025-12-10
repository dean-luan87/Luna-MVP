# Luna Badge v1.3.0 一键测试脚本使用说明

## 📋 脚本概述

本目录包含两个核心测试脚本，用于自动化 Luna Badge v1.3.0 的完整测试流程：

1. **`run_full_test.sh`** - 一键运行完整测试套件
2. **`analyze_errors.sh`** - 自动分析测试结果和错误率

---

## 🚀 快速开始

### 方式一：完整测试流程

```bash
# 1. 运行完整测试（约 2-5 分钟）
bash run_full_test.sh

# 2. 分析测试结果
bash analyze_errors.sh
```

### 方式二：仅分析已有结果

```bash
# 如果已有测试结果，直接分析
bash analyze_errors.sh
```

---

## 📊 run_full_test.sh 详细说明

### 功能

自动执行以下 5 个测试步骤：

1. **关键单元测试** (3 个模块)
   - `test_detection.py`
   - `test_fusion.py`
   - `test_path_detector.py`

2. **A-Z 全量模块测试**
   - 运行所有模块的单元测试

3. **压力测试**
   - 持续时间：60 秒
   - 并发线程：2
   - 收集 CPU/MEM 指标

4. **NAV_STUCK 监控**
   - 收集导航卡死事件统计

5. **LNB v1.1 工程评分**
   - 计算包含 NAV_STUCK 的综合评分

### 输出文件

所有测试结果保存在 `test_reports/` 目录：

- `test_detection.log` - detection 模块测试日志
- `test_fusion.log` - fusion 模块测试日志
- `test_path_detector.log` - path_detector 模块测试日志
- `test_AZ.log` - A-Z 全量测试日志
- `stress_test.log` - 压力测试日志
- `stress_report.json` - 压力测试结果（JSON）
- `nav_stuck.log` - NAV_STUCK 收集日志
- `lnb_score.log` - LNB 评分日志
- `lnb_score_nav.json` - LNB 评分结果（JSON）

---

## 🔍 analyze_errors.sh 详细说明

### 功能

自动分析所有测试结果，输出：

1. **单元测试统计**
   - 各模块的通过/失败次数

2. **压力测试统计**
   - 总测试数、成功数、失败数
   - **错误率计算**

3. **LNB 评分**
   - 总分
   - KPI7 (压力测试错误率)

4. **失败模块详情**
   - 列出所有失败的模块和次数

5. **目标达成判断**
   - 判断是否达到错误率 0% 目标

### 输出示例

```
============================================
🔍 Luna 测试结果分析
============================================

📊 单元测试结果:
  detection:      通过 1, 失败 0
  fusion:         通过 1, 失败 0
  path_detector:  通过 2, 失败 0
  A-Z:            失败 0

🔥 压力测试结果:
  总测试数: 60
  成功: 44
  失败: 16

📈 错误率: 26.67%

⭐ LNB v1.1 评分:
  总分: 82.73 / 100
  KPI7 (压力测试): 40 分

📋 失败模块详情:
  ❌ 压力测试: 16 次失败
============================================
```

---

## 🎯 目标：错误率 = 0%

### 当前状态

- **错误率**: 26.67%
- **目标**: 0%
- **差距**: 需要修复 16 次失败

### 达成路径

1. **运行测试** → `bash run_full_test.sh`
2. **分析结果** → `bash analyze_errors.sh`
3. **修复失败** → 根据失败模块详情修复
4. **重复步骤 1-3** → 直到错误率 = 0%

---

## 📈 进阶功能（可选）

如需以下功能，可以继续扩展：

- ✅ 自动修补报告生成
- ✅ 错误原因智能分类
- ✅ 模块级错误热力图
- ✅ 自动回滚机制
- ✅ 失败截图/日志上传后台
- ✅ LNB 评分趋势图
- ✅ 失败模式聚类

---

## 🔧 故障排除

### 问题 1: 脚本无执行权限

```bash
chmod +x run_full_test.sh analyze_errors.sh
```

### 问题 2: pytest 未安装

```bash
pip3 install pytest
```

### 问题 3: 测试结果文件不存在

确保先运行 `run_full_test.sh` 生成测试结果。

### 问题 4: bc 命令未找到（macOS）

`analyze_errors.sh` 已使用 Python 替代 bc，无需额外安装。

---

## 📝 注意事项

1. **测试时间**: 完整测试流程约需 2-5 分钟
2. **资源占用**: 压力测试会占用 CPU 和内存
3. **日志文件**: 所有日志保存在 `test_reports/` 目录
4. **结果持久化**: JSON 结果文件可用于后续分析

---

## 🎉 使用示例

```bash
# 完整测试流程
$ bash run_full_test.sh
🚀 Luna Badge v1.3.0 一键测试开始
>> [1/5] 运行关键单元测试 (3 modules)...
...
🎉 测试全部结束：结果请查看 test_reports/

# 分析结果
$ bash analyze_errors.sh
🔍 Luna 测试结果分析
...
🎉🎉🎉 测试通过：错误率 = 0%
```

---

**最后更新**: 2025-12-01  
**版本**: v1.3.0







