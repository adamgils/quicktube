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

    # Divide the transcript into chunks of 3500 characters
    chunk_size = 3500
    num_chunks = math.ceil(len(transcript_text) / chunk_size)
    chunks = [transcript_text[i * chunk_size:(i + 1) * chunk_size] for i in range(num_chunks)]

    # Initialize an empty list to store the summaries
    summaries = []

    # Send each chunk to the OpenAI GPT-3 API to generate a summary
    for chunk in chunks:
        prompt = f"Summarize into a concise but detailed paragraph, leave out anything that is not relevant: {chunk}"
        estimated_tokens = len(prompt) / 4

        # Send the prompt to the GPT-3 API
        response = openai.Completion.create(
            engine="text-curie-001",
            prompt=prompt,
            temperature=1,
            max_tokens=int(3800 - estimated_tokens)
        )

        # Add each summary to the list
        summaries.append(response["choices"][0]["text"])

    # Concatenate the summaries into a single string
    summary = "".join(summaries)
    return summary

if video_url:
    # Text generation spinner
    with st.spinner("Please wait while your text is being generated..."):
        # Generate the summarization text
        summary = summarize()

    # Feed the summarization text to the app
    st.write(summary)
