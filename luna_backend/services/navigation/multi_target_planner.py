"""
多目标路径规划器 (MultiTargetPlanner) v1.2.0
支持多目标路径规划（如：先去711再去医院）
"""

from typing import List, Dict, Any, Optional


class MultiTargetPlanner:
    """
    简易多目标规划器：
    输入一组目的地（带类型），输出推荐顺序
    """
    
    def __init__(self, base_planner):
        """
        初始化多目标规划器
        
        Args:
            base_planner: 现有的 path_planner（对接高德/百度/OSM）
        """
        self.base_planner = base_planner
    
    def plan_sequence(self, start: str, targets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        规划多目标路径序列
        
        Args:
            start: 起点
            targets: 目标列表，格式：
                [
                    {"name": "711便利店", "type": "shop", "id": "..."},
                    {"name": "新华医院", "type": "hospital", "id": "..."}
                ]
        
        Returns:
            规划结果字典，包含：
            {
                "ordered": [...],  # 排序后的目标列表
                "total_distance": ...,  # 总距离
                "routes": [route1, route2, ...]  # 各段路线
            }
        """
        if not targets:
            return {"ordered": [], "routes": [], "total_distance": 0}
        
        # 找出主目标（医院/政务），其他按距离排序
        main_target = None
        side_targets = []
        
        for t in targets:
            if t.get("type") in ("hospital", "gov", "office"):
                main_target = t
            else:
                side_targets.append(t)
        
        if not main_target:
            # 没有主目标，就按距离排序（从 start 出发）
            ordered = sorted(
                targets,
                key=lambda t: self._estimate_distance(start, t.get("name", ""))
            )
        else:
            side_targets_sorted = sorted(
                side_targets,
                key=lambda t: self._estimate_distance(start, t.get("name", ""))
            )
            ordered = side_targets_sorted + [main_target]
        
        # 生成具体路线
        routes = []
        total_distance = 0
        cur = start
        
        for t in ordered:
            try:
                if self.base_planner:
                    r = self.base_planner.plan_route(cur, [t.get("name", "")])
                else:
                    # 如果没有base_planner，返回占位路线
                    r = {
                        "origin": cur,
                        "destination": t.get("name", ""),
                        "distance": self._estimate_distance(cur, t.get("name", "")),
                        "duration": 0,
                        "steps": []
                    }
                routes.append(r)
                total_distance += r.get("distance", 0)
                cur = t.get("name", "")
            except Exception as e:
                # 规划失败，跳过该目标
                continue
        
        return {
            "ordered": ordered,
            "routes": routes,
            "total_distance": total_distance
        }
    
    def _estimate_distance(self, start: str, dest: str) -> float:
        """
        简易距离估算，可用一个轻量级 API 调一次，也可以缓存。
        这里先返回一个固定值占位。
        
        Args:
            start: 起点
            dest: 终点
        
        Returns:
            估算距离（米）
        """
        # TODO: 实现真实距离估算
        # 可以调用地图API或使用缓存
        return 1000.0  # 占位值



