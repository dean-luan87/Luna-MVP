# camera_loop.py
import cv2

# 创建摄像头对象
cap = cv2.VideoCapture(0)  # 摄像头设备编号为0

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("❌ 错误：无法打开摄像头")
    print("请检查：")
    print("1. 摄像头是否已连接")
    print("2. 摄像头是否被其他程序占用")
    print("3. 摄像头驱动是否正常")
    exit()

print("✅ 摄像头打开成功")
print("📹 实时摄像头画面已启动")
print("💡 按 'q' 键退出程序")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ 错误：无法读取摄像头画面")
            break

        # 显示摄像头画面
        cv2.imshow('🎥 Luna Camera Feed', frame)
        
        # 按 'q' 键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("👋 程序正常退出")
            break

except KeyboardInterrupt:
    print("\n⚠️ 程序被用户中断")
except Exception as e:
    print(f"❌ 程序出现错误: {e}")
finally:
    # 确保资源被正确释放
    print("🧹 正在释放摄像头资源...")
    cap.release()
    cv2.destroyAllWindows()
    print("✅ 资源释放完成")
