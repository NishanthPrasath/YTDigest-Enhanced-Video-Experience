import os
import openai
import tiktoken
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
import requests
from pytube import YouTube
from moviepy.editor import *
import boto3
import io
from pydub import AudioSegment
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

# Add the CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class transcribe(BaseModel):
    link: str
    language: str

@app.post('/transcribeAndStore')
async def transcribeAndStore(transcribe_model:transcribe):
    print("Transcribe Endpoint Called")

    # Set up the OpenAI API key
    openai.api_key = "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"

    # Set up the S3 client object and the bucket name and file key for your input file
    aws_access_key_id = 'AKIAYMZBIJN5VZNAER7Y'
    aws_secret_access_key = 'O0HPvki3PMMgYTj79ooSHgoa+UR5spvb/u6IvcxX'

    # Set up the AWS credentials
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    bucket_name = 'damg7245-assignment-1'

    yt = YouTube(transcribe_model.link)

    audio = yt.streams.filter(only_audio=True).first()

    audio_file = audio.download(filename_prefix="audio_")

    mp3_file = os.path.join(os.getcwd(), "audio.mp3")
    AudioFileClip(audio_file).write_audiofile(mp3_file)

    os.remove(audio_file)
    print("Audio file downloaded successfully")

    input_data = open("audio.mp3",'rb')

    if transcribe_model.language=="English" or transcribe_model.language=="english":
        transcription = openai.Audio.transcribe(model="whisper-1", file=input_data, response_format='text')
    else:
        transcription = openai.Audio.translate(model="whisper-1", file=input_data, response_format='text')

    print("Transcription completed successfully")
    outputFile = 'audio.txt'
    with open(outputFile, "w") as f:
        f.write(transcription)
        f.close()

    with open(outputFile, "rb") as f:
        s3.upload_fileobj(f, bucket_name, 'Processed_file/'+outputFile)

    print("File uploaded successfully")

    data = {'message': 'File uploaded successfully', 'status_code': '200'}
    return data