#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna 智能任务引擎 - 任务图模板库
将现有任务流程转换为TaskGraph格式
"""

import logging
from typing import Dict, List, Any
from .task_engine import TaskGraph, TaskNode, TaskEdge, NodeType, FlowControl

logger = logging.getLogger(__name__)

class TaskGraphTemplates:
    """任务图模板库"""
    
    @staticmethod
    def create_hospital_visit_template() -> TaskGraph:
        """创建医院就诊任务图模板"""
        return TaskGraph(
            graph_id="hospital_visit_template",
            scene="healthcare",
            goal="完成一次完整的医院就诊流程",
            nodes=[
                # 1. 规划路线
                TaskNode(
                    id="plan_route",
                    type=NodeType.NAVIGATION,
                    title="规划路线",
                    description="导航到医院",
                    input_schema={"destination": "string", "transport_mode": "string"},
                    output_schema={"route": "string", "estimated_time": "number", "distance": "number"},
                    precondition=[],
                    postcondition=["route_planned"],
                    executor_config={"destination": "医院", "transport_mode": "auto"},
                    timeout=300
                ),
                
                # 2. 确认出发
                TaskNode(
                    id="confirm_departure",
                    type=NodeType.INTERACTION,
                    title="确认出发",
                    description="确认用户是否准备出发",
                    input_schema={"ready": "boolean"},
                    output_schema={"confirmed": "boolean"},
                    precondition=["route_planned"],
                    postcondition=["departure_confirmed"],
                    executor_config={
                        "question": "路线已规划完成，是否现在出发？",
                        "options": ["是", "否", "等一下"]
                    },
                    timeout=60
                ),
                
                # 3. 导航执行
                TaskNode(
                    id="execute_navigation",
                    type=NodeType.NAVIGATION,
                    title="执行导航",
                    description="实际导航到目标地点",
                    input_schema={"route": "string"},
                    output_schema={"arrived": "boolean", "location": "string"},
                    precondition=["departure_confirmed"],
                    postcondition=["arrived_hospital"],
                    executor_config={"mode": "real_time_navigation"},
                    timeout=1800  # 30分钟
                ),
                
                # 4. 观察医院入口
                TaskNode(
                    id="observe_hospital_entrance",
                    type=NodeType.OBSERVATION,
                    title="观察医院入口",
                    description="识别医院入口和指示牌",
                    input_schema={},
                    output_schema={"entrance_found": "boolean", "signs": "array"},
                    precondition=["arrived_hospital"],
                    postcondition=["entrance_identified"],
                    executor_config={"type": "ocr", "target": "hospital_signs"},
                    timeout=120
                ),
                
                # 5. 挂号确认
                TaskNode(
                    id="confirm_registration",
                    type=NodeType.INTERACTION,
                    title="挂号确认",
                    description="确认是否需要挂号",
                    input_schema={"has_appointment": "boolean"},
                    output_schema={"needs_registration": "boolean"},
                    precondition=["entrance_identified"],
                    postcondition=["registration_confirmed"],
                    executor_config={
                        "question": "您是否需要挂号？",
                        "options": ["需要挂号", "已有预约", "不知道"]
                    },
                    timeout=60
                ),
                
                # 6. 寻找挂号处
                TaskNode(
                    id="find_registration_desk",
                    type=NodeType.OBSERVATION,
                    title="寻找挂号处",
                    description="识别挂号处位置",
                    input_schema={},
                    output_schema={"registration_desk_found": "boolean", "location": "string"},
                    precondition=["registration_confirmed"],
                    postcondition=["registration_desk_found"],
                    executor_config={"type": "ocr", "target": "registration_signs"},
                    timeout=180
                ),
                
                # 7. 挂号流程
                TaskNode(
                    id="registration_process",
                    type=NodeType.EXTERNAL_CALL,
                    title="挂号流程",
                    description="执行挂号操作",
                    input_schema={"department": "string", "doctor": "string"},
                    output_schema={"registration_success": "boolean", "queue_number": "string"},
                    precondition=["registration_desk_found"],
                    postcondition=["registered"],
                    executor_config={"service": "hospital_registration"},
                    timeout=600
                ),
                
                # 8. 候诊等待
                TaskNode(
                    id="wait_for_appointment",
                    type=NodeType.INTERACTION,
                    title="候诊等待",
                    description="等待叫号或确认候诊状态",
                    input_schema={"queue_number": "string"},
                    output_schema={"called": "boolean", "wait_time": "number"},
                    precondition=["registered"],
                    postcondition=["called_in"],
                    executor_config={
                        "question": "请等待叫号，或告诉我当前状态",
                        "options": ["已叫号", "还在等待", "需要帮助"]
                    },
                    timeout=3600  # 1小时
                ),
                
                # 9. 就诊过程
                TaskNode(
                    id="medical_consultation",
                    type=NodeType.EXTERNAL_CALL,
                    title="就诊过程",
                    description="与医生进行诊疗",
                    input_schema={"symptoms": "string", "history": "string"},
                    output_schema={"diagnosis": "string", "prescription": "string"},
                    precondition=["called_in"],
                    postcondition=["consultation_completed"],
                    executor_config={"service": "medical_consultation"},
                    timeout=1800  # 30分钟
                ),
                
                # 10. 缴费确认
                TaskNode(
                    id="confirm_payment",
                    type=NodeType.INTERACTION,
                    title="缴费确认",
                    description="确认是否需要缴费",
                    input_schema={"amount": "number"},
                    output_schema={"payment_needed": "boolean"},
                    precondition=["consultation_completed"],
                    postcondition=["payment_confirmed"],
                    executor_config={
                        "question": "需要缴费吗？",
                        "options": ["需要缴费", "不需要", "已缴费"]
                    },
                    timeout=60
                ),
                
                # 11. 缴费流程
                TaskNode(
                    id="payment_process",
                    type=NodeType.EXTERNAL_CALL,
                    title="缴费流程",
                    description="执行缴费操作",
                    input_schema={"amount": "number", "payment_method": "string"},
                    output_schema={"payment_success": "boolean", "receipt": "string"},
                    precondition=["payment_confirmed"],
                    postcondition=["payment_completed"],
                    executor_config={"service": "payment"},
                    timeout=300
                ),
                
                # 12. 取药确认
                TaskNode(
                    id="confirm_pharmacy",
                    type=NodeType.INTERACTION,
                    title="取药确认",
                    description="确认是否需要取药",
                    input_schema={"prescription": "string"},
                    output_schema={"pharmacy_needed": "boolean"},
                    precondition=["payment_completed"],
                    postcondition=["pharmacy_confirmed"],
                    executor_config={
                        "question": "需要取药吗？",
                        "options": ["需要取药", "不需要", "已有药品"]
                    },
                    timeout=60
                ),
                
                # 13. 寻找药房
                TaskNode(
                    id="find_pharmacy",
                    type=NodeType.OBSERVATION,
                    title="寻找药房",
                    description="识别药房位置",
                    input_schema={},
                    output_schema={"pharmacy_found": "boolean", "location": "string"},
                    precondition=["pharmacy_confirmed"],
                    postcondition=["pharmacy_found"],
                    executor_config={"type": "ocr", "target": "pharmacy_signs"},
                    timeout=180
                ),
                
                # 14. 取药流程
                TaskNode(
                    id="pharmacy_process",
                    type=NodeType.EXTERNAL_CALL,
                    title="取药流程",
                    description="执行取药操作",
                    input_schema={"prescription": "string"},
                    output_schema={"medication_received": "boolean", "instructions": "string"},
                    precondition=["pharmacy_found"],
                    postcondition=["medication_received"],
                    executor_config={"service": "pharmacy"},
                    timeout=600
                ),
                
                # 15. 完成确认
                TaskNode(
                    id="completion_confirmation",
                    type=NodeType.INTERACTION,
                    title="完成确认",
                    description="确认就诊流程完成",
                    input_schema={},
                    output_schema={"completed": "boolean"},
                    precondition=["medication_received"],
                    postcondition=["visit_completed"],
                    executor_config={
                        "question": "就诊流程已完成，还有其他需要帮助的吗？",
                        "options": ["没有", "需要其他帮助", "回家"]
                    },
                    timeout=60
                )
            ],
            edges=[
                TaskEdge(from_node="plan_route", to_node="confirm_departure"),
                TaskEdge(from_node="confirm_departure", to_node="execute_navigation"),
                TaskEdge(from_node="execute_navigation", to_node="observe_hospital_entrance"),
                TaskEdge(from_node="observe_hospital_entrance", to_node="confirm_registration"),
                TaskEdge(from_node="confirm_registration", to_node="find_registration_desk"),
                TaskEdge(from_node="find_registration_desk", to_node="registration_process"),
                TaskEdge(from_node="registration_process", to_node="wait_for_appointment"),
                TaskEdge(from_node="wait_for_appointment", to_node="medical_consultation"),
                TaskEdge(from_node="medical_consultation", to_node="confirm_payment"),
                TaskEdge(from_node="confirm_payment", to_node="payment_process"),
                TaskEdge(from_node="payment_process", to_node="confirm_pharmacy"),
                TaskEdge(from_node="confirm_pharmacy", to_node="find_pharmacy"),
                TaskEdge(from_node="find_pharmacy", to_node="pharmacy_process"),
                TaskEdge(from_node="pharmacy_process", to_node="completion_confirmation")
            ],
            flow_control=FlowControl.SEQUENTIAL,
            metadata={
                "estimated_duration": 120,  # 2小时
                "complexity": "high",
                "user_interaction_level": "high",
                "ai_assistance_level": "high"
            }
        )
    
    @staticmethod
    def create_shopping_template() -> TaskGraph:
        """创建购物任务图模板"""
        return TaskGraph(
            graph_id="shopping_template",
            scene="retail",
            goal="完成一次购物流程",
            nodes=[
                TaskNode(
                    id="plan_shopping_route",
                    type=NodeType.NAVIGATION,
                    title="规划购物路线",
                    description="导航到购物中心",
                    input_schema={"destination": "string"},
                    output_schema={"route": "string", "estimated_time": "number"},
                    precondition=[],
                    postcondition=["route_planned"],
                    executor_config={"destination": "购物中心", "transport_mode": "auto"},
                    timeout=300
                ),
                
                TaskNode(
                    id="confirm_shopping_list",
                    type=NodeType.INTERACTION,
                    title="确认购物清单",
                    description="确认要购买的商品",
                    input_schema={"shopping_list": "array"},
                    output_schema={"confirmed_list": "array"},
                    precondition=["route_planned"],
                    postcondition=["list_confirmed"],
                    executor_config={
                        "question": "请告诉我您要购买什么商品？",
                        "options": ["食品", "日用品", "服装", "其他"]
                    },
                    timeout=120
                ),
                
                TaskNode(
                    id="navigate_to_mall",
                    type=NodeType.NAVIGATION,
                    title="导航到商场",
                    description="实际导航到购物中心",
                    input_schema={"route": "string"},
                    output_schema={"arrived": "boolean"},
                    precondition=["list_confirmed"],
                    postcondition=["arrived_mall"],
                    executor_config={"mode": "real_time_navigation"},
                    timeout=1800
                ),
                
                TaskNode(
                    id="observe_mall_layout",
                    type=NodeType.OBSERVATION,
                    title="观察商场布局",
                    description="识别商场内的店铺和指示牌",
                    input_schema={},
                    output_schema={"shops": "array", "layout": "string"},
                    precondition=["arrived_mall"],
                    postcondition=["layout_identified"],
                    executor_config={"type": "ocr", "target": "mall_directory"},
                    timeout=180
                ),
                
                TaskNode(
                    id="shopping_process",
                    type=NodeType.COMPOUND_TASK,
                    title="购物过程",
                    description="执行实际购物",
                    input_schema={"shopping_list": "array"},
                    output_schema={"items_purchased": "array", "total_cost": "number"},
                    precondition=["layout_identified"],
                    postcondition=["shopping_completed"],
                    executor_config={"mode": "guided_shopping"},
                    timeout=3600
                ),
                
                TaskNode(
                    id="checkout_process",
                    type=NodeType.EXTERNAL_CALL,
                    title="结账流程",
                    description="完成购物结账",
                    input_schema={"items": "array", "total_cost": "number"},
                    output_schema={"payment_success": "boolean", "receipt": "string"},
                    precondition=["shopping_completed"],
                    postcondition=["checkout_completed"],
                    executor_config={"service": "retail_checkout"},
                    timeout=300
                )
            ],
            edges=[
                TaskEdge(from_node="plan_shopping_route", to_node="confirm_shopping_list"),
                TaskEdge(from_node="confirm_shopping_list", to_node="navigate_to_mall"),
                TaskEdge(from_node="navigate_to_mall", to_node="observe_mall_layout"),
                TaskEdge(from_node="observe_mall_layout", to_node="shopping_process"),
                TaskEdge(from_node="shopping_process", to_node="checkout_process")
            ],
            flow_control=FlowControl.SEQUENTIAL,
            metadata={
                "estimated_duration": 90,  # 1.5小时
                "complexity": "medium",
                "user_interaction_level": "medium",
                "ai_assistance_level": "medium"
            }
        )
    
    @staticmethod
    def create_transport_template() -> TaskGraph:
        """创建出行任务图模板"""
        return TaskGraph(
            graph_id="transport_template",
            scene="transportation",
            goal="完成一次出行",
            nodes=[
                TaskNode(
                    id="plan_transport_route",
                    type=NodeType.NAVIGATION,
                    title="规划出行路线",
                    description="规划出行路线和交通方式",
                    input_schema={"destination": "string", "transport_mode": "string"},
                    output_schema={"route": "string", "estimated_time": "number", "cost": "number"},
                    precondition=[],
                    postcondition=["route_planned"],
                    executor_config={"mode": "multi_modal"},
                    timeout=300
                ),
                
                TaskNode(
                    id="confirm_transport_choice",
                    type=NodeType.INTERACTION,
                    title="确认交通方式",
                    description="确认选择的交通方式",
                    input_schema={"options": "array"},
                    output_schema={"selected_mode": "string"},
                    precondition=["route_planned"],
                    postcondition=["mode_confirmed"],
                    executor_config={
                        "question": "请选择交通方式",
                        "options": ["步行", "公交", "地铁", "出租车", "网约车"]
                    },
                    timeout=60
                ),
                
                TaskNode(
                    id="execute_transport",
                    type=NodeType.NAVIGATION,
                    title="执行出行",
                    description="实际执行出行计划",
                    input_schema={"route": "string", "mode": "string"},
                    output_schema={"arrived": "boolean", "actual_time": "number"},
                    precondition=["mode_confirmed"],
                    postcondition=["arrived_destination"],
                    executor_config={"mode": "real_time_navigation"},
                    timeout=3600
                )
            ],
            edges=[
                TaskEdge(from_node="plan_transport_route", to_node="confirm_transport_choice"),
                TaskEdge(from_node="confirm_transport_choice", to_node="execute_transport")
            ],
            flow_control=FlowControl.SEQUENTIAL,
            metadata={
                "estimated_duration": 60,  # 1小时
                "complexity": "low",
                "user_interaction_level": "low",
                "ai_assistance_level": "high"
            }
        )
    
    @staticmethod
    def get_all_templates() -> Dict[str, TaskGraph]:
        """获取所有模板"""
        return {
            "hospital_visit": TaskGraphTemplates.create_hospital_visit_template(),
            "shopping": TaskGraphTemplates.create_shopping_template(),
            "transport": TaskGraphTemplates.create_transport_template()
        }
    
    @staticmethod
    def create_custom_template(graph_id: str, scene: str, goal: str, 
                              nodes: List[TaskNode], edges: List[TaskEdge],
                              metadata: Dict[str, Any] = None) -> TaskGraph:
        """创建自定义模板"""
        return TaskGraph(
            graph_id=graph_id,
            scene=scene,
            goal=goal,
            nodes=nodes,
            edges=edges,
            metadata=metadata or {}
        )


if __name__ == "__main__":
    # 测试模板库
    print("📚 Luna任务图模板库测试")
    print("=" * 60)
    
    templates = TaskGraphTemplates.get_all_templates()
    
    for template_name, template in templates.items():
        print(f"\n📋 {template_name} 模板:")
        print(f"   场景: {template.scene}")
        print(f"   目标: {template.goal}")
        print(f"   节点数: {len(template.nodes)}")
        print(f"   边数: {len(template.edges)}")
        print(f"   预计时长: {template.metadata.get('estimated_duration', 0)}分钟")
        print(f"   复杂度: {template.metadata.get('complexity', 'unknown')}")
    
    print("\n🎉 模板库测试完成！")

