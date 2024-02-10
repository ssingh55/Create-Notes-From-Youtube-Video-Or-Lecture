import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv() ## load all the environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """ 
    You are youtube video summarizer. You will be taking the transcript text
    and summarizing the entire video and provide the important summary 
    in points within 250 words. Please provide the summary of the text given here : 
"""

# Generate summary using the Gemini model by providing a transcript text and a prompt. 
# Returns the generated response text.
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(
        prompt+transcript_text
    )
    return response.text

## Getting the transcript from youtube videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([t["text"] for t in transcript])
        return transcript_text
    except Exception as e:
        raise(e)
    
st.title("Youtube Video Notes App")
youtube_link = st.text_input("Enter the youtube video link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
