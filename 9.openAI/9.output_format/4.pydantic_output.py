import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from pydantic import BaseModel

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class CityInfo(BaseModel):
    name: str
    population : int
    area_km2: float

# response = client.chat.completions.create(
response = client.chat.completions.parse( # 파이썬 객체 형태는 parse로 받아야함.
    model="gpt-4o-mini",
    messages=[
        {'role':'system', 'content': '질문에 대해 JSON으로 답하시오.'},
        {'role':'user', 'content': '서울의 인구와 면적을 알려주시오.'},
    ],
    response_format=CityInfo # 파이썬 객체(클래스) 형태로 받을 수 있다
)
# answer = response.choices[0].message.content
answer = response.choices[0].message.parsed
#print(answer)

data = json.loads(answer)
print(f"도시의 이름:  {data.name} - 인구: {data.population:,}명 ,면적 {data.area_km2}km2")