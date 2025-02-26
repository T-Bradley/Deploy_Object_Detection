from ultralytics import YOLO
import cv2
import numpy as np
import PIL
import io
import tempfile
import streamlit as st
import moviepy.editor as mpy
import random

class ObjectDetectionModel(): 
    
    def __init__(self):
        self.model = YOLO("models/yolov8n_openvino_model", task = "detect")
        self.class_names = self.model.names

        with open("utils/game_classes.txt", "r") as file:
           self.game_classes = [line.strip() for line in file if line.strip()]

    def process(self, img):
        result = self.model(img)
        img_plot = result[0].plot()

        return img_plot

    def process_image(self, img):

        if isinstance(img, np.ndarray):
            uploaded_img_cv = img
        else:
            uploaded_img = PIL.Image.open(img)
            uploaded_img_cv =  np.array(uploaded_img) 

        result = self.model(uploaded_img_cv, verbose=False)
        img_plot = result[0].plot()

        detected_classes = set()
        for box in result[0].boxes:
            class_id = int(box.cls[0])  # Class ID
            class_name = self.class_names[class_id]  # Get class name
            detected_classes.add(class_name)

        return img_plot, f'Objects Detected: {", ".join(detected_classes) if detected_classes else "No objects detected"}'

    def play_video(self, input_video):
        g = io.BytesIO(input_video.read())
        temporary_location = "upload.mp4" 
        with open(temporary_location, "wb") as out: 
            out.write(g.read())
        out.close() 
        
        camera = cv2.VideoCapture(temporary_location)
        fps = camera.get(cv2.CAP_PROP_FPS)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        video_row=[]
        total_frames = int(camera.get(cv2.CAP_PROP_FRAME_COUNT))
        progress_bar = st.progress(0)
        frame_count = 0
    
        st_frame = st.empty()
        while(camera.isOpened()):
            ret, frame = camera.read()
    
            if ret:
                img_plot, _ = self.process_image(frame)
                st_frame.image(img_plot, channels = "BGR")
                video_row.append(cv2.cvtColor(img_plot,cv2.COLOR_BGR2RGB))
                frame_count +=1
                progress_bar.progress(frame_count/total_frames, text = None)
    
            else:
                camera.release()
                st_frame.empty()
                progress_bar.empty()
                break
        clip = mpy.ImageSequenceClip(video_row,fps=fps)
        clip.write_videofile(temp_file.name)
    
        return temp_file.name

    def call_class(self):
        random_class = random.choice(list(self.game_classes))
        return random_class
    