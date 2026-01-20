"""
Base Model Adapter

所有模型适配器的基类，定义统一的预处理、推理、后处理接口。
"""


class BaseModelAdapter:
    """
    模型适配器基类
    
    职责：
    - 统一模型输入/输出格式
    - 提供预处理/推理/后处理的标准流程
    - 不包含具体业务逻辑
    """
    
    def __init__(self, model_id: str, version: str):
        """
        初始化适配器
        
        Args:
            model_id: 模型标识符
            version: 模型版本号
        """
        # TODO: 初始化适配器状态
        pass

    def preprocess(self, input_data):
        """
        预处理输入数据
        
        Args:
            input_data: 原始输入数据
            
        Returns:
            预处理后的数据
        """
        # TODO: 实现预处理逻辑
        pass

    def infer(self, input_data):
        """
        执行模型推理
        
        Args:
            input_data: 预处理后的输入数据
            
        Returns:
            模型原始输出
        """
        # TODO: 实现推理逻辑
        pass

    def postprocess(self, raw_output):
        """
        后处理模型输出
        
        Args:
            raw_output: 模型原始输出
            
        Returns:
            标准化后的输出
        """
        # TODO: 实现后处理逻辑
        pass





