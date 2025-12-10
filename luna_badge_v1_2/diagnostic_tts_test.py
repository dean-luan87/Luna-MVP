import time
import multiprocessing as mp
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="[DIAG] %(asctime)s | %(message)s",
    datefmt="%H:%M:%S"
)

logger = logging.getLogger("DIAG")


# ==============================================================
# 子进程：真正执行 pyttsx3 播报
# ==============================================================

def tts_worker(q: mp.Queue):
    import pyttsx3

    engine = pyttsx3.init(driverName="nsss")
    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)

    # 预热：重要！
    try:
        engine.say(" ")
        engine.runAndWait()
        print("[DIAG-WORKER] 预热完成")
    except Exception as e:
        print("[DIAG-WORKER] 预热失败:", e)

    while True:
        msg = q.get()
        if msg is None:
            print("[DIAG-WORKER] 收到退出指令")
            break

        print(f"[DIAG-WORKER] 开始播放: {msg!r}")
        try:
            engine.say(msg)
            engine.runAndWait()
            print(f"[DIAG-WORKER] 播放完成: {msg!r}")
        except Exception as e:
            print(f"[DIAG-WORKER] 播放出错: {e}")


# ==============================================================
# 主进程：发送语音指令
# ==============================================================

def main():
    q = mp.Queue()
    p = mp.Process(target=tts_worker, args=(q,), daemon=True)
    p.start()

    print("\n=== TTS 诊断脚本已启动 ===")
    print("每次将播放不同的语音内容，用于判断是否重复播报\n")

    samples = [
        "测试一号，Luna 语音诊断。",
        "测试二号，现在检查是否重复播报。",
        "测试三号，如果你听到三次一样的声音，就是 bug。",
        "测试四号，子进程通讯正常的话，会依次播放这些句子。",
    ]

    for i, text in enumerate(samples, start=1):
        logger.info(f"主进程发送语音 #{i}: {text}")
        q.put(text)
        time.sleep(3)  # 等每句话播完

    print("\n=== 即将结束测试 ===\n")
    q.put(None)   # 结束信号
    p.join(timeout=5)

    print("=== 诊断脚本结束 ===")


if __name__ == "__main__":
    main()


