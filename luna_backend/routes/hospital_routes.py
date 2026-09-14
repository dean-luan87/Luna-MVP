"""
医院路由 (Hospital Routes) v1.2.0
医院场景高层接口
"""

from flask import Blueprint, request
from core.response import ok, error, api_success, api_error
from config.error_codes import ERR
from services.runtime import rt

# 延迟导入
def _get_error_reporter():
    try:
        from luna_backend.services.log.error_reporter import ErrorReporter
        return ErrorReporter
    except ImportError:
        try:
            from services.log.error_reporter import ErrorReporter
            return ErrorReporter
        except ImportError:
            return None

hospital_bp = Blueprint("hospital", __name__)


@hospital_bp.route('/start_flow', methods=['POST'])
def start_hospital_flow():
    """
    启动一个医院就诊任务链
    
    请求体:
    {
        "hospital_name": "新华医院",
        "department_name": "眼科",
        "is_first_visit": true,
        "has_report_to_collect": false
    }
    """
    data = request.get_json() or {}
    hospital_name = data.get("hospital_name")
    
    if not hospital_name:
        return api_error("缺少 hospital_name", status_code=400)
    
    department_name = data.get("department_name")
    is_first_visit = bool(data.get("is_first_visit", True))
    has_report_to_collect = bool(data.get("has_report_to_collect", False))
    
    if not rt.task_engine:
        ErrorReporter = _get_error_reporter()
        ERR = _get_error_codes()
        if ErrorReporter:
            ErrorReporter.report(
                ERR.HOSPITAL_FLOW_NOT_INIT,
                {"message": "task_engine not initialized when starting hospital flow"}
            )
        return api_error("任务引擎未初始化", status_code=500)
    
    try:
        from taskchain.hospital_task import HospitalTask
        
        task_id = f"hospital_{hospital_name}_{department_name or 'unknown'}"
        task = HospitalTask(
            task_id=task_id,
            hospital_name=hospital_name,
            department_name=department_name,
            is_first_visit=is_first_visit,
            has_report_to_collect=has_report_to_collect,
        )
        
        rt.task_engine.enqueue(task)
        
        return api_success({
            "task_id": task_id,
            "hospital_name": hospital_name,
            "department_name": department_name,
        }, message="医院流程任务已创建")
    
    except Exception as e:
        from utils.logger import logger
        logger.error(f"启动医院流程失败: {e}")
        return api_error(f"启动医院流程失败: {str(e)}", status_code=500)


@hospital_bp.route('/update_stage', methods=['POST'])
def update_hospital_stage():
    """
    主动推进医院阶段，通常由前端/语音触发：
    
    请求体:
    {
        "task_id": "hospital_xxx",
        "stage": "registration_done",
        "ticket_no": "23",
        "called_no": "18"
    }
    """
    data = request.get_json() or {}
    task_id = data.get("task_id")
    
    if not task_id:
        return api_error("缺少 task_id", status_code=400)
    
    if not rt.task_engine:
        return api_error("任务引擎未初始化", status_code=500)
    
    try:
        task = rt.task_engine.get_task(task_id)
        if task is None:
            return api_error("找不到对应的医院任务", status_code=404)
        
        from taskchain.hospital_task import HospitalTask
        if not isinstance(task, HospitalTask):
            return api_error("任务类型不匹配", status_code=400)
        
        event = {
            "type": "hospital_stage_update",
            "payload": {
                "stage": data.get("stage"),
                "ticket_no": data.get("ticket_no"),
                "called_no": data.get("called_no"),
            }
        }
        task.handle_event(event)
        
        return api_success({
            "task_id": task_id,
            "stage": task.stage
        })
    
    except Exception as e:
        from utils.logger import logger
        logger.error(f"更新医院阶段失败: {e}")
        return api_error(f"更新医院阶段失败: {str(e)}", status_code=500)


