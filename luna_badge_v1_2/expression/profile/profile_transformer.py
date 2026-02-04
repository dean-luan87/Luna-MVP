"""
Profile Transformer (C-5)

表达画像转换器

职责：
- 只改表达方式，不改语义事实
- 单位转换（米 → 步）
- 方位翻译（30° → 稍微偏右）
- 复杂度降级（专业 → 口语）
- 表达裁剪（删掉无意义信息）
- 同义替换（双方都懂的词）

⚠️ 一期这里允许写得很朴素
这是刻意的 —— 二期会替换这里的规则为模型/记忆
"""

import re
from .expression_profile import ExpressionProfile


class ProfileTransformer:
    """
    C-5 核心执行器
    
    只改表达方式，不改语义事实
    
    ✅ C-5 可以做：
    - 单位转换（米 → 步）
    - 方位翻译（30° → 稍微偏右）
    - 复杂度降级（专业 → 口语）
    - 表达裁剪（删掉无意义信息）
    - 同义替换（双方都懂的词）
    
    ❌ C-5 绝对不能做：
    - 不引入新信息
    - 不改变事实
    - 不接管节奏（那是 C-4）
    - 不引入情绪（那是二期）
    - 不做世界推理（那是 B）
    """
    
    def __init__(self):
        """初始化转换器"""
        pass
    
    def apply(self, text: str, profile: ExpressionProfile) -> str:
        """
        应用表达画像转换
        
        Args:
            text: C-3 生成的原始文本
            profile: 表达画像
            
        Returns:
            str: 转换后的文本
        """
        transformed = text
        
        # 距离表达
        if profile.distance_style == "step":
            transformed = self._metric_to_step(transformed)
        elif profile.distance_style == "relative":
            transformed = self._metric_to_relative(transformed)
        
        # 方向表达
        if profile.direction_style == "relative":
            transformed = self._degree_to_relative(transformed)
        
        # 语言复杂度
        if profile.language_level == "simple":
            transformed = self._simplify_language(transformed)
        elif profile.language_level == "professional":
            transformed = self._professionalize_language(transformed)
        
        # 是否允许抽象词
        if not profile.allow_abstract:
            transformed = self._remove_abstract(transformed)
        
        # 是否允许省略精度
        if profile.allow_fuzzy:
            transformed = self._fuzzify_numbers(transformed)
        
        return transformed
    
    def _metric_to_step(self, text: str) -> str:
        """
        米 → 步转换
        
        Args:
            text: 原始文本
            
        Returns:
            str: 转换后的文本
        """
        # 简化版：将"米"替换为"步左右"
        # 注意：一期这里是示意，二期可以接入精确的步数转换
        return text.replace("米", "步左右")
    
    def _metric_to_relative(self, text: str) -> str:
        """
        米 → 相对描述转换
        
        Args:
            text: 原始文本
            
        Returns:
            str: 转换后的文本
        """
        # 例如："5米" → "很近"
        # 一期简化版
        return text
    
    def _degree_to_relative(self, text: str) -> str:
        """
        度数 → 相对方向转换
        
        Args:
            text: 原始文本
            
        Returns:
            str: 转换后的文本
        """
        # 简化版：示意
        return (
            text.replace("30度", "稍微向右")
                .replace("45度", "向右前方")
                .replace("60度", "右前方")
                .replace("90度", "右边")
                .replace("-30度", "稍微向左")
                .replace("-45度", "向左前方")
                .replace("-60度", "左前方")
                .replace("-90度", "左边")
        )
    
    def _simplify_language(self, text: str) -> str:
        """
        简化语言复杂度
        
        Args:
            text: 原始文本
            
        Returns:
            str: 简化后的文本
        """
        # 简化专业术语和复杂表达
        replacements = {
            "请注意": "",
            "即将": "马上",
            "准备": "要",
            "建议": "",
            "推荐": "",
            "前方": "前面",
            "后方": "后面",
            "左侧": "左边",
            "右侧": "右边",
        }
        
        result = text
        for old, new in replacements.items():
            result = result.replace(old, new)
        
        # 删除多余的空格
        result = re.sub(r'\s+', '', result)
        
        return result
    
    def _professionalize_language(self, text: str) -> str:
        """
        专业化语言（一期简化版）
        
        Args:
            text: 原始文本
            
        Returns:
            str: 专业化后的文本
        """
        # 一期简化版：可以添加专业术语
        return text
    
    def _remove_abstract(self, text: str) -> str:
        """
        移除抽象词
        
        Args:
            text: 原始文本
            
        Returns:
            str: 移除抽象词后的文本
        """
        # 抽象词列表（一期简化版）
        abstract_words = [
            "大约", "大概", "可能", "似乎", "也许"
        ]
        
        result = text
        for word in abstract_words:
            result = result.replace(word, "")
        
        return result
    
    def _fuzzify_numbers(self, text: str) -> str:
        """
        模糊化数字
        
        Args:
            text: 原始文本
            
        Returns:
            str: 模糊化后的文本
        """
        # 简化版：将精确数字转为模糊表达
        # 例如："5步" → "几步"
        # 一期简化版
        return text
