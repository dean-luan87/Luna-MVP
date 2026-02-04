TEMPLATES_V0 = {
    # Traffic Light Task
    "traffic_light_unknown": "我还没完全看清红绿灯状态，我们先停一下确认。",
    "traffic_light_red_wait": "现在是红灯，我们在这里等一下。",
    "traffic_light_green_go": "绿灯亮了，可以通行。",
    # Floor Arrival Task
    "floor_state_unknown": "我还没确认电梯状态，先别急着动。",
    "floor_moving": "电梯正在运行，我们稍等一下。",
    "floor_arrived": "已经到达这一层。",
    # Elevator Button Task
    "elevator_missing_target": "你要去几楼？告诉我楼层，我再提醒你按哪个按钮。",
    "elevator_press_floor": "请按一下 {target_floor} 楼按钮。",
    # Exit Finder Task
    "exit_unknown": "我还没确认出口位置，我们慢一点找。",
    "exit_searching": "我在寻找出口标识，稍等我确认方向。",
    "exit_found": "我看到出口了。",
    # C Interlock (forced)
    "c_stop": "先停一下，前方可能不安全。",
    "c_hold": "我们先等一下，我需要确认环境是否安全。",
}

FROZEN_KEYS_V0 = set(TEMPLATES_V0.keys())
