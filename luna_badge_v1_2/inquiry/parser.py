# -*- coding: utf-8 -*-
"""
Luna Badge v1.4.3 - InquiryParser 实现

问询解析器，负责将用户文本转换为结构化意图。
"""

from core.intent_schema import ParsedIntent


class InquiryParser:
    """
    问询解析器
    
    解析逻辑优先级：
    1. 同义词匹配（tpl["synonyms"]）
    2. 精确选项匹配（tpl["options"]）
    3. 特殊指令解析（如"厕所/换/买"等）
    4. 无法解析 → intent_name="UNKNOWN"
    """
    
    def parse(self, text: str, tpl: dict) -> ParsedIntent:
        """
        解析用户文本
        
        Args:
            text: 用户输入的文本
            tpl: 问询模板字典
        
        Returns:
            ParsedIntent: 解析后的意图
        """
        if not text or not text.strip():
            return ParsedIntent(
                intent_name="UNKNOWN",
                slots={},
                source="inquiry",
                need_confirm=False,
                raw=text or ""
            )
        
        normalized = text.strip().lower()
        
        # 1. 同义词匹配（优先级最高）
        synonyms = tpl.get("synonyms", {})
        map_dict = tpl.get("map", {})
        
        for key, syn_list in synonyms.items():
            for syn in syn_list:
                if syn.lower() in normalized:
                    intent_name = map_dict.get(key, "UNKNOWN")
                    return ParsedIntent(
                        intent_name=intent_name,
                        slots={},
                        source="inquiry",
                        need_confirm=False,
                        raw=text
                    )
        
        # 2. 精确选项匹配
        options = tpl.get("options", [])
        for opt in options:
            if opt.lower() in normalized:
                intent_name = map_dict.get(opt, "UNKNOWN")
                return ParsedIntent(
                    intent_name=intent_name,
                    slots={},
                    source="inquiry",
                    need_confirm=False,
                    raw=text
                )
        
        # 3. 特殊指令解析
        special = self._parse_special_intents(normalized)
        if special:
            return ParsedIntent(
                intent_name=special["intent_name"],
                slots=special.get("slots", {}),
                source="inquiry",
                need_confirm=True,
                raw=text
            )
        
        # 4. 无法解析 → UNKNOWN
        return ParsedIntent(
            intent_name="UNKNOWN",
            slots={},
            source="inquiry",
            need_confirm=False,
            raw=text
        )
    
    def _parse_special_intents(self, text: str) -> dict:
        """
        解析特殊指令
        
        Args:
            text: 标准化后的文本
        
        Returns:
            dict: 包含 intent_name 和 slots 的字典，如果未匹配则返回 None
        """
        # 检查是否包含"厕所"或"711"或"便利店"或"商店"
        if "厕所" in text or "711" in text or "便利店" in text or "商店" in text or "取快递" in text:
            if "711" in text or "便利店" in text or "商店" in text:
                return {
                    "intent_name": "INSERT_TASK",
                    "slots": {"task_type": "buy"}
                }
            elif "取快递" in text:
                return {
                    "intent_name": "INSERT_TASK",
                    "slots": {"task_type": "buy"}
                }
            else:
                return {
                    "intent_name": "INSERT_TASK",
                    "slots": {"task_type": "toilet"}
                }
        
        # 检查是否包含"换"或"改"或"不去了"（后面跟目的地）
        if "换" in text or "改" in text or ("不去了" in text and ("去" in text or "带" in text)):
            return {
                "intent_name": "CHANGE_DESTINATION",
                "slots": {}
            }
        
        # 检查是否包含"买"
        if "买" in text:
            return {
                "intent_name": "INSERT_TASK",
                "slots": {"task_type": "buy"}
            }
        
        # 检查是否包含"带我去"或"去"（导航任务）
        if "带我去" in text or ("去" in text and ("医院" in text or "银行" in text or "家" in text)):
            return {
                "intent_name": "CHANGE_DESTINATION",
                "slots": {}
            }
        
        # 检查是否包含"取消"或"算了"
        # 注意：这些可能已经在同义词中匹配，所以这里作为特殊指令需要确认
        if "取消" in text or "算了" in text or "不走了" in text:
            return {
                "intent_name": "REJECT",
                "slots": {}
            }
        
        return None

