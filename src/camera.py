import cv2

cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("ERROR: Camera not detected!")
else:
    ret, frame = cap.read()
    if not ret:
        print("ERROR: Camera frame not received!")
    else:
        print("Camera is working.")
        cv2.show(frame)

cap.release()
