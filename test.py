import cv2
import mediapipe as mp
import numpy as np
# initialize mediapipe pose solution
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose()
cap = cv2.VideoCapture("2.mp4")
codec = cv2.VideoWriter_fourcc(*"MP4V")
file_name = "output.mp4"
framerate = cap.get(cv2.CAP_PROP_FPS)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
size = (width, height)
video_output = cv2.VideoWriter(file_name, codec, framerate, size, True)
while True:
    ret, img = cap.read()
    results = pose.process(img)
    mp_draw.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                           mp_draw.DrawingSpec((255, 0, 0), 2, 2),
                           mp_draw.DrawingSpec((255, 0, 255), 2, 2)
                           )
    



    cv2.imshow("Pose Estimation", img)
    ih, iw, ic =img.shape
    img_blank=np.zeros((ih,iw,3),np.uint8)
    img_blank.fill(255)

    mp_draw.draw_landmarks(img_blank, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                        mp_draw.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                        mp_draw.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))
                           
    # display extracted pose on blank images
    cv2.imshow("Extracted Pose", img_blank)
    img_copy=np.zeros((ih,iw,3),np.uint8)
    img_copy.fill(255)
    mp_draw.draw_landmarks(img_copy, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                           mp_draw.DrawingSpec((255, 0, 0), 2, 2),
                           mp_draw.DrawingSpec((255, 0, 255), 2, 2)
                           )
    cv2.imshow("Extracted copy Pose", img_copy)
                      
    video_output.write(img_blank)
    # print all landmarks
    print(results.pose_landmarks)
    cv2.waitKey(1)
video_output.release()
cap.release()    
