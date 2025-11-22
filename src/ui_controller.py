import pyautogui

class UIController:
    def __init__(self,debug : bool = False):
        self.debug = debug
        pyautogui.FAILSAFE = False
    
    def controll(self,gesture,mouse_coords):
        if gesture == "scroll_up":
            if self.debug:
                print("#UIController ", gesture)
            pyautogui.scroll(500)

        elif gesture == "scroll_down":
            if self.debug:
                print("#UIController ", gesture)
            pyautogui.scroll(-500)

        elif gesture == "swipe_left":
            if self.debug:
                print("#UIController ", gesture)
            pyautogui.hotkey("left") 

        elif gesture == "swipe_right":
            if self.debug:
                print("#UIController ", gesture)
            pyautogui.hotkey("right")

        elif gesture == "open":
            if self.debug:
                print("#UIController ", gesture)
            pyautogui.doubleClick()

        elif gesture == "close":
            if self.debug:
                print("#UIController ", gesture)
            pyautogui.hotkey("alt", "f4")

        elif gesture == "drag":
            if self.debug:
                print("#UIController ", gesture)
            if mouse_coords is not None:
                screenWidth, screenHeight = pyautogui.size()
                print(screenWidth,screenHeight)
                #x +- 40; y +- 60
                
                pyautogui.moveTo(mouse_coords.x * screenWidth, mouse_coords.y * screenHeight)
            