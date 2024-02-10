import streamlit as st
import sqlite3
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv

load_dotenv() ## load all the environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_notes(transcript_text, subject):
    if subject == "Physics":
        prompt = """
        Title: Detailed Physics Notes from YouTube Video Transcript

            As a physics expert, your task is to provide detailed notes based on the transcript of a YouTube video I'll provide. Assume the role of a student and generate comprehensive notes covering the key concepts discussed in the video.

            Your notes should:

            - Highlight fundamental principles, laws, and theories discussed in the video.
            - Explain any relevant experiments, demonstrations, or real-world applications.
            - Clarify any mathematical equations or formulas introduced and provide explanations for their significance.
            - Use diagrams, illustrations, or examples to enhance understanding where necessary.

            Please provide the YouTube video transcript, and I'll generate the detailed physics notes accordingly.
    """
    elif subject == "Chemistry":
        prompt = """
            Title: Detailed Chemistry Notes from YouTube Video Transcript

            As a chemistry expert, your task is to provide detailed notes based on the transcript of a YouTube video I'll provide. Assume the role of a student and generate comprehensive notes covering the key concepts discussed in the video.

            Your notes should:

            - Break down chemical reactions, concepts, and properties explained in the video.
            - Include molecular structures, reaction mechanisms, and any applicable theories.
            - Discuss the significance of the discussed chemistry concepts in various contexts, such as industry, environment, or daily life.
            - Provide examples or case studies to illustrate the practical applications of the concepts discussed.

            Please provide the YouTube video transcript, and I'll generate the detailed chemistry notes accordingly.
        """
    elif subject == "Mathematics":
        prompt = """
            Title: Detailed Mathematics Notes from YouTube Video Transcript

            As a mathematics expert, your task is to provide detailed notes based on the transcript of a YouTube video I'll provide. Assume the role of a student and generate comprehensive notes covering the key mathematical concepts discussed in the video.

            Your notes should:

            - Outline mathematical concepts, formulas, and problem-solving techniques covered in the video.
            - Provide step-by-step explanations for solving mathematical problems discussed.
            - Clarify any theoretical foundations or mathematical principles underlying the discussed topics.
            - Include relevant examples or practice problems to reinforce understanding.

            Please provide the YouTube video transcript, and I'll generate the detailed mathematics notes accordingly.
        """
    elif subject == "Data Science and Statistics":
        prompt = """
            Title: Comprehensive Notes on Data Science and Statistics from YouTube Video Transcript

            Subject: Data Science and Statistics

            Prompt:

            As an expert in Data Science and Statistics, your task is to provide comprehensive notes based on the transcript of a YouTube video I'll provide. Assume the role of a student and generate detailed notes covering the key concepts discussed in the video.

            Your notes should:

            Data Science:

            Explain fundamental concepts in data science such as data collection, data cleaning, data analysis, and data visualization.
            Discuss different techniques and algorithms used in data analysis and machine learning, including supervised and unsupervised learning methods.
            Provide insights into real-world applications of data science in various fields like business, healthcare, finance, etc.
            Include discussions on data ethics, privacy concerns, and best practices in handling sensitive data.
            Statistics:

            Outline basic statistical concepts such as measures of central tendency, variability, and probability distributions.
            Explain hypothesis testing, confidence intervals, and regression analysis techniques.
            Clarify the importance of statistical inference and its role in drawing conclusions from data.
            Provide examples or case studies demonstrating the application of statistical methods in solving real-world problems.

            Your notes should aim to offer a clear understanding of both the theoretical foundations and practical applications of data science and statistics discussed in the video. Use clear explanations, examples, and visuals where necessary to enhance comprehension.

            Please provide the YouTube video transcript, and I'll generate the detailed notes on Data Science and Statistics accordingly.
        """
    elif subject == "News":
        prompt = """
        Title: Detailed News Notes from YouTube Video Transcript

            As a news anchor expert, your task is to provide detailed notes based on the transcript of a YouTube video I'll provide. Assume the role of a news anchor and generate comprehensive notes covering the key concepts discussed in the video.

            Your notes should:

            - Describe the video's content, including who made it, its main points, and any unique aspects
            - Explain any relevant experiments, demonstrations, or real-world applications.
            - Use diagrams, illustrations, or examples to enhance understanding where necessary.
            - Highlist key concept in the video

            Please provide the YouTube video transcript, and I'll generate the detailed physics notes accordingly.
    """

    transcript_text_as_strings = []
    for item in transcript_text:
        transcript_text_as_strings.append(item["text"])  # Assuming the text is in a "text" key

    transcript_text = " ".join(transcript_text_as_strings)    
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt + transcript_text)
    return response.text
        
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Prioritize manually created transcripts in preferred languages,
        # handling potential errors gracefully
        preferred_languages = ["en", "hi"]  # Customize this list as needed
        for language in preferred_languages:
            try:
                transcript = transcript_list.find_manually_created_transcript([language])
                if transcript:
                    return transcript.fetch()
            except Exception as e:
                print(f"Error finding manually created transcript: {e}")

        # If not found, try generated transcripts in preferred languages
        for language in preferred_languages:
            try:
                transcript = transcript_list.find_generated_transcript([language])
                if transcript:
                    return transcript.fetch()
            except Exception as e:
                print(f"Error finding generated transcript: {e}")

        # If still not found, try the first available transcript
        try:
            transcript = transcript_list.find_transcript()
            if transcript:
                return transcript.fetch()
        except Exception as e:
            print(f"Error finding any transcript: {e}")

        raise Exception("No suitable transcript found.")

    except Exception as e:
        print(f"Error extracting transcript: {e}")
        raise(e)

def main():
    st.title("YouTube Video Transcript Notes Generator")
    youtube_link = st.text_input("Enter the YouTube video link:")
    subject = st.selectbox("Select the subject:", ["Physics", "Chemistry", "Mathematics", "Data Science and Statistics", "News"])

    if youtube_link:
        video_id = youtube_link.split("=")[1]
        st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

    if st.button("Get Detailed Notes"):
        transcript_text = extract_transcript_details(youtube_link)
    
        if transcript_text:
            st.success("Transcript extracted successfully!")
            detailed_notes = generate_notes(transcript_text, subject)
            st.markdown("## Detailed Notes:")
            st.write(detailed_notes)
        else:
            st.error("Failed to extract transcript.")

if __name__ == "__main__":
    main()