"""
HelpCenter Stub - 帮助中心入口（Stub 实现）

当前版本只返回"帮助中心将在后续版本开放"
不修改任何任务状态
"""

from typing import Dict, Any


def handle_help_center(command_text: str) -> Dict[str, Any]:
    """
    处理帮助中心命令
    
    Args:
        command_text: 命令文本（已去掉"Luna"前缀）
    
    Returns:
        Dict: 帮助中心响应
        
    注意：
    - 不修改任何任务状态
    - 当前版本只返回 Stub 响应
    """
    return {
        "type": "HELP_CENTER_STUB",
        "message": "帮助中心将在后续版本开放。",
        "command_text": command_text
    }

