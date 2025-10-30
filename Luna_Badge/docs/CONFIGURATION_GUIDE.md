# Luna Badge 配置指南

## 📋 概述

本文档介绍 Luna Badge 系统中所有配置文件的用途、格式、默认值及修改建议。

## 📁 配置文件结构

```
Luna_Badge/
└── config/
    ├── system_config.yaml        # 系统核心配置
    ├── tts_config.yaml           # 语音播报配置
    ├── modules_enabled.yaml      # 模块启用配置
    └── safety_policy.yaml        # 安全策略配置
```

## 🔧 配置文件详解

### 1. system_config.yaml

**用途**: 系统核心配置，控制设备行为、启动模式、日志级别等。

**完整配置项**:

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `device_id` | string | `luna_badge_dev_001` | 设备唯一标识符 |
| `startup_mode` | string | `active` | 启动模式（active/idle/sleep） |
| `log_level` | string | `info` | 日志级别（debug/info/warning/error） |
| `language` | string | `zh-CN` | 系统语言 |
| `wake_word_engine` | string | `porcupine` | 唤醒词识别引擎 |
| `audio_input_device` | string | `default` | 音频输入设备 |
| `camera_device` | int | `0` | 摄像头设备号 |
| `auto_update` | bool | `false` | 是否自动更新 |

**示例配置**:

```yaml
device_id: luna_badge_dev_001
startup_mode: active
log_level: info
language: zh-CN
wake_word_engine: porcupine
audio_input_device: default
camera_device: 0
auto_update: false
```

**修改建议**:
- 首次使用时建议修改 `device_id` 以区分不同设备
- 如不需要唤醒功能，可将 `wake_word_engine` 设为空字符串
- 如遇到摄像头无法识别，可尝试调整 `camera_device` 值

---

### 2. tts_config.yaml

**用途**: 语音播报（TTS）配置，控制语音风格、速度、音调等。

**完整配置项**:

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `default_voice` | string | `zh-CN-XiaoxiaoNeural` | 默认语音模型 |
| `default_style` | string | `default` | 默认播报风格 |
| `speech_speed` | float | `1.0` | 语音速度（0.5-2.0） |
| `speech_pitch` | float | `1.0` | 语音音调（0.5-2.0） |
| `style_mapping.normal` | string | `cheerful` | 正常状态播报风格 |
| `style_mapping.caution` | string | `calm` | 警告状态播报风格 |
| `style_mapping.reroute` | string | `empathetic` | 重新规划状态播报风格 |
| `style_mapping.stop` | string | `serious` | 停止状态播报风格 |

**示例配置**:

```yaml
default_voice: zh-CN-XiaoxiaoNeural
default_style: default
speech_speed: 1.0
speech_pitch: 1.0

style_mapping:
  normal: cheerful
  caution: calm
  reroute: empathetic
  stop: serious
```

**修改建议**:
- `speech_speed` 推荐范围：0.8-1.2（过快影响理解，过慢影响体验）
- 如需更换语音，可选择 Edge-TTS 支持的其他语音模型
- 不同场景的播报风格可通过 `style_mapping` 自定义

---

### 3. modules_enabled.yaml

**用途**: 控制各功能模块的启用/禁用状态。

**完整配置项**:

| 模块类别 | 配置项 | 默认值 | 说明 |
|----------|--------|--------|------|
| `vision` | `signboard_detector` | `true` | 标识牌检测 |
| `vision` | `hazard_detector` | `true` | 危险区域检测 |
| `vision` | `crowd_detector` | `true` | 人群密度检测 |
| `navigation` | `path_evaluator` | `true` | 路径评估 |
| `navigation` | `doorplate_inference` | `true` | 门牌推理 |
| `memory` | `memory_store` | `true` | 记忆存储 |
| `memory` | `memory_caller` | `true` | 记忆调用 |
| `communication` | `tts` | `true` | 语音合成 |
| `communication` | `whisper` | `true` | 语音识别 |
| `communication` | `wakeup` | `true` | 唤醒功能 |
| `other` | `debug_mode` | `false` | 调试模式 |

**示例配置**:

```yaml
vision:
  signboard_detector: true
  hazard_detector: true
  crowd_detector: true

navigation:
  path_evaluator: true
  doorplate_inference: true

memory:
  memory_store: true
  memory_caller: true

communication:
  tts: true
  whisper: true
  wakeup: true

other:
  debug_mode: false
```

