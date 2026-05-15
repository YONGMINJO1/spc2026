# pip install python-dotenv
# .env 파일 안에서 Key 관리
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = 'YOUTUBE_API_KEY'

search_query = '파이썬 튜토리얼'