import base64, requests
from bs4 import BeautifulSoup

from dotenv import load_dotenv

from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")
client = OpenAI()

def fetch_news():
    """뉴스 검색를 가져온다."""
    url = "https://news.goolg.com/res/search"
    prarm = {
        
    }

news_agent = create_agent(
    model=llm,
    tools=(fetch_news),
    system_prompt= """
너는 뉴스 조사 에이전트다.
사영자 주제의 관련된 뉴스 목록를 수집하고,"""
)

# pipeline = (
#     RunnablePassthrough.assign(new=fetch_news)
#     | RunnablePassthrough.assign(summary= summary)
#     | RunnablePassthrough.assign(image_prompt=image_prompt)
#     | RunnablePassthrough.assign(image_path=)
# )

def main():
    story = "잰슨 황 4박 5일 한국 방문 일정"
    # 1. 뉴스를 수집한다.
    news_result = news_result.invoke({
        "message": [
            {"role":"user","content":story}
            ]
    })
    news - news_result("message")
    # 2. 뉴스 요약 및 이미지 생성 프롬프트
    image_prompt = make_image_prompt(news)
    print("\n[이미지 프롬프트]")
    print(news_result)
    # 3. 이미지 생성

if __name__ == "__main__":
    main()