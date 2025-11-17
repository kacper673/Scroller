# main.py
import cv2
import argparse
from camera import Camera
from hand_tracker import HandTracker
from gesture_classifier import GestureClassifier

def main():

    #---DEBUG---
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    #---CAMERA---
    cam = Camera(index=0)


    #---TRACKER---
    tracker = HandTracker(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )


    #---GESTURE CLASIFIER---
    classifier = GestureClassifier(debug=args.debug)


    #---MAIN LOOP---
    while True:
        ok, frame = cam.read(flip=True)
        if not ok:
            break

        result = tracker.process(frame)
        landmarks = tracker.get_first_hand_landmarks(result)

        classifier.classify(landmarks)
        
        #---DEBUG MODE---
        if args.debug:
            tracker.draw(frame, result)

            cv2.imshow("Debug - Hand Tracking", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break

        # NORMAL MODE (no cam window)
        else:
            # tutaj obrobisz gesty, sterowanie UI, scrollowanie itp.
            # ale NIE pokazujemy żadnego okna
            pass

    cam.release()

    if args.debug:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()