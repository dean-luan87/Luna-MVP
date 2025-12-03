from core.logging import get_logger

# map_renderer.py

log = get_logger("map_renderer")
"""
简易地图可视化（ASCII 卡片）
"""


def render_ascii_map(json_map):
    """
    渲染 ASCII 地图卡片
    """
    log.info("🗺 小地图结构\n")

    for n in json_map["nodes"]:
        if n["type"] == "Entrance":
            log.info(f"● 起点：{n['label']}")
        elif n["type"] == "Straight":
            log.info(f"→ 直行 {n['distance']}m")
        elif n["type"] == "TurnLeft":
            log.info("↰ 左转")
        elif n["type"] == "TurnRight":
            log.info("↱ 右转")
        elif n["type"] == "Elevator":
            log.info(f"⬆ 电梯（{n['distance']}m）")
        elif n["type"] == "Escalator":
            log.info(f"⬆ 扶梯（{n['distance']}m）")
        elif n["type"] == "Landmark":
            log.info(f"📍 {n['label']}")
        else:
            log.info(f"• {n['type']}")
        log.info("│")










