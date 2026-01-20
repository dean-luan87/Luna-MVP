# V1.8.1 Observer Mode 配置设置指南

**版本**: V1.8.1  
**创建日期**: 2025-12-29  
**用途**: 如何设置 OBSERVER_MODE_ENABLED

---

## 设置方法（三种方式）

### 方法 1: 环境变量（推荐，测试时使用）

**优点**: 快速切换，不影响配置文件

#### 设置方式

```bash
# 关闭 Observer Mode（测试 TC-06 / TC-07 时使用）
export OBSERVER_MODE_ENABLED=false

# 启用 Observer Mode（测试其他功能时使用）
export OBSERVER_MODE_ENABLED=true
```

#### 验证设置

```bash
# 检查环境变量
echo $OBSERVER_MODE_ENABLED

# 或在 Python 中检查
python3 -c "import os; print('OBSERVER_MODE_ENABLED:', os.environ.get('OBSERVER_MODE_ENABLED', 'not set'))"
```

---

### 方法 2: 修改配置文件（持久化）

#### 方式 A: 修改 config.py

编辑 `config.py` 文件：

```python
# V1.8.1: Observer Mode 配置
# 设置为 False 关闭 Observer Mode
OBSERVER_MODE_ENABLED = False  # 或 True
```

#### 方式 B: 修改 config/system_config.yaml

编辑 `config/system_config.yaml` 文件：

```yaml
# V1.8.1: Observer Mode 配置
observer_mode_enabled: false  # 或 true
```

---

### 方法 3: 创建测试配置文件（推荐，测试时使用）

#### 创建配置文件

```bash
# 创建关闭 Observer Mode 的配置文件
cp config/system_config.yaml config/system_config_observer_off.yaml

# 编辑文件，设置 observer_mode_enabled: false
```

#### 使用配置文件

```bash
# 使用关闭 Observer Mode 的配置运行
python3 main.py --config config/system_config_observer_off.yaml
```

---

## 测试场景配置

### TC-06 / TC-07 测试（回滚等价性）

**必须设置**: `OBSERVER_MODE_ENABLED=false`

```bash
# 方法 1: 环境变量（推荐）
export OBSERVER_MODE_ENABLED=false
python3 main.py

# 方法 2: 修改配置文件
# 编辑 config/system_config.yaml，设置 observer_mode_enabled: false
```

---

### 其他测试（Observer Mode 功能测试）

**设置**: `OBSERVER_MODE_ENABLED=true`

```bash
# 方法 1: 环境变量
export OBSERVER_MODE_ENABLED=true
python3 main.py

# 方法 2: 修改配置文件
# 编辑 config/system_config.yaml，设置 observer_mode_enabled: true
```

---

## 配置优先级

配置读取优先级（从高到低）：

1. **环境变量** `OBSERVER_MODE_ENABLED`（最高优先级）
2. **配置文件** `config/system_config.yaml` 中的 `observer_mode_enabled`
3. **默认值** `False`（如果都未设置）

---

## 验证配置是否生效

### 方法 1: 使用辅助脚本

```bash
python3 scripts/manual_test_tc06_tc07.py
```

### 方法 2: 在代码中检查

```python
import os
from config import OBSERVER_MODE_ENABLED

print(f"OBSERVER_MODE_ENABLED: {OBSERVER_MODE_ENABLED}")
```

### 方法 3: 检查日志

如果 Observer Mode 已关闭，日志中不应出现 `observer_*` 字段。

---

## 快速设置命令

### 关闭 Observer Mode（测试 TC-06 / TC-07）

```bash
# 设置环境变量
export OBSERVER_MODE_ENABLED=false

# 验证
echo $OBSERVER_MODE_ENABLED
```

### 启用 Observer Mode（测试其他功能）

```bash
# 设置环境变量
export OBSERVER_MODE_ENABLED=true

# 验证
echo $OBSERVER_MODE_ENABLED
```

---

## 配置文件示例

### config/system_config.yaml（关闭 Observer Mode）

```yaml
device_id: luna_badge_dev_001
platform: mac
startup_mode: active
log_level: info
language: zh-CN
wake_word_engine: porcupine
audio_input_device: default
camera_device: 0
auto_update: false
# V1.8.1: Observer Mode 配置
observer_mode_enabled: false  # 关闭 Observer Mode
```

### config/system_config.yaml（启用 Observer Mode）

```yaml
device_id: luna_badge_dev_001
platform: mac
startup_mode: active
log_level: info
language: zh-CN
wake_word_engine: porcupine
audio_input_device: default
camera_device: 0
auto_update: false
# V1.8.1: Observer Mode 配置
observer_mode_enabled: true  # 启用 Observer Mode
```

---

## 注意事项

### 测试 TC-06 / TC-07 时

- ✅ **必须设置** `OBSERVER_MODE_ENABLED=false`
- ✅ **验证设置生效**后再开始测试
- ✅ **记录配置状态**到测试记录中

### 测试其他功能时

- ✅ 可以设置 `OBSERVER_MODE_ENABLED=true`
- ✅ 测试 Observer Mode 的正常功能

---

## 故障排查

### 问题：设置后不生效

**检查步骤**:
1. 确认环境变量是否正确设置
2. 确认配置文件是否正确修改
3. 检查配置读取优先级
4. 使用辅助脚本验证

### 问题：不知道当前配置状态

**解决方法**:
```bash
# 使用辅助脚本检查
python3 scripts/manual_test_tc06_tc07.py
```

---

**最后更新**: 2025-12-29  
**维护者**: V1.8.1 开发团队


