import streamlit as st
import math
from youtube_transcript_api import YouTubeTranscriptApi
import openai

# UI Text

"""
# QuickTube: _YouTube Video Summarizer_
"""
st.markdown("Welcome to QuickTube, the fastest way to summarize videos on YouTube!")
video_url = st.text_input("_:red[Enter a YouTube URL:]_")
st.markdown("_Created by [Adam Gilani](https://twitter.com/adamgilani)_")

# Feeds API Key From StreamLit "Secrets"
openai.api_key = st.secrets["API_KEY"]

# Extracts YouTube Video ID from URL
def extract_video_ID():
    if 'watch' in video_url:
        return video_url.split("?v=")[-1]
    elif 'youtu.be' in video_url:
        return video_url.split("/")[-1]
    else:
        raise ValueError("Invalid URL")

def summarize():
    video_id = extract_video_ID()

    # Retrieve the transcript of the video
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    # Concatenate the transcript into a single string
    transcript_text = " ".join([line["text"] for line in transcript])

    # Calculate estimated amount of tokens needed for entire prompt
    estimated_tokens = len(transcript_text) / 5.1

    # Send each chunk to the OpenAI GPT-3 API to generate a summary
    prompt = f"Summarize this into a detailed paragraph: {transcript_text}"

    if estimated_tokens <= 3500:
        # Send the prompt to the GPT-3 API
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=1,
            max_tokens=500
        )
        return response["choices"][0]["text"]
    else:
        return "Video too long... try another video!"

if video_url:
    # Text generation spinner
    with st.spinner("Please wait while your summary is being generated..."):
        # Generate the summarization text
        summary = summarize()

    # Feed the summarization text to the app
    st.write(summary)
