"""
CommandEnvelope - 命令信封数据结构

用于封装命令检测结果
"""

from pydantic import BaseModel
from typing import Optional, Literal


class CommandEnvelope(BaseModel):
    """
    命令信封，封装命令检测结果
    
    Attributes:
        is_command: 是否为命令
        raw_text: 原始文本
        command_text: 去掉"Luna"后的命令主体（如果 is_command=True）
        mode: 命令模式（TASK / HELP_CENTER / UNKNOWN）
    """
    is_command: bool
    raw_text: str
    command_text: Optional[str] = None  # 去掉"Luna"后的命令主体
    mode: Literal["TASK", "HELP_CENTER", "UNKNOWN"] = "UNKNOWN"












