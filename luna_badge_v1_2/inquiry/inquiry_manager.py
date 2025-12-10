# -*- coding: utf-8 -*-
"""
Luna Badge v1.4.3 - InquiryManager 实现

问询管理器，负责生成问句和处理用户回答。
"""

import json
import os
from typing import Dict, Optional, Any
from .parser import InquiryParser
from core.intent_schema import ParsedIntent


class InquiryManager:
    """
    问询管理器
    
    职责：
    - 根据 question_type + context 生成问句（从模板中取）
    - 接收用户回答，调用 InquiryParser 生成 ParsedIntent 返回给决策层
    
    降级规则：
    - 若连续两次解析为 UNKNOWN，返回 UNKNOWN 并标记 need_confirm=False
    """
    
    def __init__(self, template_path: Optional[str] = None):
        """
        初始化问询管理器
        
        Args:
            template_path: 模板文件路径，默认使用 inquiry_templates.json
        """
        if template_path is None:
            template_path = os.path.join(
                os.path.dirname(__file__),
                "inquiry_templates.json"
            )
        
        self.template_path = template_path
        self.templates = self._load_templates()
        self.parser = InquiryParser()
        self._unknown_count = 0  # 连续 UNKNOWN 计数
    
    def _load_templates(self) -> Dict[str, Any]:
        """
        加载问询模板
        
        Returns:
            Dict: 模板字典
        """
        try:
            with open(self.template_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError as e:
            print(f"[InquiryManager] 模板文件 JSON 解析失败: {e}")
            return {}
        except Exception as e:
            print(f"[InquiryManager] 加载模板文件失败: {e}")
            return {}
    
    def build_question(self, question_type: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        构建问句
        
        Args:
            question_type: 问句类型（对应模板中的 key）
            context: 上下文信息（用于变量替换）
        
        Returns:
            Dict: 包含 question, options, internal_type 等的字典
        """
        if context is None:
            context = {}
        
        tpl = self.templates.get(question_type)
        if not tpl:
            # 降级：返回默认问句
            return {
                "type": "inquiry",
                "question": "请再说一遍，我没有听清。",
                "options": ["是", "否"],
                "internal_type": "fallback"
            }
        
        question = tpl.get("question", "")
        
        # 变量替换（如 {intent_desc}）
        if "{intent_desc}" in question and "intent_desc" in context:
            question = question.replace("{intent_desc}", context["intent_desc"])
        
        return {
            "type": "inquiry",
            "question": question,
            "options": tpl.get("options", []),
            "internal_type": question_type,
            "context": context
        }
    
    def handle_user_response(self, question_type: str, user_text: str) -> ParsedIntent:
        """
        处理用户回答
        
        Args:
            question_type: 问句类型（用于选择模板）
            user_text: 用户回答文本
        
        Returns:
            ParsedIntent: 解析后的意图
        """
        tpl = self.templates.get(question_type, {})
        parsed = self.parser.parse(user_text, tpl)
        
        # 降级策略：连续 UNKNOWN
        if parsed.intent_name == "UNKNOWN":
            self._unknown_count += 1
            if self._unknown_count >= 2:
                # 触发降级：连续两次 UNKNOWN，标记 need_confirm=False
                self._unknown_count = 0
                return ParsedIntent(
                    intent_name="UNKNOWN",
                    slots={},
                    source="inquiry",
                    need_confirm=False,
                    raw=user_text
                )
        else:
            # 成功解析，重置计数
            self._unknown_count = 0
        
        return parsed
    
    def reset_unknown_count(self) -> None:
        """重置 UNKNOWN 计数（可选，用于手动重置）"""
        self._unknown_count = 0


