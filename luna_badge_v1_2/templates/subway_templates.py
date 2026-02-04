# subway_templates.py

"""
地铁站任务模板库
"""

SUBWAY_TEMPLATES = {
    "scene": "SubwayStation",
    "templates": {
        "go_to_line": {
            "trigger": ["LineSign"],
            "steps": [
                "identify_direction",
                "follow_signs"
            ]
        },
        "enter_gate": {
            "trigger": ["Gate"],
            "steps": [
                "guide_to_gate"
            ]
        },
        "find_platform": {
            "trigger": ["PlatformSign"],
            "steps": [
                "navigate_to_platform"
            ]
        },
        "transfer": {
            "trigger": ["TransferSign"],
            "steps": [
                "identify_transfer_line",
                "navigate_to_transfer"
            ]
        }
    }
}

























