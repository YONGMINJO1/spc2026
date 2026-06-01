from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent

load_dotenv()

# 우리의 도구를 정의할때 @tool 데코레이터를 정의하고, 함수내에 주석을 쓰면, 그 내용을 읽어가서 본인이 해야할 일을 파악한다.
@tool
def calculator(expression):
    return str (eval(expression))

llm = ChatOpenAI(model="gpt-4o-mini")
agent = create_agent(llm,[calculator]) # 나의 에이전트

result = agent.invoke({
    "messages" : [("user", "(50 * 5 + 5) / 5는 얼마야?")]
})

# print('=== 전체 메시지 흐름 ===')