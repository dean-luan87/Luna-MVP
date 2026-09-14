# C1 Active Mode v0.2 验证快速开始

## 运行环境

⚠️ **注意**: 验证脚本需要在实际运行环境中执行，不能在沙箱中运行（需要摄像头和网络权限）。

## 快速开始

### 1. 使用真实摄像头（推荐，10分钟验证）

```bash
cd /Users/luanlei/Desktop/Luna-2
python3 examples/c1_v02_real_input_validation.py --duration 10
```

**说明**：
- 使用系统默认摄像头
- 运行 10 分钟连续验证
- 需要摄像头权限

### 2. 使用模拟输入（快速测试，1分钟）

```bash
cd /Users/luanlei/Desktop/Luna-2
python3 examples/c1_v02_real_input_validation.py --duration 1 --no-camera
```

**说明**：
- 使用模拟输入数据
- 快速验证脚本功能
- 不反映真实表现

### 3. 使用视频文件

```bash
cd /Users/luanlei/Desktop/Luna-2
python3 examples/c1_v02_real_input_validation.py --duration 10 --video path/to/video.mp4
```

**说明**：
- 使用视频文件作为输入
- 可重复的验证场景
- 视频时长应 ≥ 验证时长

## 验证输出

### 控制台输出

验证过程中会显示：
- 验证进度（每 10 秒）
- 已处理帧数
- 状态切换次数
- Protection 触发次数

验证结束后会显示：
- 验证结果（通过/失败）
- 统计信息
- 详细分析

### 日志文件

验证日志保存在：
- `artifacts/c1_v02_validation_log.json`

包含内容：
- 验证时间
- 验证时长
- 总帧数
- 统计数据
- 验证结果
- 最后 100 条决策记录

## 验证标准

1. **日志频率验证**：最小日志间隔 ≥ 0.1 秒（无 spam）
2. **状态稳定性验证**：状态切换频率 ≤ 1 次/秒（无频繁抖动）
3. **SKIP 原因可解释性验证**：所有 SKIP 都有明确原因
4. **导航安全验证**：NavigationExecutor 执行率 ≥ 99%

## 验证结果

### 全部通过

```
✅ 所有验证通过 - C1 Active Mode v0.2 可以上线
```

### 部分失败

```
❌ 部分验证失败 - 需要修复问题
```

查看详细日志文件了解失败原因。

## 问题排查

### 摄像头初始化失败

- 检查系统权限设置（macOS：系统设置 → 隐私与安全性 → 摄像头）
- 关闭其他使用摄像头的程序
- 使用 `--no-camera` 进行模拟测试

### 脚本崩溃

- 检查依赖是否安装完整
- 查看错误日志
- 使用 `--duration 1` 进行快速测试

### 验证结果异常

- 检查输入数据质量
- 在稳定环境中重新验证
- 查看详细日志文件

## 下一步

验证通过后：
1. 查看详细日志文件
2. 分析异常情况（如有）
3. 优化参数配置（如需要）
4. 准备上线

验证失败后：
1. 查看失败原因
2. 修复问题
3. 重新验证

## 相关文档

- 完整验证指南：`docs/C1_V02_REAL_INPUT_VALIDATION_GUIDE.md`
- 测试报告：`docs/C1_ACTIVE_MODE_V02_TEST_REPORT.md`
- 验证脚本：`examples/c1_v02_real_input_validation.py`


