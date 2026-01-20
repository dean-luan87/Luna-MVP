"""
CommandPrefixDetector - 命令前缀检测器

判断一条文本是否为 Luna 命令，并提取命令主体
"""

import re
from .envelope import CommandEnvelope


def detect_prefix(text: str) -> CommandEnvelope:
    """
    检测文本是否为 Luna 命令，并提取命令主体
    
    Args:
        text: 原始文本（由上层语音识别转为文本后传入）
    
    Returns:
        CommandEnvelope: 命令信封，包含检测结果
    
    规则：
    - 支持以下前缀形式：
      - "Luna，"
      - "Luna,"
      - "Luna 请" / "Luna请"
      - "Luna 帮我" 等变体
    - 去掉前缀后，剩余部分作为 command_text
    - 若整条语句只有 "Luna" 或 "Luna…" 没有实际命令内容，
      仍视为 is_command = True，但 command_text 为空
    """
    if not text or not isinstance(text, str):
        return CommandEnvelope(
            is_command=False,
            raw_text=text or "",
            command_text=None,
            mode="UNKNOWN"
        )
    
    # 去除首尾空格
    text = text.strip()
    
    # 检查是否为帮助中心模式
    if _is_help_center_command(text):
        # 提取帮助中心相关文本
        help_text = _extract_help_text(text)
        return CommandEnvelope(
            is_command=True,
            raw_text=text,
            command_text=help_text,
            mode="HELP_CENTER"
        )
    
    # 定义命令前缀模式（支持中英文标点）
    patterns = [
        r"^Luna[，,]\s*(.+)$",           # "Luna，" 或 "Luna,"
        r"^Luna\s+请\s*(.+)$",           # "Luna 请"
        r"^Luna请\s*(.+)$",              # "Luna请"（无空格）
        r"^Luna\s+帮我\s*(.+)$",          # "Luna 帮我"
        r"^Luna帮我\s*(.+)$",            # "Luna帮我"（无空格）
        r"^Luna\s+(.+)$",                # "Luna XXX"（通用模式）
    ]
    
    # 尝试匹配命令前缀
    for pattern in patterns:
        match = re.match(pattern, text, re.IGNORECASE)
        if match:
            command_text = match.group(1).strip() if match.lastindex else ""
            return CommandEnvelope(
                is_command=True,
                raw_text=text,
                command_text=command_text if command_text else None,
                mode="TASK"
            )
    
    # 检查是否只有 "Luna"（无后续内容）
    if re.match(r"^Luna[，,。.]?$", text, re.IGNORECASE):
        return CommandEnvelope(
            is_command=True,
            raw_text=text,
            command_text=None,  # 无实际命令内容
            mode="TASK"
        )
    
    # 不是命令
    return CommandEnvelope(
        is_command=False,
        raw_text=text,
        command_text=None,
        mode="UNKNOWN"
    )


def _is_help_center_command(text: str) -> bool:
    """
    判断是否为帮助中心命令
    
    Args:
        text: 文本
    
    Returns:
        bool: 是否为帮助中心命令
    """
    help_keywords = ["帮助中心", "帮助", "help", "求助", "使用说明"]
    text_lower = text.lower()
    for keyword in help_keywords:
        if keyword in text_lower:
            return True
    return False


def _extract_help_text(text: str) -> str:
    """
    提取帮助中心相关文本
    
    Args:
        text: 原始文本
    
    Returns:
        str: 提取的帮助文本
    """
    # 简单提取：去掉 "Luna" 前缀，保留后续内容
    patterns = [
        r"^Luna[，,]\s*(.+)$",
        r"^Luna\s+(.+)$",
    ]
    
    for pattern in patterns:
        match = re.match(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return text.strip()












