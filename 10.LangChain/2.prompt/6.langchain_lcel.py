import os
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate
)

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("당신은 브랜딩 컨텐츠 기획자 입니다."),
    HumanMessagePromptTemplate.from_template("회사를 홍보하기 위한 {company} 회사의 {product} 상품을 기반으로 캐치프라이즈를 만들어주세요")
])

llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# 아래 체이닝 문법을 LCEL (LangChain Expression Language) 라고 부름
chain = prompt | llm | parser

inputs = {"company":"삼성전자", "product":"메모리"}
messages = prompt.format_messages(**inputs)

result = chain.invoke(inputs)
final_result = {"response": result}
print(final_result)