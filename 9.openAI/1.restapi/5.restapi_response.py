import os
import requests
from dotenv import load_dotenv

load_dotenv() # 내가 읽어갈 경로를 지정가능

openai_api_key = os.getenv('OPENAI_API_KEY')

user_input = '대한민국의 수도는 어디야?'

respnse = requests.post(
    #"http://api.openai.com/api/v1/chat/competions"
    "http://api.openai.com/api/v1/responses",
    
    header = {
        'Content-Type': "application/json",
        'Authorizstion': f'Bearer {openai_api_key}'
    },
    body = {
        'model': 'get-4o-mini',
        'input' : user_input,
    }
)

data = respnse.json()
print(data)
print('-'*30)
answer = data['output'][0]['content'][0]['text']
print('응답: ', answer)
print('응답ID: ', data['id']) 