import pyautogui

class UIController:
    def __init__(self,debug : bool = False):
        self.debug = debug
    
    def controll(self,gesture):
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
            #pyautogui.doubleClick()

        elif gesture == "close":
            if self.debug:
                print("#UIController ", gesture)
            #pyautogui.hotkey("alt", "f4")
