import cv2
import mediapipe as mp
import numpy as np
import math

# --- MediaPipe Hands ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# --- Kamera ---
cap = cv2.VideoCapture(0)

prev_x, prev_y = None, None
canvas = None

pen_down = False  
threshold = 0.1  
threshold_rst = 0.1
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    if canvas is None:
        canvas = np.zeros_like(frame)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)
    h, w, c = frame.shape

    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        
        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        middle_tip = hand_landmarks.landmark[12]
        ring_tip = hand_landmarks.landmark[16]
        pinky_tip = hand_landmarks.landmark[20]
        wrist = hand_landmarks.landmark[0]

        
        tx, ty = thumb_tip.x, thumb_tip.y
        ix, iy = index_tip.x, index_tip.y

       
        dist = math.sqrt((tx - ix) ** 2 + (ty - iy) ** 2)

        dist_rst = math.sqrt((middle_tip.x - wrist.x) ** 2 + (middle_tip.y - wrist.y) ** 2)
        
        if dist < threshold:
            
            new_pen_down = True
        else:
            
            new_pen_down = False

        if(dist_rst) < threshold_rst:
            canvas = np.zeros_like(frame)
        
        
        if pen_down and not new_pen_down:
            prev_x, prev_y = None, None

        pen_down = new_pen_down

        
        cx, cy = int(ix * w), int(iy * h)

        
        if pen_down:
            if prev_x is not None and prev_y is not None:
                cv2.line(canvas, (prev_x, prev_y), (cx, cy), (255, 255, 255), 5)
            prev_x, prev_y = cx, cy
        else:
            prev_x, prev_y = None, None

        
        color = (0, 255, 0) if pen_down else (0, 0, 255)
        cv2.circle(frame, (cx, cy), 7, color, -1)

        
        cv2.putText(frame, f"dist={dist:.3f}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
    else:
        prev_x, prev_y = None, None
        pen_down = False

    combined = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)

    cv2.putText(combined, "ESC - exit, C - clear | Thumb+Index = DRAW",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Air Drawing - Pen Gesture", combined)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        break
    elif key in (ord('c'), ord('C')):
        canvas = np.zeros_like(frame)

cap.release()
cv2.destroyAllWindows()
