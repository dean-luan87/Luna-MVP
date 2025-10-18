#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna-2 完整语音导航演示
"""

import asyncio
import pyttsx3
from navigation.route_planner import RoutePlanner, TransportMode

class VoiceNavigationDemo:
    """语音导航演示类"""
    
    def __init__(self):
        self.engine = None
        self.route_planner = None
        self._init_voice_engine()
        self._init_route_planner()
    
    def _init_voice_engine(self):
        """初始化语音引擎"""
        try:
            self.engine = pyttsx3.init()
            
            # 查找中文女声
            voices = self.engine.getProperty('voices')
            chinese_voice = None
            
            # 优先选择中文女声
            for voice in voices:
                if 'Chinese' in voice.name and 'China' in voice.name and 'Flo' in voice.name:
                    chinese_voice = voice
                    break
            
            # 如果没有找到女声，使用其他中文语音
            if not chinese_voice:
                for voice in voices:
                    if 'Chinese' in voice.name and 'China' in voice.name:
                        chinese_voice = voice
                        break
            
            if chinese_voice:
                self.engine.setProperty('voice', chinese_voice.id)
                gender = "女声" if "Flo" in chinese_voice.name else "男声"
                print(f"🎯 使用语音: {chinese_voice.name} ({gender})")
            
            # 设置参数
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 0.8)
            
            print("✅ 语音引擎初始化成功")
        except Exception as e:
            print(f"❌ 语音引擎初始化失败: {e}")
    
    def _init_route_planner(self):
        """初始化路径规划器"""
        try:
            # 使用配置的 API 密钥
            from navigation_config import get_ors_api_key
            api_key = get_ors_api_key()
            self.route_planner = RoutePlanner("openrouteservice", api_key)
            print("✅ 路径规划器初始化成功")
        except Exception as e:
            print(f"❌ 路径规划器初始化失败: {e}")
    
    def speak(self, text):
        """语音播报"""
        if self.engine:
            print(f"🔊 播报: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
            print("✅ 播报完成")
    
    async def demo_navigation(self):
        """演示语音导航"""
        print("🎯 Luna-2 语音导航演示")
        print("=" * 40)
        
        # 欢迎语音
        self.speak("你好，我是 Luna 语音助手")
        await asyncio.sleep(1)
        
        # 演示路线
        start = (121.4737, 31.2304)  # 上海市中心
        end = (121.4997, 31.2397)    # 外滩
        
        print(f"📍 起点: 上海市中心")
        print(f"📍 终点: 外滩")
        print(f"🚶 交通方式: 步行")
        
        self.speak("开始规划路线，从上海市中心到外滩")
        await asyncio.sleep(1)
        
        # 规划路径
        route = self.route_planner.plan_route(start, end, TransportMode.WALKING)
        
        if route:
            distance = route['distance']
            duration = route['duration']
            steps = route.get('steps', [])
            
            print(f"✅ 路径规划成功: {distance:.1f}km, {duration:.1f}min")
            
            # 播报路线信息
            self.speak(f"路线规划完成，总距离{distance:.1f}公里，预计用时{duration:.1f}分钟")
            await asyncio.sleep(1)
            
            # 播报前3步导航
            self.speak("开始语音导航")
            await asyncio.sleep(3)  # 增加等待时间
            
            for i, step in enumerate(steps[:3], 1):
                if self.route_planner.service == 'openrouteservice':
                    instruction = step['instruction']
                    distance = step['distance'] / 1000 if step['distance'] > 1000 else step['distance']
                    unit = "公里" if step['distance'] > 1000 else "米"
                else:
                    instruction = f"第{i}步"
                    distance = 0
                    unit = "米"
                
                # 简化播报内容
                if "Head northeast" in instruction:
                    instruction = "向东北方向前进"
                elif "Keep left" in instruction:
                    instruction = "保持左侧"
                elif "Turn slight right" in instruction:
                    instruction = "向右转"
                elif "Turn right" in instruction:
                    instruction = "右转"
                elif "Turn left" in instruction:
                    instruction = "左转"
                elif "Continue straight" in instruction:
                    instruction = "直行"
                
                step_text = f"第{i}步，{instruction}，距离{distance:.0f}{unit}"
                self.speak(step_text)
                await asyncio.sleep(4)  # 增加等待时间，确保语音播放完成
            
            self.speak("语音导航演示完成")
            print("🎉 语音导航演示完成！")
            
        else:
            self.speak("路径规划失败")
            print("❌ 路径规划失败")

async def main():
    demo = VoiceNavigationDemo()
    await demo.demo_navigation()

if __name__ == "__main__":
    asyncio.run(main())
