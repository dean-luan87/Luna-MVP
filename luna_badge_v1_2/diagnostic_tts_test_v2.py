import time
import multiprocessing as mp
import logging
import sys
import traceback

logging.basicConfig(
    level=logging.INFO,
    format="[DIAG] %(asctime)s | %(message)s",
    datefmt="%H:%M:%S"
)

logger = logging.getLogger("DIAG")


def tts_worker(q: mp.Queue):
    print("[WORKER] 子进程启动")
    try:
        import pyttsx3
        engine = pyttsx3.init(driverName="nsss")
        engine.setProperty("rate", 170)
        engine.setProperty("volume", 1.0)
        print("[WORKER] pyttsx3 初始化完成")
    except Exception as e:
        print("[WORKER] 初始化失败:", e)
        traceback.print_exc()
        return

    # 预热
    try:
        print("[WORKER] 开始预热")
        engine.say("预热完成")
        engine.runAndWait()
        print("[WORKER] 预热 OK")
    except Exception as e:
        print("[WORKER] 预热失败:", e)
        traceback.print_exc()

    while True:
        msg = q.get()
        if msg is None:
            print("[WORKER] 收到退出信号，结束")
            break

        print(f"[WORKER] 即将播放: {msg!r}")

        try:
            engine.say(msg)
            print("[WORKER] 已调用 engine.say()")
            engine.runAndWait()
            print("[WORKER] 播放完成")
        except Exception as e:
            print("[WORKER] 播放失败:", e)
            traceback.print_exc()


def main():
    q = mp.Queue()
    p = mp.Process(target=tts_worker, args=(q,), daemon=True)
    p.start()

    samples = [
        "测试一号 Luna 语音诊断。",
        "测试二号，检查是否播报中断。",
        "测试三号，确认 runAndWait 是否正常执行。",
        "测试四号，如果你能听到这句话，说明问题不在子进程。",
    ]

    time.sleep(1)

    for s in samples:
        logger.info(f"发送语音: {s}")
        q.put(s)
        time.sleep(4)  # 明确给播放时间

    q.put(None)
    p.join()


if __name__ == "__main__":
    main()













