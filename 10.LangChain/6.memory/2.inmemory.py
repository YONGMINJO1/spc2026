from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_messages([
    ("system","당신은 친절한 챗봇입니다."),
    MessagesPlaceholder("histroy"),
    ("user", "{input}"),
])

chain = prompt | llm | StrOutputParser()

history = InMemoryChatMessageHistory()

# 프로세스 종료 시 삭제
def chat(message):
    print(f"질문: {message}")
    answer = chain.invoke({
        "input":message,
        # "histroy":history.messages, # 우리의 저장소에 있는 메시지 그대로 다
        "histroy":history.messages[-10], # 최근 10개의 대화만 기억 
    })
    print(f"답변: {answer}")
    history.add_user_message(message)
    history.add_ai_message(answer)

chat("안녕하세요..")
chat("제 이름은 곽길동입니다.")
chat("저는 겨울에 바닷가에 가서 서핑하는 것을 좋아합니다.")
chat("제 이름과 취미가 뭐라고 했죠?")