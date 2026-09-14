#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edge TTS 测试脚本
使用 Microsoft Edge 的免费 TTS 服务
"""

import asyncio
import edge_tts
import os
import ssl
import aiohttp

async def test_edge_tts():
    """测试 Edge TTS 功能"""
    print("🎵 Edge TTS 测试")
    print("=" * 40)
    
    # 测试文本
    text = "你好，我是 Luna，现在使用 Edge TTS 为您发声。"
    voice = "zh-CN-XiaoxiaoNeural"  # 中文女声
    output_file = "edge_tts_output.wav"
    
    print(f"📝 测试文本: {text}")
    print(f"🎤 使用语音: {voice}")
    print(f"📁 输出文件: {output_file}")
    
    try:
        # 创建 SSL 上下文，禁用证书验证
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # 创建 TTS 对象
        communicate = edge_tts.Communicate(text, voice)
        
        # 生成音频文件
        print("🔄 正在生成音频...")
        await communicate.save(output_file)
        
        # 检查文件是否生成成功
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"✅ 音频生成成功！")
            print(f"📊 文件大小: {file_size} bytes")
            print(f"💾 保存路径: {os.path.abspath(output_file)}")
        else:
            print("❌ 音频文件生成失败")
            
    except Exception as e:
        print(f"❌ 生成过程中出错: {e}")

if __name__ == "__main__":
    asyncio.run(test_edge_tts())
