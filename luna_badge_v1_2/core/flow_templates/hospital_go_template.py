# core/flow_templates/hospital_go_template.py
from typing import Dict
from .base_templates import BaseFlowTemplate
from ..flow_engine.flow_types import (
    FlowDefinition,
    FlowNode,
    FlowEdge,
    FlowNodeType,
    FlowContext,
)
from ..flow_engine.planner import PlanningInput


# 导入 hook point 常量
from pieces.builtin.map_record_piece import HOOK_POINT_GO_BEFORE
from pieces.builtin.staff_assist_piece import HOOK_POINT_REGISTER_BEFORE


# 一些简单的节点执行器，真实环境里你可以拆出去单独管理
def exec_query_destination(ctx: FlowContext, params: Dict) -> Dict:
    # 将要播报的问题写入 context.prompts
    question = params.get("question", "你要去哪个医院？")
    ctx.append_prompt(question)
    # 这里只标记需要外部填充，真实交互里 Answer 来自用户语音
    return {"status": "success", "need_user_answer": True, "slot": "hospital_name"}


def exec_navigate_to_hospital(ctx: FlowContext, params: Dict) -> Dict:
    hospital = ctx.data.get("hospital_name") or params.get("default_hospital", "医院")
    text = f"好的，我会带你前往 {hospital}。现在请沿着前方人行道直行，注意安全。"
    ctx.append_prompt(text)
    return {"status": "success"}


def exec_wait_arrival(ctx: FlowContext, params: Dict) -> Dict:
    # 在真实系统里，这里会监听 GPS / 视觉确认是否到达
    ctx.append_prompt("当你感觉自己已经到达医院门口时，可以对我说：我到了。")
    return {"status": "success"}


class GoHospitalTemplate(BaseFlowTemplate):
    id = "go_hospital_basic"
    supported_intents = ["go_hospital"]
    supported_scenes = ["outdoor", "unknown"]
    
    # Hook 点定义
    hook_points = {
        "GO_BEFORE": "ask_hospital",        # 出发前准备阶段（在询问医院之前）
        "before_navigate": "navigate",      # 导航开始前
        "after_navigate": "navigate",      # 导航结束后
        "before_waiting": "wait_arrival",   # 等待到达前
        "after_waiting": "wait_arrival",    # 等待到达后
        # 未来可扩展：
        # "before_register": "register",
        # "after_register": "register",
        # "before_room_entry": "room_entry",
    }

    def instantiate(self, planning_input: PlanningInput) -> FlowDefinition:
        nodes: Dict[str, FlowNode] = {
            "ask_hospital": FlowNode(
                id="ask_hospital",
                node_type=FlowNodeType.QUERY_USER,
                params={
                    "question": "你要去哪个医院？如果是上次那家，也可以说：就去上次那家医院。",
                },
                executor=exec_query_destination,
            ),
            "navigate": FlowNode(
                id="navigate",
                node_type=FlowNodeType.NAVIGATE,
                params={},
                executor=exec_navigate_to_hospital,
            ),
            "wait_arrival": FlowNode(
                id="wait_arrival",
                node_type=FlowNodeType.WAIT_EVENT,
                params={},
                executor=exec_wait_arrival,
            ),
        }

        edges = [
            FlowEdge(source_id="ask_hospital", target_id="navigate", condition="success"),
            FlowEdge(source_id="navigate", target_id="wait_arrival", condition="success"),
        ]

        flow_def = FlowDefinition(
            id=self.id,
            nodes=nodes,
            edges=edges,
            entry_node_id="ask_hospital",
            hook_points=self.hook_points.copy(),  # 传递 Hook 点信息
        )
        
        # === 新增：声明本模板支持的 hook points ===
        # hook_points 列表
        hook_points = flow_def.metadata.get("hook_points", [])
        
        for hp in (HOOK_POINT_GO_BEFORE, HOOK_POINT_REGISTER_BEFORE):
            if hp not in hook_points:
                hook_points.append(hp)
        flow_def.metadata["hook_points"] = hook_points
        
        # === 新增：hook_points_detail，声明 attach_node ===
        hook_points_detail = flow_def.metadata.get("hook_points_detail", {})
        
        # 出发前：挂在 ask_hospital 之后
        hook_points_detail[HOOK_POINT_GO_BEFORE] = {
            "attach_node": "ask_hospital",
        }
        
        # 挂号前：先挂在 navigate 之后（当前流程为 ask_hospital -> navigate -> wait_arrival）
        # 后续你有更细的挂号节点，可以改这里
        hook_points_detail[HOOK_POINT_REGISTER_BEFORE] = {
            "attach_node": "navigate",
        }
        
        flow_def.metadata["hook_points_detail"] = hook_points_detail
        
        return flow_def

