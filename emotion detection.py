
import cv2
from deepface import DeepFace
from datetime import datetime
import time

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Camera could not be opened.")
    raise SystemExit

print("Emotion Detection Started")
print("Press S to save a photo")
print("Press Q to quit")

last_analysis = 0
faces = []

while True:
    success, frame = camera.read()

    if not success:
        print("Failed to read camera.")
        break

    frame = cv2.flip(frame, 1)

    if time.time() - last_analysis > 0.5:
        try:
            results = DeepFace.analyze(
                img_path=frame,
                actions=["emotion"],
                detector_backend="opencv",
                enforce_detection=False,
                silent=True
            )

            faces = []

            for result in results:
                region = result["region"]

                if region["w"] > 0 and region["h"] > 0:
                    faces.append({
                        "x": region["x"],
                        "y": region["y"],
                        "w": region["w"],
                        "h": region["h"],
                        "emotion": result["dominant_emotion"]
                    })

        except Exception as error:
            print("Analysis error:", error)

        last_analysis = time.time()

    for face in faces:
        x = face["x"]
        y = face["y"]
        w = face["w"]
        h = face["h"]
        emotion = face["emotion"]

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            emotion.upper(),
            (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    cv2.imshow("AI Emotion Detection", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        filename = (
            "emotion_"
            + datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".jpg"
        )

        cv2.imwrite(filename, frame)
        print("Photo saved:", filename)

    elif key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
