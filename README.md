# YouTubeDigest - Enhancing user's watching experience

YouTubeDigest is an AI application created to enhance user's video watching experience with features of audio translation, topic wise chapter maker, comments sentiment analysis, and overall context summarization. 

## Resources

- [Application link](http://34.148.127.152:8502/) <br>
- [Codelab Documentation](https://codelabs-preview.appspot.com/?file_id=1xg3GM0WPZ6wiiJ1tQuYKwh3pL3GA_JjXaTEAWP4Pf4k#0)

## What is YouTubeDigest?

In present day, Topic-wise chapter timestamps are manually provided by the user which make its availability totally uncertain. Additionally, YouTube recently discontinued the 'dislike' count on videos which makes it hard to judge the content before watching it. To solve for these shortcomings we developed an AI powered tool which leverages combination of OPENAI Whisper, GPT API, Google Youtube and TTS(Text-to-speech) API to process Youtube videos. This tool streamlines the process of translating different language audio to English, generating topic-vise chapter timestamps, comment sentimental analysis and summaries for long videos. YouTubeDigest is able to process long transcripts (tested upto 57 mins| ~8000 tokens) by uniquely processing text into smaller chunks for GPT api to be able to process 

## Features
- Youtube videos transcribed to text (English and other languages) 
- Translation of audio to English
- Topic-wise Chapter Timestamp generation
- Comment sentiment analysis
- Video script summarization 

## Tech Deliverables

- The overall architecture involves storing data into AWS S3 buckets
- Using Whisper API to transcribe/translate audio based on Language
- Topic-wise chapter timestamp generation using GPT3.5-turbo and GPT-davinci Models
- Comment sentiment analysis using YouTube and GPT3.5-turbo API
- Translating and converting it to speech using Google TTS API

## Steps to reproduce
To run it locally please follow the steps below - 
- clone the repo 
- create a virtual environment and install requirements.txt
- create a .env file with following variables

```
OPEN_AI_API_KEY=
DEVELOPER_KEY= <Google API KEY>
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
```

- run streamlit frontend using the following command 
```
streamlit run App.py
```
