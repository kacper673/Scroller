#gesture_classifier.py
import math
import time

class GestureClassifier:

    def __init__(self, close_threshold=0.1,open_threshold = 0.11,debug: bool = False): 

        self.close_threshold = close_threshold
        self.open_threshold = open_threshold

        self.scroll_dt = 0.8
        self.scroll_down_start = None
        self.scroll_up_start = None

        self.swipe_left_start = None
        self.swipe_right_start = None

        self.swipe_left_coords = None
        self.swipe_right_coords = None

        #preventing detecting unwanted accidental swipe/scroll gestures
        self.last_gesture = None
        self.last_time = 0.0
        self.repeat_threashold = 1.0

        self.debug = debug

    def dist(self, a, b):
        return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

    def _gesture_allowed(self, gesture: str) -> bool:
       
        now = time.perf_counter()

        if self.last_gesture is None:
            self.last_gesture = gesture
            self.last_time = now
            return True

        dt = now - self.last_time

        if dt < self.repeat_threashold:
            if gesture == self.last_gesture:
                self.last_time = now 
                return True
            else:
                if self.debug:
                    print(f"Gesture '{gesture}' zablokowany - za szybko po '{self.last_gesture}' ({dt:.3f}s)")
                return False
        else:
            self.last_gesture = gesture
            self.last_time = now
            return True
 
    def classify(self, landmarks):
        
        if landmarks is None:
            return None

        wrist = landmarks.landmark[0]
        thumb_tip = landmarks.landmark[4]
        pointing_tip = landmarks.landmark[8]
        middle_tip = landmarks.landmark[12]
        ring_tip = landmarks.landmark[16]
        pinky_tip = landmarks.landmark[20]
                    
            
        # --- CLOSE GESTURE ---
        # if self.dist(wrist, middle_tip) < self.close_threshold:
        #     if self.debug:
        #         print("Close gesture")

        #     return "close"  #later some coce eg -1 for close

        #--- OPEN GESTURE ---
        if self.dist(pointing_tip,middle_tip) > self.open_threshold  and self.dist(ring_tip,pinky_tip) > self.open_threshold:
            if self.debug:
                print("Open gesture")
            return "open"
        


       
        #---SCROLL DOWN GESTURE---

        if pointing_tip.y > 0.4 and pointing_tip.y < 0.7:   
            if self.scroll_down_start is None:
                self.scroll_down_start = time.perf_counter()

        elif pointing_tip.y > 0.7:
                if self.scroll_down_start is not None:
                    dt = time.perf_counter() - self.scroll_down_start
                    self.scroll_down_start = None
                    if dt < self.scroll_dt:
                        if(self._gesture_allowed("scroll_down")):
                            if self.debug:
                                print("Scroll down")
                            return "scroll_down"



        #---SCROLL UP GESTURE---
        if pointing_tip.y < 0.7 and pointing_tip.y > 0.4:   
            if self.scroll_up_start is None:
                self.scroll_up_start = time.perf_counter()

        elif pointing_tip.y < 0.4:
                if self.scroll_up_start is not None:
                    dt = time.perf_counter() - self.scroll_up_start
                    self.scroll_up_start = None
                    if dt < self.scroll_dt:
                        if(self._gesture_allowed("scroll_up")):
                            if self.debug:
                                print("Scroll up")
                            return "scroll_up"

        #---SWIPE LEFT GESTURE---
        if pointing_tip.x > 0.7:   
            if self.swipe_left_start is None:
                self.swipe_left_start = time.perf_counter()

        elif pointing_tip.x < 0.7 and pointing_tip.x > 0.45:
                if self.swipe_left_start is not None:
                    dt = time.perf_counter() - self.swipe_left_start
                    self.swipe_left_start = None
                    if dt < self.scroll_dt:
                        if(self._gesture_allowed("swipe_left")):
                            if self.debug:
                                print("Swipe left")
                            return "swipe_left"

        

        #---SWIPE RIGHT GESTURE---
        if pointing_tip.x < 0.3:   
            if self.swipe_right_start is None:
                self.swipe_right_start = time.perf_counter()

        elif pointing_tip.x > 0.3 and pointing_tip.x  < 0.55:
                if self.swipe_right_start is not None:
                    dt = time.perf_counter() - self.swipe_right_start
                    self.swipe_right_start = None
                    if dt < self.scroll_dt:
                        if(self._gesture_allowed("swipe_right")):
                            if self.debug:
                                print("Swipe right")
                            return "swipe_right"          
        
        
        #if self.debug:
         #   print("No gesture recognised")
         
        return None
