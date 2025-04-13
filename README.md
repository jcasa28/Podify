Podify - Podcast Generator from PDF
Podify is a Python-powered app that lets you generate a podcast-style audio summary from a PDF
file.
It uses OpenAI's GPT to summarize content and pyttsx3 for offline text-to-speech playback.
Features
- Upload a PDF
- Summarize content using OpenAI's GPT-3.5
- Listen to the summary with text-to-speech
- Play/Stop buttons for audio control
- Future support for pace and volume control (UI-ready)
Tech Stack
- Streamlit - Web UI
- OpenAI API - Text summarization
- pyttsx3 - Text-to-speech (offline)
- PyPDF2 - PDF text extraction
- threading - Non-blocking speech playback
  
Getting Started
1. Clone the repo
   
`git clone https://github.com/jcasa28/podify.git`

`cd podcast_generator_backend`

3. Create a virtual environment
   
`python -m venv venv`

`source venv/bin/activate`

`# On Windows: `

`venv\Scripts\activate`

4. Install dependencies
   
```pip install -r requirements.txt```

6. Set your OpenAI API key
Replace the hardcoded API key in ai_generator.py with:
`import os`

`openai.api_key = os.getenv("OPENAI_API_KEY")`

Then create a .env file:

`OPENAI_API_KEY=your-key-here`

8. Run the app
   
```streamlit run ai_generator.py```

To Do
- Add support for adjusting volume and pace
- Export podcast as downloadable MP3
- Better error handling for large PDFs
- UI enhancements
Example Use Case
Upload a PDF on a topic like 'Artificial Intelligence' and instantly get a summarized spoken version -
perfect for learning on the go!

License

MIT License
