from core.logging import get_logger

# hospital_step_factory.py

log = get_logger("hospital_step_factory")
"""
医院步骤工厂：将模板 step_id 转换为可执行的 Step 节点
"""

from core.scenes.flow_builder import Step
from typing import Dict, Any, Optional


def build_hospital_step(step_name: str, context: Optional[Dict[str, Any]] = None) -> Step:
    """
    根据医院模板的 step_name 创建对应的 Step 节点
    
    参数：
    - step_name: 模板中的步骤ID（如 'locate_registration_zone'）
    - context: 上下文信息（OCR、YOLO、地图、用户状态等）
    
    返回：
    - Step 对象
    """
    if context is None:
        context = {}
    
    # 医院入口流程步骤
    if step_name == "check_opening_hours":
        return Step(
            "正在确认医院接诊时间…",
            action=lambda: print("[Action] Check opening hours"),
            step_type="check"
        )
    
    if step_name == "detect_main_hall":
        return Step(
            "正在确认您已进入门诊大厅…",
            action=lambda: print("[Action] Detect main hall"),
            step_type="detect"
        )
    
    if step_name == "ask_user_purpose":
        return Step(
            "请告诉我您来医院的目的（挂号/复诊/取药等）",
            action=lambda: print("[Action] Ask user purpose"),
            step_type="interaction"
        )
    
    if step_name == "choose_first_flow":
        return Step(
            "正在根据您的目的选择流程…",
            action=lambda: print("[Action] Choose first flow"),
            step_type="decision"
        )
    
    # 挂号流程步骤
    if step_name == "confirm_required_docs":
        return Step(
            "请确认您已携带医保卡和相关证件，如果没有，也可以尝试先去咨询台询问。",
            action=lambda: print("[Action] Confirm required docs"),
            step_type="reminder"
        )
    
    if step_name == "locate_registration_zone":
        return Step(
            "正在为您查找挂号区域…",
            action=lambda: _locate_zone("Registration", context),
            step_type="locate"
        )
    
    if step_name == "choose_registration_path":
        return Step(
            "正在为您选择挂号方式（咨询台/人工窗口/自助机）…",
            action=lambda: _choose_registration_path(context),
            step_type="decision"
        )
    
    if step_name == "navigate_to_target_counter":
        return Step(
            "正在引导您前往挂号窗口…",
            action=lambda: print("[Action] Navigate to counter"),
            step_type="navigate"
        )
    
    if step_name == "queue_and_wait_call":
        return Step(
            "正在排队等待叫号…",
            action=lambda: print("[Action] Queue and wait"),
            step_type="wait"
        )
    
    if step_name == "assist_registration_dialog":
        return Step(
            "正在协助您与窗口工作人员沟通…",
            action=lambda: print("[Action] Assist registration dialog"),
            step_type="assist"
        )
    
    if step_name == "write_back_visit_record":
        return Step(
            "正在记录您的就诊信息…",
            action=lambda: print("[Action] Write visit record"),
            step_type="memory"
        )
    
    # 去科室流程步骤
    if step_name == "read_department_info":
        return Step(
            "正在读取科室信息（科室、楼层、房间号）…",
            action=lambda: print("[Action] Read department info"),
            step_type="read"
        )
    
    if step_name == "find_floor_path":
        return Step(
            "正在确定需要前往的楼层…",
            action=lambda: print("[Action] Find floor path"),
            step_type="plan"
        )
    
    if step_name == "navigate_to_elevator_or_stairs":
        return Step(
            "正在导航到电梯或楼梯…",
            action=lambda: print("[Action] Navigate to elevator or stairs"),
            step_type="navigate"
        )
    
    if step_name == "switch_floor":
        return Step(
            "正在上下楼…",
            action=lambda: print("[Action] Switch floor"),
            step_type="action"
        )
    
    if step_name == "navigate_to_department_area":
        return Step(
            "正在导航到科室区域…",
            action=lambda: print("[Action] Navigate to department area"),
            step_type="navigate"
        )
    
    if step_name == "locate_department_room":
        return Step(
            "正在定位具体诊室…",
            action=lambda: print("[Action] Locate department room"),
            step_type="locate"
        )
    
    if step_name == "enter_waiting_area":
        return Step(
            "正在进入候诊区…",
            action=lambda: print("[Action] Enter waiting area"),
            step_type="action"
        )
    
    # 缴费流程步骤
    if step_name == "locate_payment_zone":
        return Step(
            "正在查找缴费区域…",
            action=lambda: _locate_zone("Payment", context),
            step_type="locate"
        )
    
    if step_name == "choose_payment_path":
        return Step(
            "正在选择缴费方式（人工窗口/自助机）…",
            action=lambda: print("[Action] Choose payment path"),
            step_type="decision"
        )
    
    if step_name == "navigate_to_payment_point":
        return Step(
            "正在导航到缴费窗口…",
            action=lambda: print("[Action] Navigate to payment point"),
            step_type="navigate"
        )
    
    if step_name == "assist_payment_steps":
        return Step(
            "请插卡或扫码完成缴费",
            action=lambda: print("[Action] Assist payment steps"),
            step_type="assist"
        )
    
    if step_name == "update_bill_memory":
        return Step(
            "正在记录缴费信息…",
            action=lambda: print("[Action] Update bill memory"),
            step_type="memory"
        )
    
    # 检验/检查流程步骤
    if step_name == "locate_lab_zone":
        return Step(
            "正在查找检验科区域…",
            action=lambda: _locate_zone("Lab", context),
            step_type="locate"
        )
    
    if step_name == "navigate_to_lab_counter":
        return Step(
            "正在导航到检验科窗口…",
            action=lambda: print("[Action] Navigate to lab counter"),
            step_type="navigate"
        )
    
    if step_name == "enter_room_when_called":
        return Step(
            "听到叫号后，正在引导您进入检查室…",
            action=lambda: print("[Action] Enter room when called"),
            step_type="action"
        )
    
    if step_name == "record_test_order":
        return Step(
            "正在记录检查项目…",
            action=lambda: print("[Action] Record test order"),
            step_type="memory"
        )
    
    # 取药流程步骤
    if step_name == "locate_pharmacy":
        return Step(
            "正在查找药房…",
            action=lambda: _locate_zone("Pharmacy", context),
            step_type="locate"
        )
    
    if step_name == "assist_pickup_steps":
        return Step(
            "请把处方单递给窗口工作人员",
            action=lambda: print("[Action] Assist pickup steps"),
            step_type="assist"
        )
    
    if step_name == "record_medication_info":
        return Step(
            "正在记录药品信息和使用注意事项…",
            action=lambda: print("[Action] Record medication info"),
            step_type="memory"
        )
    
    # 默认步骤
    return Step(
        f"执行步骤：{step_name}",
        action=lambda: print(f"[Action] {step_name}"),
        step_type="action"
    )


def _locate_zone(zone_type: str, context: Dict[str, Any]):
    """
    定位区域（占位实现）
    """
    log.info(f"[Action] Locate zone: {zone_type}")
    # TODO: 实际实现中，这里应该调用 SceneGraph 查找最近节点


def _choose_registration_path(context: Dict[str, Any]):
    """
    选择挂号路径（占位实现）
    优先级：咨询台 > 人工窗口 > 自助机
    """
    log.info("[Action] Choose registration path (InquiryDesk > Counter > SelfService)")














