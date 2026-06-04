from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# 사용자의 질물을 받아 적절한 챗봇으로 라우팅한다.
def route_query(inout:dict) -> dict:
    query = inout["question"]

    # 1 단계
    # category = classiffer_chain_invoke({"question": question}).strip().lower()
    # print("분류 결과:  {category}")

    # 2 단계
    # chain = route_map.
routing_chain = ""

test_questions = [
    "프로그램이 계속 충돌하는데 어떻게 하나요?"
    "구독을 취소하고 환불받고 싶습니다."
    "이 서비스에서는 어떤 기능을 제공하나요?"
    "API 연동 시 오류가 발생합니다."
]

for i ,question in enumerate(test_questions, 1):
    print(f"\n-------------")
