"""
SemanticNormalizer v1 - 语义归一化器

将各种口语化的命令文本归一化成有限几种 intent_type + slots
"""

import re
from pydantic import BaseModel
from typing import Dict, Any, Optional, Union


class NormalizedCommand(BaseModel):
    """
    归一化后的命令结构
    
    Attributes:
        intent_type: 意图类型，如 "NAVIGATE", "CANCEL_TASK", "INSERT_TASK", "REPLACE_TASK"
        slots: 槽位字典，如 {"place_category": "hospital", "place_name": None}
        need_confirm: 是否需要确认
    """
    intent_type: str            # e.g. "NAVIGATE", "CANCEL_TASK", "INSERT_TASK", "REPLACE_TASK"
    slots: Dict[str, Any]       # e.g. {"place_category": "hospital", "place_name": None}
    need_confirm: bool = False


def normalize_command(text: str) -> NormalizedCommand:
    """
    将口语化的命令文本归一化为标准化命令
    
    Args:
        text: 命令文本（已去掉"Luna"前缀）
    
    Returns:
        NormalizedCommand: 归一化后的命令
        
    支持的意图类型：
    - NAVIGATE: 导航到某个地点
    - CANCEL_TASK: 取消当前任务
    - INSERT_TASK: 插入子任务
    - REPLACE_TASK: 替换当前任务
    
    约束：
    - 不允许做"自由意图推断"（即不根据情绪/主观句推任务）
    - 对于无法识别的命令，返回 UNKNOWN 意图类型
    """
    if not text or not isinstance(text, str):
        return NormalizedCommand(
            intent_type="UNKNOWN",
            slots={},
            need_confirm=False
        )
    
    text = text.strip()
    text_lower = text.lower()
    
    # 1. 检查 CANCEL_TASK
    if _is_cancel_task(text_lower):
        return NormalizedCommand(
            intent_type="CANCEL_TASK",
            slots={},
            need_confirm=False
        )
    
    # 2. 检查 INSERT_TASK（插入子任务）
    insert_result = _parse_insert_task(text_lower, text)
    if insert_result:
        return insert_result
    
    # 3. 检查 REPLACE_TASK（替换任务）
    replace_result = _parse_replace_task(text_lower, text)
    if replace_result:
        return replace_result
    
    # 4. 检查 NAVIGATE（导航）
    navigate_result = _parse_navigate(text_lower, text)
    if navigate_result:
        return navigate_result
    
    # 5. 无法识别
    return NormalizedCommand(
        intent_type="UNKNOWN",
        slots={},
        need_confirm=False
    )


def _is_cancel_task(text_lower: str) -> bool:
    """判断是否为取消任务命令"""
    cancel_keywords = [
        "取消", "停止", "中止", "放弃", "不做了",
        "cancel", "stop", "abort"
    ]
    for keyword in cancel_keywords:
        if keyword in text_lower:
            return True
    return False


def _parse_insert_task(text_lower: str, text: str) -> Optional[NormalizedCommand]:
    """
    解析插入任务命令
    
    示例：
    - "顺便去711" → INSERT_TASK, {"place_category": "convenience_store", "place_name": "711"}
    - "先去711" → INSERT_TASK, {"place_category": "convenience_store", "place_name": "711"}
    - "顺便去厕所" → INSERT_TASK, {"place_category": "toilet", "place_name": None}
    """
    # 检查插入任务关键词
    insert_keywords = ["顺便", "先去", "先到", "顺路"]
    is_insert = any(keyword in text_lower for keyword in insert_keywords)
    
    if not is_insert:
        return None
    
    # 解析地点
    place_info = _extract_place(text_lower, text)
    if place_info:
        return NormalizedCommand(
            intent_type="INSERT_TASK",
            slots=place_info,
            need_confirm=True  # 插入任务需要确认
        )
    
    return None


