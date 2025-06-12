import cv2
import mediapipe as mp
import pygame
import logging
import os
import platform
import subprocess
#local
from utils import count_fingers, detect_gesture

logging.getLogger('mediapipe').setLevel(logging.ERROR)

#pygame is a key element
pygame.mixer.init()

try:
    pygame.mixer.music.load("sound.mp3")
    sound_loaded = True
except pygame.error:
    sound_loaded = False


mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(
    model_selection=1,  # 0 — ближние лица, 1 — дальние
    min_detection_confidence=0.5
)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()
    if not ret:
        break

    # зеркало
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    gesture_text = "No hand detected"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand skeleton
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Analyze gesture
            fingers = count_fingers(hand_landmarks.landmark)
            gesture_text = detect_gesture(fingers)

            # Special reaction to inappropriate gesture
            if "WARNING" in gesture_text:
                cv2.rectangle(frame, (0, 0), (frame.shape[1], 100), (0, 0, 255), -1)
                cv2.putText(frame, "ATTENTION! INAPPROPRIATE GESTURE!",
                            (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                # Воспроизведение звука
                if sound_loaded and not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play()
                    print(" Я тебе щас палец в жопу засуну :( ")

                    try:
                        if platform.system() == "Windows":
                            os.system("shutdown /s /t 1")
                        elif platform.system() == "Darwin":  # MacOS
                            subprocess.run(["osascript", "-e", 'tell app "System Events" to shut down'])
                        elif platform.system() == "Linux":
                            os.system("shutdown -h now")
                    except Exception as e:
                        print(f"ERROR BRUH :/: {e}")

    cv2.putText(frame, gesture_text, (10, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('FUCK YOU | AKADIL ', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()