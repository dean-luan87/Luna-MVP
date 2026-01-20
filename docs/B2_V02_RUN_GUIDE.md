# B2 v0.2 缓存逻辑运行指南

## 快速验证

由于模块依赖关系，建议在实际运行环境中测试。以下是验证步骤：

### 1. 代码语法检查 ✅

所有核心文件已通过语法检查：
- ✅ `world_signature.py`
- ✅ `future_scene_cache.py`
- ✅ `advisory_cache.py`
- ✅ `b2_cache_observer.py`

### 2. 运行方式

#### 方式 A：在完整 pipeline 中运行

```bash
# 运行 pipeline（确保 B2 v0.2 已启用）
python your_pipeline.py > b2_log.txt 2>&1

# 使用观测工具分析
python -m vision_pipeline.b2.b2_cache_observer b2_log.txt
```

#### 方式 B：单独测试 B2 模块（需要修复导入）

如果要在隔离环境中测试，需要：
1. 修改相对导入为绝对导入
2. 或使用 `PYTHONPATH` 设置

```bash
export PYTHONPATH=/path/to/Luna-2:$PYTHONPATH
python examples/b2_v02_cache_test.py
```

### 3. 观察日志

运行后，查找以下日志关键词：

```
[B2] world_signature=12345678
[B2] future_cache=reused age=4.2s
[B2] future_cache=expired recompute
[B2] advisory suppressed (same as last, age=9.3s)
[B2-v0.2][timestamp] PREWARN|DEESCALATE|WORLD_NOTE | ...
```

### 4. 使用观测工具

观测工具会自动分析日志并生成报告：

```bash
python -m vision_pipeline.b2.b2_cache_observer b2_log.txt
```

报告包含：
- WorldSignature 变化频率
- FutureCache 命中率
- AdvisoryCache 抑制次数
- 综合判断（4 个 YES/NO）

### 5. 预期结果

如果缓存逻辑正常工作，应该看到：

1. ✅ **WorldSignature 稳定**：在相同场景下，signature 持续 ≥ 10s
2. ✅ **FutureCache 复用**：reuse 比例 ≥ 30%（复杂场景）或 ≥ 60%（简单场景）
3. ✅ **AdvisoryCache 抑制**：suppressed 比例 ≥ 30%
4. ✅ **B2 输出间隔**：avg ≥ 8s，min ≥ 1.5s

### 6. 如果遇到问题

**问题：导入错误**
- 确保在正确的 Python 环境中运行
- 检查 `PYTHONPATH` 设置
- 确保所有依赖已安装

**问题：日志格式不匹配**
- 检查 `b2_cache_observer.py` 中的正则表达式
- 根据实际日志格式调整

**问题：缓存不生效**
- 检查 WorldSignature 是否正确生成
- 检查 TTL 设置是否合理
- 查看详细日志输出

---

## 总结

B2 v0.2 缓存逻辑的核心代码已完成并通过语法检查。在实际运行环境中，应该能够：

1. ✅ 正确生成 WorldSignature
2. ✅ 复用 FutureCache（世界没变时）
3. ✅ 抑制重复 Advisory（相同建议时）
4. ✅ 显著降低 B2 输出频率

所有功能已实现，等待在实际 pipeline 中验证。