def _parse_replace_task(text_lower: str, text: str) -> Optional[NormalizedCommand]:
    """
    解析替换任务命令
    
    示例：
    - "改去医院" → REPLACE_TASK, {"place_category": "hospital", "place_name": None}
    - "换到711" → REPLACE_TASK, {"place_category": "convenience_store", "place_name": "711"}
    """
    # 检查替换任务关键词
    replace_keywords = ["改", "换", "更改", "更换", "改成", "换成"]
    is_replace = any(keyword in text_lower for keyword in replace_keywords)
    
    if not is_replace:
        return None
    
    # 解析地点
    place_info = _extract_place(text_lower, text)
    if place_info:
        return NormalizedCommand(
            intent_type="REPLACE_TASK",
            slots=place_info,
            need_confirm=True  # 替换任务需要确认
        )
    
    return None


def _parse_navigate(text_lower: str, text: str) -> Optional[NormalizedCommand]:
    """
    解析导航命令
    
    示例：
    - "带我去医院" → NAVIGATE, {"place_category": "hospital", "place_name": None}
    - "导航到医院" → NAVIGATE, {"place_category": "hospital", "place_name": None}
    - "我得去趟医院" → NAVIGATE, {"place_category": "hospital", "place_name": None}
    """
    # 检查导航关键词
    navigate_keywords = [
        "带我去", "去", "到", "导航到", "导航", "前往", "去往",
        "go to", "navigate", "take me to"
    ]
    is_navigate = any(keyword in text_lower for keyword in navigate_keywords)
    
    if not is_navigate:
        return None
    
    # 解析地点
    place_info = _extract_place(text_lower, text)
    if place_info:
        return NormalizedCommand(
            intent_type="NAVIGATE",
            slots=place_info,
            need_confirm=True  # 导航任务需要确认
        )
    
    return None


def _extract_place(text_lower: str, text: str) -> Optional[Dict[str, Any]]:
    """
    从文本中提取地点信息
    
    Returns:
        Dict: {"place_category": str, "place_name": str | None}
        如果无法识别，返回 None
    """
    # 地点类别映射
    place_categories = {
        "hospital": ["医院", "hospital", "诊所", "clinic"],
        "convenience_store": ["711", "7-11", "便利店", "convenience store", "小卖部"],
        "toilet": ["厕所", "洗手间", "卫生间", "toilet", "restroom", "wc"],
        "bank": ["银行", "bank", "atm"],
        "pharmacy": ["药店", "药房", "pharmacy"],
        "restaurant": ["餐厅", "饭店", "restaurant", "食堂"],
        "supermarket": ["超市", "supermarket", "商场", "mall"],
    }
    
    import re
    
    for category, keywords in place_categories.items():
        for keyword in keywords:
            if keyword in text_lower:
                # 找到关键词在文本中的位置
                keyword_pos = text_lower.find(keyword)
                if keyword_pos == -1:
                    continue
                
                # 尝试提取完整地点名称
                # 模式1: 提取 "XXX医院"、"XXX银行" 等（中文地点名称）
                # 在包含关键词的文本片段中查找
                start_pos = max(0, keyword_pos - 12)  # 最多向前12个字符
                end_pos = min(len(text), keyword_pos + len(keyword) + 4)  # 包含关键词及之后
                text_segment = text[start_pos:end_pos]
                
                # 匹配关键词前的2-4个中文字符（地点名称）+ 关键词
                # 例如："虹口医院"、"瑞金医院"、"北京协和医院"
                pattern = r'([\u4e00-\u9fa5]{2,4})' + re.escape(keyword)
                match = re.search(pattern, text_segment)
                if match:
                    prefix = match.group(1)
                    full_name = prefix + keyword
                    
                    # 验证：完整名称长度合理（3-10个字符）
                    if 3 <= len(full_name) <= 10:
                        return {
                            "place_category": category,
                            "place_name": full_name
                        }
                
                # 模式2: 数字或短名称（如 "711"）
                if keyword.isdigit() or (len(keyword) <= 5 and keyword.isalnum()):
                    return {
                        "place_category": category,
                        "place_name": keyword
                    }
                
                # 模式3: 只有类别关键词，没有具体名称
                return {
                    "place_category": category,
                    "place_name": None
                }
    
    # 无法识别地点
    return None

