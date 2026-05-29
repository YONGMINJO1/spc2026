# 목적 - 질문 유형에 따라 적합한 항목으로 답변한다
# 질문 유형 -> 배송조회 상담원
#          -> 결제관련 상담원
#          -> 기술지원 상담원
# RunnableBranch
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_core.runnables import RunnableBranch, RunnableLambda

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 질문을 읽고 유형 판단
classifier_prompt = ChatPromptTemplate.from_messages([
    ("system","고객의 질문을 읽고 아래 셋 중 하나로만 분류하세요."
    "배송/결제/기술지원"
    "반드시 이 세 단어 중 하나만 출력하세요. 다른 말은 쓰지 마세요."),
    ("human","{question}")
])

# LCEL (랭체인 익스프레스 랭귀지)
# chain = prompt | llm | parser
classifier_chain = classifier_prompt | llm | StrOutputParser()

# 배송 상담원
delivery_prompt = ChatPromptTemplate.from_messages([
    ("system",
        "당신은 배송 전문 상담원입니다.\n"
        "배송 조회, 배송 지연, 주소 변경 등의 문제를 친절하게 안내하세요."),
    ("human", "{question}")
])
delivery_chain = delivery_prompt | llm | StrOutputParser()

# 결제 상담원
payment_prompt = ChatPromptTemplate.from_messages([
    ("system",
        "당신은 결제 전문 상담원입니다.\n"
        "결제 오류, 환불, 카드 문제 등을 친절하게 안내하세요."),
    ("human", "{question}")
])
payment_chain = payment_prompt | llm | StrOutputParser()

# 기술지원
tech_prompt = ChatPromptTemplate.from_messages([
    ("system",
        "당신은 기술지원 전문 상담원입니다.\n"
        "앱 오류, 로그인 문제, 기능 오작동 등을 친절하게 안내하세요."),
    ("human", "{question}")
])
tech_chain = tech_prompt | llm | StrOutputParser()

branch = RunnableBranch(
    # (조건 함수,  실행할 체인)
    (lambda x: x["type"] == "배송",     delivery_chain),
    (lambda x: x["type"] == "결제",     payment_chain),
    (lambda x: x["type"] == "기술지원", tech_chain),
    # 위 조건 모두 해당 없으면 실행되는 기본 체인
    RunnableLambda(lambda x: "죄송합니다. 해당 문의는 담당자 연결이 필요합니다.")
)

# 분류 결과 + 원래 질문을 dict으로 묶는 함수
def build_input(inputs):
    question = inputs["question"]
    category = classifier_chain.invoke({"question": question}).strip()
    print(f"분류 결과: [{category}] 상담원 연결 중...")
    return {"type": category, "question": question}

# 전체 체인 조립
full_chain = RunnableLambda(build_input) | branch

questions = [
    "주문한 상품이 아직도 안 왔어요. 어디쯤 오고 있나요?",
    "카드 결제가 두 번 된 것 같아요. 확인해주세요.",
    "앱에서 로그인이 계속 튕겨요. 어떻게 해야 하나요?",
    "영업시간이 어떻게 되나요?",   # 기본 케이스 테스트
]

for q in questions:
    print("-" * 40)
    print(f"고객: {q}")
    result = full_chain.invoke({"question": q})
    print(f"상담원: {result}")

print("-" * 40)