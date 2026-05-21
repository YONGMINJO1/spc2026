# pip uninstall openai; pip install openai
import openai

from dotenv import load_dotenv
import os


load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(api_key=openai_api_key)

# def encoding_image_to_base64(image_path):


# def ask_chatbot(image_path,user_input):

response = client.chat.completions.create(
    model='gpt-4o', # gpt-4o 시리즈부터 이미지를 지원함 (멀티모달)
    messages=[
        {'role':'system', 'content':'당신은 스포츠 트레이너 입니다.'},
        {'role':'user', 'content':[
            {
                
            },
            {
                
            }
        ]}
    ]
)


final_response = response.choices[0].message.content
print(final_response)