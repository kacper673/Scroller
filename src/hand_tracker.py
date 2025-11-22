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

        self.last_gesture = "None "

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

    


    def draw_fingertip_distances(
    self,
    frame_bgr,
    hand_landmarks,
    pairs=None,
    color=(0, 255, 0),
    thickness=2,
    font_scale=0.6,
):

        if hand_landmarks is None:
            return {}

        h, w = frame_bgr.shape[:2]

        tips = {
            "thumb": 4,
            "index": 8,
            "middle": 12,
            "ring": 16,
            "pinky": 20
        }

        # domyślne pary czubków
        if pairs is None:
            tip_ids = list(tips.values())
            pairs = [(tip_ids[a], tip_ids[b]) for a in range(len(tip_ids)) for b in range(a+1, len(tip_ids))]

        # dystans w układzie 0–1
        def dist_norm(lm1, lm2):
            dx = lm1.x - lm2.x
            dy = lm1.y - lm2.y
            return (dx*dx + dy*dy)**0.5

        # konwersja do px (tylko dla rysowania)
        def to_px(lm):
            return int(lm.x * w), int(lm.y * h)

        distances = {}

        for i, j in pairs:
            lm_i = hand_landmarks.landmark[i]
            lm_j = hand_landmarks.landmark[j]

            # dystans NORMALIZOWANY
            d = dist_norm(lm_i, lm_j)
            distances[(i, j)] = d

            # rysowanie wymaga pikseli
            pi = to_px(lm_i)
            pj = to_px(lm_j)

            cv2.line(frame_bgr, pi, pj, color, thickness)

            # podpis w połowie
            mid = ((pi[0] + pj[0]) // 2, (pi[1] + pj[1]) // 2)
            cv2.putText(
                frame_bgr,
                f"{d:.3f}",   
                (mid[0] + 5, mid[1] - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_scale,
                color,
                2,
                cv2.LINE_AA
            )

        return distances

    def print_last_gesture(self, frame_bgr,gesture):
        if gesture != None:
            self.last_gesture = gesture
        cv2.putText(frame_bgr, f"last_gest {self.last_gesture}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
