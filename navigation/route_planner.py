#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
路径规划模块
支持多种地图服务的路径规划
"""

import logging
from typing import Tuple, List, Dict, Any, Optional
from enum import Enum

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TransportMode(Enum):
    """交通方式枚举"""
    WALKING = "foot-walking"
    DRIVING = "driving-car"
    CYCLING = "cycling-regular"
    PUBLIC_TRANSPORT = "public-transport"

class RoutePlanner:
    """路径规划器类"""
    
    def __init__(self, service: str = "openrouteservice", api_key: str = None):
        """
        初始化路径规划器
        
        Args:
            service: 地图服务 ("openrouteservice", "google", "baidu")
            api_key: API 密钥
        """
        self.service = service
        self.api_key = api_key
        self.client = None
        
        # 初始化客户端
        self._init_client()
    
    def _init_client(self):
        """初始化地图服务客户端"""
        try:
            if self.service == "openrouteservice":
                self._init_openrouteservice()
            elif self.service == "google":
                self._init_google_maps()
            elif self.service == "baidu":
                self._init_baidu_maps()
            else:
                logger.warning(f"⚠️ 不支持的地图服务: {self.service}")
        except Exception as e:
            logger.error(f"❌ 初始化地图服务客户端失败: {e}")
    
    def _init_openrouteservice(self):
        """初始化 OpenRouteService 客户端"""
        try:
            import openrouteservice
            if self.api_key and self.api_key != "你的_API_KEY":
                self.client = openrouteservice.Client(key=self.api_key)
                logger.info("✅ OpenRouteService 客户端初始化成功")
            else:
                logger.warning("⚠️ 请设置有效的 OpenRouteService API 密钥")
                logger.info("💡 注册地址: https://openrouteservice.org/")
        except ImportError:
            logger.error("❌ openrouteservice 未安装，请运行: pip install openrouteservice")
    
    def _init_google_maps(self):
        """初始化 Google Maps 客户端"""
        try:
            import googlemaps
            if self.api_key:
                self.client = googlemaps.Client(key=self.api_key)
                logger.info("✅ Google Maps 客户端初始化成功")
            else:
                logger.warning("⚠️ 请设置有效的 Google Maps API 密钥")
        except ImportError:
            logger.error("❌ googlemaps 未安装，请运行: pip install googlemaps")
    
    def _init_baidu_maps(self):
        """初始化百度地图客户端"""
        try:
            # 百度地图 API 通常使用 HTTP 请求
            logger.info("✅ 百度地图客户端初始化成功")
        except Exception as e:
            logger.error(f"❌ 百度地图客户端初始化失败: {e}")
    
    def plan_route(self, start: Tuple[float, float], end: Tuple[float, float], 
                   mode: TransportMode = TransportMode.WALKING) -> Optional[Dict[str, Any]]:
        """
        规划路径
        
        Args:
            start: 起点坐标 (经度, 纬度)
            end: 终点坐标 (经度, 纬度)
            mode: 交通方式
            
        Returns:
            路径信息字典
        """
        if not self.client:
            logger.error("❌ 地图服务客户端未初始化")
            return None
        
        try:
            logger.info(f"🗺️ 规划路径: {start} -> {end} ({mode.value})")
            
            if self.service == "openrouteservice":
                return self._plan_route_openrouteservice(start, end, mode)
            elif self.service == "google":
                return self._plan_route_google(start, end, mode)
            elif self.service == "baidu":
                return self._plan_route_baidu(start, end, mode)
            else:
                logger.error(f"❌ 不支持的地图服务: {self.service}")
                return None
                
        except Exception as e:
            logger.error(f"❌ 路径规划失败: {e}")
            return None
    
    def _plan_route_openrouteservice(self, start: Tuple[float, float], end: Tuple[float, float], 
                                   mode: TransportMode) -> Optional[Dict[str, Any]]:
        """使用 OpenRouteService 规划路径"""
        try:
            route = self.client.directions(
                coordinates=[start, end],
                profile=mode.value,
                format='geojson',
                instructions=True,
            )
            
            # 提取路径信息
            feature = route['features'][0]
            properties = feature['properties']
            segments = properties['segments'][0]
            
            route_info = {
                'distance': segments['distance'] / 1000,  # 公里
                'duration': segments['duration'] / 60,    # 分钟
                'steps': segments['steps'],
                'geometry': feature['geometry'],
                'service': 'openrouteservice'
            }
            
            logger.info(f"✅ 路径规划成功: {route_info['distance']:.1f}km, {route_info['duration']:.1f}min")
            return route_info
            
        except Exception as e:
            logger.error(f"❌ OpenRouteService 路径规划失败: {e}")
            return None
    
    def _plan_route_google(self, start: Tuple[float, float], end: Tuple[float, float], 
                         mode: TransportMode) -> Optional[Dict[str, Any]]:
        """使用 Google Maps 规划路径"""
        try:
            # Google Maps API 调用
            directions = self.client.directions(
                origin=start,
                destination=end,
                mode=mode.value.replace('-', '_'),
                units='metric'
            )
            
            # 解析 Google Maps 响应
            route = directions[0]
            leg = route['legs'][0]
            
            route_info = {
                'distance': leg['distance']['value'] / 1000,  # 公里
                'duration': leg['duration']['value'] / 60,    # 分钟
                'steps': leg['steps'],
                'service': 'google'
            }
            
            logger.info(f"✅ 路径规划成功: {route_info['distance']:.1f}km, {route_info['duration']:.1f}min")
            return route_info
            
        except Exception as e:
            logger.error(f"❌ Google Maps 路径规划失败: {e}")
            return None
    
    def _plan_route_baidu(self, start: Tuple[float, float], end: Tuple[float, float], 
                        mode: TransportMode) -> Optional[Dict[str, Any]]:
        """使用百度地图规划路径"""
        # 百度地图 API 实现
        logger.warning("⚠️ 百度地图 API 暂未实现")
        return None
    
    def get_directions_text(self, route_info: Dict[str, Any]) -> str:
        """
        将路径信息转换为文本导航说明
        
        Args:
            route_info: 路径信息字典
            
        Returns:
            文本导航说明
        """
        if not route_info:
            return "❌ 无法获取路径信息"
        
        try:
            text_directions = []
            
            # 添加总体信息
            text_directions.append(f"路线总长度: {route_info['distance']:.1f}公里")
            text_directions.append(f"预计用时: {route_info['duration']:.1f}分钟")
            text_directions.append("")
            
            # 添加详细步骤
            steps = route_info.get('steps', [])
            for i, step in enumerate(steps, 1):
                if route_info['service'] == 'openrouteservice':
                    instruction = step['instruction']
                    distance = step['distance'] / 1000 if step['distance'] > 1000 else step['distance']
                    unit = "公里" if step['distance'] > 1000 else "米"
                elif route_info['service'] == 'google':
                    instruction = step['html_instructions'].replace('<b>', '').replace('</b>', '')
                    distance = step['distance']['value'] / 1000 if step['distance']['value'] > 1000 else step['distance']['value']
                    unit = "公里" if step['distance']['value'] > 1000 else "米"
                else:
                    continue
                
                text_directions.append(f"{i}. {instruction} ({distance:.0f}{unit})")
            
            return "\n".join(text_directions)
            
        except Exception as e:
            logger.error(f"❌ 生成导航文本失败: {e}")
            return "❌ 生成导航文本失败"
    
    def get_route_summary(self, route_info: Dict[str, Any]) -> str:
        """
        获取路径摘要信息
        
        Args:
            route_info: 路径信息字典
            
        Returns:
            路径摘要文本
        """
        if not route_info:
            return "❌ 无法获取路径信息"
        
        distance = route_info.get('distance', 0)
        duration = route_info.get('duration', 0)
        steps_count = len(route_info.get('steps', []))
        
        return f"距离: {distance:.1f}公里, 用时: {duration:.1f}分钟, 共{steps_count}个步骤"


# 便捷函数
def create_route_planner(service: str = "openrouteservice", api_key: str = None) -> RoutePlanner:
    """创建路径规划器实例"""
    return RoutePlanner(service, api_key)


if __name__ == "__main__":
    # 测试代码
    def test_route_planner():
        try:
            planner = RoutePlanner()
            start = (121.4737, 31.2304)  # 上海市中心
            end = (121.4997, 31.2397)    # 外滩
            
            route = planner.plan_route(start, end, TransportMode.WALKING)
            if route:
                print("✅ 路径规划测试成功")
                print(planner.get_route_summary(route))
            else:
                print("❌ 路径规划测试失败")
        except Exception as e:
            print(f"❌ 路径规划测试异常: {e}")
    
    test_route_planner()
