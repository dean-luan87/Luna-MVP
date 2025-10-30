# Luna 地图分享与设备同步指南

## 📋 目录

1. [概述](#概述)
2. [快速分享方案](#快速分享方案)
3. [数据结构标准](#数据结构标准)
4. [设备快速解析](#设备快速解析)
5. [部署示例](#部署示例)

---

## 概述

Luna 地图卡片包含可视化图像和元数据JSON，可在设备间同步与解析。

### 地图文件组成

```
地图卡片包/
├── map_card.png              # 可视化地图图像
├── map_card.meta.json        # 元数据（路径、节点、区域信息）
└── path_data.json            # 原始路径数据（可选）
```

---

## 快速分享方案

### 方案 A：图像+元数据（推荐）

**适用场景**：快速分享、轻量传输

**文件结构**：
```json
{
  "version": "1.0",
  "format": "luna_map_card",
  "map_image": "hospital_main_enhanced_emotional.png",
  "metadata": {
    "path_id": "hospital_main_enhanced",
    "path_name": "医院完整导航路径",
    "map_direction_reference": "上 = 北",
    "compass_added": true,
    "icons_used": true,
    "icon_types": ["elevator", "entrance", "destination"],
    "regions_detected": ["三楼病区", "挂号大厅"],
    "node_count": 6,
    "total_distance": "100米",
    "generation_timestamp": "2025-10-30T16:29:28"
  }
}
```

### 方案 B：完整路径数据

**适用场景**：设备端重新渲染、离线编辑

**数据结构**：
```json
{
  "version": "1.0",
  "format": "luna_path_data",
  "paths": [
    {
      "path_id": "hospital_main_enhanced",
      "path_name": "医院完整导航路径",
      "nodes": [
        {
          "node_id": "node1",
          "label": "医院入口",
          "type": "entrance",
          "level": "挂号大厅",
          "emotion": ["嘈杂"],
          "distance": 0
        },
        {
          "node_id": "node2",
          "label": "挂号处",
          "type": "building",
          "level": "挂号大厅",
          "emotion": ["推荐", "明亮"],
          "distance": 15,
          "movement": "walking"
        }
      ]
    }
  ]
}
```

---

## 数据结构标准

### 元数据字段说明

| 字段 | 类型 | 说明 | 必填 |
|------|------|------|------|
| `version` | string | 版本号 | ✅ |
| `format` | string | 格式标识 | ✅ |
| `path_id` | string | 路径唯一ID | ✅ |
| `path_name` | string | 路径名称 | ✅ |
| `map_direction_reference` | string | 方向参考 | ⚠️ |
| `compass_added` | boolean | 是否包含指南针 | ⚠️ |
| `icons_used` | boolean | 是否使用图标 | ⚠️ |
| `icon_types` | array | 使用的图标类型 | ⚠️ |
| `regions_detected` | array | 检测到的区域 | ⚠️ |
| `node_count` | int | 节点数量 | ⚠️ |
| `total_distance` | string | 总距离 | ⚠️ |
| `generation_timestamp` | string | 生成时间戳 | ⚠️ |

### 节点数据字段说明

| 字段 | 类型 | 说明 | 必填 |
|------|------|------|------|
| `node_id` | string | 节点唯一ID | ✅ |
| `label` | string | 节点标签 | ✅ |
| `type` | string | 节点类型 | ✅ |
| `level` | string | 层级/区域 | ⚠️ |
| `emotion` | array | 情绪标签 | ⚠️ |
| `distance` | int | 到下一个节点的距离 | ⚠️ |
| `movement` | string | 移动方式 | ⚠️ |

### 节点类型标准

| 类型 | 说明 | 图标 |
|------|------|------|
| `entrance` | 入口 | 🚪 |
| `elevator` | 电梯 | 🛗 |
| `destination` | 目的地 | 🎯 |
| `building` | 建筑 | 🏠 |
| `toilet` | 卫生间 | 🚽 |
| `registration` | 挂号处 | ℹ️ |
| `bus` | 公交站 | 🚌 |

### 移动方式标准

| 方式 | 说明 | 线型 |
|------|------|------|
| `walking` | 步行 | 实线灰色 |
| `elevator` | 电梯 | 虚线蓝色 |
| `stairs` | 楼梯 | 点线棕色 |

---

## 设备快速解析

### Python 解析示例

```python
import json
from PIL import Image
from pathlib import Path

class LunaMapLoader:
    """Luna 地图卡片加载器"""
    
    def __init__(self, map_dir: str):
        self.map_dir = Path(map_dir)
    
    def load_map_card(self, map_id: str):
        """加载地图卡片（图像+元数据）"""
        # 加载图像
        image_path = self.map_dir / f"{map_id}_emotional.png"
        image = Image.open(image_path) if image_path.exists() else None
        
        # 加载元数据
        meta_path = self.map_dir / f"{map_id}_emotional.meta.json"
        metadata = json.loads(meta_path.read_text()) if meta_path.exists() else None
        
        return {
            "image": image,
            "metadata": metadata
        }
    
    def load_path_data(self, path_id: str):
        """加载原始路径数据"""
        # 查找包含该路径的数据文件
        for json_file in self.map_dir.glob("*.json"):
            if json_file.stem.endswith("_meta"):
                continue
            
            try:
                data = json.loads(json_file.read_text())
                # 检查是否包含路径
                if "paths" in data:
                    for path in data["paths"]:
                        if path.get("path_id") == path_id:
                            return path
            except:
                continue
        
        return None
    
    def parse_map_for_voice(self, metadata: dict) -> str:
        """解析元数据生成语音提示"""
        if not metadata:
            return "无法解析地图信息"
        
        path_name = metadata.get("path_name", "未知路径")
        node_count = metadata.get("node_count", 0)
        total_distance = metadata.get("total_distance", "未知距离")
        regions = metadata.get("regions_detected", [])
        
        voice_text = f"导航路径：{path_name}，共{node_count}个节点，"
        voice_text += f"总距离{total_distance}，"
        
        if regions:
            voice_text += f"途经区域：{', '.join(regions)}"
        
        return voice_text
    
    def extract_navigation_sequence(self, path_data: dict) -> list:
        """提取导航序列"""
        if not path_data or "nodes" not in path_data:
            return []
        
        sequence = []
        nodes = path_data["nodes"]
        
        for i, node in enumerate(nodes):
            label = node.get("label", f"节点{i+1}")
            distance = node.get("distance", 0)
            movement = node.get("movement", "walking")
            
            sequence.append({
                "step": i + 1,
                "action": self._get_movement_description(movement),
                "target": label,
                "distance": distance
            })
        
        return sequence
    
    def _get_movement_description(self, movement: str) -> str:
        """获取移动方式描述"""
        movement_map = {
            "walking": "步行前往",
            "elevator": "乘电梯前往",
            "stairs": "通过楼梯前往"
        }
        return movement_map.get(movement, "前往")


# 使用示例
if __name__ == "__main__":
    # 初始化加载器
    loader = LunaMapLoader("data/map_cards")
    
    # 加载地图卡片
    map_card = loader.load_map_card("hospital_main_enhanced")
    
    # 显示元数据
    print(json.dumps(map_card["metadata"], indent=2, ensure_ascii=False))
    
    # 生成语音提示
    voice_prompt = loader.parse_map_for_voice(map_card["metadata"])
    print(f"\n🗣️ 语音提示：{voice_prompt}")
    
    # 加载路径数据
    path_data = loader.load_path_data("hospital_main_enhanced")
    
    # 提取导航序列
    if path_data:
        sequence = loader.extract_navigation_sequence(path_data)
        print("\n🗺️ 导航序列：")
        for step in sequence:
            print(f"  步骤{step['step']}：{step['action']}{step['target']}（{step['distance']}米）")
```

### 轻量设备解析（JSON Only）

```python
# 最小化解析器（仅需JSON和基础数学库）
def parse_map_minimal(map_json_path: str):
    """最小化地图解析器"""
    import json
    
    with open(map_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 提取关键信息
    result = {
        "path_name": data.get("path_name", "未知"),
        "node_count": data.get("node_count", 0),
        "total_distance": data.get("total_distance", "0米"),
        "regions": data.get("regions_detected", [])
    }
    
    return result
```

---

## 部署示例

### 场景 1：蓝牙/局域网分享

```python
# 发送端
def send_map_card(device_address: str, map_id: str):
    """发送地图卡片到设备"""
    import bluetooth  # 或其他传输协议
    
    # 打包文件
    map_files = [
        f"{map_id}_emotional.png",
        f"{map_id}_emotional.meta.json"
    ]
    
    # 发送
    for file in map_files:
        send_file(device_address, f"data/map_cards/{file}")

# 接收端
def receive_map_card():
    """接收地图卡片"""
    received_files = receive_files()
    
    # 解析
    loader = LunaMapLoader("received_maps/")
    for file in received_files:
        if file.endswith(".meta.json"):
            metadata = json.loads(file.read_text())
            # 加载地图
            map_card = loader.load_map_card(metadata["path_id"])
```

### 场景 2：二维码分享

```python
from qrcode import QRCode
import base64

def generate_map_qr_code(map_data: dict) -> QRCode:
    """生成地图QR码"""
    # 压缩数据
    json_str = json.dumps(map_data, ensure_ascii=False)
    encoded = base64.b64encode(json_str.encode('utf-8'))
    
    # 生成二维码
    qr = QRCode()
    qr.add_data(encoded)
    qr.make(fit=True)
    
    return qr

def scan_and_load_map(qr_image):
    """扫描并加载地图"""
    # 扫描二维码
    data = scan_qr_code(qr_image)
    
    # 解码
    decoded = base64.b64decode(data)
    map_data = json.loads(decoded.decode('utf-8'))
    
    return map_data
```

### 场景 3：云端同步

```python
def sync_map_to_cloud(map_id: str, cloud_storage):
    """同步地图到云端"""
    map_files = {
        "image": f"{map_id}_emotional.png",
        "metadata": f"{map_id}_emotional.meta.json"
    }
    
    # 上传
    for file_type, filename in map_files.items():
        cloud_storage.upload(f"maps/{map_id}/{filename}")

def sync_map_from_cloud(map_id: str, cloud_storage):
    """从云端同步地图"""
    # 下载
    files = cloud_storage.download(f"maps/{map_id}/")
    
    # 保存到本地
    for file in files:
        save_locally(file)
```

---

## 最佳实践

### 1. 版本兼容性

```python
def check_compatibility(metadata: dict) -> bool:
    """检查版本兼容性"""
    version = metadata.get("version", "0.9")
    
    # 支持的版本
    supported_versions = ["1.0", "1.1"]
    
    return version in supported_versions
```

### 2. 数据验证

```python
def validate_map_data(data: dict) -> bool:
    """验证地图数据完整性"""
    required_fields = ["path_id", "path_name", "node_count"]
    
    for field in required_fields:
        if field not in data:
            return False
    
    return True
```

### 3. 错误处理

```python
def safe_load_map(map_id: str):
    """安全加载地图"""
    try:
        loader = LunaMapLoader("data/map_cards")
        map_card = loader.load_map_card(map_id)
        
        # 验证
        if not validate_map_data(map_card["metadata"]):
            raise ValueError("地图数据不完整")
        
        return map_card
    except FileNotFoundError:
        logger.error(f"地图文件不存在：{map_id}")
        return None
    except json.JSONDecodeError:
        logger.error(f"地图元数据解析失败：{map_id}")
        return None
```

---

## 总结

- **图像+元数据**：适合快速展示与传输
- **完整路径数据**：支持设备端重渲染与编辑
- **跨设备标准**：统一的JSON，易于解析与集成
- **语音适配**：元数据可直接转为语音提示
- **云端同步**：支持远程分发与更新

通过这套方案，新设备可快速接入Luna地图系统。

