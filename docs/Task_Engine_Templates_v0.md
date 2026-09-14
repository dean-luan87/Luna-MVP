# Task Engine 模板 key 清单（v0 冻结）

原则：
- Task 只产出 template_key，不产出文案
- 文案层可独立迭代 / 本地模型加工
- v0 模板偏“稳妥、克制、不像传统导航播报”

---

## 1) Traffic Light Task

template_key | 触发场景
---|---
traffic_light_unknown | 红绿灯不可见 / 不确定
traffic_light_red_wait | 红灯
traffic_light_green_go | 绿灯

默认文案（v0）
- "traffic_light_unknown": "我还没完全看清红绿灯状态，我们先停一下确认。"
- "traffic_light_red_wait": "现在是红灯，我们在这里等一下。"
- "traffic_light_green_go": "绿灯亮了，可以通行。"

---

## 2) Floor Arrival Task

template_key | 触发场景
---|---
floor_state_unknown | 楼层状态未知
floor_moving | 电梯运行中
floor_arrived | 到达目标楼层

默认文案（v0）
- "floor_state_unknown": "我还没确认电梯状态，先别急着动。"
- "floor_moving": "电梯正在运行，我们稍等一下。"
- "floor_arrived": "已经到达这一层。"

---

## 3) Elevator Button Task

template_key | 触发场景
---|---
elevator_missing_target | 未提供目标楼层
elevator_press_floor | 指挥按楼层按钮

默认文案（v0）
- "elevator_missing_target": "你要去几楼？告诉我楼层，我再提醒你按哪个按钮。"
- "elevator_press_floor": "请按一下 {target_floor} 楼按钮。"

---

## 4) Exit Finder Task

template_key | 触发场景
---|---
exit_unknown | 出入口不确定
exit_searching | 正在寻找
exit_found | 已识别出口

默认文案（v0）
- "exit_unknown": "我还没确认出口位置，我们慢一点找。"
- "exit_searching": "我在寻找出口标识，稍等我确认方向。"
- "exit_found": "我看到出口了。"

---

## 5) C 互锁专用模板（必须保留）

这些不是 Task 模板，而是 Speech Dispatcher 在 C=STOP/HOLD 时强制使用。

- "c_stop": "先停一下，前方可能不安全。"
- "c_hold": "我们先等一下，我需要确认环境是否安全。"

---

## 模板冻结规则
- v0 不允许删除已有 key
- 只允许：
  - 改文案
  - 增加新 key
- Task 代码不得硬编码文案
