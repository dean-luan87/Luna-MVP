"""
World Signature Builder - B2 v0.2 缓存逻辑

Task 1.2: WorldSignatureBuilder

输入：
- ego motion（heading / speed）
- navigation_result（是否有 path）
- modeling_result（objects / regions）

规则（先写死）：
- heading_bucket = int(heading / 30)
- speed_bucket = {0,1,2,3}  # 静止 / 慢 / 中 / 快
- density_bucket = {LOW, MID, HIGH}

⚠️ 不允许使用精确数值
"""

from typing import Optional, Set, Tuple, Any
from .world_signature import WorldSignature


class WorldSignatureBuilder:
    """
    B2 v0.2 缓存逻辑：WorldSignature 构建器
    
    Task 1.2: WorldSignatureBuilder
    
    核心职责：
    - 从真实 pipeline 输入构建 WorldSignature
    - 使用粗粒度分桶（抗抖动、抗噪声）
    """
    
    # 分桶参数（固定，不允许使用精确数值）
    HEADING_BUCKET_SIZE = 30  # 每 30° 一档
    SPEED_BUCKETS = [0.0, 0.5, 1.5, 3.0]  # 静止/慢/中/快（m/s）
    DENSITY_THRESHOLDS = [0, 3, 8]  # 低/中/高的动态目标数量阈值
    
    @staticmethod
    def build(
        world_snapshot: Any,
        navigation_result: Optional[Any] = None,
    ) -> WorldSignature:
        """
        从 WorldSnapshot 构建 WorldSignature
        
        Args:
            world_snapshot: 世界快照
            navigation_result: 导航结果（可选）
        
        Returns:
            WorldSignature: 世界指纹
        """
        # 提取 ego 信息
        ego = world_snapshot.ego if hasattr(world_snapshot, 'ego') else None
        
        # 1. heading_bucket（朝向分桶）
        heading = ego.heading if ego else 0.0
        heading_bucket = int(heading / WorldSignatureBuilder.HEADING_BUCKET_SIZE)
        
        # 2. speed_bucket（速度分桶）
        speed = ego.speed if ego else 0.0
        speed_bucket = 0  # 默认静止
        for i, threshold in enumerate(WorldSignatureBuilder.SPEED_BUCKETS[1:], start=1):
            if speed >= threshold:
                speed_bucket = i
            else:
                break
        
        # 3. has_path（是否存在任务链路径）
        has_path = False
        if navigation_result:
            if hasattr(navigation_result, 'route') and navigation_result.route:
                if hasattr(navigation_result.route, 'points'):
                    has_path = len(navigation_result.route.points) > 0
                elif isinstance(navigation_result.route, (list, tuple)):
                    has_path = len(navigation_result.route) > 0
        
        # 4. region_ids（可见大区域 ID）
        # 简化：暂时从 world_snapshot.extra 或 modeling_result 提取
        # 后续可以从 NavigationExecutor / WorldModel 获取
        region_ids: Set[str] = set()
        if hasattr(world_snapshot, 'extra') and world_snapshot.extra:
            # 从 extra 中提取 region_ids（如果存在）
            if isinstance(world_snapshot.extra, dict):
                regions = world_snapshot.extra.get("regions", [])
                if isinstance(regions, list):
                    for r in regions:
                        if isinstance(r, dict):
                            region_id = r.get("id") or r.get("region_id")
                            if region_id:
                                region_ids.add(str(region_id))
        
        # 排序 region_ids 以确保一致性（转换为元组）
        sorted_region_ids = tuple(sorted(region_ids))
        
        # 5. density_bucket（动态目标密度）
        objects = world_snapshot.objects if hasattr(world_snapshot, 'objects') else []
        object_count = len(objects) if objects else 0
        density_bucket = 0  # 默认低密度
        for i, threshold in enumerate(WorldSignatureBuilder.DENSITY_THRESHOLDS[1:], start=1):
            if object_count >= threshold:
                density_bucket = i
            else:
                break
        
        # 构建 WorldSignature（frozen dataclass）
        return WorldSignature(
            heading_bucket=heading_bucket,
            speed_bucket=speed_bucket,
            density_bucket=density_bucket,
            has_path=has_path,
            region_ids=sorted_region_ids,
        )

