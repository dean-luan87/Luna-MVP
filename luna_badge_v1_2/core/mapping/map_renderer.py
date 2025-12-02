# map_renderer.py

"""
简易地图可视化（ASCII 卡片）
"""


def render_ascii_map(json_map):
    """
    渲染 ASCII 地图卡片
    """
    print("🗺 小地图结构\n")

    for n in json_map["nodes"]:
        if n["type"] == "Entrance":
            print(f"● 起点：{n['label']}")
        elif n["type"] == "Straight":
            print(f"→ 直行 {n['distance']}m")
        elif n["type"] == "TurnLeft":
            print("↰ 左转")
        elif n["type"] == "TurnRight":
            print("↱ 右转")
        elif n["type"] == "Elevator":
            print(f"⬆ 电梯（{n['distance']}m）")
        elif n["type"] == "Escalator":
            print(f"⬆ 扶梯（{n['distance']}m）")
        elif n["type"] == "Landmark":
            print(f"📍 {n['label']}")
        else:
            print(f"• {n['type']}")
        print("│")










