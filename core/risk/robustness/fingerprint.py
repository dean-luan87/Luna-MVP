# -*- coding: utf-8 -*-
"""
v1.8.4: Risk 参数指纹生成器（Fingerprint Generator）

目标：
生成 risk_params_fingerprint，用于标识影响 risk 行为的参数组合。

原则：
- 只包含真正影响行为的参数
- 不包含 debug 开关、日志频率等非行为参数
"""

from __future__ import annotations
from typing import Dict, Any
import json
import hashlib

from core.risk.risk_types import RISK_TYPE_CONFIG


def calculate_risk_params_fingerprint() -> str:
    """
    计算风险参数指纹
    
    包含的参数：
    - delta_warn
    - d0
    - cooldown_s
    - hazard_base
    - proximity 曲线参数（如果有）
    - trend 权重（如果有）
    
    Returns:
        str: SHA256 哈希值（格式：sha256:...）
    """
    # 收集所有影响行为的参数
    params = {}
    
    # 从 RISK_TYPE_CONFIG 收集参数
    for risk_type, config in RISK_TYPE_CONFIG.items():
        params[f"{risk_type}.hazard_base"] = config.get("hazard_base", 0.0)
        params[f"{risk_type}.d0"] = config.get("d0", 0.0)
        params[f"{risk_type}.delta_warn"] = config.get("delta_warn", 0.0)
        params[f"{risk_type}.cooldown_s"] = config.get("cooldown_s", 0.0)
    
    # 排序参数（确保一致性）
    sorted_params = dict(sorted(params.items()))
    
    # 转换为 JSON 字符串
    params_json = json.dumps(sorted_params, sort_keys=True, ensure_ascii=False)
    
    # 计算 SHA256 哈希
    hash_obj = hashlib.sha256(params_json.encode('utf-8'))
    hash_hex = hash_obj.hexdigest()
    
    return f"sha256:{hash_hex}"


def get_build_info() -> Dict[str, str]:
    """
    获取构建信息
    
    Returns:
        Dict[str, str]: 包含 git_commit 和 build_id 的字典
    """
    import subprocess
    import os
    
    # 获取 git commit
    git_commit = "unknown"
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        )
        if result.returncode == 0:
            git_commit = result.stdout.strip()[:7]  # 只取前 7 位
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    
    # 获取 build_id（从环境变量或默认值）
    build_id = os.environ.get("BUILD_ID", "local-dev")
    
    return {
        "git_commit": git_commit,
        "build_id": build_id
    }


