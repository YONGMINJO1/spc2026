# whisper - STT

import os
import base64

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

# def transcribe_audio(file):
#     with open(file,"rd") as af:
#         transcript = cilent.audio.transcriptions.create(
#             model
#         )
#         return transcript