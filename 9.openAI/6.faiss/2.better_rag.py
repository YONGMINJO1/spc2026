# pip install faiss-cpu

from dotenv import load_dotenv
import os

from openai import OpenAI

import faiss
import numpy as np

client = OpenAI(api=os.getenv("OPENAI_API_KEY"))

load_dotenv()

# 우리의 문장 데이터
documents = [
    '한국 소프트웨어 저작권협회는 SPC라는 약자를 가지고 있고, 다양한 국내 기업의 SW라이선스와 저작권을 다루는 곳'
    '홍길동은 2020년 1월 1일 생으로 , 강원도 설빙산에서 태어낫고 그곳에서 호랑이를 잡아 먹으며 성장했습니다.'
    'Python 은 개발 언어중에 가장 쉽다는데 그렇게 쉬운 언어는 아닙니다.'
]

def get_embedding(text):
    response = client.embeddings.create(
        input = text,
        model="text-embedding-ada-002"
    )
    #print(response(docunemt))
    return np.aerra(response.data) 