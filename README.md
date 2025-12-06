# SCROLLER

Simple Windows UI Controller, using hand gestures. The programm supports following actions:

- scroll up/down
- swipe left/ right,
- close/open
- volume up/down
- mouse drag

which allows user to controll ceratin actions like swiping through photo gallery, scrolling the pdf or fauvorite website, closing curently opend app, draggin a mouse and opening a new one or regulating volume WITHOUT any use of keyboard and mouse, only relaying on camera and hand gestures. 

The project covers aspects of machine vision and image recognition models, using external python liberies - MediaPipe Hands for recognising hand landmarks and OpenCV for camera image processing. Hand lanmarks are then classified into certain gestures that are mapped in system actions allowing keyboardless and mouseless system controll. 

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Tutorial

### Scroll Up

1. Hold your hand in the **upper half** of the camera frame.  
2. Extend your **index finger** upward.  
3. Move your fingertip **smoothly upward** in a single, continuous motion.  
4. Begin the movement above the **middle vertical zone** of the screen.  
5. Finish with your fingertip reaching the **upper zone** to trigger the scroll-up gesture.


### Scroll Down

1. Hold your hand in the **upper or middle** part of the frame.  
2. Extend your **index finger** downward.  
3. Move your fingertip **smoothly downward** in one motion.  
4. Begin the movement below the **middle vertical zone**.  
5. Finish with your fingertip reaching the **lower zone** to trigger the scroll-down gesture.


### Swipe Left

1. Position your index fingertip on the **right side** of the camera frame.  
2. Extend your index finger forward.  
3. Move your fingertip **leftwards** toward the center of the frame.  
4. The gesture triggers once the finger crosses into the **middle horizontal zone**.  
5. Perform the motion within the allowed time window to complete the swipe.


### Swipe Right

1. Position your index fingertip on the **left side** of the screen.  
2. Extend your index finger forward.  
3. Move your fingertip **rightwards** toward the center.  
4. The gesture is detected when the finger enters the **middle region**.  
5. Perform the movement smoothly and within the gesture timing limit.


### Open Gesture

1. Fully open your hand and face the palm toward the camera.  
2. Spread your fingers so that the distances between finger tips are **large and clearly visible**.  
4. Hold the open hand steady—the gesture is detected instantly.


### Close Gesture

1. Make a quick **closing movement** with your hand (as if forming a loose fist).  
2. Ensure your **ring finger moves close to the wrist**.  
3. Briefly open the hand again.  
4. Perform a second closing motion quickly.  
5. When both steps are detected in sequence, the close gesture is triggered.


### Drag Gesture

1. Bring your **index finger and thumb** close together to create a **pinch** shape.  
2. Keep the middle, ring, and pinky fingers slightly curled so that the distances between them stay small.  
3. Once the pinch is recognized, move your hand—  
   the mouse cursor will follow the fingertip.  
4. Maintaining the pinch continues the drag action.


### Volume Up / Volume Down

1. Hold your thumb **horizontally**, aligned with the wrist  
2. Keep your hand very still for **~2 seconds** to activate volume mode.  
3. After activation, move your **thumb upward** to increase volume.  
4. Move your **thumb downward** to decrease volume.  
5. The direction is determined by comparing thumb position to its initial reference point.


---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Installation & Running

pip install opencv-python mediapipe pyautogui

python main.py --debug

Debug mode shows:

- camera window
- hand landmarks
- printed gesture logs

Normal mode runs silently, performing system actions.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


## Technical apsects:

I use MediaPipe hands model for recognising hand landmarks, captured from a camera frame using OpenCV that are later processed and classified. 

Pipeline:

1. Capture frame using OpenCV

2. Detect hand landmarks via MediaPipe

3. Classify pose + movement into gesture

4. Execute system action using PyAutoGUI

Gestures map:

- scroll gesture -> PyAutoGui.scroll(y/-y)
- swipe gesture -> PyAutoGui.hotkey(ledft/right)
- open gesture -> PyAutoGui.doubleClick()
- close gesture -> PyAutoGui.hotkey("alt", "f4")
- mouse drag gesture -> pyautogui.moveTo(mouse_coords.x * screenWidth, mouse_coords.y * screenHeight)
- volume gesture -> pyautogui.press("volumeup"/"volumedown")

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


## DISCLAIMER

This program can execute system-level actions such as Alt + F4, global hotkeys and mouse control.
The author is not responsible for any damage, data loss, or unintended actions caused by using this software.
Use at your own risk and test it in a safe environment before everyday use

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




