"""
Luna Badge v1.5 - 语音交互增强：验证码语音输入与反馈
实现文件：core/voice_verification_code.py
"""
import os
import json
from typing import Optional, Dict, Any
from core.user_manager import UserManager
from core.tts_manager import speak
from core.whisper_recognizer import get_whisper_recognizer


class VoiceVerificationCodeHandler:
    """
    验证码语音输入与反馈处理
    功能：通过语音输入验证码、发送验证码、播报验证结果
    """
    
    def __init__(self, user_manager: UserManager = None):
        self.user_manager = user_manager or UserManager()
        self.whisper = get_whisper_recognizer(model_name="base")
    
    def voice_send_verification_code(self, phone: str) -> Dict[str, Any]:
        """
        语音触发发送验证码
        
        Args:
            phone: 手机号
            
        Returns:
            发送结果
        """
        # 发送验证码
        success = self.user_manager.send_verification_code(phone)
        
        if success:
            # 语音反馈
            speak("验证码已发送，请告诉我6位数字验证码")
            
            return {
                "success": True,
                "message": "验证码已发送",
                "phone": phone
            }
        else:
            # 语音反馈
            speak("发送验证码失败，可能是因为请求过于频繁，请稍后再试")
            
            return {
                "success": False,
                "message": "发送失败",
                "phone": phone
            }
    
    def voice_input_verification_code(self, phone: str, speech_text: str) -> Dict[str, Any]:
        """
        通过语音输入验证码
        将用户说的中文数字转换为阿拉伯数字
        
        Args:
            phone: 手机号
            speech_text: 语音识别结果，如"一二三四五六"
            
        Returns:
            验证结果
        """
        # 将中文数字转换为阿拉伯数字
        code = self._convert_chinese_numbers_to_digits(speech_text)
        
        if not code or len(code) != 6:
            speak("验证码格式不正确，请输入6位数字")
            return {
                "success": False,
                "message": "格式错误",
                "code": code
            }
        
        # 验证验证码
        success = self.user_manager.verify_code(phone, code)
        
        if success:
            # 验证成功
            speak("验证码正确，登录成功")
            
            return {
                "success": True,
                "message": "验证成功",
                "code": code
            }
        else:
            # 验证失败，计算剩余尝试次数
            remaining = self._get_remaining_attempts(phone)
            
            if remaining > 0:
                speak(f"验证码错误，还有{remaining}次机会，请重新输入")
            else:
                speak("验证码错误次数过多，请重新获取验证码")
            
            return {
                "success": False,
                "message": "验证失败",
                "remaining_attempts": remaining,
                "code": code
            }
    
    def voice_resend_verification_code(self, phone: str) -> Dict[str, Any]:
        """
        语音触发再次发送验证码
        
        Args:
            phone: 手机号
            
        Returns:
            发送结果
        """
        speak("好的，正在重新发送验证码，请稍候")
        
        return self.voice_send_verification_code(phone)
    
    def voice_input_with_recording(self, prompt: str, duration: int = 5) -> str:
        """
        通过录音输入验证码
        
        Args:
            prompt: 提示信息
            duration: 录音时长（秒）
            
        Returns:
            str: 识别的文本
        """
        speak(prompt)
        
        # 录音并识别
        text, details = self.whisper.recognize_from_microphone(duration=duration)
        
        return text
    
    def _convert_chinese_numbers_to_digits(self, text: str) -> str:
        """
        将中文数字转换为阿拉伯数字
        
        支持格式：
        - "一二三四五六" → "123456"
        - "1 2 3 4 5 6" → "123456"
        - "一 二 三 四 五 六" → "123456"
        """
        # 中文数字映射
        chinese_numbers = {
            "零": "0", "一": "1", "二": "2", "三": "3", "四": "4",
            "五": "5", "六": "6", "七": "7", "八": "8", "九": "9"
        }
        
        result = ""
        
        # 处理可能的空格
        text = text.replace(" ", "").replace("，", "").replace(",", "")
        
        for char in text:
            if char.isdigit():
                result += char
            elif char in chinese_numbers:
                result += chinese_numbers[char]
        
        return result
    
    def _get_remaining_attempts(self, phone: str) -> int:
        """获取剩余尝试次数"""
        if phone not in self.user_manager.verification_codes:
            return 0
        
        vc = self.user_manager.verification_codes[phone]
        attempts = vc.get('attempts', 0)
        max_attempts = self.user_manager.max_attempts
        
        return max(0, max_attempts - attempts)


def handle_voice_verification_command(command: str, phone: str, speech_text: str = None) -> Dict[str, Any]:
    """
    处理验证码相关的语音命令
    
    Args:
        command: 语音命令
        phone: 手机号
        speech_text: 语音识别的文本（用于输入验证码）
        
    Returns:
        处理结果
    """
    handler = VoiceVerificationCodeHandler()
    
    if "发送验证码" in command or "重新发送验证码" in command or "再次发送验证码" in command:
        # 再次发送验证码
        return handler.voice_resend_verification_code(phone)
    
    elif "验证码" in command and speech_text:
        # 输入验证码
        return handler.voice_input_verification_code(phone, speech_text)
    
    return {
        "success": False,
        "message": "未识别的命令"
    }
