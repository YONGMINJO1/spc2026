from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent

load_dotenv()

@tool
def calculator(expression: str) -> str:

    try:
        # 예외처리를 잘 하지 않으면, LLM에 지멋대로 입력하는 값으로 우리코드가 죽을 수 있음
        return str(eval(expression))
    except Exception as e:
      return f"계산 오류: {e}"
    
llm = ChatOpenAI(model="gpt-4o-mini")
agent = create_agent(llm,[calculator()])

result = agent.invoke