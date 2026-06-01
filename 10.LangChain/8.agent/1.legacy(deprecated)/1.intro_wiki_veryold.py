# pip install wikipedia
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent, AgentType

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

tools = load_tools(["wikipedia"])

# 에이전트 초기화
agent = initialize_agent (
    tools = tools,
    llm = llm,
    agent= AgentType.Zero_SHOT_REACT_DESCRIPTION,
    verbose=True
)

result = agent.invoke("인공지능의 역사에 대해 간략히 설명해.")
print(result)