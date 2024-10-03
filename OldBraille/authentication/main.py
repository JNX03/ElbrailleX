import streamlit as st
import os
import json

def run_voice_auth(command):
    os.system(command)

st.title('Test Ai Speaker reconition')

tab1, tab2 = st.tabs(["Train Model", "Authen Test"])

with tab1:
    st.header("Train Model")
    user_name = st.text_input("Train voice name")
    audio_file = st.file_uploader("Upload your voice", type=['m4a', 'wav', 'mp3'])
    if audio_file is not None and user_name:
        audio_path = f"C:\\Users\\jeans\\Desktop\\SpeakerRegonized\\sound\\{user_name}.wav"
        with open(audio_path, "wb") as f:
            f.write(audio_file.getbuffer())
        enroll_command = f"python voice_auth.py -t enroll -n \"{user_name}\" -f \"{audio_path}\""
        run_voice_auth(enroll_command)
        st.success("Done Training!!! 💀")

with tab2:
    st.header("Authentication Test")
    audio_file_test = st.file_uploader("Upload your voice for testing", type=['m4a', 'wav', 'mp3'], key="test")
    if audio_file_test is not None:
        audio_test_path = "C:\\Users\\jeans\\Desktop\\SpeakerRegonized\\sound\\test_audio.wav"
        with open(audio_test_path, "wb") as f:
            f.write(audio_file_test.getbuffer())
        recognize_command = f"python voice_auth.py -t recognize -f \"{audio_test_path}\""
        run_voice_auth(recognize_command)
        
        with open("recognition_result.json", "r") as json_file:
            recognition_result = json.load(json_file)
        
        recognized_user = recognition_result.get("recognized_user")
        st.success(f"Authenticated user as : {recognized_user}")
