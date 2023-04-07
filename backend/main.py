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
import whisper
import re
import googleapiclient.discovery
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

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

class ask_GPT(BaseModel):
    question: str
    filename: str

class videoUrl(BaseModel):
   url: str

load_dotenv()

openai.api_key = os.environ['OPEN_AI_API_KEY']
DEVELOPER_KEY = os.environ['DEVELOPER_KEY']
model=whisper.load_model('base')
aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']

def transcribe_audio(audio, lang='English'):
  # languages = {"af_za": "Afrikaans", "am_et": "Amharic", "ar_eg": "Arabic", "as_in": "Assamese", "az_az": "Azerbaijani", "be_by": "Belarusian", "bg_bg": "Bulgarian", "bn_in": "Bengali", "bs_ba": "Bosnian", "ca_es": "Catalan", "cmn_hans_cn": "Chinese", "cs_cz": "Czech", "cy_gb": "Welsh", "da_dk": "Danish", "de_de": "German", "el_gr": "Greek", "en_us": "English", "es_419": "Spanish", "et_ee": "Estonian", "fa_ir": "Persian", "fi_fi": "Finnish", "fil_ph": "Tagalog", "fr_fr": "French", "gl_es": "Galician", "gu_in": "Gujarati", "ha_ng": "Hausa", "he_il": "Hebrew", "hi_in": "Hindi", "hr_hr": "Croatian", "hu_hu": "Hungarian", "hy_am": "Armenian", "id_id": "Indonesian", "is_is": "Icelandic", "it_it": "Italian", "ja_jp": "Japanese", "jv_id": "Javanese", "ka_ge": "Georgian", "kk_kz": "Kazakh", "km_kh": "Khmer", "kn_in": "Kannada", "ko_kr": "Korean", "lb_lu": "Luxembourgish", "ln_cd": "Lingala", "lo_la": "Lao", "lt_lt": "Lithuanian", "lv_lv": "Latvian", "mi_nz": "Maori", "mk_mk": "Macedonian", "ml_in": "Malayalam", "mn_mn": "Mongolian", "mr_in": "Marathi", "ms_my": "Malay", "mt_mt": "Maltese", "my_mm": "Myanmar", "nb_no": "Norwegian", "ne_np": "Nepali", "nl_nl": "Dutch", "oc_fr": "Occitan", "pa_in": "Punjabi", "pl_pl": "Polish", "ps_af": "Pashto", "pt_br": "Portuguese", "ro_ro": "Romanian", "ru_ru": "Russian", "sd_in": "Sindhi", "sk_sk": "Slovak", "sl_si": "Slovenian", "sn_zw": "Shona", "so_so": "Somali", "sr_rs": "Serbian", "sv_se": "Swedish", "sw_ke": "Swahili", "ta_in": "Tamil", "te_in": "Telugu", "tg_tj": "Tajik", "th_th": "Thai", "tr_tr": "Turkish", "uk_ua": "Ukrainian", "ur_pk": "Urdu", "uz_uz": "Uzbek", "vi_vn": "Vietnamese", "yo_ng": "Yoruba"}
  language = lang
  options = dict(language=language, beam_size=5, best_of=5)
  translate_options = dict(task="translate", **options)
  print("11111111")
  print(audio)
  print("11111111")
  translation_segments = model.transcribe(audio, **translate_options)["segments"]
  transcript_seg=[]
  for i in range(len(translation_segments)):
    transcript_seg.append('[' + str(round(translation_segments[i]['start'],2))+'-'+str(round(translation_segments[i]['end'],2)) + ']' + translation_segments[i]['text'])
  
  return transcript_seg

def chat(inp, ques, message_history, role="user"):

    """Question to be asked to the chatgpt api
    Args:
        inp (str): Input from the user
        message_history (list): Message history
        role (str): Role of the user
    Returns:
        reply (str): Reply from the chatgpt api
    """

    inp = inp + ques

    # Append the input message to the message history
    message_history.append({"role": role, "content": f"{inp}"})

    # Generate a chat response using the OpenAI API
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history
    )

    # Grab just the text from the API completion response
    reply_content = completion.choices[0].message.content

    # Append the generated response to the message history
    message_history.append({"role": "assistant", "content": f"{reply_content}"})

    # Return the generated response.
    return reply_content

def count_tokens(text):

    """Count the number of tokens in a text
    Args:
        text (str): Text to count tokens for
    Returns:
        num_tokens (int): Number of tokens in the text
    """
    encoding = tiktoken.get_encoding("gpt2")
    input_ids = encoding.encode(text)
    num_tokens = len(input_ids)
    return num_tokens


def break_up_file_to_chunks(text, chunk_size=2000, overlap=100):

    tokens = encoding.encode(text)
    num_tokens = len(tokens)
    
    chunks = []
    for i in range(0, num_tokens, chunk_size - overlap):
        chunk = tokens[i:i + chunk_size]
        chunks.append(chunk)
    
    return chunks

