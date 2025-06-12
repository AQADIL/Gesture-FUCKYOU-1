def count_fingers(landmarks):
    finger_tips = [4, 8, 12, 16, 20]
    finger_pips = [3, 6, 10, 14, 18]

    fingers = []

    fingers.append(1 if landmarks[finger_tips[0]].x > landmarks[finger_tips[0] - 1].x else 0)

    for i in range(1, 5):
        fingers.append(1 if landmarks[finger_tips[i]].y < landmarks[finger_pips[i]].y else 0)

    return fingers


def detect_gesture(fingers):
    total_fingers = sum(fingers)

    if total_fingers == 0:
        return "Fist"
    if total_fingers == 5:
        return "Open palm"

    # Specific patterns
    if fingers == [0, 1, 0, 0, 0]:
        return "Index finger"
    if fingers == [0, 1, 1, 0, 0]:
        return "Two fingers"
    if fingers == [0, 1, 1, 1, 0]:
        return "Three fingers"
    if fingers == [0, 0, 1, 0, 0]:
        return "WARNING: Inappropriate gesture!"
    if fingers == [1, 0, 0, 0, 1]:
        return "Rock gesture"

    return f"Gesture: {total_fingers} fingers"