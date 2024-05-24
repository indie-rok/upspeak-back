from openai import OpenAI 
import os
import cv2
from moviepy.editor import VideoFileClip
import time
import base64
from IPython.display import Image, display, Audio, Markdown

## Set the API key and model name
client = OpenAI(api_key="sk-proj-0qfvR3QhGsdmGnPcRTR2T3BlbkFJpG6G8xT2qmOy9bhX5oQe")

def get_audio_transcript(audio_path):
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=open(audio_path, "rb"),
        response_format="verbose_json", 
        timestamp_granularities=["word"],
        prompt= "I was like, was like, I'm like, you know what I mean, kind of, um, ah, huh, and so, so um, uh, and um, like um, so like, like it's, it's like, i mean, yeah, ok so, uh so, so uh, yeah so, you know, it's uh, uh and, and uh, like, kind"
    )

    print('transcription',transcription.text)

    return transcription