def split_tokens_chat(transcript_seg, type):
  prompt_response = []
  encoding = tiktoken.get_encoding("gpt2")
  chunks = break_up_file_to_chunks(transcript_seg)

  for i, chunk in enumerate(chunks):

      prompt_request = "Summarize this: " + encoding.decode(chunks[i])
      messages = [{"role": "system", "content": "This is text summarization."}]    
      messages.append({"role": "user", "content": prompt_request})

      response = openai.ChatCompletion.create(
              model="gpt-3.5-turbo",
              messages=messages,
              temperature=.5,
              max_tokens=500,
              top_p=1,
              frequency_penalty=0,
              presence_penalty=0
      )
      
      prompt_response.append(response["choices"][0]["message"]['content'].strip())

  if type == 'summarize':
    prompt_request = "Can you summarize this? " + str(prompt_response)
  
  if type == 'main_topics':
    prompt_request = "What are all the main topics and their corresponding start and end time stamps in the text? \
     follow this format: Main topic name followed by a comma then start time followed by a comma  not hyphen then end time followed by ; not new line dont use any other characters " + str(prompt_response)

  response = openai.Completion.create(
          model="text-davinci-003",
          prompt=prompt_request,
          temperature=.5,
          max_tokens=1000,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
      )

  reply = response["choices"][0]["text"].strip()
  return reply

def convert_text(text):
  names = []
  start_times = []
  end_times = []

  # Split the data into entries using semicolons
  entries = text.split(';')

  for entry in entries:
      if entry.strip() == '':
          continue
      # Split each entry using commas
      segments = entry.split(',')

      # Append the respective values to their lists
      names.append(segments[0].strip())
      start_times.append(float(segments[1].strip())/60)
      
      # Remove any trailing periods from the end time and convert it to a float
      end_time = segments[2].strip()
      if end_time.endswith('.'):
          end_time = end_time[:-1]
      end_times.append(float(end_time)/60)

  return names, start_times, end_times

@app.post('/ask_GPT')
def ask_GPT(ask_gpt:ask_GPT):
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    bucket_name = 'damg7245-assignment-1'
    file_name = ask_gpt.filename + 'txt'
    file_key = 'Processed_file/' + file_name

    # Use the client object to get the contents of the file
    response = s3.get_object(Bucket=bucket_name, Key=file_key)

    # Get the content of the file from the response object
    transcript_seg = response['Body'].read().decode('utf-8')

    num_tokens = count_tokens(transcript_seg)
    if num_tokens > 2000:
        reply = split_tokens_chat(transcript_seg, 'summarize')

    else:
        message_history = []
        # reply = chat(transcript_seg, "What are all the main topics and their corresponding start and end time stamps in the text?",message_history )
        reply = chat(transcript_seg, ask_gpt.question ,message_history)

@app.post('/transcribeAndStore')
async def transcribeAndStore(transcribe_model:transcribe):
    print("Transcribe Endpoint Called")

    # Set up the AWS credentials
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    bucket_name = 'damg7245-assignment-1'

    # yt = YouTube(transcribe_model.link)

    # audio = yt.streams.filter(only_audio=True).first()

    # audio_file = audio.download(filename_prefix="audio_")

    # mp3_file = os.path.join(os.getcwd(), "audio.mp3")
    # AudioFileClip(audio_file).write_audiofile(mp3_file)
    print("Audio file downloaded successfully")

    # current_dir = os.getcwd()
    # print(current_dir)

    # current_dir = current_dir.replace("\\","/")
    transcription = transcribe_audio("audio.mp3",transcribe_model.language)

    #os.remove(audio_file)

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

@app.post('/sentimentAnalysis')
def sentiment_analysis(url:videoUrl):
    video_url = url.url
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    youtube = googleapiclient.discovery.build(
    YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    # Extract the video ID from the URL
    video_id = re.findall(r"(?<=v=)[\w-]+|(?<=be/)[\w-]+", video_url)[0]

    # Call the YouTube API to retrieve the comments of the video
    message_history = []
    results = youtube.commentThreads().list(part="snippet", videoId=video_id, textFormat="plainText", maxResults=25).execute()

    # Extract the comments and concatenate them into a single string
    comments = ""
    for item in results["items"]:
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments += comment + " "

    message_history.append({"role": "user", "content": f"Analyze the sentiment of the comments of the YouTube video with ID {video_id}. The comments are:\n{comments}\nProvide a summary of the overall sentiment."})

    # Generate a chat response using the OpenAI API
    completion = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=message_history)

    # Grab just the text from the API completion response
    reply_content = completion.choices[0].message.content

    # Append the generated response to the message history
    message_history.append({"role": "assistant", "content": f"{reply_content}"})

    return message_history[1]['content'].strip()