#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Legacy / Reference（原型资产）：

本文件是基于 Vosk 的语音转文本 CLI 原型工具，不属于当前主链正式输入系统。
- 目的：参考/对照/原型验证
- 约束：不接入主链，不扩展为正式输入方案
"""

import os
import sys
import json
import argparse
import wave
from pathlib import Path

try:
    import vosk
    VOSK_AVAILABLE = True
except ImportError:
    VOSK_AVAILABLE = False
    print("❌ Vosk 库未安装")
    print("请安装: pip install vosk")
    sys.exit(1)

class VoiceToText:
    def __init__(self):
        self.model = None
        self.recognizer = None
        
    def find_model(self):
        """自动查找可用的 Vosk 模型"""
        current_dir = Path(__file__).parent.parent
        model_dirs = [
            current_dir / "vosk-model-small-cn-0.22",
            current_dir / "vosk-model-small-en-us-0.15",
            current_dir / "models" / "vosk-model-small-cn-0.22",
            current_dir / "models" / "vosk-model-small-en-us-0.15"
        ]
        
        for model_dir in model_dirs:
            if model_dir.exists() and (model_dir / "am" / "final.mdl").exists():
                print(f"✅ 找到模型: {model_dir}")
                return str(model_dir)
        
        return None
    
    def load_model(self, model_path=None):
        """加载 Vosk 模型"""
        if model_path is None:
            model_path = self.find_model()
            
        if model_path is None:
            print("❌ 未找到 Vosk 模型")
            print("请下载模型并放入以下路径之一：")
            print("  - vosk-model-small-cn-0.22/")
            print("  - vosk-model-small-en-us-0.15/")
            print("  - models/vosk-model-small-cn-0.22/")
            print("  - models/vosk-model-small-en-us-0.15/")
            print("\n模型下载地址：")
            print("  - 中文模型: https://alphacephei.com/vosk/models")
            print("  - 英文模型: https://alphacephei.com/vosk/models")
            return False
            
        try:
            print(f"🔧 正在加载模型: {model_path}")
            self.model = vosk.Model(model_path)
            self.recognizer = vosk.KaldiRecognizer(self.model, 16000)
            print("✅ 模型加载成功")
            return True
        except Exception as e:
            print(f"❌ 模型加载失败: {e}")
            return False
    
    def wav_to_text(self, wav_file_path):
        """将 WAV 文件转换为文本"""
        if not os.path.exists(wav_file_path):
            print(f"❌ 文件不存在: {wav_file_path}")
            return None
            
        if not wav_file_path.lower().endswith('.wav'):
            print("❌ 只支持 WAV 格式文件")
            return None
            
        if self.recognizer is None:
            print("❌ 模型未加载，请先调用 load_model()")
            return None
            
        try:
            print(f"🎵 正在处理文件: {wav_file_path}")
            
            # 检查 WAV 文件格式
            with wave.open(wav_file_path, 'rb') as wf:
                if wf.getnchannels() != 1:
                    print("⚠️  警告: 文件不是单声道，可能影响识别效果")
                if wf.getsampwidth() != 2:
                    print("⚠️  警告: 文件不是16位，可能影响识别效果")
                if wf.getframerate() != 16000:
                    print("⚠️  警告: 文件采样率不是16kHz，可能影响识别效果")
            
            # 读取并处理音频数据
            with wave.open(wav_file_path, 'rb') as wf:
                data = wf.readframes(4000)
                while data:
                    if self.recognizer.AcceptWaveform(data):
                        pass
                    data = wf.readframes(4000)
                
                # 获取最终结果
                result = self.recognizer.FinalResult()
                result_dict = json.loads(result)
                
                if 'text' in result_dict and result_dict['text'].strip():
                    return result_dict['text'].strip()
                else:
                    return "未识别到语音内容"
                    
        except Exception as e:
            print(f"❌ 处理文件时出错: {e}")
            return None

def main():
    """命令行主函数"""
    parser = argparse.ArgumentParser(description='基于 Vosk 的语音转文本工具')
    parser.add_argument('--file', '-f', required=True, help='WAV 文件路径')
    parser.add_argument('--model', '-m', help='指定模型路径（可选）')
    
    args = parser.parse_args()
    
    # 创建语音识别实例
    vtt = VoiceToText()
    
    # 加载模型
    if not vtt.load_model(args.model):
        sys.exit(1)
    
    # 转换语音为文本
    result = vtt.wav_to_text(args.file)
    
    if result is not None:
        print(f"\n📝 识别结果: {result}")
    else:
        print("\n❌ 识别失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
