#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音导航模块
集成路径规划和语音播报的完整导航解决方案
"""

import asyncio
import logging
import os
from typing import Tuple, List, Dict, Any, Optional

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 导入相关模块
from .route_planner import RoutePlanner, TransportMode
from voice import Speaker

class VoiceNavigator:
    """语音导航器类"""
    
    def __init__(self, route_service: str = "openrouteservice", api_key: str = None):
        """
        初始化语音导航器
        
        Args:
            route_service: 路径规划服务
            api_key: API 密钥
        """
        self.route_planner = None
        self.speaker = None
        self.current_route = None
        self.current_step = 0
        self.route_service = route_service
        self.api_key = api_key
    
    async def _init_route_planner(self, service: str, api_key: str):
        """初始化路径规划器"""
        try:
            # 如果没有提供 API 密钥，尝试从配置文件获取
            if not api_key or api_key == "你的_ORS_API_KEY":
                from navigation_config import get_ors_api_key
                api_key = get_ors_api_key()
            
            self.route_planner = RoutePlanner(service, api_key)
            logger.info("✅ 路径规划器初始化成功")
        except Exception as e:
            logger.error(f"❌ 路径规划器初始化失败: {e}")
    
    async def _init_speaker(self):
        """初始化语音播报器"""
        try:
            # 强制使用 pyttsx3 引擎，确保本地语音播报
            self.speaker = Speaker(engine_type='pyttsx3')
            logger.info("✅ 语音播报器初始化成功（使用 pyttsx3）")
        except Exception as e:
            logger.error(f"❌ 语音播报器初始化失败: {e}")
    
    async def start_navigation(self, start: Tuple[float, float], end: Tuple[float, float], 
                              mode: TransportMode = TransportMode.WALKING, 
                              voice: str = "zh-CN-XiaoxiaoNeural") -> bool:
        """
        开始语音导航
        
        Args:
            start: 起点坐标
            end: 终点坐标
            mode: 交通方式
            voice: 语音模型
            
        Returns:
            导航是否成功启动
        """
        logger.info("🚀 开始语音导航")
        
        try:
            # 初始化组件（如果尚未初始化）
            if not self.route_planner:
                await self._init_route_planner(self.route_service, self.api_key)
            if not self.speaker:
                await self._init_speaker()
            
            # 规划路径
            self.current_route = self.route_planner.plan_route(start, end, mode)
            if not self.current_route:
                logger.error("❌ 路径规划失败")
                return False
            
            # 播报导航开始
            await self._announce_navigation_start()
            
            # 播报详细路线
            await self._announce_route_details(voice)
            
            self.current_step = 0
            logger.info("✅ 语音导航启动成功")
            return True
            
        except Exception as e:
            logger.error(f"❌ 启动语音导航失败: {e}")
            return False
    
    async def _announce_navigation_start(self):
        """播报导航开始"""
        if not self.current_route:
            return
        
        distance = self.current_route['distance']
        duration = self.current_route['duration']
        steps_count = len(self.current_route.get('steps', []))
        
        announcement = f"导航开始，总距离{distance:.1f}公里，预计用时{duration:.1f}分钟，共{steps_count}个步骤"
        await self.speaker.speak(announcement)
    
    async def _announce_route_details(self, voice: str):
        """播报详细路线"""
        if not self.current_route:
            return
        
        directions_text = self.route_planner.get_directions_text(self.current_route)
        
        # 分段播报
        lines = directions_text.split('\n')
        for line in lines:
            if line.strip() and not line.startswith('❌'):
                await self.speaker.speak(line, voice, block=True)
                await asyncio.sleep(0.3)  # 短暂停顿
    
    async def get_next_instruction(self, voice: str = "zh-CN-XiaoxiaoNeural") -> bool:
        """
        获取下一个导航指令
        
        Args:
            voice: 语音模型
            
        Returns:
            是否有下一个指令
        """
        if not self.current_route or not self.current_route.get('steps'):
            return False
        
        steps = self.current_route['steps']
        if self.current_step >= len(steps):
            await self._announce_navigation_end()
            return False
        
        step = steps[self.current_step]
        
        # 播报当前步骤
        if self.route_planner.service == 'openrouteservice':
            instruction = step['instruction']
            distance = step['distance'] / 1000 if step['distance'] > 1000 else step['distance']
            unit = "公里" if step['distance'] > 1000 else "米"
        elif self.route_planner.service == 'google':
            instruction = step['html_instructions'].replace('<b>', '').replace('</b>', '')
            distance = step['distance']['value'] / 1000 if step['distance']['value'] > 1000 else step['distance']['value']
            unit = "公里" if step['distance']['value'] > 1000 else "米"
        else:
            instruction = f"第{self.current_step + 1}步"
            distance = 0
            unit = "米"
        
        instruction_text = f"第{self.current_step + 1}步: {instruction}"
        if distance > 0:
            instruction_text += f"，距离{distance:.0f}{unit}"
        
        await self.speaker.speak(instruction_text, voice)
        
        self.current_step += 1
        return True
    
    async def _announce_navigation_end(self):
        """播报导航结束"""
        await self.speaker.speak("导航结束，您已到达目的地")
        logger.info("🎉 导航结束")
    
    async def replay_instruction(self, voice: str = "zh-CN-XiaoxiaoNeural"):
        """重复当前指令"""
        if self.current_step > 0:
            self.current_step -= 1
            await self.get_next_instruction(voice)
    
    async def get_route_summary(self, voice: str = "zh-CN-XiaoxiaoNeural"):
        """播报路线摘要"""
        if not self.current_route:
            return
        
        summary = self.route_planner.get_route_summary(self.current_route)
        await self.speaker.speak(f"路线摘要: {summary}", voice)
    
    def save_navigation_to_file(self, filename: str = "navigation.txt"):
        """保存导航信息到文件"""
        if not self.current_route:
            logger.warning("⚠️ 没有当前路线信息")
            return
        
        try:
            directions_text = self.route_planner.get_directions_text(self.current_route)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("🗺️ Luna-2 语音导航路线\n")
                f.write("=" * 50 + "\n\n")
                f.write(directions_text)
                f.write(f"\n\n当前步骤: {self.current_step + 1}/{len(self.current_route.get('steps', []))}")
            
            logger.info(f"💾 导航信息已保存到: {filename}")
        except Exception as e:
            logger.error(f"❌ 保存导航信息失败: {e}")
    
    async def save_navigation_audio(self, filename: str = "navigation.mp3", 
                                   voice: str = "zh-CN-XiaoxiaoNeural"):
        """保存导航语音到音频文件"""
        if not self.current_route:
            logger.warning("⚠️ 没有当前路线信息")
            return False
        
        try:
            directions_text = self.route_planner.get_directions_text(self.current_route)
            
            # 添加导航开始和结束的语音
            full_text = f"导航开始。{directions_text}。导航结束，您已到达目的地。"
            
            if hasattr(self.speaker.tts_engine, 'engine') and self.speaker.tts_engine.engine_type == "edge-tts":
                await self.speaker.tts_engine.synthesize(full_text, voice, filename)
                logger.info(f"🎵 导航语音已保存到: {filename}")
                return True
            else:
                logger.warning("⚠️ 当前引擎不支持保存音频文件")
                return False
        except Exception as e:
            logger.error(f"❌ 保存导航语音失败: {e}")
            return False
    
    def get_navigation_status(self) -> Dict[str, Any]:
        """获取导航状态"""
        if not self.current_route:
            return {"status": "no_route", "message": "没有当前路线"}
        
        total_steps = len(self.current_route.get('steps', []))
        progress = (self.current_step / total_steps * 100) if total_steps > 0 else 0
        
        return {
            "status": "navigating",
            "current_step": self.current_step,
            "total_steps": total_steps,
            "progress": progress,
            "distance": self.current_route.get('distance', 0),
            "duration": self.current_route.get('duration', 0)
        }
    
    def reset_navigation(self):
        """重置导航状态"""
        self.current_route = None
        self.current_step = 0
        logger.info("🔄 导航状态已重置")


# 便捷函数
async def quick_navigate(start: Tuple[float, float], end: Tuple[float, float], 
                        service: str = "openrouteservice", api_key: str = None,
                        mode: TransportMode = TransportMode.WALKING) -> bool:
    """快速语音导航"""
    navigator = VoiceNavigator(service, api_key)
    return await navigator.start_navigation(start, end, mode)


if __name__ == "__main__":
    # 测试代码
    async def test_voice_navigator():
        try:
            navigator = VoiceNavigator()
            start = (121.4737, 31.2304)  # 上海市中心
            end = (121.4997, 31.2397)    # 外滩
            
            success = await navigator.start_navigation(start, end, TransportMode.WALKING)
            if success:
                print("✅ 语音导航测试成功")
                
                # 测试逐步导航
                for i in range(3):  # 测试前3步
                    has_next = await navigator.get_next_instruction()
                    if not has_next:
                        break
                    await asyncio.sleep(1)
                
                # 保存导航信息
                navigator.save_navigation_to_file()
                await navigator.save_navigation_audio()
            else:
                print("❌ 语音导航测试失败")
        except Exception as e:
            print(f"❌ 语音导航测试异常: {e}")
    
    asyncio.run(test_voice_navigator())
