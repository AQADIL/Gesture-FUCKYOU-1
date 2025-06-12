# 🤖 AI Hand Gesture Shutdown System  
### ✋ "Flip Off to Shutdown!" – A MediaPipe-Powered Safety Feature  

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.9.0-red?logo=google)
![OpenCV](https://img.shields.io/badge/OpenCV-4.7-brightgreen?logo=opencv)
![OS](https://img.shields.io/badge/Windows%2FLinux%2FmacOS-✔-success)

![Demo](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDk2dWlqY2V5Z3R0eTZ6Y2J6N2VtbmRyb2VlYzB6ZGx4dWZ0eSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3orieS4jfHJaKwkeli/giphy.gif)

</div>

## 🔍 **Project Overview**  
Real-time hand tracking system that **shuts down your computer when detecting offensive gestures** (like 🖕) using:  
- 21-point hand landmark detection via MediaPipe  
- Geometric logic for finger state analysis  
- Cross-platform shutdown commands  

---

## 🦴 **Anatomy of Hand Landmarks**  
MediaPipe uses a standardized **21-point skeletal model**:

### 📐 **Landmark IDs Logic**  
| Landmark | Body Part          | Finger Association |
|----------|--------------------|--------------------|
| 0        | Wrist              | -                  |
| 1-4      | Thumb              | 1 (Tip: 4)         |
| 5-8      | Index Finger       | 2 (Tip: 8)         |
| 9-12     | Middle Finger      | 3 (Tip: 12)        |
| 13-16    | Ring Finger        | 4 (Tip: 16)        |
| 17-20    | Pinky              | 5 (Tip: 20)        |

### 🤌 **Finger State Detection**  
```python
# Finger Tip (TIP) vs Proximal Interphalangeal Joint (PIP) Comparison
def is_finger_up(tip_y, pip_y):
    return tip_y < pip_y  # Lower Y-value = higher position in image coords

# Thumb requires X-axis comparison (moves horizontally)
def is_thumb_up(tip_x, pip_x, is_right_hand):
    return (tip_x > pip_x) if is_right_hand else (tip_x < pip_x)
