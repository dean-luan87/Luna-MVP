#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 商品成分识别与联网反馈模块
识别商品标签内容，并联网获取评价信息
"""

import logging
import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import time
import re

logger = logging.getLogger(__name__)

class HealthLevel(Enum):
    """健康等级"""
    HEALTHY = "healthy"           # 健康
    MODERATE = "moderate"        # 中等
    UNHEALTHY = "unhealthy"      # 不健康
    WARNING = "warning"          # 警告

class ProductRisk(Enum):
    """产品风险"""
    SAFE = "safe"                # 安全
    CAUTION = "caution"          # 谨慎
    WARNING = "warning"         # 警告
    DANGER = "danger"           # 危险

@dataclass
class IngredientInfo:
    """成分信息"""
    name: str                    # 成分名称
    category: str                # 类别
    health_level: HealthLevel   # 健康等级
    description: str             # 描述
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "name": self.name,
            "category": self.category,
            "health_level": self.health_level.value,
            "description": self.description
        }

@dataclass
class ProductInfo:
    """产品信息"""
    name: str                     # 产品名称
    barcode: Optional[str]        # 条形码
    ingredients: List[IngredientInfo]  # 成分列表
    overall_risk: ProductRisk     # 总体风险
    health_score: float           # 健康评分
    timestamp: float              # 时间戳
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "name": self.name,
            "barcode": self.barcode,
            "ingredients": [i.to_dict() for i in self.ingredients],
            "overall_risk": self.overall_risk.value,
            "health_score": self.health_score,
            "timestamp": self.timestamp
        }

class ProductInfoChecker:
    """商品信息检查器"""
    
    def __init__(self):
        """初始化检查器"""
        self.logger = logging.getLogger(__name__)
        
        # 不健康成分列表
        self.unhealthy_ingredients = {
            "亚硝酸钠", "味精", "防腐剂", "人工色素",
            "反式脂肪酸", "高果糖玉米糖浆", "阿斯巴甜",
            "苯甲酸钠", "山梨酸钾", "硝酸钠",
            "nitrates", "MSG", "artificial color"
        }
        
        # 违规成分列表
        self.forbidden_ingredients = {
            "苏丹红", "三聚氰胺", "瘦肉精", "塑化剂",
            "sudan red", "melamine", "clenbuterol"
        }
        
        # 成分数据库（预留接口）
        self.ingredient_db: Dict[str, IngredientInfo] = {}
        
        self.logger.info("🛒 商品信息检查器初始化完成")
    
    def check_product(self, ocr_text: str, barcode: Optional[str] = None) -> ProductInfo:
        """
        检查商品信息
        
        Args:
            ocr_text: OCR识别的文本
            barcode: 条形码（可选）
            
        Returns:
            ProductInfo: 产品信息
        """
        # 提取产品名称
        product_name = self._extract_product_name(ocr_text)
        
        # 提取成分列表
        ingredients = self._extract_ingredients(ocr_text)
        
        # 分析健康等级
        health_score = self._calculate_health_score(ingredients)
        
        # 评估总体风险
        overall_risk = self._assess_risk(ingredients)
        
        result = ProductInfo(
            name=product_name,
            barcode=barcode,
            ingredients=ingredients,
            overall_risk=overall_risk,
            health_score=health_score,
            timestamp=time.time()
        )
        
        self.logger.info(f"🛒 商品检查: {product_name}, "
                        f"风险={overall_risk.value}, "
                        f"评分={health_score:.1f}/10")
        
        return result
    
    def _extract_product_name(self, text: str) -> str:
        """
        提取产品名称
        
        Args:
            text: OCR文本
            
        Returns:
            str: 产品名称
        """
        lines = text.split('\n')
        
        # 尝试从第一行或标题行提取
        for line in lines[:5]:
            if len(line) > 0 and len(line) < 50:
                # 移除常见的前缀
                name = re.sub(r'^(品名|名称|产品名|Product)[:：]', '', line).strip()
                if name:
                    return name
        
        # 返回第一行非空文本
        for line in lines:
            if line.strip():
                return line.strip()[:50]
        
        return "未知商品"
    
    def _extract_ingredients(self, text: str) -> List[IngredientInfo]:
        """
        提取成分列表
        
        Args:
            text: OCR文本
            
        Returns:
            List[IngredientInfo]: 成分列表
        """
        ingredients = []
        
        # 查找成分列表（通常在"配料"或"成分"关键词后）
        ingredient_pattern = r'(配料|成分|原料|Ingredients|Composition)[:：]\s*(.+?)(?:\n|$)'
        match = re.search(ingredient_pattern, text, re.IGNORECASE)
        
        if match:
            ingredient_text = match.group(2)
            # 分割成分（按逗号、分号、或换行）
            ingredients_list = re.split(r'[,，;；\n]', ingredient_text)
            
            for ingredient in ingredients_list:
                ingredient = ingredient.strip()
                if ingredient:
                    # 分类成分
                    category = self._classify_ingredient_category(ingredient)
                    health_level = self._assess_ingredient_health(ingredient)
                    
                    info = IngredientInfo(
                        name=ingredient,
                        category=category,
                        health_level=health_level,
                        description=self._get_ingredient_description(ingredient)
                    )
                    ingredients.append(info)
        
        return ingredients
    
    def _classify_ingredient_category(self, ingredient: str) -> str:
        """分类成分类别"""
        # 简单的分类逻辑
        if any(kw in ingredient for kw in ['油', '脂', 'oil', 'fat']):
            return "油脂类"
        elif any(kw in ingredient for kw in ['糖', '糖浆', 'sugar', 'syrup']):
            return "甜味剂"
        elif any(kw in ingredient for kw in ['盐', 'sodium']):
            return "调味品"
        elif any(kw in ingredient for kw in ['添加剂', '防腐剂', 'preservative']):
            return "添加剂"
        else:
            return "其他"
    
    def _assess_ingredient_health(self, ingredient: str) -> HealthLevel:
        """评估成分健康等级"""
        ingredient_lower = ingredient.lower()
        
        # 检查是否为违规成分
        for forbidden in self.forbidden_ingredients:
            if forbidden.lower() in ingredient_lower:
                return HealthLevel.WARNING
        
        # 检查是否为不健康成分
        for unhealthy in self.unhealthy_ingredients:
            if unhealthy.lower() in ingredient_lower:
                return HealthLevel.UNHEALTHY
        
        # 一般成分
        return HealthLevel.MODERATE
    
    def _get_ingredient_description(self, ingredient: str) -> str:
        """获取成分描述"""
        health_level = self._assess_ingredient_health(ingredient)
        
        descriptions = {
            HealthLevel.HEALTHY: "健康成分",
            HealthLevel.MODERATE: "常见成分",
            HealthLevel.UNHEALTHY: "不健康成分",
            HealthLevel.WARNING: "风险成分"
        }
        
        return descriptions.get(health_level, "未知")
    
    def _calculate_health_score(self, ingredients: List[IngredientInfo]) -> float:
        """计算健康评分（0-10）"""
        if not ingredients:
            return 5.0
        
        base_score = 10.0
        
        for ingredient in ingredients:
            if ingredient.health_level == HealthLevel.WARNING:
                base_score -= 3.0
            elif ingredient.health_level == HealthLevel.UNHEALTHY:
                base_score -= 1.5
            elif ingredient.health_level == HealthLevel.MODERATE:
                base_score -= 0.5
        
        return max(0.0, min(10.0, base_score))
    
    def _assess_risk(self, ingredients: List[IngredientInfo]) -> ProductRisk:
        """评估总体风险"""
        if not ingredients:
            return ProductRisk.SAFE
        
        warning_count = sum(1 for i in ingredients 
                           if i.health_level == HealthLevel.WARNING)
        unhealthy_count = sum(1 for i in ingredients 
                              if i.health_level == HealthLevel.UNHEALTHY)
        
        if warning_count > 0:
            return ProductRisk.DANGER
        elif unhealthy_count > 2:
            return ProductRisk.WARNING
        elif unhealthy_count > 0:
            return ProductRisk.CAUTION
        else:
            return ProductRisk.SAFE
    
    async def query_online_info(self, barcode: str) -> Optional[Dict[str, Any]]:
        """
        联网查询产品信息（预留接口）
        
        Args:
            barcode: 条形码
            
        Returns:
            Optional[Dict]: 产品信息（如果可用）
        """
        # 这里应该调用外部API，例如：
        # - 商品数据库API
        # - 第三方认证API
        # - 消费者评价API
        
        # 示例实现
        self.logger.info(f"🔍 联网查询条形码: {barcode}")
        
        # 模拟API响应
        return {
            "barcode": barcode,
            "product_name": "示例商品",
            "verified": True,
            "rating": 4.5,
            "source": "product_db_api"
        }


# 全局检查器实例
global_product_checker = ProductInfoChecker()

def check_product(ocr_text: str, barcode: Optional[str] = None) -> ProductInfo:
    """检查商品的便捷函数"""
    return global_product_checker.check_product(ocr_text, barcode)


if __name__ == "__main__":
    # 测试商品信息检查
    import logging
    logging.basicConfig(level=logging.INFO)
    
    checker = ProductInfoChecker()
    
    # 模拟OCR文本
    ocr_text = """产品名称: 某某饼干
配料: 小麦粉、植物起酥油、白砂糖、食盐、碳酸钠、味精、防腐剂、人工色素
条码: 1234567890123"""
    
    result = checker.check_product(ocr_text, barcode="1234567890123")
    
    print("\n" + "=" * 60)
    print("🛒 商品信息检查结果")
    print("=" * 60)
    
    print(f"\n产品名称: {result.name}")
    print(f"条形码: {result.barcode}")
    print(f"健康评分: {result.health_score:.1f}/10")
    print(f"总体风险: {result.overall_risk.value}")
    
    print(f"\n成分列表 ({len(result.ingredients)}个):")
    for i, ingredient in enumerate(result.ingredients, 1):
        print(f"  {i}. {ingredient.name}")
        print(f"     类别: {ingredient.category}")
        print(f"     健康等级: {ingredient.health_level.value}")
        print(f"     描述: {ingredient.description}")
    
    print("\n" + "=" * 60)
