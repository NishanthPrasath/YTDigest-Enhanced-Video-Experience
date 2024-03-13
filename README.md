# YouTubeDigest - Enhancing Your YouTube Watching Experience

YouTubeDigest is an AI-powered application designed to revolutionize the way you watch YouTube videos. With features like audio translation, topic-wise chapter generation, comment sentiment analysis, and overall context summarization, YouTubeDigest aims to provide a seamless and enriched video watching experience.

## Features

- 🌍 **Multilingual Support**: Transcribe and translate YouTube videos to English and other languages, making content accessible to a wider audience.
- 📑 **Topic-wise Chapters**: Automatically generate topic-wise chapter timestamps for easy navigation and quick access to specific sections of the video.
- 📊 **Comment Sentiment Analysis**: Gain valuable insights into viewer opinions and reactions through sentiment analysis of video comments.
- 📝 **Context Summarization**: Get concise summaries of long videos, saving you time while still capturing the essential information.
- 🎧 **Text-to-Speech**: Convert the translated and summarized content into spoken audio using Google TTS API.

## Why YouTubeDigest?

Currently, topic-wise chapter timestamps are manually provided by users, making their availability uncertain. Additionally, with YouTube's recent decision to discontinue the 'dislike' count on videos, it has become challenging to assess the content quality before watching. YouTubeDigest addresses these limitations by leveraging a combination of powerful APIs, including OpenAI Whisper, GPT, Google YouTube, and Text-to-Speech (TTS).

Our unique approach involves processing long transcripts (tested up to 57 minutes, approximately 8000 tokens) by intelligently splitting the text into smaller chunks, enabling the GPT API to handle the content effectively.

## Architecture Diagram
<img src="Assignment 5 Arch Diagram.png" alt="Architecture Diagram" width = 600>

## Tech Stack

- FastAPI for creating REST API endpoints
- AWS S3 for data storage
- OpenAI Whisper API for audio transcription and translation
- GPT-3.5-turbo and GPT-davinci models for topic-wise chapter timestamp generation
- YouTube and GPT-3.5-turbo API for comment sentiment analysis
- Google TTS API for translating and converting text to speech

## Getting Started

To run YouTubeDigest locally, follow these steps:

1. Clone the repository
2. Create a virtual environment and install the dependencies from `requirements.txt`
3. Create a `.env` file with the following variables:
   ```
   OPEN_AI_API_KEY=
   DEVELOPER_KEY= <Google API KEY>
   AWS_ACCESS_KEY_ID=
   AWS_SECRET_ACCESS_KEY=
   ```
4. Run the Streamlit frontend using the command:
   ```
   streamlit run App.py
   ```

## Resources

- [Application Link](http://34.148.127.152:8502/)
- [Codelab Documentation](https://codelabs-preview.appspot.com/?file_id=1xg3GM0WPZ6wiiJ1tQuYKwh3pL3GA_JjXaTEAWP4Pf4k#0)
