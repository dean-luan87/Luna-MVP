"""
Output Adapter (C-3.4)

输出适配器

一期默认 stdout
后续可替换为 TTS / 硬件输出
"""


class OutputAdapter:
    """
    输出适配器
    
    职责：
    - 将文本输出到目标通道
    - 一期：stdout
    - 二期：TTS / 硬件输出
    """
    
    def output(self, text: str):
        """
        输出文本
        
        Args:
            text: 要输出的文本
        """
        print(text)
    
    def output_with_metadata(self, text: str, metadata: dict = None):
        """
        输出文本（带元数据）
        
        Args:
            text: 要输出的文本
            metadata: 元数据（可选）
        """
        if metadata:
            print(f"[{metadata.get('source', 'renderer')}] {text}")
        else:
            print(text)
