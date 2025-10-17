"""
通义千问 在线模式（qwen_online.py）
--------------------------------
功能：
1. 调用阿里云 DashScope API；
2. 输入一句文本，返回智能回复；
3. 可在 main.py 或 HybridEngine 中直接调用。
"""

import os
import requests

class QwenOnline:
    def __init__(self, api_key=None, model="qwen-plus"):
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self.model = model
        self.api_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

    def get_reply(self, text: str) -> str:
        if not self.api_key:
            return "⚠️ 未检测到 DashScope API Key，请设置环境变量 DASHSCOPE_API_KEY。"
        try:
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            payload = {
                "model": self.model,
                "input": {"messages": [{"role": "user", "content": text}]}
            }
            response = requests.post(self.api_url, headers=headers, json=payload)
            data = response.json()
            if "output" in data and "text" in data["output"]:
                return data["output"]["text"]
            elif "output" in data and "choices" in data["output"]:
                return data["output"]["choices"][0]["message"]["content"]
            else:
                return f"⚠️ 无法解析返回结果：{data}"
        except Exception as e:
            return f"❌ 请求失败：{e}"

if __name__ == "__main__":
    bot = QwenOnline()
    print("🌐 Qwen 在线模式启动（通义千问）")
    while True:
        user_input = input("🎤 你说：")
        if user_input.lower() in ["exit", "quit", "再见"]:
            print("👋 再见～")
            break
        print("🤖 Luna：", bot.get_reply(user_input))
