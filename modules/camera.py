# camera.py
import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def detect_face_live():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ 摄像头未打开")
        return

    print("🎥 摄像头已打开，按 Q 退出")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ 无法获取画面")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=6)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        text = f"检测到人脸数: {len(faces)}"
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        cv2.imshow("🧠 Luna 摄像头视图", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_face_live()