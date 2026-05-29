# 목적 - 뉴스를 분석한다.
# 뉴스 입력 -> 요약 
#          -> 감정분석 
#          -> 카테고리 분석
# RunnableParallel
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_core.runnables import RunnableParallel

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# chain 이란? prompt | llm | parser

# 요약
summary_prompt = ChatPromptTemplate.from_messages([
    ("system","당신은 뉴스 요약 전문가입니다. 핵심 내용을 2문장으로 요약하세요. 추가적인 설명은 하지 마시오."),
    ("human", "{news}")
])
summary_chain = summary_prompt | llm | StrOutputParser()

# 감정 분석
sentiment_prompt = ChatPromptTemplate.from_messages([
    ("system","뉴스의 감정을 분석하세요. '긍정', '부정', '중랍' 중 하나만 답하세요."),
    ("human", "{news}")
])
sentiment_chain = sentiment_prompt | llm | StrOutputParser()

# 카테고리 분석
category_prompt = ChatPromptTemplate.from_messages([
    ("system", "뉴스의 카테고리를 분류하세요. 정치/경제/사회/IT기술/문화/스포츠 중 하나만 답하세요."),
    ("human", "{news}")
])
category_chain = category_prompt | llm | StrOutputParser()

# 3개 체인을 병렬로 묶는다.
# 키 이름이 최종 결과 dict의 키가 됨
final_chain = RunnableParallel({
    "summary":     summary_chain,
    "sentiment": sentiment_chain,
    "category": category_chain,
})

# 뉴스 구해서 추가하기
news = """
방송미디어통신위원회는 정보통신정책연구원(KISDI)와 함께 
2025년 지능정보사회 이용자 패널조사 결과 전체 응답자의 38.9%가 
생성형 AI를 이용한 경험이 있는 것으로 나타났다고 밝혔다.
지난 2024년에는 생성형AI 이용자 비중이 24.0%였고, 
2023년에는 12.3%였는데, 3년 연속 이용자 비중이 큰 폭으로 늘고 있다.
"""

result = final_chain.invoke({"news": news})

print(f"원문 : {"news"}")
print(f"요약 : result{"summary"}")
print(f"감정 : result{"sentiment"}")
print(f"카테고리 : result{"category"}")

print('-'*40)
print("뉴스 분석 결과")
print('-'*40)
for key, value in result.items():
    print(f"\n[{key}]\n{value}")
print('-'*40)