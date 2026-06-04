# whisper (속삭임) 말을 기반으로text로 변환 - text (speech-to-text)

import os
import base64

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def transcribe_audio(file):
    with open(file,"rd") as af: # af = audio file
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=af,
            response_format = "text", # json
            language="ko" # 한국어
        )
        return transcript
    
result = transcribe_audio("harvard.wav")
result = transcribe_audio("Track021_생각해봐요.mpe3")
print("결과: ", result)