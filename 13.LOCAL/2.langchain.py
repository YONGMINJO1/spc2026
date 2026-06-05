# pip install langchain-openai langchain-anthropic
# pip install langchain-ollama

from langchain_ollama import ChatOllama

llm= ChatOllama(model="mistral")

response = llm.invoke("안녕? 한마디로 너를 소개해")
print(response.content)