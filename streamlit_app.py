# streamlit_app.py
import streamlit as st
from PIL import Image
import pytesseract
from gtts import gTTS
import os
from io import BytesIO

st.title("OCR and Speech Recognition")
st.write("Upload an image, extract text, and convert it to speech!")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Open image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # OCR
    try:
        text = pytesseract.image_to_string(image)
        st.subheader("Extracted Text")
        st.write(text if text.strip() != "" else "No text detected.")

        # Text-to-Speech
        if st.button("Convert to Speech"):
            tts = gTTS(text)
            audio_bytes = BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            st.audio(audio_bytes, format="audio/mp3")

    except Exception as e:
        st.error(f"Error: {e}")
