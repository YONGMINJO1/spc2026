from dotenv import load_dotenv

# pip install langchain-anthropic
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm = ChatAnthropic(model= "claude-sonnet-4-6")

template = PromptTemplate.from_template("다음 주제에 대해 설명하시오")

formatted_prompt = template.format(topic = "LLM 기술")
response = llm.invoke(formatted_prompt)
print(response.content)

formatted_prompt = template.format(topic=Transfor)

response = llm.invoke("인공지능에 대해서 설명해주세요.")
print(response.content)

##################################333

# chat_template=