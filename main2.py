import cv2
import mediapipe as mp
import pygame
import logging
import os
import platform
import subprocess
import numpy as np

from utils import count_fingers, detect_gesture

logging.getLogger('mediapipe').setLevel(logging.ERROR)

pygame.mixer.init()

try:
    pygame.mixer.music.load("sound.mp3")
    sound_loaded = True
except pygame.error:
    sound_loaded = False

try:
    overlay_face = cv2.imread("face.png", cv2.IMREAD_UNCHANGED)
    if overlay_face is None:
        raise FileNotFoundError
except Exception as e:
    print("erroe")
    overlay_face = None


mp_hands = mp.solutions.hands
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

face_detection = mp_face_detection.FaceDetection(
    model_selection=1,
    min_detection_confidence=0.5
)

cap = cv2.VideoCapture(0)


def apply_face_overlay(frame, face_detection_result, overlay_img):
    if overlay_img is None:
        overlay_img = 255 * np.ones((200, 200, 3), dtype=np.uint8)  # Чёрный квадрат побольше

    frame_height, frame_width = frame.shape[:2]

    if face_detection_result.detections:
        for detection in face_detection_result.detections:
            bbox = detection.location_data.relative_bounding_box

            # Увеличиваем область обнаружения в 1.5 раза
            w = int(bbox.width * frame_width * 1.5)
            h = int(bbox.height * frame_height * 1.5)
            x = int(bbox.xmin * frame_width - w * 0.15)  # Смещаем центр
            y = int(bbox.ymin * frame_height - h * 0.15)  # Смещаем центр

            # Корректируем границы
            x, y = max(0, x), max(0, y)
            w, h = min(w, frame_width - x), min(h, frame_height - y)

            resized_overlay = cv2.resize(overlay_img, (w, h))

            if resized_overlay.shape[2] == 4:
                alpha = resized_overlay[:, :, 3] / 255.0
                for c in range(3):
                    frame[y:y + h, x:x + w, c] = (1 - alpha) * frame[y:y + h, x:x + w, c] + alpha * resized_overlay[:,
                                                                                                    :, c]
            else:
                frame[y:y + h, x:x + w] = resized_overlay

    return frame


while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    hand_results = hands.process(rgb_frame)

    face_results = face_detection.process(rgb_frame)

    frame = apply_face_overlay(frame, face_results, overlay_face)

    gesture_text = "No hand detected"
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            fingers = count_fingers(hand_landmarks.landmark)
            gesture_text = detect_gesture(fingers)

            if "WARNING" in gesture_text:
                cv2.rectangle(frame, (0, 0), (frame.shape[1], 100), (0, 0, 255), -1)
                cv2.putText(frame, "ATTENTION! INAPPROPRIATE GESTURE!",
                            (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                if sound_loaded and not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play()
                    print("Я тебе щас палец в жопу засуну :(")


                    try:
                        if platform.system() == "Windows":
                            os.system("shutdown /s /t 1")
                        elif platform.system() == "Darwin":  # MacOS
                            subprocess.run(["osascript", "-e", 'tell app "System Events" to shut down'])
                        elif platform.system() == "Linux":
                            os.system("shutdown -h now")
                    except Exception as e:
                        print(f"Ошибка при выключении: {e}")

    cv2.putText(frame, gesture_text, (10, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('FUCK YOU | AKADIL', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()