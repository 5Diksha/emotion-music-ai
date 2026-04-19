from deepface import DeepFace
import cv2

def detect_emotion():
    try:
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Final Emotion: CameraError")
            return "CameraError"

        emotion = "neutral"

        print("Press 'q' to capture emotion...")

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            try:
                result = DeepFace.analyze(
                    frame,
                    actions=['emotion'],
                    enforce_detection=False
                )

                emotion = result[0]['dominant_emotion']

                cv2.putText(
                    frame,
                    f'Emotion: {emotion}',
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

            except Exception as e:
                pass  # don't crash

            cv2.imshow("Emotion Detection", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        print(f"Final Emotion: {emotion}")
        return emotion

    except Exception as e:
        print("Final Emotion: Error")
        return "Error"


if __name__ == "__main__":
    detect_emotion()