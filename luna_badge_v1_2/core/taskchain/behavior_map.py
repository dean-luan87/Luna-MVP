# behavior_map.py

"""
行为映射表：节点标签 → 任务链映射
"""

BEHAVIOR_MAP = {
    "Toilet": {
        "task_chain": "privacy_protect",
        "mode": "insert",   # 插入任务链
        "priority": 90
    },
    "Elevator": {
        "task_chain": "elevator_flow",
        "mode": "continue",
        "priority": 40
    },
    "Stair": {
        "task_chain": "stair_safe_flow",
        "mode": "insert",
        "priority": 80
    },
    "Registration": {
        "task_chain": "hospital_registration",
        "mode": "switch",   # 完整替换主任务链
        "priority": 100
    },
    "Payment": {
        "task_chain": "hospital_payment_flow",
        "mode": "switch",
        "priority": 100
    },
    "InquiryDesk": {
        "task_chain": "consult_flow",
        "mode": "insert",
        "priority": 50
    },
    "SubwayEntrance": {
        "task_chain": "subway_enter_flow",
        "mode": "continue",
        "priority": 30
    },
    "BusStop": {
        "task_chain": "bus_waiting_flow",
        "mode": "continue",
        "priority": 30
    },
    "Danger": {
        "task_chain": "danger_stop",
        "mode": "force",
        "priority": 999
    }
}










