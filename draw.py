import cv2
import mediapipe as mp
import winsound
import threading

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

last_warning_time = 0


def play_warning_sound():
    try:
        import os
        os.system("start sound.mp3")
    except:
        # Если файл не найден, используем системный звук
        winsound.Beep(1000, 1000)


def count_fingers(landmarks):
    finger_tips = [4, 8, 12, 16, 20]  # Fingertip IDs
    finger_pips = [3, 6, 10, 14, 18]  # Finger joint IDs

    fingers = []

    if landmarks[finger_tips[0]].x > landmarks[finger_tips[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    for i in range(1, 5):
        if landmarks[finger_tips[i]].y < landmarks[finger_pips[i]].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers


def detect_gesture(fingers):
    total_fingers = sum(fingers)

    if total_fingers == 0:
        return "Fist"
    elif total_fingers == 5:
        return "Open palm"
    elif fingers == [0, 1, 0, 0, 0]:
        return "Index finger"
    elif fingers == [0, 1, 1, 0, 0]:
        return "Two fingers"
    elif fingers == [0, 1, 1, 1, 0]:
        return "Three fingers"
    elif fingers == [0, 0, 1, 0, 0]:
        return "WARNING: Inappropriate gesture!"
    elif fingers == [1, 0, 0, 0, 1]:
        return "Rock gesture"
    else:
        return f"Gesture: {total_fingers} fingers"


while True:
    ret, frame = cap.read()
    if not ret:
        break

    # зеркало
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process image
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

            # Special
            if "WARNING" in gesture_text:
                cv2.rectangle(frame, (0, 0), (frame.shape[1], 100), (0, 0, 255), -1)
                cv2.putText(frame, "ATTENTION! INAPPROPRIATE GESTURE!",
                            (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                import time

                current_time = time.time()
                if current_time - last_warning_time > 4:
                    threading.Thread(target=play_warning_sound, daemon=True).start()
                    last_warning_time = current_time
                    print("🚨 Я сейчас тебе пальчик в жопу засуну :")

    # Display gesture information
    cv2.putText(frame, gesture_text, (10, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Hand Gesture Recognition', frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()