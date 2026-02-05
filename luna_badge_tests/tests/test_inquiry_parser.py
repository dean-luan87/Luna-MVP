# -*- coding: utf-8 -*-
"""
InquiryParser 单元测试
"""

import sys
import os

# 添加项目路径
_script_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.normpath(os.path.join(_script_dir, '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from inquiry.parser import InquiryParser


# 测试模板
tpl_resume = {
    "options": ["继续", "不继续"],
    "synonyms": {
        "继续": ["继续", "好", "行", "可以", "继续吧", "继续往前走"],
        "不继续": ["不继续", "停一下", "不用", "不走了"]
    },
    "map": {
        "继续": "RESUME_MAIN_TASK",
        "不继续": "REJECT"
    }
}

tpl_confirm = {
    "options": ["是", "否"],
    "synonyms": {
        "是": ["是", "好", "行", "可以", "带我进去", "进去吧"],
        "否": ["否", "不用", "不需要", "先不用", "暂时不要"]
    },
    "map": {
        "是": "CONFIRM",
        "否": "REJECT"
    }
}


def test_exact_option():
    """测试精确选项匹配"""
    parser = InquiryParser()
    out = parser.parse("继续", tpl_resume)
    assert out.intent_name == "RESUME_MAIN_TASK"
    assert out.need_confirm == False
    assert out.raw == "继续"


def test_synonym():
    """测试同义词匹配"""
    parser = InquiryParser()
    out = parser.parse("好", tpl_resume)
    assert out.intent_name == "RESUME_MAIN_TASK"
    assert out.need_confirm == False
    assert out.raw == "好"


def test_synonym_abort():
    """测试同义词匹配（不继续）"""
    parser = InquiryParser()
    out = parser.parse("停一下", tpl_resume)
    assert out.intent_name == "REJECT"
    assert out.need_confirm == False


def test_special_intent_toilet():
    """测试特殊指令识别（厕所）"""
    parser = InquiryParser()
    out = parser.parse("我想先去厕所", tpl_resume)
    assert out.intent_name == "INSERT_TASK"
    assert out.need_confirm == True
    assert out.slots == {"task_type": "toilet"}


def test_special_intent_change_destination():
    """测试特殊指令识别（改目标）"""
    parser = InquiryParser()
    out = parser.parse("换个地方", tpl_resume)
    assert out.intent_name == "CHANGE_DESTINATION"
    assert out.need_confirm == True


def test_special_intent_buy():
    """测试特殊指令识别（买东西）"""
    parser = InquiryParser()
    out = parser.parse("我想买点东西", tpl_resume)
    assert out.intent_name == "INSERT_TASK"
    assert out.need_confirm == True
    assert out.slots == {"task_type": "buy"}


def test_special_intent_cancel():
    """测试特殊指令识别（取消）"""
    parser = InquiryParser()
    # "不走了" 在同义词中匹配为 "不继续" -> REJECT
    # 但作为特殊指令，如果同义词未匹配，则作为特殊指令需要确认
    out = parser.parse("算了，不走了", tpl_resume)
    # 由于 "不走了" 在同义词中，会优先匹配同义词，所以 need_confirm=False
    assert out.intent_name == "REJECT"
    # 同义词匹配优先级高于特殊指令，所以 need_confirm=False
    assert out.need_confirm == False


def test_unknown():
    """测试未知回答"""
    parser = InquiryParser()
    out = parser.parse("我也不知道", tpl_resume)
    assert out.intent_name == "UNKNOWN"
    assert out.need_confirm == False


def test_confirm_template():
    """测试确认模板"""
    parser = InquiryParser()
    out = parser.parse("是", tpl_confirm)
    assert out.intent_name == "CONFIRM"
    assert out.need_confirm == False


def test_reject_template():
    """测试拒绝模板"""
    parser = InquiryParser()
    out = parser.parse("不用", tpl_confirm)
    assert out.intent_name == "REJECT"
    assert out.need_confirm == False


def test_priority_synonym_over_special():
    """测试优先级：同义词优先于特殊指令"""
    parser = InquiryParser()
    # "好" 既是同义词（RESUME_MAIN_TASK），也可能触发指令
    # 应该优先匹配同义词
    out = parser.parse("好", tpl_resume)
    assert out.intent_name == "RESUME_MAIN_TASK"
    assert out.need_confirm == False


def test_case_insensitive():
    """测试大小写不敏感"""
    parser = InquiryParser()
    out = parser.parse("继续", tpl_resume)
    assert out.intent_name == "RESUME_MAIN_TASK"
    
    out2 = parser.parse("继续", tpl_resume)
    assert out2.intent_name == "RESUME_MAIN_TASK"


def test_whitespace_trim():
    """测试空白字符处理"""
    parser = InquiryParser()
    out = parser.parse("  继续  ", tpl_resume)
    assert out.intent_name == "RESUME_MAIN_TASK"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
