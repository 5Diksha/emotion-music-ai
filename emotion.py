from deepface import DeepFace
import cv2

def detect_emotion():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return "CameraError"

    emotion = "Unknown"

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            emotion = result[0]['dominant_emotion']

            cv2.putText(frame, f'Emotion: {emotion}', (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 2)

        except:
            pass

        cv2.imshow("Emotion Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    print(f"Final Emotion: {emotion}")
    return emotion


if __name__ == "__main__":
    detect_emotion()