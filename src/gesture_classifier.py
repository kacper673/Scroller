#gesture_classifier.py
import math
import time

class GestureClassifier:

    def __init__(self, close_threshold=0.08,open_threshold = 0.11,debug: bool = False): 

        self.close_threshold = close_threshold
        self.close_start = None
        self.closed_once = False

        self.open_threshold = open_threshold

        self.scroll_dt = 0.8
        self.scroll_down_start = None
        self.scroll_up_start = None

        self.swipe_left_start = None
        self.swipe_right_start = None

        self.volume_start = None
        self.setting_volume = False
        self.vol_beg_pos_thumb = None
        self.vol_beg_pos_writs = None

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
            return None, None

        wrist = landmarks.landmark[0]
        thumb_tip = landmarks.landmark[4]
        pointing_tip = landmarks.landmark[8]
        middle_tip = landmarks.landmark[12]
        ring_tip = landmarks.landmark[16]
        pinky_tip = landmarks.landmark[20]
                    
            


        #---TO ADD---
        # ENTER gest ass thumnb up
        # MAUSE TRACKING as thumg + index
        # ZOOM IN as middle and thumb gesture
        # ZOOM OUT as pinky and thumb gesture
    
        #in DEV 
        #volume up/down
        #----------------------------------------------



        #--- CLOSE GESTURE ---
        if self.dist(wrist, ring_tip) < self.close_threshold:
            if self.close_start is not None and self.closed_once == True:
                if time.perf_counter() - self.close_start < 0.4:
                    if self.debug:
                        print("Close gesture finalized")
                    self.close_start = None
                    self.closed_once = False
                    return "close", None
                else:
                    self.closed_once = False

            if self.close_start is None:
                self.close_start = time.perf_counter()
                if(self.debug):
                    print("first close recognized...waiting for second")

                    
                    
        elif self.dist(wrist, ring_tip) > 0.15:
                if self.close_start is not None:
                    if time.perf_counter() - self.close_start < 0.4:
                        if self.debug:
                            print("open hand for second close gesture...")
                        if self.closed_once is not True:
                            self.closed_once = True
                            self.close_start = time.perf_counter()
                        else:
                            self.closed_once = True
                            
                        
                            

                    else:
                        if self.debug:
                            print("second close gesture not recognised")
                        self.close_start = None

                        

        #--- OPEN GESTURE ---
        if self.dist(pointing_tip,middle_tip) > self.open_threshold  and self.dist(ring_tip,pinky_tip) > self.open_threshold and self.dist(pointing_tip,thumb_tip) > 0.3:
            if self.debug:
                print("Open gesture")
            return "open", None
        
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
                            return "scroll_down", None



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
                            return "scroll_up", None

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
                            return "swipe_left", None

        

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
                            return "swipe_right", None          
        
        #---DRAG GESTURE---
        if self.dist(pointing_tip,thumb_tip) < 0.07:
            if self.debug:
                print("Drag")
            return "drag", pointing_tip
        
        #---VOLUME GESTURE---
        if abs(thumb_tip.y - wrist.y) < 0.1:                    #if thumb and writs is leveled 
            if self.debug:
                print("Ready to set volume...")
            self.vol_beg_pos_thumb = thumb_tip
            self.vol_beg_pos_writs = wrist
            self.volume_start = time.perf_counter()

        if self.volume_start is not None:
            if time.perf_counter() - self.volume_start > 1:         #start gesture when levrl postion is held for one second
                    self.setting_volume = True
        
        if self.setting_volume == True:
            if abs(wrist.y - self.vol_beg_pos_writs.y) < 0.1 and abs(wrist.x - self.vol_beg_pos_writs.x):     #if hand level hasnt moved 
                    cos = self.dist(self.vol_beg_pos_thumb,self.vol_beg_pos_writs) / self.dist(thumb_tip, self.vol_beg_pos_writs)   #return angle between cur pos of thumb and const pos of wrist and begin pos of thumb and wrist
                    if thumb_tip.y < self.vol_beg_pos_thumb.y:        #vol down
                        if self.debug:
                            print("Volume up, degree: ",cos)
                        return "volume_up", cos
                    if thumb_tip.y > self.vol_beg_pos_thumb.y:        #vol up
                        if self.debug:
                            print("Volume down, degree: ",cos)
                        return "volume_down", cos
            else:
                self.setting_volume = False 
                    
            #I implemented changing volume by percentege (how much you showed), but later discovered pyautogui cannot change volume by percenetage, so now it changes by defoalt system step :(. Sure, everything works, but mayby later I will consider adding another libary for that
            #It turned out to be pretty accure actually...even though it does use the angle
                
                    
                


            


        #if self.debug:
         #   print("No gesture recognised") 
        return None, None
