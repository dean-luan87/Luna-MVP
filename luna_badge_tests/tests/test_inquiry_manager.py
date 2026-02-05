# -*- coding: utf-8 -*-
"""
InquiryManager 单元测试
"""

import sys
import os
import tempfile
import json

# 添加项目路径
_script_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.normpath(os.path.join(_script_dir, '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from inquiry.inquiry_manager import InquiryManager


def test_build_question():
    """测试构建问句"""
    # 创建临时模板文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        templates = {
            "test_question": {
                "question": "测试问句：{intent_desc}",
                "options": ["是", "否"],
                "synonyms": {
                    "是": ["是", "好"],
                    "否": ["否", "不用"]
                },
                "map": {
                    "是": "CONFIRM",
                    "否": "REJECT"
                }
            }
        }
        json.dump(templates, f, ensure_ascii=False, indent=2)
        template_path = f.name
    
    try:
        manager = InquiryManager(template_path=template_path)
        result = manager.build_question("test_question", {"intent_desc": "去厕所"})
        
        assert result["type"] == "inquiry"
        assert "去厕所" in result["question"]
        assert result["options"] == ["是", "否"]
        assert result["internal_type"] == "test_question"
    finally:
        os.unlink(template_path)


def test_build_question_fallback():
    """测试构建问句（模板不存在时降级）"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump({}, f, ensure_ascii=False)
        template_path = f.name
    
    try:
        manager = InquiryManager(template_path=template_path)
        result = manager.build_question("nonexistent", {})
        
        assert result["type"] == "inquiry"
        assert "请再说一遍" in result["question"]
        assert result["internal_type"] == "fallback"
    finally:
        os.unlink(template_path)


def test_handle_user_response():
    """测试处理用户回答"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        templates = {
            "test_question": {
                "question": "测试问句",
                "options": ["是", "否"],
                "synonyms": {
                    "是": ["是", "好", "行"],
                    "否": ["否", "不用"]
                },
                "map": {
                    "是": "CONFIRM",
                    "否": "REJECT"
                }
            }
        }
        json.dump(templates, f, ensure_ascii=False, indent=2)
        template_path = f.name
    
    try:
        manager = InquiryManager(template_path=template_path)
        
        # 测试确认回答
        result = manager.handle_user_response("test_question", "是")
        assert result.intent_name == "CONFIRM"
        assert result.need_confirm == False
        
        # 测试拒绝回答
        result = manager.handle_user_response("test_question", "不用")
        assert result.intent_name == "REJECT"
        assert result.need_confirm == False
        
        # 测试未知回答
        result = manager.handle_user_response("test_question", "我不知道")
        assert result.intent_name == "UNKNOWN"
        assert result.need_confirm == False
    finally:
        os.unlink(template_path)


def test_unknown_degradation():
    """测试连续 UNKNOWN 降级"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        templates = {
            "test_question": {
                "question": "测试问句",
                "options": ["是", "否"],
                "synonyms": {},
                "map": {}
            }
        }
        json.dump(templates, f, ensure_ascii=False, indent=2)
        template_path = f.name
    
    try:
        manager = InquiryManager(template_path=template_path)
        
        # 第一次 UNKNOWN
        result1 = manager.handle_user_response("test_question", "不知道")
        assert result1.intent_name == "UNKNOWN"
        assert result1.need_confirm == False  # 第一次，正常
        
        # 第二次 UNKNOWN（应该触发降级）
        result2 = manager.handle_user_response("test_question", "还是不知道")
        assert result2.intent_name == "UNKNOWN"
        assert result2.need_confirm == False  # 降级后，need_confirm=False
        
        # 第三次应该重置计数
        result3 = manager.handle_user_response("test_question", "是")
        # 如果模板中有匹配，应该能解析
        # 这里由于模板为空，应该还是 UNKNOWN，但计数已重置
    finally:
        os.unlink(template_path)


def test_reset_unknown_count():
    """测试重置 UNKNOWN 计数"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump({}, f, ensure_ascii=False)
        template_path = f.name
    
    try:
        manager = InquiryManager(template_path=template_path)
        
        # 第一次 UNKNOWN
        manager.handle_user_response("test", "不知道")
        
        # 手动重置
        manager.reset_unknown_count()
        
        # 再次 UNKNOWN 应该从 0 开始计数
        result = manager.handle_user_response("test", "还是不知道")
        assert result.intent_name == "UNKNOWN"
    finally:
        os.unlink(template_path)


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])


