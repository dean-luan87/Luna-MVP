"""
Renderer Pipeline (C-3 总入口)

渲染器总入口
"""

from .template_selector import TemplateSelector
from .expression_composer import ExpressionComposer
from .output_adapter import OutputAdapter
from .template_registry import TemplateRegistry
from .render_profile import RenderProfile
from ..calibration.expression_params import ExpressionParams
from ..governance.output_boundary import OutputGovernanceBoundary
from ..profile.profile_transformer import ProfileTransformer
from ..profile.expression_profile import ExpressionProfile


class RendererPipeline:
    """
    渲染器管道
    
    职责：
    - 协调模板选择、文本组合、输出适配
    - 提供统一的渲染接口
    - 接入 C-4 输出治理边界
    """
    
    def __init__(
        self,
        registry: TemplateRegistry,
        governance=None,
        expression_profile: ExpressionProfile = None
    ):
        """
        初始化渲染器管道
        
        Args:
            registry: 模板注册器
            governance: 输出治理边界（可选，默认创建 OutputGovernanceBoundary）
            expression_profile: 表达画像（可选，默认使用 ExpressionProfile.default()）
        """
        self.selector = TemplateSelector()
        self.composer = ExpressionComposer()
        self.adapter = OutputAdapter()
        self.registry = registry
        
        # C-5 表达画像转换器
        if expression_profile is None:
            expression_profile = ExpressionProfile.default()
        self.expression_profile = expression_profile
        self.transformer = ProfileTransformer()
        
        # C-4 输出治理边界
        if governance is None:
            from ..governance.output_boundary import OutputGovernanceBoundary
            self.governance = OutputGovernanceBoundary()
        else:
            self.governance = governance
    
    def _render_text(
        self,
        params: ExpressionParams,
        profile: RenderProfile
    ) -> str:
        """
        内部方法：渲染文本（不输出）
        
        Args:
            params: 表达参数
            profile: 表达风格
            
        Returns:
            str: 渲染后的文本
        """
        # 1. 选择模板
        template = self.selector.select(
            self.registry.all(),
            params.action,
            profile
        )
        
        # 2. 组合文本
        text = self.composer.compose(template, params, profile)
        
        return text
    
    def render(
        self,
        params: ExpressionParams,
        profile: RenderProfile = None
    ) -> str:
        """
        渲染表达文本（接入 C-4 治理）
        
        Args:
            params: 表达参数
            profile: 表达风格（可选，默认使用 RenderProfile.default()）
            
        Returns:
            str: 渲染后的文本
        """
        if profile is None:
            profile = RenderProfile.default()
        
        # 1. 渲染文本（C-3）
        text = self._render_text(params, profile)
        
        # 2. C-5 表达画像转换（在 C-3 之后，C-4 之前）
        text = self.transformer.apply(text, self.expression_profile)
        
        # 3. C-4 治理评估
        # 从 params 中提取治理所需字段（兼容旧代码）
        contract_id = getattr(params, 'contract_id', params.action)
        scene = getattr(params, 'scene', 'navigation')
        urgency = getattr(params, 'urgency', 'normal')
        duplicate_key = getattr(params, 'duplicate_key', None)
        
        decision = self.governance.evaluate(
            rendered_text=text,
            contract_id=contract_id,
            scene=scene,
            urgency=urgency,
            duplicate_key=duplicate_key
        )
        
        # 4. 执行输出（根据治理决策）
        self.governance.execute(
            decision,
            lambda: self.adapter.output(text)
        )
        
        return text
    
    def render_with_metadata(
        self,
        params: ExpressionParams,
        profile: RenderProfile = None,
        metadata: dict = None
    ) -> str:
        """
        渲染表达文本（带元数据）
        
        Args:
            params: 表达参数
            profile: 表达风格（可选）
            metadata: 元数据（可选）
            
        Returns:
            str: 渲染后的文本
        """
        if profile is None:
            profile = RenderProfile.default()
        
        # 1. 渲染文本（C-3）
        text = self._render_text(params, profile)
        
        # 2. C-5 表达画像转换
        text = self.transformer.apply(text, self.expression_profile)
        
        # 3. 输出（带元数据）
        self.adapter.output_with_metadata(text, metadata)
        
        return text
