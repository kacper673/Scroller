# camera.py
import cv2

class Camera:
    def __init__(self, index: int = 0, width: int | None = None, height: int | None = None):
        self.cap = cv2.VideoCapture(index)

        if width is not None:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        if height is not None:
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def read(self, flip: bool = True):
        """Zwraca (ok, frame). ok=False jeśli nie udało się pobrać klatki."""
        ret, frame = self.cap.read()
        if not ret:
            return False, None
        if flip:
            frame = cv2.flip(frame, 1)
        return True, frame

    def release(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
