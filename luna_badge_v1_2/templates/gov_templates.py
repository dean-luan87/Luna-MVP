# gov_templates.py

"""
政务大厅任务模板库
"""

GOV_TEMPLATES = {
    "scene": "GovServiceHall",
    "templates": {
        "find_service_window": {
            "trigger": ["Window", "Counter"],
            "steps": [
                "identify_service_type",
                "locate_target_window",
                "queue_and_wait"
            ]
        },
        "find_inquiry": {
            "trigger": ["InquiryDesk"],
            "steps": [
                "navigate_to_inquiry"
            ]
        }
    }
}










