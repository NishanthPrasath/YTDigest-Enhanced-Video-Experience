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
#language = st.selectbox("Language", ["English", "Others"])
language = st.selectbox("Select an Language", ["English", "Afrikaans", "Amharic", "Arabic", "Assamese", "Azerbaijani", "Belarusian", "Bulgarian", "Bengali", "Bosnian", "Catalan", "Chinese", "Czech", "Welsh", "Danish", "German", "Greek", "Spanish", "Estonian", "Persian", "Finnish", "Tagalog", "French", "Galician", "Gujarati", "Hausa", "Hebrew", "Hindi", "Croatian", "Hungarian", "Armenian", "Indonesian", "Icelandic", "Italian", "Japanese", "Javanese", "Georgian", "Kazakh", "Khmer", "Kannada", "Korean", "Luxembourgish", "Lingala", "Lao", "Lithuanian", "Latvian", "Maori", "Macedonian", "Malayalam", "Mongolian", "Marathi", "Malay", "Maltese","Myanmar", "Norwegian", "Nepali", "Dutch", "Occitan", "Punjabi", "Polish", "Pashto", "Portuguese", "Romanian", "Russian", "Sindhi", "Slovak", "Slovenian", "Shona", "Somali", "Serbian", "Swedish", "Swahili", "Tamil", "Telugu", "Tajik", "Thai", "Turkish", "Ukrainian", "Urdu", "Uzbek", "Vietnamese","Yoruba" ])

if st.button('Submit'):
    if selected_option == "Summarizer":
        st.subheader('Summarizer')
        data = {
                    "link": video_url,
                    "language": language
                    }
        with st.spinner('Summarizing...'):
            res = requests.post('http://localhost:8000/transcribeAndStore',json=data)
            response = res.json()

            if response["status_code"] == 200 or response["status_code"] == '200':
                data = {
                        "question": "summarize",
                        "filename": "audio"
                        }
                res1 = requests.post('http://localhost:8000/ask_GPT',json=data)
                response1 = res1.json()
                if response1["status_code"] == 200 or response1["status_code"] == '200':
                    st.write(response1["data"])


 


    if selected_option == "Viewers Sentiments":
        st.subheader('Viewers Sentiments')
        data = {
                    "link": video_url
                    }
        
        with st.spinner('Analyzing user comments'):
            res = requests.post('http://localhost:8000/sentimentAnalysis',json=data)
            response = res.json()

            if response["status_code"] == 200 or response["status_code"] == '200':
                st.write(response["data"])

    if selected_option == "Text to Speech":
        data = {
                    "link": video_url,
                    "language": language
                    }
        with st.spinner('Translating language to english...'):
            res = requests.post('http://localhost:8000/textToSpeech',json=data)
            response = res.json()

            if response["status_code"] == 200 or response["status_code"] == '200':
                st.audio('audio_translated.mp3')

