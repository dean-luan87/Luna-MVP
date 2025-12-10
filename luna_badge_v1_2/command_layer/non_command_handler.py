"""
NonCommandHandler - 非命令处理器

对非命令输入统一返回"当前仅支持明确指令"的提示
不进入 Inquiry / DecisionCore / TaskChain
"""

from typing import Dict, Any


def handle_non_command(text: str) -> Dict[str, Any]:
    """
    处理非命令输入
    
    Args:
        text: 非命令文本
    
    Returns:
        Dict: 统一响应结构
        
    禁止：
    - 在 NonCommandHandler 内调用 TaskChain / DecisionCore
    - 修改任何与任务相关的状态
    """
    return {
        "type": "NON_COMMAND_RESPONSE",
        "message": "我现在处于任务模式，只能执行明确的指令。如果你想聊天或问问题，这部分能力会在后续版本开放。",
        "raw_text": text
    }

