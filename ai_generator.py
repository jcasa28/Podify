import openai
import pyttsx3
import streamlit as st
import PyPDF2
import io
import threading
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")   
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)
speech_thread = None
stop_flag = threading.Event()

def ask_openai(theme):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can use "gpt-4" if available to you
            messages=[
                {"role": "system", "content": f"you're going to make a script for a podcast about {theme}"},
                {"role": "user", "content": theme}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {e}"

def speak_text(text):
    words = text.split()
    chunk = []
    for word in words:
        if stop_flag.is_set():
            break
        chunk.append(word)
        # if len(chunk) >= 10:
        #     engine.say(' '.join(chunk))
        #     engine.runAndWait()
        #     chunk = []
    if chunk and not stop_flag.is_set():
        engine.say(' '.join(chunk))
        engine.runAndWait()

def start_speech(text):
    global speech_thread
    stop_flag.clear()
    speech_thread = threading.Thread(target=speak_text, args=(text,))
    speech_thread.start()

def stop_speech():
    stop_flag.set()
    engine.stop()

def extract_text_from_pdf(uploaded_file):
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

# Example usage
if __name__ == "__main__":
    st.title("Podify 🎙️")
    st.divider()
    st.subheader("Generate your podcast from a PDF")

    uploaded_pdf = st.file_uploader("Upload a PDF 📁", type="pdf")

    if uploaded_pdf:
        pdf_text = extract_text_from_pdf(uploaded_pdf)

        summary = ask_openai(f"Summarize the following text:\n\n{pdf_text}")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("PDF Content")
            extracted_PDF = st.text_area("Extracted Text", pdf_text, height=300)

        with col2:
            st.subheader("Summary")
            summary_text = st.text_area("Summary", summary, height=300)

        if st.button("Generate Podcast"):
            start_speech(summary)

        if st.button("⏯️"):
            stop_speech()

        # volume control
#         volume = st.slider("volume",min_value=1.0, max_value=10.0)
#         engine.setProperty('volume', volume)
#
#         pace = st.selectbox("🕒 Pace", ["0.5x","0.75x","1x", "1.5x", "1.75x", "2x"])
#         pace_map = {
#             "0.5x":100 ,
#             "0.75x": 125,
#             "1x": 150,
#             "1.5x": 200,
#             "1.75x": 225,
#             "2x": 250
#         }
#         engine.setProperty('rate', pace_map[pace])
#