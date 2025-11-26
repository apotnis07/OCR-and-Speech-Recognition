# OCR-and-Voice-Recognition

## Overview

This project is a multi-modal OCR and Speech Recognition application built in Python. It allows users to:

1. Extract text from images using OCR (Tesseract).

2. Extract text from audio files using Google Speech Recognition.

3. Perform arithmetic calculations on recognized text.

4. Save and download the recognized text as a file.

5. Convert extracted text from images into speech using gTTS.

The project is implemented as a web application with Streamlit, making it interactive and easy to use.


## Features
### 1. Image OCR

- Upload an image (.png, .jpg, .jpeg).

- Automatically extract text using Tesseract OCR.

- Perform arithmetic calculations if the text contains expressions.

- Save and download the recognized text.

- Convert extracted text to speech (Text-to-Speech).

### 2. Voice Recognition

- Upload a .wav audio file.

- Automatically extract spoken text using Google Speech Recognition.

- Perform arithmetic calculations if the audio contains expressions.

- Save and download the recognized text.

- Text-to-Speech is disabled for voice input to avoid redundancy.

### 3. Calculations

- Supports addition (+), subtraction (-), multiplication (x), and division (/).

- Can handle multiple operands in a single expression.

- Handles division by zero.


## Installation

### 1. Clone Repository

```
git clone https://github.com/apotnis07/OCR-and-Speech-Recognition.git
cd OCR-and-Speech-Recognition
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. System Dependencies for Tesseract OCR

```
brew install tesseract
```

## Running the App

```
streamlit run streamlit_app.py
```
