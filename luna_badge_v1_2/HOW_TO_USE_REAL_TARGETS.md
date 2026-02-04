# 如何使用真实目标

## 📍 当前示例目标是假的

### 当前实现

在 `main.py` 中：

```python
# 初始化一个示例目标
demo_target = Target(
    id="t1", name="示例地点", lat=0.0, lng=0.0, extra={}
)
```

**问题**：
- ✅ `lat=0.0, lng=0.0` 是随便写的坐标（赤道和本初子午线交点）
- ✅ 导航逻辑只是简单的距离递减，没有真正使用 GPS
- ✅ 这是 **Dummy 实现**，用于演示系统功能

### 导航逻辑也是假的

在 `navigation/navigation_controller.py` 中：

```python
# 这里只做一个非常简单的"距离递减"
self._distance = max(0.0, self._distance - 0.5)
```

**说明**：
- 每步减少 0.5 米
- 不依赖真实的 GPS 定位
- 不依赖真实的地图数据
- 仅用于演示系统流程

## 🔧 如何替换为真实目标

### 方法 1：修改示例目标（简单）

在 `main.py` 中修改：

```python
# 替换为真实坐标（例如：北京天安门）
demo_target = Target(
    id="t1", 
    name="天安门广场", 
    lat=39.9042,    # 真实纬度
    lng=116.4074,   # 真实经度
    extra={"address": "北京市东城区"}
)
```

**注意**：即使改了坐标，导航逻辑仍然是假的（距离递减），需要替换导航实现。

### 方法 2：从配置文件读取（推荐）

创建 `config/targets.yaml`：

```yaml
targets:
  - id: "t1"
    name: "天安门广场"
    lat: 39.9042
    lng: 116.4074
    extra:
      address: "北京市东城区"
  - id: "t2"
    name: "故宫博物院"
    lat: 39.9163
    lng: 116.3972
    extra:
      address: "北京市东城区"
```

在 `main.py` 中读取：

```python
import yaml

with open('config/targets.yaml', 'r') as f:
    config = yaml.safe_load(f)
    
for target_data in config['targets']:
    target = Target(
        id=target_data['id'],
        name=target_data['name'],
        lat=target_data['lat'],
        lng=target_data['lng'],
        extra=target_data.get('extra', {})
    )
    self.multi_target_buffer.add_target(target)
```

### 方法 3：从命令行参数读取

```python
import sys

if len(sys.argv) > 1:
    # 从命令行读取目标
    # python main.py --target "天安门" 39.9042 116.4074
    target_name = sys.argv[1]
    lat = float(sys.argv[2])
    lng = float(sys.argv[3])
    
    demo_target = Target(
        id="t1", 
        name=target_name, 
        lat=lat, 
        lng=lng, 
        extra={}
    )
else:
    # 使用默认示例目标
    demo_target = Target(
        id="t1", name="示例地点", lat=0.0, lng=0.0, extra={}
    )
```

### 方法 4：从用户输入读取

```python
def get_target_from_user():
    print("请输入目标信息：")
    name = input("目标名称: ")
    lat = float(input("纬度: "))
    lng = float(input("经度: "))
    
    return Target(
        id="t1", 
        name=name, 
        lat=lat, 
        lng=lng, 
        extra={}
    )

demo_target = get_target_from_user()
```

## 🗺️ 如何实现真实导航

### 需要替换的部分

1. **NavigationController.step()** - 当前是假的距离递减

```python
# 当前实现（假）
def step(self, vision_objects):
    self._distance = max(0.0, self._distance - 0.5)  # 假的
    return NavState(at_target=self._distance <= 0.5, distance=self._distance)
```

**真实实现需要**：
- GPS 定位获取当前位置
- 计算到目标的真实距离
- 使用地图 API 规划路径
- 根据视觉结果调整路径

```python
# 真实实现示例
def step(self, vision_objects):
    # 1. 获取当前位置（GPS）
    current_pos = self.gps.get_current_position()  # (lat, lng)
    
    # 2. 计算到目标的真实距离
    distance = self.calculate_distance(
        current_pos, 
        (self._target.lat, self._target.lng)
    )
    
    # 3. 使用地图 API 规划路径
    route = self.map_api.get_route(current_pos, self._target)
    
    # 4. 根据视觉结果调整
    if vision_objects:
        # 检测障碍物，调整路径
        adjusted_route = self.adjust_route_for_obstacles(route, vision_objects)
    
    # 5. 判断是否到达
    at_target = distance < 5.0  # 5 米内认为到达
    
    return NavState(at_target=at_target, distance=distance)
```

### 需要的依赖

1. **GPS 模块**
   ```python
   class GPSModule:
       def get_current_position(self):
           # 使用 GPS 硬件获取位置
           return (lat, lng)
   ```

2. **地图 API**
   ```python
   class MapAPI:
       def get_route(self, start, end):
           # 使用高德/百度/Google Maps API
           return route
       
       def calculate_distance(self, pos1, pos2):
           # 计算两点间距离
           return distance_in_meters
   ```

3. **距离计算**
   ```python
   from math import radians, cos, sin, asin, sqrt
   
   def haversine_distance(lat1, lng1, lat2, lng2):
       """计算两点间距离（米）"""
       R = 6371000  # 地球半径（米）
       lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
       dlat = lat2 - lat1
       dlng = lng2 - lng1
       a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
       c = 2 * asin(sqrt(a))
       return R * c
   ```

## 📝 快速修改示例

### 修改 main.py 使用真实坐标

```python
# 在 main.py 的 start() 方法中，替换：

# 原来的假目标
# demo_target = Target(
#     id="t1", name="示例地点", lat=0.0, lng=0.0, extra={}
# )

# 改为真实坐标（例如：北京天安门）
demo_target = Target(
    id="t1", 
    name="天安门广场", 
    lat=39.9042,    # 真实纬度
    lng=116.4074,   # 真实经度
    extra={"address": "北京市东城区"}
)

# 或者添加多个真实目标
targets = [
    Target(id="t1", name="天安门", lat=39.9042, lng=116.4074, extra={}),
    Target(id="t2", name="故宫", lat=39.9163, lng=116.3972, extra={}),
    Target(id="t3", name="王府井", lat=39.9097, lng=116.4178, extra={}),
]

for target in targets:
    self.multi_target_buffer.add_target(target)
```

## ⚠️ 注意事项

1. **坐标格式**：
   - 纬度 (lat)：-90 到 90
   - 经度 (lng)：-180 到 180
   - 中国地区：lat 约 18-54，lng 约 73-135

2. **导航逻辑**：
   - 即使改了真实坐标，导航逻辑仍然是假的
   - 需要替换 `NavigationController.step()` 实现
   - 需要集成 GPS 和地图 API

3. **测试建议**：
   - 先用假目标测试系统流程
   - 确认所有模块正常工作
   - 再替换为真实导航实现

## 🎯 总结

- ✅ **当前示例目标是假的**：`lat=0.0, lng=0.0` 是随便写的
- ✅ **导航逻辑也是假的**：只是简单的距离递减
- ✅ **可以随便改坐标**：改成任何真实坐标都可以
- ⚠️ **但导航逻辑不会变**：除非替换 `NavigationController` 实现

**建议**：
1. 先用假目标测试系统功能
2. 确认所有模块正常后
3. 再替换为真实的 GPS + 地图导航实现