@hospital_bp.route('/set_stage', methods=['POST'])
def set_hospital_stage():
    """
    设置医院阶段（兼容旧接口）
    
    请求体:
    {
        "stage": "registration",  # "entering" / "registration" / "waiting" / "in_exam" / "leaving"
        "department_name": "眼科",
        "ticket_no": "A123"
    }
    """
    if rt.navigation_manager is None:
        return error(ERR.NAV_NOT_READY, "导航管理器未初始化", http_status=500)
    
    try:
        data = request.get_json() or {}
        stage = data.get('stage', 'unknown')
        department_name = data.get('department_name')
        ticket_no = data.get('ticket_no')
        
        ctx = rt.navigation_manager.context
        ctx.scene_type = "hospital"
        ctx.hospital_stage = stage
        
        if department_name:
            ctx.department_name = department_name
        
        if ticket_no:
            ctx.registration_ticket_no = ticket_no
        
        return ok({
            'message': '医院阶段已设置',
            'stage': stage,
            'context': ctx.to_dict()
        })
    
    except Exception as e:
        return error(ERR.NAV_UPDATE_FAIL, f"设置医院阶段失败: {str(e)}", http_status=500)


@hospital_bp.route('/hospital/update_ticket', methods=['POST'])
def update_ticket():
    """
    更新叫号信息
    
    请求体:
    {
        "called_ticket_no": "A120",
        "queue_len": 5
    }
    """
    if rt.navigation_manager is None:
        return error(ERR.NAV_NOT_READY, "导航管理器未初始化", http_status=500)
    
    try:
        data = request.get_json() or {}
        called_ticket_no = data.get('called_ticket_no')
        queue_len = data.get('queue_len')
        
        ctx = rt.navigation_manager.context
        if called_ticket_no:
            ctx.called_ticket_no = called_ticket_no
        if queue_len is not None:
            ctx.queue_len_estimate = int(queue_len)
        
        return ok({
            'message': '叫号信息已更新',
            'context': ctx.to_dict()
        })
    
    except Exception as e:
        return error(ERR.NAV_UPDATE_FAIL, f"更新叫号信息失败: {str(e)}", http_status=500)


@hospital_bp.route('/status', methods=['GET'])
def hospital_status():
    """
    查询当前医院上下文 + 任务状态，方便前端调试 / 日志
    
    query: ?task_id=xxx
    """
    task_id = request.args.get("task_id")
    
    if not task_id:
        # 如果没有task_id，返回导航上下文状态
        if rt.navigation_manager is None:
            return api_error("导航管理器未初始化", status_code=500)
        
        try:
            ctx = rt.navigation_manager.context
            return api_success({
                'hospital_stage': ctx.hospital_stage,
                'department_name': ctx.department_name,
                'has_registered': ctx.has_registered,
                'ticket_no': ctx.registration_ticket_no,
                'called_ticket_no': ctx.called_ticket_no,
                'queue_len': ctx.queue_len_estimate,
            })
        except Exception as e:
            return api_error(f"获取状态失败: {str(e)}", status_code=500)
    
    # 如果有task_id，返回任务状态
    if not rt.task_engine:
        return api_error("任务引擎未初始化", status_code=500)
    
    try:
        task = rt.task_engine.get_task(task_id)
        if task is None:
            return api_error("找不到对应的医院任务", status_code=404)
        
        from taskchain.hospital_task import HospitalTask
        if not isinstance(task, HospitalTask):
            return api_error("任务类型不匹配", status_code=400)
        
        ctx = None
        if rt.navigation_manager and hasattr(rt.navigation_manager, "context"):
            ctx = rt.navigation_manager.context
        
        ctx_dict = None
        if ctx:
            ctx_dict = {
                "scene_type": ctx.scene_type,
                "hospital_name": ctx.hospital_name,
                "hospital_stage": ctx.hospital_stage,
                "department_name": ctx.department_name,
                "registration_ticket_no": ctx.registration_ticket_no,
                "called_ticket_no": ctx.called_ticket_no,
            }
        
        return api_success({
            "task": {
                "task_id": task.task_id,
                "state": task.get_state(),
                "stage": task.stage,
                "hospital_name": task.hospital_name,
                "department_name": task.department_name,
            },
            "context": ctx_dict
        })
    
    except Exception as e:
        from utils.logger import logger
        logger.error(f"获取医院状态失败: {e}")
        return api_error(f"获取状态失败: {str(e)}", status_code=500)

