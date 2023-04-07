import streamlit as st
import os
import re
from streamlit_player import st_player



# # Add a title and subtitle
st.title('YouTube Digest :movie_camera:')



video_url = st.text_input('YouTube Video URL')

# Embed the video using the HTML code for the video player
if video_url:

    # Check if the URL is a valid YouTube URL
    if re.match(r"^https:\/\/(?:www\.)?youtube\.com\/watch\?v=[a-zA-Z0-9_-]{11}$", video_url):

        # Extract the video ID from the URL
        video_id = video_url.split("v=")[1]
        # Construct the shortened URL
        short_url = f"https://youtu.be/{video_id}"
        st.video(short_url)
    else:
        # The URL is not a valid YouTube URL
        st.error("Invalid YouTube URL")

    # Embed the video using Streamlit-Player


    # video_id = video_url.split('=')[-1]

    # Embed the video using an iframe
    # st.write(f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>', unsafe_allow_html=True)
    # st.video(video_url)
    # st.components.v1.html(f'<iframe width="560" height="315" src="{video_url}" frameborder="0" allowfullscreen></iframe>')





selected_option = st.selectbox("Select an option", ["Select", "Summarizer", "Topic Generator", "Viewers Sentiments", "Custom"])

if selected_option == "Summarizer":
    st.subheader('Summarizer')


if selected_option == "Topic Generator":
    st.subheader('Topic Generator')


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
