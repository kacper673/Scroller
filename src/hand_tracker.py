# hand_tracker.py
import cv2
import mediapipe as mp

class HandTracker:
    def __init__(
        self,
        max_num_hands: int = 1,
        min_detection_confidence: float = 0.7,
        min_tracking_confidence: float = 0.7
    ):
        self._mp_hands = mp.solutions.hands
        self._hands = self._mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self._drawer = mp.solutions.drawing_utils

    def process(self, frame_bgr):
        """Przetwarza klatkę BGR i zwraca wynik MediaPipe."""
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        result = self._hands.process(frame_rgb)
        return result

    def draw(self, frame_bgr, result):
        """Rysuje landmarki dłoni na podanej klatce (in-place)."""
        if not result.multi_hand_landmarks:
            return

        for hand_landmarks in result.multi_hand_landmarks:
            self._drawer.draw_landmarks(
                frame_bgr,
                hand_landmarks,
                self._mp_hands.HAND_CONNECTIONS
            )

    def get_first_hand_landmarks(self, result):
        """Zwraca landmarki pierwszej dłoni albo None."""
        if result.multi_hand_landmarks:
            return result.multi_hand_landmarks[0]
        return None
