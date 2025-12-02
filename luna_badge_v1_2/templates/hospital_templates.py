# hospital_templates.py

"""
医院任务模板库（可执行版本）

包含6个核心流程模板：
1. hospital_entry_flow - 进入医院后的总引导
2. hospital_registration_flow - 挂号流程
3. hospital_goto_department_flow - 去某个科室
4. hospital_payment_flow - 缴费流程
5. hospital_lab_test_flow - 检验/检查流程
6. hospital_pharmacy_flow - 取药流程
"""

HOSPITAL_TEMPLATES = {
    "scene": "HospitalHall",
    "templates": {
        "hospital_entry_flow": {
            "trigger": ["HospitalEntrance", "HospitalHall"],
            "steps": [
                "check_opening_hours",
                "detect_main_hall",
                "ask_user_purpose",
                "choose_first_flow"
            ]
        },
        "hospital_registration_flow": {
            "trigger": ["Registration", "InquiryDesk"],
            "steps": [
                "confirm_required_docs",
                "locate_registration_zone",
                "choose_registration_path",
                "navigate_to_target_counter",
                "queue_and_wait_call",
                "assist_registration_dialog",
                "write_back_visit_record"
            ]
        },
        "hospital_goto_department_flow": {
            "trigger": ["DepartmentSign", "DoctorRoomSign"],
            "steps": [
                "read_department_info",
                "find_floor_path",
                "navigate_to_elevator_or_stairs",
                "switch_floor",
                "navigate_to_department_area",
                "locate_department_room",
                "enter_waiting_area"
            ]
        },
        "hospital_payment_flow": {
            "trigger": ["Payment", "Cashier"],
            "steps": [
                "locate_payment_zone",
                "choose_payment_path",
                "navigate_to_payment_point",
                "queue_and_wait_call",
                "assist_payment_steps",
                "update_bill_memory"
            ]
        },
        "hospital_lab_test_flow": {
            "trigger": ["Lab", "BloodTest", "Imaging"],
            "steps": [
                "locate_lab_zone",
                "navigate_to_lab_counter",
                "queue_and_wait_call",
                "enter_room_when_called",
                "record_test_order"
            ]
        },
        "hospital_pharmacy_flow": {
            "trigger": ["Pharmacy"],
            "steps": [
                "locate_pharmacy",
                "queue_and_wait_call",
                "assist_pickup_steps",
                "record_medication_info"
            ]
        }
    }
}

