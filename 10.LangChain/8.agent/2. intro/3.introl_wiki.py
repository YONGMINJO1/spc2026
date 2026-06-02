import wikipedia

from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import create_agent

tools = load_tools(["wikipedia"])

llm = ChatOpenAI(model="gat-4o-mini")
agent = create_agent(llm, tools)

result = agent.invoke({"messages": [{"user","파이썬 프로그램밍 언어는 누가 만들었어?"}]})
print(result)