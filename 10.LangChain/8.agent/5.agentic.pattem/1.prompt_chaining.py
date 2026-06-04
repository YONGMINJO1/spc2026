from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()


# [1단계] 리서치 수행중
research_prompt = ChatPromptTemplate.from_template(
    "다음 주제에 대해 핵심 사실 5가지를 간결하게 정리해주세요."
    "\n\n주제: {topic}"
)
#

research_chain = research_prompt | llm | parser

# [2단계] 게이트 검증 수행중
gate_prompt = ChatPromptTemplate.from_template(
    "다음 리서치 결과가 충분한지 YES 또는 NO로 답하세요.\n\n{research}"
)
print("2단계 결과: ", gate_prompt)

gate_chain = gate_prompt | llm | parser
# [3단계] 분석 수행중

# [4단계] 보고서 생성 수행중

def run_chaining_pipeline(topic):
    # 1 단계: 리서치 
    print("[1단계] 리서치 수행중")
    research = research_chain.invoke({"topic":topic})

    # 2 단계: 게이트 검증
    print("[2단계] 게이트 검증 수행중")
    gate_result = gate_result.invoke({"research": research})

    # 3 단계: 분석 수행 
    print("[3단계] 분석 수행중")

    # 4 단계: 보고서 작성 
    print("[4단계] 보고서 생성 수행중")
    return {
        "research":research,
        "gate_result": gate_result
    }


# 질문
# 1. 2026년도 생성형 AI 시장 동향 조사를 해오시오.
topic = "2026년도 생성형 AI 시장 동향 조사를 해오시오,"

result = run_chaining_pipeline(topic)
print(result)