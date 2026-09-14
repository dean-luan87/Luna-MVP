# vision_pipeline/b2/v03/param_registry.py
from __future__ import annotations
from .param_schema import ParamSpec

# v0.4 参数全集（先覆盖你点名的关键场景 + 通用因子）
PARAMS: list[ParamSpec] = [
    # env
    ParamSpec("env.scene_type.indoor", "binary", "scene is indoor"),
    ParamSpec("env.scene_type.outdoor", "binary", "scene is outdoor"),
    ParamSpec("env.enclosure.enclosed", "binary", "enclosure type is enclosed"),
    ParamSpec("env.vertical_transport.is_elevator", "binary", "elevator detected"),
    ParamSpec("env.vertical_transport.state.entering", "binary", "entering elevator"),
    ParamSpec("env.vertical_transport.state.inside", "binary", "inside elevator"),
    ParamSpec("env.vertical_transport.state.exiting", "binary", "exiting elevator"),

    # people
    ParamSpec("people.count", "float", "people count (normalized)", 0.0, 1.0),
    ParamSpec("people.density.value", "float", "people density value", 0.0, 1.0),
    ParamSpec("people.density.delta", "float", "people density delta", -1.0, 1.0),
    ParamSpec("people.motion.bidirectional", "binary", "people motion bidirectional"),
    ParamSpec("people.motion.crossing", "binary", "people motion crossing"),
    ParamSpec("people.motion.chaotic", "binary", "people motion chaotic"),
    ParamSpec("people.crowd_scene.is_market", "binary", "market-like crowd scene"),
    ParamSpec("people.opposite_flow.detected", "binary", "opposite flow detected"),

    # path（预留，按你真实字段补）
    ParamSpec("path.surface.changed", "binary", "path surface changed"),

    # motion（可选）
    ParamSpec("motion.speed", "float", "speed normalized", 0.0, 1.0),
    ParamSpec("motion.motion_pattern.vertical_shift", "binary", "vertical motion pattern"),

    # event
    ParamSpec("event.near_miss", "binary", "near miss detected"),
    ParamSpec("event.collision_risk", "binary", "collision risk detected"),
    ParamSpec("event.severity", "float", "event severity", 0.0, 1.0),
]

