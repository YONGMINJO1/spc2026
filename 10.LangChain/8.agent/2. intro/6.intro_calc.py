# pip install 

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_community.agent_toolkits.load_tools import load_tools

load_dotenv()

llm = ChatOpenAI(model="gpt=-4o-mini")
tools = load_tools(["llm-math"], llm=llm)
agent = create_agent(llm,tools)

result = agent.invoke({"messages"})