"""
Luna Badge v1.5 - 语音交互增强：WiFi语音扫描和配网
实现文件：core/voice_wifi_setup.py
"""
import os
import json
from typing import List, Dict, Any, Optional
from core.tts_manager import speak


class VoiceWiFiSetup:
    """
    WiFi语音配网系统
    功能：语音扫描WiFi、语音播报列表、语音输入密码
    """
    
    def __init__(self):
        self.scanned_wifi_list = []
    
    def voice_scan_wifi(self) -> List[Dict[str, Any]]:
        """
        语音触发扫描WiFi
        
        Returns:
            WiFi列表
        """
        speak("正在扫描附近的WiFi网络，请稍候")
        
        # 扫描WiFi（模拟实现，实际应该调用系统WiFi扫描接口）
        wifi_list = self._scan_wifi_networks()
        
        if not wifi_list:
            speak("未找到可用的WiFi网络")
            return []
        
        # 语音播报结果
        count = len(wifi_list)
        speak(f"找到{count}个WiFi网络")
        
        # 语音播报WiFi列表
        for i, wifi in enumerate(wifi_list, 1):
            ssid = wifi['ssid']
            signal = wifi['signal_strength']
            signal_text = self._signal_to_text(signal)
            
            speak(f"第{i}个，{ssid}，信号{signal_text}")
        
        self.scanned_wifi_list = wifi_list
        
        return wifi_list
    
    def voice_select_wifi(self, user_choice: str, user_number: int = None) -> Optional[Dict[str, Any]]:
        """
        通过语音选择WiFi
        
        Args:
            user_choice: 用户选择的WiFi名称或序号
            user_number: 用户说出的数字（如"第一个"）
            
        Returns:
            选中的WiFi信息
        """
        if not self.scanned_wifi_list:
            speak("请先扫描WiFi网络")
            return None
        
        # 如果提供了数字，通过序号选择
        if user_number:
            if 1 <= user_number <= len(self.scanned_wifi_list):
                selected = self.scanned_wifi_list[user_number - 1]
                speak(f"你选择了{selected['ssid']}")
                return selected
            else:
                speak(f"请选择1到{len(self.scanned_wifi_list)}之间的数字")
                return None
        
        # 如果提供了WiFi名称，通过名称匹配（模糊搜索）
        if user_choice:
            matches = self._fuzzy_search_wifi(user_choice)
            
            if not matches:
                speak("未找到该WiFi网络，请重新选择")
                return None
            elif len(matches) == 1:
                # 唯一匹配
                selected = matches[0]
                speak(f"找到了{selected['ssid']}，现在请输入密码")
                return selected
            else:
                # 多个匹配
                speak(f"找到{len(matches)}个相似的WiFi网络")
                for i, wifi in enumerate(matches, 1):
                    signal_text = self._signal_to_text(wifi['signal_strength'])
                    speak(f"第{i}个，{wifi['ssid']}，信号{signal_text}")
                speak("请告诉我选择第几个")
                return None
        
        return None
    
    def _fuzzy_search_wifi(self, keyword: str) -> List[Dict[str, Any]]:
        """
        模糊搜索WiFi
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            匹配的WiFi列表
        """
        matches = []
        keyword_lower = keyword.lower()
        
        for wifi in self.scanned_wifi_list:
            ssid_lower = wifi['ssid'].lower()
            
            # 完全匹配
            if keyword_lower == ssid_lower:
                matches.insert(0, wifi)  # 完全匹配放在最前面
            # 包含匹配
            elif keyword_lower in ssid_lower:
                matches.append(wifi)
            # 相似度匹配（简单的字符相似度）
            elif self._calculate_similarity(keyword_lower, ssid_lower) > 0.5:
                matches.append(wifi)
        
        return matches
    
    def _calculate_similarity(self, s1: str, s2: str) -> float:
        """
        计算字符串相似度（简单的Levenshtein距离）
        
        Args:
            s1, s2: 要比较的字符串
            
        Returns:
            相似度（0-1）
        """
        # 简单的字符匹配率
        if not s1 or not s2:
            return 0.0
        
        # 计算公共字符数
        common_chars = set(s1) & set(s2)
        total_chars = set(s1) | set(s2)
        
        if not total_chars:
            return 0.0
        
        return len(common_chars) / len(total_chars)
    
    def voice_input_wifi_password(self, ssid: str, password_speech: str) -> Dict[str, Any]:
        """
        通过语音输入WiFi密码
        
        Args:
            ssid: WiFi名称
            password_speech: 用户说的密码（可能是中文数字或字母）
            
        Returns:
            连接结果
        """
        # 转换语音输入的密码
        password = self._parse_password_from_speech(password_speech)
        
        if not password:
            speak("密码格式不正确，请重新输入")
            return {
                "success": False,
                "message": "密码格式错误"
            }
        
        # 尝试连接
        speak("正在连接WiFi，请稍候")
        
        success = self._connect_to_wifi(ssid, password)
        
        if success:
            speak(f"连接成功！已连接到{ssid}")
            
            # 保存配置
            self._save_wifi_config(ssid, password)
            
            return {
                "success": True,
                "message": "连接成功",
                "ssid": ssid
            }
        else:
            speak("连接失败，请检查密码是否正确")
            
            return {
                "success": False,
                "message": "连接失败",
                "ssid": ssid
            }
    
    def complete_voice_wifi_setup(self) -> Dict[str, Any]:
        """
        完整的语音WiFi配网流程（多轮交互）
        
        Returns:
            配网结果
        """
        # 1. 扫描WiFi
        speak("让我们开始设置WiFi网络")
        wifi_list = self.voice_scan_wifi()
        
        if not wifi_list:
            return {
                "success": False,
                "message": "未找到WiFi网络"
            }
        
        # 2. 多轮交互选择WiFi
        selected = None
        max_attempts = 3
        attempts = 0
        
        while not selected and attempts < max_attempts:
            if attempts == 0:
                speak("请告诉我你想连接哪一个，可以说第几个或者WiFi名称")
            else:
                speak("请重新选择，可以说第几个或者WiFi名称")
            
            # 等待用户输入（实际应该使用语音识别）
            user_input = input("你的选择: ").strip()
            
            # 解析用户输入
            selected = self._parse_user_selection(user_input)
            attempts += 1
        
        if not selected:
            return {
                "success": False,
                "message": "选择超时或失败"
            }
        
        # 3. 输入密码（多轮确认）
        password = None
        max_password_attempts = 3
        password_attempts = 0
        
        while not password and password_attempts < max_password_attempts:
            if password_attempts == 0:
                speak(f"请告诉我{selected['ssid']}的密码，你可以一个字一个字告诉我")
            else:
                speak("密码输入有误，请重新输入")
            
            # 等待用户输入（实际应该使用语音识别）
            user_input = input("WiFi密码: ").strip()
            
            # 解析密码
            password = self._parse_password_from_speech(user_input)
            password_attempts += 1
        
        if not password:
            return {
                "success": False,
                "message": "密码输入失败"
            }
        
        # 4. 尝试连接
        result = self.voice_input_wifi_password(selected['ssid'], user_input)
        
        return result
    
    def _parse_user_selection(self, user_input: str) -> Optional[Dict[str, Any]]:
        """
        解析用户选择
        
        支持格式:
        - 数字: "1", "第一个", "第一个WiFi"
        - WiFi名称: "Home_WiFi", "我的WiFi"
        
        Args:
            user_input: 用户输入
            
        Returns:
            选中的WiFi信息
        """
        # 尝试解析为数字
        import re
        numbers = re.findall(r'\d+', user_input)
        chinese_numbers = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
        
        # 检查中文数字
        for i, num in enumerate(chinese_numbers, 1):
            if num in user_input:
                return self.scanned_wifi_list[i - 1] if 1 <= i <= len(self.scanned_wifi_list) else None
        
        # 检查阿拉伯数字
        if numbers:
            num = int(numbers[0])
            if 1 <= num <= len(self.scanned_wifi_list):
                return self.scanned_wifi_list[num - 1]
            else:
                speak(f"请选择1到{len(self.scanned_wifi_list)}之间的数字")
                return None
        
        # 尝试按名称匹配
        if user_input:
            matches = self._fuzzy_search_wifi(user_input)
            
            if len(matches) == 1:
                return matches[0]
            elif len(matches) > 1:
                # 多个匹配，重新选择
                return self.voice_select_wifi(user_input)
        
        return None
    
    def _scan_wifi_networks(self) -> List[Dict[str, Any]]:
        """
        扫描WiFi网络（模拟实现）
        
        实际实现应该调用系统WiFi扫描API
        """
        # 模拟WiFi列表
        return [
            {
                "ssid": "Home_WiFi",
                "signal_strength": -45,
                "security": "WPA2"
            },
            {
                "ssid": "Office_Network",
                "signal_strength": -68,
                "security": "WPA2"
            },
            {
                "ssid": "Public_WiFi",
                "signal_strength": -85,
                "security": "Open"
            }
        ]
    
    def _connect_to_wifi(self, ssid: str, password: str) -> bool:
        """
        连接WiFi（模拟实现）
        
        实际实现应该调用系统WiFi连接API
        """
        # TODO: 实现实际WiFi连接
        import time
        time.sleep(1)
        return True
    
    def _save_wifi_config(self, ssid: str, password: str):
        """保存WiFi配置"""
        config_path = "data/wifi_config.json"
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        config = {
            "ssid": ssid,
            "connected_at": __import__('datetime').datetime.now().isoformat()
        }
        
        # 不保存明文密码，保存哈希
        import hashlib
        config['password_hash'] = hashlib.sha256(password.encode()).hexdigest()
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def _signal_to_text(self, signal: int) -> str:
        """将信号强度转换为文字描述"""
        if signal >= -50:
            return "很强"
        elif signal >= -60:
            return "强"
        elif signal >= -70:
            return "中等"
        elif signal >= -80:
            return "弱"
        else:
            return "很弱"
    
    def _parse_password_from_speech(self, speech: str) -> str:
        """
        解析语音输入的密码
        支持格式：
        - 纯数字：123456
        - 中文数字：一二三四五六
        - 字母（需拼读）：A-B-C-D
        """
        # 移除空格和标点
        speech = speech.replace(" ", "").replace("，", "").replace(",", "")
        speech = speech.replace("-", "").replace("_", "")
        
        # 如果是纯数字或中文数字，转换
        result = ""
        
        chinese_numbers = {
            "零": "0", "一": "1", "二": "2", "三": "3", "四": "4",
            "五": "5", "六": "6", "七": "7", "八": "8", "九": "9"
        }
        
        for char in speech:
            if char.isdigit():
                result += char
            elif char in chinese_numbers:
                result += chinese_numbers[char]
            elif char.isalpha():
                result += char
        
        return result
