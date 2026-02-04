"""
Calibration Hint Probe (v1.4.8 Step 10)

Hint 探针：桥接器

职责：
- 从 EvidenceAlignmentIndex 读取对齐帧
- 调用 Builder 构建 Hint
- 调用 Store 存储 Hint
- 提供导出接口
"""

from typing import Optional
from navigation.calibration_hint_builder import CalibrationHintBuilder
from navigation.calibration_hint_store import CalibrationHintStore
from navigation.calibration_hint_exporter import CalibrationHintExporter
from navigation.evidence_alignment_index import EvidenceAlignmentIndex


class CalibrationHintProbe:
    """
    校准提示探针：桥接器
    
    功能：
    - 从 EvidenceAlignmentIndex 读取对齐帧
    - 构建 Hint
    - 存储 Hint
    - 提供导出接口
    """
    
    def __init__(
        self,
        alignment_index: Optional[EvidenceAlignmentIndex] = None,
        logger=None,
        enable_hint_generation: bool = True,
        max_hints: int = 100,
        landmark_unstable_window_s: float = 3.0,
        authority_flip_window_s: float = 5.0,
        authority_flip_threshold: int = 3,
        gps_only_zone_duration_s: float = 10.0
    ):
        """
        初始化 Hint 探针
        
        Args:
            alignment_index: 对齐索引（可选）
            logger: 日志记录器（可选）
            enable_hint_generation: 是否启用 Hint 生成（Feature Flag，默认 True）
            max_hints: 最大 Hint 数（默认 100）
            landmark_unstable_window_s: 地标不稳定时间窗（秒，默认 3.0）
            authority_flip_window_s: Authority 切换时间窗（秒，默认 5.0）
            authority_flip_threshold: Authority 切换阈值（次数，默认 3）
            gps_only_zone_duration_s: GPS 专用区域持续时间（秒，默认 10.0）
        """
        self.alignment_index = alignment_index
        self.logger = logger
        self.enable_hint_generation = enable_hint_generation
        
        # 初始化 Builder、Store、Exporter
        self.builder = CalibrationHintBuilder(
            landmark_unstable_window_s=landmark_unstable_window_s,
            authority_flip_window_s=authority_flip_window_s,
            authority_flip_threshold=authority_flip_threshold,
            gps_only_zone_duration_s=gps_only_zone_duration_s
        )
        self.store = CalibrationHintStore(max_hints=max_hints)
        self.exporter = CalibrationHintExporter()
    
    def generate_hints_from_frames(
        self,
        frames: list
    ) -> list:
        """
        从对齐帧列表生成 Hint
        
        Args:
            frames: 对齐帧列表（必须按时间排序）
            
        Returns:
            CalibrationHint 列表
        """
        if not self.enable_hint_generation or not frames:
            return []
        
        # 构建 Hint
        hints = self.builder.build_hints_from_frames(frames)
        
        # 存储 Hint
        for hint in hints:
            self.store.add_hint(hint)
        
        # 日志（极低频）
        if self.logger and hints:
            stats = self.store.get_stats()
            hint_types = ",".join(set(hint.hint_type for hint in hints))
            log_msg = f"[HINT] generated={len(hints)} types={hint_types}"
            if hasattr(self.logger, 'info'):
                self.logger.info("CalibrationHintProbe", "hints_generated", {
                    "count": len(hints),
                    "types": hint_types,
                    "stats": stats
                })
            else:
                self.logger(log_msg)
        
        return hints
    
    def generate_hints_from_index(
        self,
        start_ts: Optional[float] = None,
        end_ts: Optional[float] = None
    ) -> list:
        """
        从 AlignmentIndex 生成 Hint（按时间范围）
        
        Args:
            start_ts: 开始时间戳（可选）
            end_ts: 结束时间戳（可选）
            
        Returns:
            CalibrationHint 列表
        """
        if not self.alignment_index:
            return []
        
        # 获取时间范围内的帧
        if start_ts is not None or end_ts is not None:
            frames = self.alignment_index.get_by_time_range(
                t0=start_ts or 0.0,
                t1=end_ts or float('inf')
            )
        else:
            frames = self.alignment_index.get_all()
        
        # 按时间排序
        frames = sorted(frames, key=lambda f: f.ts)
        
        return self.generate_hints_from_frames(frames)
    
    def export_json(self) -> str:
        """导出为 JSON"""
        hints = self.store.get_all()
        return self.exporter.export_json(hints)
    
    def export_text_timeline(self, base_ts: float = 0.0) -> str:
        """导出为可读文本"""
        hints = self.store.get_all()
        return self.exporter.export_text_timeline(hints, base_ts=base_ts)
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        return self.store.get_stats()






