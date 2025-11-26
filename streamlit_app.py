# streamlit_app.py
import streamlit as st
from PIL import Image
import pytesseract
import cv2
import os
import speech_recognition as sr
from io import BytesIO
from gtts import gTTS

st.title("OCR and Speech Recognition Project")
st.write("Extract text from images or audio, perform calculations, and convert text to speech.")

# Sidebar for mode selection
mode = st.sidebar.selectbox("Choose Input Method", ["Image OCR", "Voice Recognition"])

# ===================== IMAGE OCR =====================
if mode == "Image OCR":
    uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Save temporarily for OpenCV & pytesseract processing
        temp_filename = f"{os.getpid()}.png"
        image.save(temp_filename)

        # OCR
        text = pytesseract.image_to_string(Image.open(temp_filename))
        st.subheader("Extracted Text")
        st.write(text if text.strip() != "" else "No text detected.")

        # Save text to file
        if st.button("Save Text to File"):
            with open("Proj.txt", "w") as f:
                f.write(text)
            st.success("Text saved to Proj.txt")

        # Perform calculations
        if st.button("Perform Calculations"):
            a = []
            result = 0
            x = len(text)
            for i in range(x):
                if text[i] == '-':
                    a.append(text[0:i])
                    a.append(text[i + 1:x + 1])
                    result = int(a[0]) - int(a[1])
                elif text[i] == '+':
                    a.append(text[0:i])
                    a.append(text[i + 1:x + 1])
                    result = int(a[0]) + int(a[1])
                elif text[i] == '/':
                    a.append(text[0:i])
                    a.append(text[i + 1:x + 1])
                    d = int(a[1])
                    result = "Invalid" if d == 0 else int(a[0]) / int(a[1])
                elif text[i] == '*':
                    a.append(text[0:i])
                    a.append(text[i + 1:x + 1])
                    result = int(a[0]) * int(a[1])
            st.write("Operands:", a)
            st.write("Result:", result)

        # Text-to-Speech
        if st.button("Convert Text to Speech"):
            if text.strip() != "":
                tts = gTTS(text)
                audio_bytes = BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)
                st.audio(audio_bytes, format="audio/mp3")
            else:
                st.warning("No text available for speech.")

        # Cleanup
        os.remove(temp_filename)

# ===================== VOICE RECOGNITION =====================
elif mode == "Voice Recognition":
    uploaded_audio = st.file_uploader("Upload an audio file (wav)", type=["wav"])
    if uploaded_audio:
        st.audio(uploaded_audio, format="audio/wav")
        r = sr.Recognizer()
        with sr.AudioFile(uploaded_audio) as source:
            audio = r.record(source)
        try:
            text = r.recognize_google(audio)
            st.subheader("Recognized Text from Audio")
            st.write(text)
        except sr.UnknownValueError:
            st.error("Google Speech Recognition could not understand audio")
            text = ""
        except sr.RequestError:
            st.error("Couldn't get results from Google SR")
            text = ""

        # Save text to file
        if st.button("Save Recognized Text to File"):
            with open("Proj.txt", "w") as f:
                f.write(text)
            st.success("Text saved to Proj.txt")

        # Helper function to parse operations safely
        def parse_operations(m):
            ops = ['+', '-', 'x', '/']
            for op in ops:
                if op in m:
                    parts = m.split(op)
                    return parts, op
            return [], None

        # Perform calculations
        if st.button("Perform Calculations from Audio"):
            m = text.strip()
            if m != "":
                parts, op = parse_operations(m)
                if op:
                    try:
                        numbers = [int(p.strip()) for p in parts]
                        result = None
                        if op == '+':
                            result = sum(numbers)
                        elif op == '-':
                            numbers.sort(reverse=True)
                            result = numbers[0]
                            for n in numbers[1:]:
                                result -= n
                        elif op == 'x':
                            result = 1
                            for n in numbers:
                                result *= n
                        elif op == '/':
                            result = numbers[0]
                            for n in numbers[1:]:
                                if n == 0:
                                    result = "Invalid (division by zero)"
                                    break
                                result /= n
                        st.write("Operands:", numbers)
                        st.write("Operation:", op)
                        st.write("Result:", result)
                    except ValueError:
                        st.error("Could not parse numbers from text.")
                else:
                    st.warning("No recognized operation found in the text.")
            else:
                st.warning("No text available for calculations.")

        # Text-to-Speech
        if st.button("Convert Recognized Text to Speech"):
            if text.strip() != "":
                tts = gTTS(text)
                audio_bytes = BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)
                st.audio(audio_bytes, format="audio/mp3")
            else:
                st.warning("No text available for speech.")
