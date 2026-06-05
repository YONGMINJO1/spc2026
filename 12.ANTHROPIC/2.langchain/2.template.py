from dotenv import load_dotenv

# pip install langchain-anthropic
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

load_dotenv()

llm = ChatAnthropic(model= "claude-sonnet-4-6")

template = PromptTemplate.from_template("다음 주제에 대해 설명하시오: {topic}\n\n 답변에 이모지 포함 금지. 글 문제를 AI느낌이 나지 않도록 사람이 쓴 것처럼 최대한 표현해줄 것")

# formatted_prompt = template.format(topic = "LLM 기술")
# response = llm.invoke(formatted_prompt)
# print(response.content)

# formatted_prompt = template.format(topic="Transformer 기술")
# response = llm.invoke(formatted_prompt)
# print(response.content)

# response = llm.invoke("인공지능에 대해서 설명해주세요.")
# print(response.content)

##################################333

chat_template = ChatPromptTemplate.from_messages([
    ("system", "당신은 {role} 전문가입니다. 질문에 자세히 답변해주세요."),
    ("human", "다음 개념에 대해서 설명해주세요: {concept}"),
])

chain = chat_template | llm

response = chain.invoke({"role": "인공지능", "concept": "트랜스포머"})
# response = chain.invoke({"role": "전기", "concept": "트랜스포머"})
print(response.content)