**修改建议**:
- 如设备性能不足，可关闭部分非核心模块
- 关闭 `debug_mode` 可减少日志输出，提升性能
- 可根据实际使用场景开启/关闭特定功能模块

---

### 4. safety_policy.yaml

**用途**: 安全策略配置，包括隐私区域、摄像头锁定、故障处理等。

**完整配置项**:

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `privacy_zones.toilet.camera_lock` | bool | `true` | 卫生间区域是否锁定摄像头 |
| `privacy_zones.toilet.gps_radius` | int | `5` | GPS半径（米） |
| `privacy_zones.toilet.lock_duration` | int | `300` | 锁定持续时间（秒） |
| `privacy_zones.toilet.manual_unlock_allowed` | bool | `false` | 是否允许手动解锁 |
| `privacy_zones.hospital.camera_lock` | bool | `false` | 医院区域是否锁定摄像头 |
| `failover_behavior.gps_unavailable` | string | `allow_with_warning` | GPS不可用时的处理方式 |
| `failover_behavior.config_file_missing` | string | `auto_generate_defaults` | 配置文件缺失时的处理方式 |

**示例配置**:

```yaml
privacy_zones:
  toilet:
    camera_lock: true
    gps_radius: 5
    lock_duration: 300
    manual_unlock_allowed: false
  hospital:
    camera_lock: false

failover_behavior:
  gps_unavailable: allow_with_warning
  config_file_missing: auto_generate_defaults
```

**修改建议**:
- 根据实际隐私需求调整隐私区域设置
- `lock_duration` 建议设置为 300-600 秒（5-10分钟）
- 如不需要GPS功能，可调整 `gps_unavailable` 处理方式

---

## 🔍 配置校验

系统启动时会自动调用 `core/config_validator.py` 进行配置校验：

```python
from core.config_validator import validate_configs

# 校验配置文件
status = validate_configs(force_overwrite=False)

# 返回状态：
# "created": 新创建的配置文件
# "loaded": 成功加载已有配置文件
# "overwritten": 强制覆盖的配置文件
```

## 📖 配置使用示例

### 1. 加载配置

```python
from core.config_validator import load_config

# 加载系统配置
system_config = load_config("system_config.yaml")
print(system_config["startup_mode"])

# 加载TTS配置
tts_config = load_config("tts_config.yaml")
print(tts_config["default_voice"])
```

### 2. 获取配置值

```python
from core.config_validator import get_config_value

# 获取嵌套配置值
crowd_detector_enabled = get_config_value(
    "modules_enabled.yaml", 
    "vision.crowd_detector",
    default=False
)

# 获取系统配置值
startup_mode = get_config_value(
    "system_config.yaml",
    "startup_mode",
    default="active"
)
```

### 3. 更新配置

```python
from core.config_validator import update_config

# 更新单个配置项
update_config("system_config.yaml", {
    "auto_update": True
})

# 更新多个配置项
update_config("tts_config.yaml", {
    "speech_speed": 1.2,
    "speech_pitch": 1.1
})
```

## 🛠️ 调试建议

### 问题排查

1. **配置文件不存在**
   - 系统会自动创建默认配置文件
   - 可通过日志查看创建状态

2. **配置项无效**
   - 检查 YAML 格式是否正确
   - 查看日志中的配置加载错误信息

3. **配置不生效**
   - 确认重启系统以加载新配置
   - 检查配置项名称是否拼写正确

### 日志输出

```bash
# 查看配置校验日志
python3 core/config_validator.py

# 查看系统启动日志
python3 main_mac.py 2>&1 | grep -i config
```

## 📝 最佳实践

1. **首次使用**: 使用默认配置进行测试，确认系统正常运行
2. **个性化配置**: 根据实际使用场景调整配置项
3. **定期备份**: 定期备份配置文件以便快速恢复
4. **版本控制**: 建议将配置文件纳入版本控制系统

## 🔐 安全注意事项

1. **隐私配置**: 谨慎设置隐私区域锁定策略
2. **设备标识**: 在生产环境中修改默认设备ID
3. **更新策略**: 建议关闭自动更新功能，手动控制更新时机
4. **日志级别**: 生产环境建议使用 `info` 或 `warning` 级别

## 📚 参考文档

- [system_control.py](../core/system_control.py) - 系统控制模块
- [speech_style_manager.py](../core/speech_style_manager.py) - 播报风格管理
- [privacy_protection.py](../core/privacy_protection.py) - 隐私保护模块

---

**最后更新**: 2025-10-28  
**版本**: v1.0
