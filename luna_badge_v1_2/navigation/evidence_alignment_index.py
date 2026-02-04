"""
Evidence Alignment Index (v1.4.8 Step 9)

索引层：管理 EvidenceAlignmentFrame 的内存存储

存储策略：
- RingBuffer（FIFO）
- 最大长度：MAX_ALIGNMENT_FRAMES = 300
- 超限自动丢弃最旧数据
"""

from typing import List, Optional
from navigation.evidence_alignment_frame import EvidenceAlignmentFrame


class EvidenceAlignmentIndex:
    """
    证据对齐索引：内存存储管理器
    
    职责：
    - 管理 EvidenceAlignmentFrame 的内存存储
    - 提供基础查询能力
    """
    
    def __init__(self, max_frames: int = 300):
        """
        初始化索引
        
        Args:
            max_frames: 最大帧数（默认 300）
        """
        self.max_frames = max_frames
        self._frames: List[EvidenceAlignmentFrame] = []
    
    def add_frame(self, frame: EvidenceAlignmentFrame) -> None:
        """
        添加帧
        
        如果超过 max_frames，自动丢弃最旧的数据
        
        Args:
            frame: 证据对齐帧
        """
        self._frames.append(frame)
        
        # 如果超过上限，移除最旧的帧
        if len(self._frames) > self.max_frames:
            self._frames.pop(0)
    
    def get_by_time_range(
        self,
        t0: float,
        t1: float
    ) -> List[EvidenceAlignmentFrame]:
        """
        按时间范围查询
        
        Args:
            t0: 开始时间戳
            t1: 结束时间戳
            
        Returns:
            时间范围内的帧列表（拷贝）
        """
        filtered = [
            frame for frame in self._frames
            if t0 <= frame.ts <= t1
        ]
        return filtered.copy()
    
    def get_by_authority(
        self,
        authority: str
    ) -> List[EvidenceAlignmentFrame]:
        """
        按主权查询
        
        Args:
            authority: 主权名称（"VISUAL", "MAP_VISION", "GPS"）
            
        Returns:
            匹配的帧列表（拷贝）
        """
        filtered = [
            frame for frame in self._frames
            if frame.active_authority == authority
        ]
        return filtered.copy()
    
    def get_by_local_map(
        self,
        local_map_id: str
    ) -> List[EvidenceAlignmentFrame]:
        """
        按本地地图 ID 查询
        
        Args:
            local_map_id: 本地地图 ID
            
        Returns:
            匹配的帧列表（拷贝）
        """
        filtered = [
            frame for frame in self._frames
            if frame.local_map_id == local_map_id
        ]
        return filtered.copy()
    
    def get_all(self) -> List[EvidenceAlignmentFrame]:
        """
        获取所有帧
        
        Returns:
            所有帧的列表（拷贝）
        """
        return self._frames.copy()
    
    def size(self) -> int:
        """获取当前帧数"""
        return len(self._frames)
    
    def clear(self) -> None:
        """清空索引"""
        self._frames.clear()
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        if not self._frames:
            return {
                "frame_count": 0,
                "oldest_ts": None,
                "newest_ts": None,
                "duration_s": 0.0,
                "map_count": 0,
                "authority_count": {}
            }
        
        oldest = self._frames[0].ts
        newest = self._frames[-1].ts
        
        # 统计不同 map_id 的数量
        map_ids = set(
            frame.local_map_id
            for frame in self._frames
            if frame.local_map_id
        )
        
        # 统计不同 authority 的数量
        authority_count = {}
        for frame in self._frames:
            auth = frame.active_authority
            authority_count[auth] = authority_count.get(auth, 0) + 1
        
        return {
            "frame_count": len(self._frames),
            "oldest_ts": oldest,
            "newest_ts": newest,
            "duration_s": newest - oldest if newest > oldest else 0.0,
            "map_count": len(map_ids),
            "authority_count": authority_count
        }






