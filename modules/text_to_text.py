"""
文本理解模块（text_to_text.py）
--------------------------------
功能：
1. 接收语音识别结果文本；
2. 基于关键词和上下文进行简单逻辑回复（离线模式）；
3. 未来可切换为调用大模型API的在线模式。
"""

import random

class TextResponder:
    def __init__(self):
        # 可扩展的关键词库
        self.reply_map = {
            "你好": ["你好呀～", "嗨，我在这儿呢。", "哈喽！很高兴听到你的声音。"],
            "天气": ["今天天气不错，适合出去走走。", "看起来外面有点阴，记得带伞。"],
            "你是谁": ["我是 Luna，一个正在成长的AI。", "我是你的语音助手 Luna。"],
            "再见": ["再见啦～", "下次再聊。", "期待我们的下一次对话。"]
        }

    def get_reply(self, text: str) -> str:
        """根据输入文本生成回复"""
        if not text.strip():
            return "我没听清楚，可以再说一遍吗？"

        # 遍历关键词
        for key, replies in self.reply_map.items():
            if key in text:
                return random.choice(replies)
        
        # 默认回复
        return random.choice([
            "我明白了～", 
            "这听起来挺有意思的。",
            "你想聊点别的吗？",
            "我在认真听哦。"
        ])


if __name__ == "__main__":
    bot = TextResponder()
    while True:
        user_input = input("🎤 你说：")
        if user_input.lower() in ["exit", "quit", "再见"]:
            print("👋 再见～")
            break
        print("🤖 Luna：", bot.get_reply(user_input))
