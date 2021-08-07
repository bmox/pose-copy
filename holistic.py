import streamlit as st
import shutil
import cv2
import mediapipe as mp
import os
from os import path
import numpy as np

st.title("Pose copy")
try:
    os.mkdir("temp")
except:
    pass
for i in os.listdir("./temp/"):
    try:
        os.remove(os.remove(f"./temp/{i}"))
    except:
        pass
input_file_path = ""
uploaded_file = st.file_uploader("Upload Files", type=["mp4"])
if uploaded_file is not None:
    with open(f"./temp/{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.getbuffer())
    input_file_path = f"./temp/{uploaded_file.name}"


folder_path = st.text_input("Paste the folder location where you want to save:")
flag = path.exists(folder_path)


def main(flip_the_video):
    global folder_path
    global input_file_path
    input_file = input_file_path
    FRAME_WINDOW = st.image([])
    cap = cv2.VideoCapture(input_file_path)
    framerate = cap.get(cv2.CAP_PROP_FPS)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    size = (width, height)
    file_name = "./temp/output.mp4"
    if folder_path.endswith("/"):
        export_file_path = f"{folder_path}"
    else:
        export_file_path = f"{folder_path}/"

    var1 = os.system(f'ffmpeg -i {input_file} "./temp/audio.mp3"')

    if var1 == 0:
        print("audio extracted")
    # codec = cv2.VideoWriter_fourcc(*"mpeg")
    codec = cv2.VideoWriter_fourcc(*"MP4V")
    video_output = cv2.VideoWriter(file_name, codec, framerate, size, True)





    # mp_pose = mp.solutions.pose
    # mp_draw = mp.solutions.drawing_utils


    mp_drawing = mp.solutions.drawing_utils
    mp_holistic = mp.solutions.holistic

    # pose = mp_pose.Pose()
    holistic=mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    if cap.isOpened():
        ret, frame = cap.read()
    else:
        ret = False


    while ret:
        success, img = cap.read()
        if flip_the_video =="Yes":
            img = cv2.flip(img, 1)
        elif flip_the_video == "No":
            pass
    
        try:
            results = holistic.process(img)
            # 1. Draw face landmarks
            # mp_drawing.draw_landmarks(img, results.face_landmarks, mp_holistic.FACE_CONNECTIONS, 
            #                          mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
            #                          mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
            #                          )
            
            # 2. Right hand
            mp_drawing.draw_landmarks(img, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                            mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=1),
                            mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                            )

            # 3. Left Hand
            mp_drawing.draw_landmarks(img, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=1),
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                    )

            # 4. Pose Detections
            mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                            )

            ih, iw, ic =img.shape
            image=np.zeros((ih,iw,3),np.uint8)
            image.fill(255)
            # 1. Draw face landmarks
            # mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS, 
            #                          mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
            #                          mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
            #                          )
            
            # 2. Right hand
            mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                            mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=1),
                            mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=2, circle_radius=2)
                            )

            # 3. Left Hand
            mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=1),
                                    mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=2, circle_radius=2)
                                    )

            # 4. Pose Detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
                                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=2, circle_radius=2)
                                            )
            

            
                            
        except Exception as e:
            print(f"error is {e}")
        if img is None:
                break
        video_output.write(image) 
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame) 
    video_output.release()
    cap.release()



    aduio_file = "./temp/audio.mp3"
    blur_video = "./temp/blur.mp4"
    os.system(
        f"ffmpeg -i {file_name} -i {aduio_file} -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 {blur_video}"
    )
    rename_file_name = f"{export_file_path}output_" + input_file.split("/")[-1]
    try:
        os.remove(rename_file_name)
    except:
        pass
    shutil.copy(blur_video, rename_file_name)

if __name__ == "__main__":
    flip_the_video = st.selectbox("Horizontally flip video ",("No","Yes"))

    if st.button("Start"):
        if flag:
            main(flip_the_video)
            st.markdown(f"##  complete check your export folder")
            for i in os.listdir("./temp/"):
                try:
                    os.remove(os.remove(f"./temp/{i}"))
                except:
                    pass
        else:
            st.error("Export folder not exist.")
