"""
模块3：产品语音引导系统（Luna播报）
实现文件：core/luna_usage_guide.py
"""
import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from core.tts_manager import speak, TTSStyle


class LunaUsageGuide:
    """
    Luna产品语音引导系统
    功能：支持完整介绍、分步骤讲解、追问式提醒
    支持多种触发方式和动态配置
    """
    
    def __init__(self, config_path="data/usage_guide.json"):
        self.config_path = config_path
        self.ensure_data_dir()
        self.guides = self.load_guides()
    
    def ensure_data_dir(self):
        """确保数据目录存在"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
    
    def load_guides(self) -> Dict[str, List[str]]:
        """加载引导配置"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载引导配置失败: {e}")
        
        # 默认引导内容
        return self.get_default_guides()
    
    def get_default_guides(self) -> Dict[str, List[str]]:
        """获取默认引导内容"""
        return {
            "intro": [
                "你好，我是 Luna，是你的语音视觉导航助手。",
                "我可以为你导航、识别标志、记录提醒，还能帮你找路、找人和找卫生间。",
                "你可以随时问我：Luna，怎么用扫码功能？ 或 Luna，带我一步一步设置Wi-Fi。"
            ],
            "how_to_navigate": [
                "导航功能开启方式：你可以说 'Luna，带我去医院'。",
                "我会帮你规划路线，并用语音一步一步指引你前进。",
                "在导航过程中，我会随时提醒你注意障碍物和方向。"
            ],
            "how_to_remind": [
                "你可以说：Luna，提醒我晚上8点吃药 或 Luna，帮我记住这个电话号码",
                "我会记录并在指定时间提醒你，所有内容都能随时调用或修改。",
                "你也可以问：Luna，我有什么提醒？ 来查看所有待办事项。"
            ],
            "how_to_scan": [
                "扫码功能使用方式：将二维码或标志牌对准摄像头。",
                "我会自动识别并提供相关信息。",
                "比如识别到卫生间标志，我会告诉你位置和方向。"
            ],
            "step_by_step_wifi": [
                "好的，我们来一步一步设置Wi-Fi。",
                "请告诉我你要连接的Wi-Fi名称。",
                "现在请输入密码，你可以一个字一个字告诉我。",
                "连接成功后，我会告诉你网络状态。"
            ],
            "step_by_step_account": [
                "我们来设置你的账号。",
                "你可以选择创建新账号或登录已有账号。",
                "创建新账号：直接说你的昵称。",
                "登录已有账号：请提供你的账号ID或扫码登录。"
            ],
            "help": [
                "我是Luna，一个智能导航助手。",
                "你可以问我：",
                "1. Luna，怎么导航？（如何使用导航功能）",
                "2. Luna，怎么设置提醒？（如何使用提醒功能）",
                "3. Luna，怎么用扫码？（如何使用扫码功能）",
                "4. Luna，教我设置Wi-Fi（Wi-Fi配网教程）",
                "5. Luna，怎么登录账号？（账号设置教程）",
                "还有其他问题吗？随时问我。"
            ]
        }
    
    def luna_usage_guide(self, trigger: str = "intro") -> List[str]:
        """
        模块化 Luna 引导系统
        
        Args:
            trigger: 触发类型，可为 'intro', 'how_to_navigate', 'how_to_remind', 
                    'step_by_step_wifi', 'help' 等
            
        Returns:
            引导文本列表
        """
        guides = self.guides.get(trigger)
        
        if not guides:
            guides = ["对不起，我还没有这部分的说明。你可以问我：Luna，帮助"]
        
        return guides
    
    def speak_guide(self, trigger: str = "intro", use_tts: bool = True):
        """
        播报引导内容
        
        Args:
            trigger: 触发类型
            use_tts: 是否使用TTS语音播报
        """
        guides = self.luna_usage_guide(trigger)
        
        for line in guides:
            print(f"Luna: {line}")
            
            if use_tts:
                # TODO: 接入TTS模块
                self._speak_text(line)
    
    def _speak_text(self, text: str):
        """文本转语音"""
        # 使用TTS管理器播报
        speak(text, style=TTSStyle.CHEERFUL)
    
    def add_custom_guide(self, trigger: str, content: List[str]) -> bool:
        """
        添加自定义引导内容
        
        Args:
            trigger: 触发关键词
            content: 引导内容列表
            
        Returns:
            是否添加成功
        """
        self.guides[trigger] = content
        return self.save_guides()
    
    def save_guides(self) -> bool:
        """保存引导配置到文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.guides, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存引导配置失败: {e}")
            return False
    
    def parse_user_question(self, question: str) -> Optional[str]:
        """
        解析用户提问，返回对应的触发类型
        
        Args:
            question: 用户提问文本
            
        Returns:
            触发类型
        """
        question = question.lower()
        
        # 关键词匹配
        if "怎么" in question or "如何" in question or "help" in question or "帮助" in question:
            if "导航" in question:
                return "how_to_navigate"
            elif "提醒" in question or "记忆" in question:
                return "how_to_remind"
            elif "扫码" in question or "扫描" in question:
                return "how_to_scan"
            elif "wifi" in question or "网络" in question or "配网" in question:
                return "step_by_step_wifi"
            elif "账号" in question or "登录" in question:
                return "step_by_step_account"
            else:
                return "help"
        elif "介绍" in question or "intro" in question:
            return "intro"
        
        return None
    

def run_interactive_guide():
    """运行交互式引导演示"""
    guide = LunaUsageGuide()
    
    print("=" * 60)
    print("Luna 语音引导系统演示")
    print("=" * 60)
    print("\n你可以输入以下命令进行测试：")
    print("  - 'intro' 或 '介绍'")
    print("  - 'how_to_navigate' 或 '怎么导航'")
    print("  - 'how_to_remind' 或 '怎么提醒'")
    print("  - 'help' 或 '帮助'")
    print("  - 'exit' 退出\n")
    
    while True:
        user_input = input("你: ").strip()
        
        if user_input.lower() in ['exit', '退出', 'quit']:
            print("再见！")
            break
        
        if not user_input:
            continue
        
        # 解析用户问题
        trigger = guide.parse_user_question(user_input)
        
        if trigger:
            print("\n" + "-" * 60)
            guide.speak_guide(trigger, use_tts=False)
            print("-" * 60 + "\n")
        else:
            print("未识别的命令，请说 'Luna，帮助'")
