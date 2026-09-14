#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户习惯分析引擎
记录用户行走习惯，分析用户行为模式，优化任务执行策略
"""

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class WalkingSession:
    """行走会话记录"""
    session_id: str
    timestamp: str
    start_location: Dict[str, Any]  # 起始位置
    end_location: Dict[str, Any]  # 结束位置
    route: List[Dict[str, Any]]  # 路径点
    duration: float  # 持续时间（秒）
    distance: float  # 距离（米）
    average_speed: float  # 平均速度（米/秒）
    weather: Optional[str] = None  # 天气
    time_of_day: Optional[str] = None  # 时间段：morning, afternoon, evening, night
    day_of_week: Optional[str] = None  # 星期几
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'WalkingSession':
        """从字典创建"""
        return cls(**data)


@dataclass
class UserHabitProfile:
    """用户习惯画像"""
    user_id: str
    total_sessions: int
    total_distance: float
    total_duration: float
    average_speed: float
    
    # 时间段偏好
    time_preferences: Dict[str, int]  # {time_of_day: count}
    
    # 星期偏好
    day_preferences: Dict[str, int]  # {day_of_week: count}
    
    # 常用路线
    frequent_routes: List[Dict[str, Any]]  # [{start, end, count}, ...]
    
    # 速度模式
    speed_patterns: Dict[str, float]  # {time_of_day: average_speed}
    
    # 路线偏好
    route_preferences: Dict[str, Any]  # 路线偏好分析
    
    # 更新时间
    last_updated: str
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'UserHabitProfile':
        """从字典创建"""
        return cls(**data)


class UserHabitAnalyzer:
    """用户习惯分析引擎"""
    
    def __init__(self, data_dir: Optional[Path] = None):
        """
        初始化用户习惯分析引擎
        
        Args:
            data_dir: 数据存储目录，默认为 ./data/user_habits
        """
        if data_dir is None:
            data_dir = Path(__file__).parent.parent.parent / "data" / "user_habits"
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.sessions_file = self.data_dir / "walking_sessions.json"
        self.profiles_file = self.data_dir / "user_profiles.json"
        
        # 内存缓存
        self._sessions: Dict[str, List[WalkingSession]] = defaultdict(list)
        self._profiles: Dict[str, UserHabitProfile] = {}
        
        # 加载数据
        self._load_data()
    
    def _load_data(self):
        """加载历史数据"""
        try:
            # 加载会话记录
            if self.sessions_file.exists():
                with open(self.sessions_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for user_id, sessions in data.items():
                        self._sessions[user_id] = [
                            WalkingSession.from_dict(s) for s in sessions
                        ]
                logger.info(f"已加载 {sum(len(s) for s in self._sessions.values())} 条会话记录")
            
            # 加载用户画像
            if self.profiles_file.exists():
                with open(self.profiles_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._profiles = {
                        user_id: UserHabitProfile.from_dict(p)
                        for user_id, p in data.items()
                    }
                logger.info(f"已加载 {len(self._profiles)} 个用户画像")
        except Exception as e:
            logger.error(f"加载数据失败: {e}")
    
    def _save_data(self):
        """保存数据到文件"""
        try:
            # 保存会话记录
            sessions_data = {
                user_id: [s.to_dict() for s in sessions]
                for user_id, sessions in self._sessions.items()
            }
            with open(self.sessions_file, 'w', encoding='utf-8') as f:
                json.dump(sessions_data, f, ensure_ascii=False, indent=2)
            
            # 保存用户画像
            profiles_data = {
                user_id: profile.to_dict()
                for user_id, profile in self._profiles.items()
            }
            with open(self.profiles_file, 'w', encoding='utf-8') as f:
                json.dump(profiles_data, f, ensure_ascii=False, indent=2)
            
            logger.debug("数据保存成功")
        except Exception as e:
            logger.error(f"保存数据失败: {e}")
    
    def record_walking_session(
        self,
        user_id: str,
        start_location: Dict[str, Any],
        end_location: Dict[str, Any],
        route: List[Dict[str, Any]],
        duration: float,
        distance: float,
        weather: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        记录行走会话
        
        Args:
            user_id: 用户ID
            start_location: 起始位置
            end_location: 结束位置
            route: 路径点列表
            duration: 持续时间（秒）
            distance: 距离（米）
            weather: 天气
            **kwargs: 其他参数
            
        Returns:
            会话ID
        """
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_id}"
        
        # 计算平均速度
        average_speed = distance / duration if duration > 0 else 0
        
        # 获取时间段
        now = datetime.now()
        hour = now.hour
        if 6 <= hour < 12:
            time_of_day = "morning"
        elif 12 <= hour < 18:
            time_of_day = "afternoon"
        elif 18 <= hour < 22:
            time_of_day = "evening"
        else:
            time_of_day = "night"
        
        # 获取星期几
        day_of_week = now.strftime("%A").lower()
        
        session = WalkingSession(
            session_id=session_id,
            timestamp=now.isoformat(),
            start_location=start_location,
            end_location=end_location,
            route=route,
            duration=duration,
            distance=distance,
            average_speed=average_speed,
            weather=weather,
            time_of_day=time_of_day,
            day_of_week=day_of_week,
            **kwargs
        )
        
        # 添加到内存
        self._sessions[user_id].append(session)
        
        # 更新用户画像
        self._update_user_profile(user_id)
        
        # 保存数据
        self._save_data()
        
        logger.info(f"已记录会话 {session_id} for user {user_id}")
        return session_id
    
    def _update_user_profile(self, user_id: str):
        """更新用户画像"""
        sessions = self._sessions[user_id]
        if not sessions:
            return
        
        # 基础统计
        total_sessions = len(sessions)
        total_distance = sum(s.distance for s in sessions)
        total_duration = sum(s.duration for s in sessions)
        average_speed = total_distance / total_duration if total_duration > 0 else 0
        
        # 时间段偏好
        time_preferences = defaultdict(int)
        for s in sessions:
            if s.time_of_day:
                time_preferences[s.time_of_day] += 1
        
        # 星期偏好
        day_preferences = defaultdict(int)
        for s in sessions:
            if s.day_of_week:
                day_preferences[s.day_of_week] += 1
        
        # 常用路线
        route_counts = defaultdict(int)
        for s in sessions:
            route_key = f"{s.start_location.get('name', '')}->{s.end_location.get('name', '')}"
            route_counts[route_key] += 1
        
        frequent_routes = [
            {
                "start": s.start_location,
                "end": s.end_location,
                "count": count
            }
            for (route_key, count), s in zip(
                sorted(route_counts.items(), key=lambda x: x[1], reverse=True)[:10],
                sessions[:10]
            )
        ]
        
        # 速度模式
        speed_patterns = defaultdict(list)
        for s in sessions:
            if s.time_of_day:
                speed_patterns[s.time_of_day].append(s.average_speed)
        
        speed_patterns_avg = {
            time: sum(speeds) / len(speeds) if speeds else 0
            for time, speeds in speed_patterns.items()
        }
        
        # 路线偏好分析
        route_preferences = {
            "favorite_routes": frequent_routes[:5],
            "route_count": len(route_counts),
        }
        
        profile = UserHabitProfile(
            user_id=user_id,
            total_sessions=total_sessions,
            total_distance=total_distance,
            total_duration=total_duration,
            average_speed=average_speed,
            time_preferences=dict(time_preferences),
            day_preferences=dict(day_preferences),
            frequent_routes=frequent_routes,
            speed_patterns=speed_patterns_avg,
            route_preferences=route_preferences,
            last_updated=datetime.now().isoformat()
        )
        
        self._profiles[user_id] = profile
    
    def get_user_profile(self, user_id: str) -> Optional[UserHabitProfile]:
        """
        获取用户画像
        
        Args:
            user_id: 用户ID
            
        Returns:
            用户画像，如果不存在返回None
        """
        return self._profiles.get(user_id)
    
    def get_recent_sessions(
        self,
        user_id: str,
        days: int = 7,
        limit: Optional[int] = None
    ) -> List[WalkingSession]:
        """
        获取最近的会话记录
        
        Args:
            user_id: 用户ID
            days: 最近N天
            limit: 返回数量限制
            
        Returns:
            会话记录列表
        """
        sessions = self._sessions.get(user_id, [])
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent = [
            s for s in sessions
            if datetime.fromisoformat(s.timestamp) >= cutoff_date
        ]
        
        # 按时间倒序排序
        recent.sort(key=lambda s: s.timestamp, reverse=True)
        
        if limit:
            recent = recent[:limit]
        
        return recent
    
    def estimate_walking_time(
        self,
        user_id: str,
        distance: float,
        time_of_day: Optional[str] = None
    ) -> float:
        """
        估算行走时间
        
        Args:
            user_id: 用户ID
            distance: 距离（米）
            time_of_day: 时间段，如果不提供则使用当前时间段
            
        Returns:
            估算时间（秒）
        """
        profile = self.get_user_profile(user_id)
        if not profile:
            # 默认速度 1.2 m/s (约4.3 km/h)
            default_speed = 1.2
            return distance / default_speed
        
        # 如果指定了时间段，使用该时间段的平均速度
        if time_of_day and time_of_day in profile.speed_patterns:
            speed = profile.speed_patterns[time_of_day]
        else:
            speed = profile.average_speed
        
        # 如果速度为0，使用默认速度
        if speed == 0:
            speed = 1.2
        
        return distance / speed
    
    def get_favorite_routes(self, user_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        获取常用路线
        
        Args:
            user_id: 用户ID
            limit: 返回数量
            
        Returns:
            常用路线列表
        """
        profile = self.get_user_profile(user_id)
        if not profile:
            return []
        
        return profile.frequent_routes[:limit]
    
    def get_preferred_time(self, user_id: str) -> Optional[str]:
        """
        获取用户偏好的时间段
        
        Args:
            user_id: 用户ID
            
        Returns:
            最偏好的时间段
        """
        profile = self.get_user_profile(user_id)
        if not profile or not profile.time_preferences:
            return None
        
        return max(profile.time_preferences.items(), key=lambda x: x[1])[0]
    
    def get_statistics(self, user_id: str) -> Dict[str, Any]:
        """
        获取用户统计信息
        
        Args:
            user_id: 用户ID
            
        Returns:
            统计信息字典
        """
        profile = self.get_user_profile(user_id)
        if not profile:
            return {
                "user_id": user_id,
                "total_sessions": 0,
                "message": "用户画像不存在"
            }
        
        sessions = self.get_recent_sessions(user_id, days=30)
        
        return {
            "user_id": user_id,
            "total_sessions": profile.total_sessions,
            "total_distance_km": round(profile.total_distance / 1000, 2),
            "total_duration_hours": round(profile.total_duration / 3600, 2),
            "average_speed_kmh": round(profile.average_speed * 3.6, 2),
            "recent_sessions_30d": len(sessions),
            "preferred_time": self.get_preferred_time(user_id),
            "favorite_routes_count": len(profile.frequent_routes),
            "last_updated": profile.last_updated
        }
    
    def export_data(self, user_id: str, output_file: Path) -> bool:
        """
        导出用户数据
        
        Args:
            user_id: 用户ID
            output_file: 输出文件路径
            
        Returns:
            是否成功
        """
        try:
            profile = self.get_user_profile(user_id)
            sessions = self._sessions.get(user_id, [])
            
            data = {
                "user_id": user_id,
                "profile": profile.to_dict() if profile else None,
                "sessions": [s.to_dict() for s in sessions],
                "export_time": datetime.now().isoformat()
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"已导出用户 {user_id} 的数据到 {output_file}")
            return True
        except Exception as e:
            logger.error(f"导出数据失败: {e}")
            return False

