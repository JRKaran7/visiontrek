import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Store previous foot positions for movement tracking
prev_left_y, prev_right_y = None, None
movement_threshold = 0.05  # Adjust as needed

def detect_leg_movement(frame):
    global prev_left_y, prev_right_y

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    if results.pose_landmarks:
        left_foot = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX]
        right_foot = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX]

        # Get current foot Y positions (normalized)
        left_y = left_foot.y
        right_y = right_foot.y

        # Ensure we have previous positions for comparison
        if prev_left_y is None or prev_right_y is None:
            prev_left_y, prev_right_y = left_y, right_y
            return False

        # Calculate foot displacement (difference from previous frame)
        left_displacement = abs(left_y - prev_left_y)
        right_displacement = abs(right_y - prev_right_y)
        # Update previous positions
        prev_left_y, prev_right_y = left_y, right_y

        # Detect step-like movement (one foot moves while the other is more stable)
        if (left_displacement > movement_threshold and right_displacement < movement_threshold) or \
           (right_displacement > movement_threshold and left_displacement < movement_threshold):
            return True  # Walking detected

    return False
