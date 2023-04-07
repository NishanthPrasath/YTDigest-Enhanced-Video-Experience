import streamlit as st
import os
import re
from streamlit_player import st_player
import requests



# # Add a title and subtitle
st.title('YouTube Digest :movie_camera:')



video_url = st.text_input('YouTube Video URL')

# Embed the video using the HTML code for the video player
if video_url:
    # Extract the video ID from the URL
    video_id = video_url.split("v=")[1]
    # Construct the shortened URL
    short_url = f"https://youtu.be/{video_id}"
    st.video(short_url)

    # Embed the video using Streamlit-Player


    # video_id = video_url.split('=')[-1]

    # Embed the video using an iframe
    # st.write(f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>', unsafe_allow_html=True)
    # st.video(video_url)
    # st.components.v1.html(f'<iframe width="560" height="315" src="{video_url}" frameborder="0" allowfullscreen></iframe>')





selected_option = st.selectbox("Select an option", ["Select", "Summarizer", "Text to Speech", "Viewers Sentiments"])
language = st.selectbox("Language", ["English", "Others"])

if selected_option == "Summarizer":
    st.subheader('Summarizer')
    data = {
                "link": video_url,
                "language": language
                }
    res = requests.post('http://localhost:8000/transcribeAndStore',data=data)
    print(res)
    response = res.json()
    print(response)

    if response["status_code"] == 200:
        data = {
                "question": "Can you summarize?",
                "filename": "audio"
                }
        res1 = requests.post('http://localhost:8000/ask_GPT',data=data)
        print(res1)
        response1 = res1.json()
        print(response1)
        if response1["status_code"] == 200:
            st.write(response1["data"])


if selected_option == "Topic Generator":
    st.subheader('Topic Generator')
    data = {
                "link": video_url,
                "language": language
                }
    res = requests.post('http://localhost:8000/transcribeAndStore',data=data)
    print(res)
    response = res.json()
    print(response)
    if response["status_code"] == 200:
        data = {
                "question": "What are the main topics discussed?",
                "filename": "audio"
                }
        res1 = requests.post('http://localhost:8000/ask_GPT',data=data)
        response1 = res1.json()
        if response1["status_code"] == 200:
            st.write(response1["data"])


if selected_option == "Viewers Sentiments":
    st.subheader('Viewers Sentiments')


if selected_option == "Custom":
    st.subheader('Custom')




# # Add a text input
# search_query = st.text_input('Search on YouTube')

# # Add a button
# if st.button('Search'):
#     st.write(f'Searching for "{search_query}"...')

# # Add a video player
# video_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
# st.video(video_url)
