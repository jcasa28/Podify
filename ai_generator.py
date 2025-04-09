import openai
import pyttsx3
import streamlit as st
import PyPDF2
import io

openai.api_key = "consiguete tu API"

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
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()

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
    st.title("AI Podcast Generator")

    user = st.text_input("Type a theme: ")
    uploaded_pdf = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_pdf:
        pdf_text = extract_text_from_pdf(uploaded_pdf)
        st.subheader("PDF Content")
        st.text_area("Extracted Text", pdf_text, height=300)

        st.subheader("Generating Summary...")
        summary = ask_openai(f"Summarize the following text:\n\n{pdf_text}")
        st.text_area("Summary", summary, height=200)

        if st.button("Generate Podcast"):
            st.subheader("Podcast Script")
            st.text_area("Podcast", summary, height=200)
            speak_text(summary)

    elif user:
        reply = ask_openai(user)
        st.text_area("AI Response", reply, height=200)

        if st.button("Generate Podcast"):
            speak_text(reply)