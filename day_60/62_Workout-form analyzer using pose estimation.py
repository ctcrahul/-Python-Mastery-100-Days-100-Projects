"""                                                             Day = 62      
      
                                                  Workout Form Analyzer using Pose Estimation
------------------------------------------
Features:
 - Real-time webcam feed (OpenCV)
 - MediaPipe Pose detection
 - Joint angle calculation:
       * Elbow Angle
       * Knee Angle
       * Shoulder-Hip-Knee Back Angle
 - Automatic rep counter for:
       * Bicep Curls
       * Squats
 - Basic form warnings based on joint angles
 - Clean on-screen overlay

Run:
    python workout_form_analyzer.py
"""

import cv2
import mediapipe as mp
import numpy as np
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
# ----------------------------------------
# Helper: calculate angle between 3 points
# ----------------------------------------
import cv2
import mediapipe as mp
import numpy as np
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# ----------------------------------------
# Helper: calculate angle between 3 points
# ----------------------------------------
def calc_angle(a, b, c):
    a = np.array(a)  # First point
    b = np.array(b)  # Mid point
    c = np.array(c)  # End point

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
              np.arctan2(a[1]-b[1], a[0]-b[0])

    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180:
        angle = 360 - angle
    return angle

# ----------------------------------------
# Live Workout Analyzer
# ----------------------------------------
def start_analyzer():
    cap = cv2.VideoCapture(0)

    curl_count = 0
    curl_state = "down"

    squat_count = 0
    squat_state = "up"

    with mp_pose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                  
def calc_angle(a, b, c):
    a = np.array(a)  # First point
    b = np.array(b)  # Mid point
    c = np.array(c)  # End point

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
              np.arctan2(a[1]-b[1], a[0]-b[0])

    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180:
        angle = 360 - angle
    return angle

# ----------------------------------------
# Live Workout Analyzer
# ----------------------------------------
def start_analyzer():
    cap = cv2.VideoCapture(0)

    curl_count = 0
    curl_state = "down"

    squat_count = 0
    squat_state = "up"

    with mp_pose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape

            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = pose.process(img_rgb)

            if result.pose_landmarks:
                lm = result.pose_landmarks.landmark

                # Extract key points
                shoulder = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER].x * w,
                            lm[mp_pose.PoseLandmark.LEFT_SHOULDER].y * h]
                elbow = [lm[mp_pose.PoseLandmark.LEFT_ELBOW].x * w,
                         lm[mp_pose.PoseLandmark.LEFT_ELBOW].y * h]
                wrist = [lm[mp_pose.PoseLandmark.LEFT_WRIST].x * w,
                         lm[mp_pose.PoseLandmark.LEFT_WRIST].y * h]
                hip = [lm[mp_pose.PoseLandmark.LEFT_HIP].x * w,
                       lm[mp_pose.PoseLandmark.LEFT_HIP].y * h]
                knee = [lm[mp_pose.PoseLandmark.LEFT_KNEE].x * w,
                        lm[mp_pose.PoseLandmark.LEFT_KNEE].y * h]
                ankle = [lm[mp_pose.PoseLandmark.LEFT_ANKLE].x * w,
                         lm[mp_pose.PoseLandmark.LEFT_ANKLE].y * h]

               # --------------------------
                # Angles
                # --------------------------
                elbow_angle = calc_angle(shoulder, elbow, wrist)
                knee_angle = calc_angle(hip, knee, ankle)
                back_angle = calc_angle(shoulder, hip, knee)

                # --------------------------
                # BICEP CURL DETECTION
                # --------------------------
                if elbow_angle < 40:
                    curl_state = "up"
                if elbow_angle > 150 and curl_state == "up":
                    curl_count += 1
                    curl_state = "down"
                 
               # --------------------------
                # SQUAT DETECTION
                # --------------------------
                if knee_angle < 70:
                    squat_state = "down"
                if knee_angle > 160 and squat_state == "down":
                    squat_count += 1
                    squat_state = "up"

                # --------------------------
                # Form Warnings
                # --------------------------
                warning = ""

                if back_angle < 140:
                    warning = "⚠ Keep your back straighter!"
                elif knee_angle < 60:
                    warning = "⚠ Don't go too deep!"
                elif elbow_angle > 160 and curl_state == "down":
                    warning = "Extend fully but don't lock joints."

               # --------------------------
                # Draw Overlay
                # --------------------------
                cv2.putText(frame, f"Elbow Angle: {int(elbow_angle)}", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)
                cv2.putText(frame, f"Knee Angle: {int(knee_angle)}", (20, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)
                cv2.putText(frame, f"Back Angle: {int(back_angle)}", (20, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

                cv2.putText(frame, f"Curls: {curl_count}", (400, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                cv2.putText(frame, f"Squats: {squat_count}", (400, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
             
          if warning:
                    cv2.putText(frame, warning, (20, 450),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255), 3)

                mp_drawing.draw_landmarks(
                    frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            cv2.imshow("Workout Form Analyzer", frame)
            if cv2.waitKey(5) & 0xFF == 27:
                break


      
                # Extract key points
                shoulder = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER].x * w,
                            lm[mp_pose.PoseLandmark.LEFT_SHOULDER].y * h]
                elbow = [lm[mp_pose.PoseLandmark.LEFT_ELBOW].x * w,
                         lm[mp_pose.PoseLandmark.LEFT_ELBOW].y * h]
                wrist = [lm[mp_pose.PoseLandmark.LEFT_WRIST].x * w,
                         lm[mp_pose.PoseLandmark.LEFT_WRIST].y * h]
                hip = [lm[mp_pose.PoseLandmark.LEFT_HIP].x * w,
                       lm[mp_pose.PoseLandmark.LEFT_HIP].y * h]
                knee = [lm[mp_pose.PoseLandmark.LEFT_KNEE].x * w,
                        lm[mp_pose.PoseLandmark.LEFT_KNEE].y * h]
                ankle = [lm[mp_pose.PoseLandmark.LEFT_ANKLE].x * w,
                         lm[mp_pose.PoseLandmark.LEFT_ANKLE].y * h]

                # --------------------------
                # Angles
                # --------------------------
                elbow_angle = calc_angle(shoulder, elbow, wrist)
                knee_angle = calc_angle(hip, knee, ankle)
                back_angle = calc_angle(shoulder, hip, knee)

                # --------------------------
                # BICEP CURL DETECTION
                # --------------------------
                if elbow_angle < 40:
                    curl_state = "up"
                if elbow_angle > 150 and curl_state == "up":
                    curl_count += 1
                    curl_state = "down"

                # --------------------------
                # SQUAT DETECTION
                # --------------------------
                if knee_angle < 70:
                    squat_state = "down"
                if knee_angle > 160 and squat_state == "down":
                      
    cap.release()
    cv2.destroyAllWindows()

# Run
if __name__ == "__main__":
    start_analyzer()


#===========================================================================================================================================================================
                                                                  Keep Learning Keep Exploring.
#===========================================================================================================================================================================
