import openai
from gtts import gTTS
import io
import streamlit as st
import PyPDF2
import os
from dotenv import load_dotenv
import base64
import streamlit.components.v1 as components

load_dotenv()

openai.api_key = st.secrets["OPENAI_API_KEY"]

def ask_openai(theme):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can use "gpt-4" if available to you
            messages=[
                {"role": "system", "content": f"you're going to make a script for a podcast about this PDF that has al this text: {theme}"},
                {"role": "user", "content": theme}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {e}"

def generate_audio(text):
    tts = gTTS(text)
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes

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

        if st.button("Make Script"):
            summary = ask_openai(f"create a podcast script of: \n\n{pdf_text}")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("PDF Content")
                extracted_PDF = st.text_area("Extracted Text", pdf_text, height=300)

            with col2:
                st.subheader("Summary")
                summary_text = st.text_area("Summary", summary, height=300)

            if st.button("Generate Podcast"):
                # Generate audio bytes and embed via HTML for better mobile support
                audio_bytes = generate_audio(summary).getvalue()
                b64 = base64.b64encode(audio_bytes).decode()
                audio_html = f'<audio controls src="data:audio/mp3;base64,{b64}"></audio>'
                components.html(audio_html, height=100)