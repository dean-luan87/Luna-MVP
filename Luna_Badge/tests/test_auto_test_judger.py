#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoTestJudger 单元测试
"""

import pytest

from backend.auto_test.auto_test_judger import AutoTestJudger


@pytest.mark.parametrize(
    "keyword,description,expected",
    [
        ("人行道", "画面中有一条人行道，旁边有人在走路。", True),
        ("斑马线", "可以看到清晰的斑马线和红绿灯。", True),
        ("地铁入口", "这是一个商场入口，门口有广告牌。", False),
        ("红绿灯", "前方有红绿灯，现在是红灯状态。", True),
        ("盲道", "地面上有导盲砖，这是盲道。", True),
        ("道路施工", "前方有施工区域，设置了围挡。", True),
        ("台阶", "前方有台阶，需要小心上下。", True),
        ("公交站牌", "这里是公交站，有公交车站牌。", True),
        ("自动扶梯", "商场里有自动扶梯，可以上下楼。", True),
        ("电梯入口", "这里是电梯入口，可以乘坐电梯。", True),
    ],
)
def test_auto_test_judger_basic(keyword, description, expected):
    """测试 AutoTestJudger 的基本匹配功能"""
    match, hit = AutoTestJudger.judge(keyword, description)
    assert match == expected, f"关键词 '{keyword}' 在描述 '{description}' 中应该{'匹配' if expected else '不匹配'}"


def test_auto_test_judger_empty_description():
    """测试空描述的情况"""
    match, hit = AutoTestJudger.judge("人行道", "")
    assert match is False
    assert hit is None


def test_auto_test_judger_none_description():
    """测试 None 描述的情况"""
    match, hit = AutoTestJudger.judge("人行道", None)
    assert match is False
    assert hit is None


def test_auto_test_judger_case_insensitive():
    """测试大小写不敏感"""
    match, hit = AutoTestJudger.judge("人行道", "画面中有一条人行道")
    assert match is True
    
    match2, hit2 = AutoTestJudger.judge("人行道", "画面中有一条人行道".upper())
    assert match2 is True


def test_auto_test_judger_unknown_keyword():
    """测试未知关键词（降级为关键词本身搜索）"""
    match, hit = AutoTestJudger.judge("未知关键词", "画面中有未知关键词")
    assert match is True
    assert hit == "未知关键词"


