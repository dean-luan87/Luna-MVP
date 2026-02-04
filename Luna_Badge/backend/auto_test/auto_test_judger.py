#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动测试判断器
根据关键词，检查描述里是否出现对应的词 / 同义词
"""


class AutoTestJudger:
    """
    简单规则：根据关键词，检查描述里是否出现对应的词 / 同义词
    后面可以升级成 Embedding 相似度。
    """
    
    MATCH_RULES = {
        "斑马线": ["斑马线", "人行横道", "zebra crossing"],
        "红绿灯": ["红绿灯", "信号灯", "traffic light", "红灯", "绿灯"],
        "人行道": ["人行道", "sidewalk", "行人道", "走道"],
        "盲道": ["盲道", "导盲砖", "凸起砖"],
        "道路施工": ["施工", "路障", "围挡", "施工区域"],
        "台阶": ["台阶", "楼梯", "台阶上下"],
        "坡道": ["坡道", "斜坡", "缓坡"],
        "公交站牌": ["公交站", "公交车站", "bus stop"],
        "地铁入口": ["地铁", "subway", "metro", "出入口"],
        "自动扶梯": ["自动扶梯", "扶梯", "escalator"],
        "电梯入口": ["电梯", "elevator"],
        "商场入口": ["商场", "mall"],
        "医院挂号大厅": ["医院", "挂号", "大厅"],
        "医院科室门牌": ["科室", "门牌", "诊室"],
        "小区大门": ["小区", "小区门口", "小区大门"],
        "小区停车场": ["停车场", "车位", "地面停车"],
        "小区道路": ["小区道路", "居民区道路"],
    }
    
    @staticmethod
    def normalize(s: str) -> str:
        return (s or "").lower().strip()
    
    @classmethod
    def judge(cls, keyword: str, description: str):
        """
        Args:
            keyword: 测试关键词
            description: 场景描述文本
        
        Returns:
            match: bool
            hit_word: str or None
        """
        if not description:
            return False, None
        
        desc = cls.normalize(description)
        rules = cls.MATCH_RULES.get(keyword, [])
        
        for w in rules:
            if cls.normalize(w) in desc:
                return True, w
        
        # 没有配置规则时，降级为关键词本身搜索
        if not rules and cls.normalize(keyword) in desc:
            return True, keyword
        
        return False, None

