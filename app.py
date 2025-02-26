import streamlit as st
import cv2
from utils import object_detection_brainai as odb
object_detection = odb.ObjectDetectionModel()

st.set_page_config(
    page_title = "객체 인식", 
    page_icon = ":black_cat:",
    layout = "wide")

st.title(":blue[Object Detection] :black_cat:")
st.sidebar.header("메뉴")
source_radio = st.sidebar.radio("선택하세요", ["IMAGE", "VIDEO", "GAME"])
if "random_class" not in st.session_state:
    st.session_state.random_class = object_detection.call_class()

if source_radio == "IMAGE":
    st.write(":green[왼쪽 메뉴 'Browse files' 버튼을 클릭하여 이미지 파일을 선택하면 AI 추론이 시작됩니다.]" )
    st.sidebar.header("이미지 파일 업로드")
    input_img = st.sidebar.file_uploader("이미지 파일을 선택하세요.", type=("jpg", "png"))

    if input_img is not None:
        result_img, detected_object = object_detection.process_image(input_img)
        col1, col2 = st.columns(2)
        with col1:
            st.image(result_img)
        with col2:
            st.header(detected_object)
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.image("data/table.jpg")
        with col2:
            st.header("Objects detected: chair, potted plant, vase, dining table")
        
elif source_radio == "VIDEO":
    st.write(":green[왼쪽 메뉴 'Browse files' 버튼을 클릭하여 비디오 파일을 선택하면 AI 추론이 시작됩니다.]" )
    st.sidebar.header("비디오 파일 업로드")
    input_video = st.sidebar.file_uploader("비디오 파일을 선택하세요..", type=("mp4"))
    print(input_video)
    if input_video is not None:
        temp_file = object_detection.play_video(input_video)
        st.video(temp_file)
    else:
        st.video("data/breakfast.mp4")

elif source_radio == "GAME":
    input_img = st.sidebar.file_uploader("이미지 파일을 선택하세요.", type=("jpg", "png"))
    
    if input_img:

        result_img, detected_object = object_detection.process_image(input_img)
        detected_objects_list = detected_object.split(": ")[1].split(", ")
        if st.session_state.random_class  in detected_objects_list:
            st.header(f':{st.session_state.random_class}: 찾습니다!')
        else:
            st.header(f':{st.session_state.random_class}: 찾을 수 없습니다')
        st.image(result_img)    

    else:
        col1, col2 = st.columns([3, 1])  
        with col1:
            st.title(f':{st.session_state.random_class}: 있는 이미지를 업로드')  
        with col2:
            if st.button('새로운 객체'):
                st.session_state.random_class = object_detection.call_class()
