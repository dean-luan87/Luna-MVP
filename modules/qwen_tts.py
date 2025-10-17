#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通义千问 TTS 模块（qwen_tts.py）
--------------------------------
功能：
1. 使用阿里云 DashScope HTTP TTS 接口
2. 支持文本转语音合成
3. 自动播放生成的音频文件
4. 修复音频数据提取问题
5. 增强音色兼容性和调试输出
"""

import os
import sys
import logging
import subprocess
import base64
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    import dashscope
    from dashscope.audio.qwen_tts import SpeechSynthesizer
    DASHSCOPE_AVAILABLE = True
except ImportError:
    DASHSCOPE_AVAILABLE = False
    logger.error("❌ dashscope 库未安装")
    logger.error("请安装: pip install dashscope")
    sys.exit(1)

class QwenTTS:
    def __init__(self, api_key=None):
        """
        初始化 TTS 模块
        
        Args:
            api_key: DashScope API Key，如果为None则从环境变量读取
        """
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self.model = "qwen-tts"
        
        # DashScope qwen-tts 支持的音色列表
        self.DEFAULT_VOICE = "Serena"
        self.VOICE_LIST = ["Cherry", "Serena", "Ethan", "Chelsie"]
        self.voice_list = self.VOICE_LIST
        self.current_voice_index = 0
        self.voice = self.voice_list[self.current_voice_index]
        
        # 打印使用的音色和模型
        print("🎤 使用音色：", self.voice)
        print("🧩 当前模型：", self.model)
        
        if not self.api_key:
            logger.warning("⚠️ 未检测到 DashScope API Key")
            logger.info("💡 请设置环境变量 DASHSCOPE_API_KEY")
            logger.info("🔗 获取 API Key: https://dashscope.aliyun.com/")
            self.synthesizer = None
            return
            
        # 设置 API Key
        dashscope.api_key = self.api_key
        
        # 初始化语音合成器
        try:
            self.synthesizer = SpeechSynthesizer()
            logger.info(f"✅ TTS 模块初始化成功，模型: {self.model}")
            
            # 执行模型验证
            self._validate_model()
            
        except Exception as e:
            logger.error(f"❌ TTS 模块初始化失败: {e}")
            self.synthesizer = None
    
    def _validate_model(self):
        """
        验证模型可用性
        """
        try:
            logger.info("🔍 正在验证模型可用性...")
            
            # 使用简单的测试文本进行模型验证
            test_response = self.synthesizer.call(
                model=self.model,
                input="测试",
                voice=self.voice,
                format="wav",
                sample_rate=16000,
                result_format="bytes"
            )
            
            # 检查响应状态
            if hasattr(test_response, 'status_code'):
                if test_response.status_code == 200:
                    logger.info("✅ 模型验证成功")
                    return True
                elif test_response.status_code == 400:
                    # 检查是否是模型不存在错误
                    if hasattr(test_response, 'message') and "Model not exist" in str(test_response.message):
                        logger.warning(f"⚠️ 模型 {self.model} 不存在，尝试切换到备用模型")
                        self.model = "qwen-tts-flash"
                        print("⚠️ 模型已自动切换为 qwen-tts-flash")
                        logger.info(f"🔄 已切换到备用模型: {self.model}")
                        return True
                    else:
                        logger.warning(f"⚠️ 模型验证失败，状态码: {test_response.status_code}")
                        return False
                else:
                    logger.warning(f"⚠️ 模型验证返回状态码: {test_response.status_code}")
                    return False
            else:
                logger.warning("⚠️ 模型验证响应格式异常")
                return False
                
        except Exception as e:
            logger.warning(f"⚠️ 模型验证过程中出错: {e}")
            # 如果验证失败，尝试切换到备用模型
            if "Model not exist" in str(e) or "model" in str(e).lower():
                logger.warning(f"⚠️ 检测到模型问题，尝试切换到备用模型")
                self.model = "qwen-tts-flash"
                print("⚠️ 模型已自动切换为 qwen-tts-flash")
                logger.info(f"🔄 已切换到备用模型: {self.model}")
            return False
    
    def _extract_audio_bytes(self, response):
        """
        优化音频数据提取函数，支持多种返回格式
        
        Args:
            response: DashScope API 响应对象
            
        Returns:
            bytes: 音频字节流，失败返回 None
        """
        try:
            logger.info(f"📋 开始提取音频数据，响应类型: {type(response)}")
            
            # 检查响应状态
            if not hasattr(response, 'status_code') or response.status_code != 200:
                logger.error(f"❌ API 响应状态异常: {getattr(response, 'status_code', 'Unknown')}")
                if hasattr(response, 'message'):
                    logger.error(f"错误信息: {response.message}")
                return None
            
            # 方法1: 检查 response.output.audio
            if hasattr(response, 'output') and hasattr(response.output, 'audio'):
                audio_data = response.output.audio
                logger.info(f"📋 从 response.output.audio 提取数据，类型: {type(audio_data)}")
                
                return self._process_audio_data(audio_data, "response.output.audio")
            
            # 方法2: 检查 response.audio
            elif hasattr(response, 'audio'):
                audio_data = response.audio
                logger.info(f"📋 从 response.audio 提取数据，类型: {type(audio_data)}")
                
                return self._process_audio_data(audio_data, "response.audio")
            
            # 方法3: 检查完整响应体
            else:
                logger.error("❌ 返回结构无音频字段")
                logger.error(f"响应对象属性: {[attr for attr in dir(response) if not attr.startswith('_')]}")
                return None
                
        except Exception as e:
            logger.error(f"❌ 音频数据提取过程中出错: {e}")
            logger.exception("详细错误信息:")
            return None
    
    def _process_audio_data(self, audio_data, source):
        """
        处理音频数据，支持 bytes、base64、dict 格式
        
        Args:
            audio_data: 音频数据
            source: 数据来源描述
            
        Returns:
            bytes: 处理后的音频字节流
        """
        try:
            # 如果是 bytes，直接返回
            if isinstance(audio_data, bytes):
                logger.info(f"✅ 从 {source} 获取音频字节流，长度: {len(audio_data)} bytes")
                return audio_data
            
            # 如果是 base64 字符串，解码
            elif isinstance(audio_data, str):
                try:
                    decoded_audio = base64.b64decode(audio_data)
                    logger.info(f"✅ 从 {source} Base64 解码成功，长度: {len(decoded_audio)} bytes")
                    return decoded_audio
                except Exception as e:
                    logger.error(f"❌ 从 {source} Base64 解码失败: {e}")
                    return None
            
            # 如果是字典，尝试提取音频数据
            elif isinstance(audio_data, dict):
                logger.info(f"📋 从 {source} 字典格式提取音频数据")
                logger.info(f"字典键: {list(audio_data.keys())}")
                
                # 尝试不同的键名
                for key in ['audio', 'data', 'content', 'binary', 'sound', 'voice']:
                    if key in audio_data:
                        data = audio_data[key]
                        logger.info(f"尝试从键 '{key}' 提取数据，类型: {type(data)}")
                        
                        if isinstance(data, str):
                            try:
                                decoded_audio = base64.b64decode(data)
                                logger.info(f"✅ 从字典键 '{key}' 解码音频，长度: {len(decoded_audio)} bytes")
                                return decoded_audio
                            except Exception as e:
                                logger.warning(f"⚠️ 键 '{key}' 解码失败: {e}")
                                continue
                        elif isinstance(data, bytes):
                            logger.info(f"✅ 从字典键 '{key}' 获取音频字节流，长度: {len(data)} bytes")
                            return data
                
                logger.error(f"❌ 无法从 {source} 字典中提取音频数据")
                logger.error(f"字典内容: {audio_data}")
                return None
            
            else:
                logger.error(f"❌ 未知的音频数据格式: {type(audio_data)}")
                return None
                
        except Exception as e:
            logger.error(f"❌ 处理 {source} 音频数据时出错: {e}")
            return None
    
    def _try_next_voice(self):
        """
        尝试下一个音色
        
        Returns:
            str: 下一个音色名称，如果已用完返回 None
        """
        self.current_voice_index += 1
        if self.current_voice_index < len(self.voice_list):
            self.voice = self.voice_list[self.current_voice_index]
            logger.info(f"🔄 切换到下一个音色: {self.voice}")
            return self.voice
        else:
            logger.error("❌ 所有音色都已尝试完毕")
            return None
    
    def synthesize_text(self, text, output_path="output.wav"):
        """
        将文本合成为语音文件，支持音色自动切换
        
        Args:
            text: 要合成的文本
            output_path: 保存的语音文件路径
            
        Returns:
            str: 成功返回文件路径，失败返回错误信息
        """
        if not self.api_key:
            return "⚠️ 未检测到 DashScope API Key，请设置环境变量 DASHSCOPE_API_KEY"
            
        # 检查文本输入
        if not text or not text.strip():
            logger.warning("⚠️ 文本输入为空，无法合成")
            return "⚠️ 文本输入为空，无法合成。"
            
        if self.synthesizer is None:
            return "❌ TTS 模块未正确初始化"
        
        # 重置音色索引
        self.current_voice_index = 0
        self.voice = self.voice_list[self.current_voice_index]
        
        while self.voice is not None:
            try:
                logger.info(f"🎤 当前音色: {self.voice}")
                logger.info(f"🧠 模型: {self.model}")
                logger.info(f"📖 输入文本长度: {len(text)}")
                logger.info(f"🎵 正在合成语音: {text[:50]}{'...' if len(text) > 50 else ''}")
                
                # 使用 HTTP 模式进行语音合成，强制使用指定参数
                response = self.synthesizer.call(
                    model=self.model,
                    input=text,
                    voice=self.voice,
                    format="wav",
                    sample_rate=16000,
                    result_format="bytes"
                )
                
                # 提取音频字节流
                audio_bytes = self._extract_audio_bytes(response)
                
                if audio_bytes is None or len(audio_bytes) == 0:
                    logger.warning(f"⚠️ 音色 {self.voice} 未生成有效音频")
                    print(f"⚠️ 音色 {self.voice} 未生成有效音频，尝试下一个。")
                    
                    # 尝试下一个音色
                    next_voice = self._try_next_voice()
                    if next_voice is None:
                        return "❌ 所有音色均无法生成音频，请检查 API 权限或模型开通状态。"
                    continue
                
                # 检查音频大小
                logger.info(f"📦 返回音频大小: {len(audio_bytes)} bytes")
                if len(audio_bytes) < 1000:
                    logger.warning(f"⚠️ 音频过小 ({len(audio_bytes)} bytes)，疑似合成失败")
                    print(f"⚠️ 音色 {self.voice} 未生成有效音频，尝试下一个。")
                    
                    # 尝试下一个音色
                    next_voice = self._try_next_voice()
                    if next_voice is None:
                        return "❌ 所有音色均无法生成音频，请检查 API 权限或模型开通状态。"
                    continue
                
                # 确保输出目录存在
                output_file = Path(output_path)
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                # 保存音频文件
                try:
                    with open(output_file, 'wb') as f:
                        f.write(audio_bytes)
                    
                    logger.info(f"✅ 语音合成成功，已保存到: {output_file.absolute()}")
                    print("✅ 合成成功，文件保存在: output.wav")
                    
                    # 检测文件大小
                    file_size = output_file.stat().st_size
                    if file_size == 0:
                        logger.warning("⚠️ 生成的音频文件大小为 0 bytes")
                        print("⚠️ 未生成有效音频数据，请检查模型或 voice 参数。")
                    else:
                        logger.info(f"📊 音频文件大小: {file_size} bytes")
                    
                    # 自动播放音频
                    self._play_audio(output_file)
                    
                    return str(output_file.absolute())
                    
                except Exception as e:
                    error_msg = f"❌ 文件保存失败: {e}"
                    logger.error(error_msg)
                    return error_msg
                    
            except Exception as e:
                logger.error(f"❌ 音色 {self.voice} 合成过程中出错: {e}")
                print(f"❌ 合成失败，错误详情: {e}")
                
                # 尝试下一个音色
                next_voice = self._try_next_voice()
                if next_voice is None:
                    error_msg = f"❌ 所有音色均无法生成音频，请检查 API 权限或模型开通状态。"
                    logger.error(error_msg)
                    return error_msg
                continue
        
        return "❌ 所有音色均无法生成音频，请检查 API 权限或模型开通状态。"
    
    def _play_audio(self, audio_file):
        """
        播放音频文件（macOS）
        
        Args:
            audio_file: 音频文件路径
        """
        try:
            # 检查是否为 macOS
            if sys.platform == "darwin":
                logger.info("🔊 正在播放音频...")
                subprocess.run(['afplay', str(audio_file)], check=True)
                logger.info("✅ 音频播放完成")
            else:
                logger.info(f"ℹ️  非 macOS 系统，请手动播放: {audio_file}")
        except subprocess.CalledProcessError as e:
            logger.warning(f"⚠️  音频播放失败: {e}")
            print("⚠️ 音频播放失败，请手动播放 output.wav。")
        except Exception as e:
            logger.warning(f"⚠️  播放过程中出错: {e}")
            print("⚠️ 音频播放失败，请手动播放 output.wav。")
    
    def get_status(self):
        """获取 TTS 模块状态"""
        return {
            "api_key_set": bool(self.api_key),
            "model": self.model,
            "voice": self.voice,
            "voice_list": self.voice_list,
            "current_voice_index": self.current_voice_index,
            "synthesizer_ready": self.synthesizer is not None,
            "dashscope_available": DASHSCOPE_AVAILABLE,
            "mode": "HTTP"
        }

def main():
    """命令行测试函数"""
    print("🎵 通义千问 TTS 测试 (HTTP 模式)")
    print("=" * 60)
    
    tts = QwenTTS()
    
    # 显示状态
    status = tts.get_status()
    print(f"📊 TTS 状态: {status}")
    
    if not status["api_key_set"]:
        print("❌ 请先设置 DASHSCOPE_API_KEY 环境变量")
        print("🔗 获取 API Key: https://dashscope.aliyun.com/")
        return
    
    if not status["synthesizer_ready"]:
        print("❌ TTS 模块初始化失败")
        return
    
    # 测试文本
    test_text = "你好，我是 Luna，一个有情绪的AI，现在由通义千问为我发声。"
    output_file = "output.wav"
    
    print(f"\n🧪 测试文本: {test_text}")
    print(f"📁 输出文件: {output_file}")
    
    # 合成语音
    result = tts.synthesize_text(test_text, output_file)
    
    if result.startswith("❌") or result.startswith("⚠️"):
        print(f"❌ 合成失败: {result}")
    else:
        print(f"✅ 合成成功: {result}")

if __name__ == "__main__":
    main()