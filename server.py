import streamlit as st
import shutil
import cv2
import mediapipe as mp
import os
from os import path
import numpy as np


import os
import base64
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href





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


# folder_path = st.text_input("Paste the folder location where you want to save:")
# flag = path.exists(folder_path)
folder_path="."
flag= True
def main(flip_the_video):
    global input_file_path
    input_file = input_file_path
    FRAME_WINDOW = st.image([])
    cap = cv2.VideoCapture(input_file_path)
    framerate = cap.get(cv2.CAP_PROP_FPS)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    size = (width, height)
    file_name = "./temp/output.mp4"
    export_file_path = "./"

    var1 = os.system(f'ffmpeg -i {input_file} "./temp/audio.mp3"')

    if var1 == 0:
        print("audio extracted")
    # codec = cv2.VideoWriter_fourcc(*"mpeg")
    codec = cv2.VideoWriter_fourcc(*"MP4V")
    video_output = cv2.VideoWriter(file_name, codec, framerate, size, True)





    mp_pose = mp.solutions.pose
    mp_draw = mp.solutions.drawing_utils
    pose = mp_pose.Pose()

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
            results = pose.process(img)
            mp_draw.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                           mp_draw.DrawingSpec((255, 0, 0), 2, 2),
                           mp_draw.DrawingSpec((255, 0, 255), 2, 2)
                           )




            ih, iw, ic =img.shape
            img_blank=np.zeros((ih,iw,3),np.uint8)
            img_blank.fill(255)
            mp_draw.draw_landmarks(img_blank, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_draw.DrawingSpec((255, 0, 0), 2, 2),
                                mp_draw.DrawingSpec((255, 0, 255), 2, 2)
                                )
            
                            
        except Exception as e:
            print(f"error is {e}")
        if img is None:
                break
        video_output.write(img_blank) 
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
    return rename_file_name

if __name__ == "__main__":
    flip_the_video = st.selectbox("Horizontally flip video ",("No","Yes"))

    if st.button("Start"):
        if flag:
            rename_file_name=main(flip_the_video)
            st.markdown(f"## pose copy complete")
            st.markdown(get_binary_file_downloader_html(f'{rename_file_name}', 'Video'), unsafe_allow_html=True)
#             for i in os.listdir("./temp/"):
#                 try:
#                     os.remove(os.remove(f"./temp/{i}"))
#                 except:
#                     pass
        else:
            st.error("Export folder not exist.")
