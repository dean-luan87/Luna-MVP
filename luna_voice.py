import asyncio
import edge_tts
import ssl
import aiohttp

async def main():
    # 旁白文本（可自行修改）
    text = "欢迎来到 Luna 项目。这是一段测试语音。我们正在探索情绪与智能的未来。"
    
    # 语音选择：中文女声（广播风）
    voice = "zh-CN-XiaoyiNeural"
    
    # 输出文件名
    output_file = "luna_voice.mp3"

    print(f"🎵 开始生成语音...")
    print(f"📝 文本: {text}")
    print(f"🎤 语音: {voice}")
    print(f"📁 输出: {output_file}")

    try:
        # 创建 SSL 上下文，禁用证书验证
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # 合成语音并保存
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        print(f"✅ 已生成语音文件：{output_file}")
        
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        print("💡 建议：检查网络连接或稍后重试")

if __name__ == "__main__":
    asyncio.run(main())
