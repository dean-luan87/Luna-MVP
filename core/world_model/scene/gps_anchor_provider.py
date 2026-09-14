# -*- coding: utf-8 -*-
"""
v1.8.5 Phase C 包 B: GPS Anchor Provider（GPS 弱锚点输入通道）

职责：
- 定义最小 provider（一期只提供 anchor，不做融合）
- 后续真实接 GPS 时只需替换实现，不动 registry 逻辑

设计原则：
- GPS 不直接切 Scene，只用来约束 Scene 候选的空间范围（粗滤）
- 在 drift_suspected=True 时触发 relocalizing=True
- relocalizing=True 时：SceneRegistry 冻结 current_scene，不切
"""

from typing import Optional, Tuple


class GPSAnchorProvider:
    """
    GPS 弱锚点提供者（接口预留）
    
    一期实现：返回 None（不做真实 GPS 接入）
    后续实现：替换为真实 GPS 数据源
    """
    
    def get_anchor(self) -> Optional[Tuple[float, float]]:
        """
        获取 GPS 弱锚点
        
        Returns:
            Optional[Tuple[float, float]]: GPS 坐标 (lat, lon)，如果未就绪则返回 None
        """
        # 一期实现：返回 None（不做真实 GPS 接入）
        return None


