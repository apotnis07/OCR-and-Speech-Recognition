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

        # Perform calculations
        if st.button("Perform Calculations from Audio"):
            m = text
            dict_calc = {}
            dict1 = {}
            length = len(m)
            result = 0
            count1 = count2 = count3 = count4 = 0

            def check(m, i):
                z = i
                for i in range(z, length):
                    if m[i] == '+':
                        nonlocal count1
                        x = m.count('+')
                        count1 += 1
                        r = i
                        dict_calc[count1] = m[z:r]
                        dict_calc[count1+1] = m[r+1:length]
                        if count1 == x:
                            dict_calc.update({'No': count1+1, 'op':'plus'})
                            return dict_calc
                        else:
                            return check(m, r+1)
                    elif m[i] == '-':
                        nonlocal count2
                        y = m.count('-')
                        count2 += 1
                        r = i
                        dict_calc[count2] = m[z:r]
                        dict_calc[count2+1] = m[r+1:length]
                        if count2 == y:
                            dict_calc.update({'No': count2+1, 'op':'minus'})
                            return dict_calc
                        else:
                            return check(m, r+1)
                    elif m[i] == 'x':
                        nonlocal count3
                        n = m.count('x')
                        count3 += 1
                        r = i
                        dict_calc[count3] = m[z:r]
                        dict_calc[count3+1] = m[r+1:length]
                        if count3 == n:
                            dict_calc.update({'No': count3+1, 'op':'multiply'})
                            return dict_calc
                        else:
                            return check(m, r+1)
                    elif m[i] == '/':
                        nonlocal count4
                        d = m.count('/')
                        count4 += 1
                        r = i
                        dict_calc[count4] = m[z:r]
                        dict_calc[count4+1] = m[r+1:length]
                        if count4 == d:
                            dict_calc.update({'No': count4+1, 'op':'divide'})
                            return dict_calc
                        else:
                            return check(m, r+1)

            if m.strip() != "":
                dict_calc = check(m, 0)
                # Calculation based on operation
                if dict_calc['op']=='plus':
                    x = dict_calc['No']
                    res = 0
                    for i in range(x):
                        res += int(dict_calc[i+1])
                    st.write("Result:", res)
                elif dict_calc['op']=='multiply':
                    x = dict_calc['No']
                    mult = 1
                    for i in range(x):
                        mult *= int(dict_calc[i+1])
                    st.write("Result:", mult)
                elif dict_calc['op']=='divide':
                    x = dict_calc['No']
                    div1 = int(dict_calc[1])
                    for i in range(2, x+1):
                        div1 = div1/int(dict_calc[i])
                    st.write("Result:", div1)
                elif dict_calc['op']=='minus':
                    x = dict_calc['No']
                    vals = [int(dict_calc[i]) for i in range(1,x+1)]
                    vals.sort(reverse=True)
                    result = vals[0]
                    for val in vals[1:]:
                        result -= val
                    st.write("Result:", result)

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
