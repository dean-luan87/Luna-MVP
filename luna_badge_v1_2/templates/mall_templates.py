# mall_templates.py

"""
商场任务模板库
"""

MALL_TEMPLATES = {
    "scene": "MallIndoor",
    "templates": {
        "find_store": {
            "trigger": ["StoreSign"],
            "steps": [
                "find_floor",
                "navigate_to_location"
            ]
        },
        "find_toilet": {
            "trigger": ["Toilet"],
            "steps": [
                "navigate_to_toilet"
            ]
        },
        "find_exit": {
            "trigger": ["Exit"],
            "steps": [
                "navigate_to_exit"
            ]
        },
        "find_elevator": {
            "trigger": ["Elevator"],
            "steps": [
                "navigate_to_elevator",
                "select_floor"
            ]
        }
    }
}














