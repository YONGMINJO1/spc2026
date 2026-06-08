from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage,SystemMessage

from langgraph.graph import StateGraph, START, END, MessagesState

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

# 그래프 구조
# ┌───────┐
# │ START │ 엣지
# └───┬───┘
#     │
#     ▼
# ┌─────────┐
# │  model  │ 노드
# └───┬─────┘
#     │
#     ▼
# ┌─────┐
# │ END │ 엣지
# └─────┘

# MessagesState는 기본타입 - 여기 MessageState 에는 
graph = StateGraph(state_schema=MessagesState)
# graph = StateGraph(MessagesState)

def call_model(state):
    """LLM 메시지를 전달하고 응답하는 함수"""
    messages = state["messages"]
    system_message = SystemMessage(content="당신은 친절한 AI 비서입니다.")
    all_messages = [system_message] + messages
    
    print("모델 호출 함수 실행중 ... 메시지 수: ", len(messages))
    response = llm.invoke(all_messages)
    print("모델 응답 생성 완료 :", response.content[:50])
    return {"messages" : response}

graph.add_node("model", call_model)
graph.add_edge(START, "model")
graph.add_edge("model", END)

app = graph.compile()

user_input = input("\n 질문을 입력하세요:")
result = app.invoke({"messages": [HumanMessage(content=user_input)]})

for i, message in enumerate(result["messages"]):
    print(f"메시지 {i}: {message.type}-{message.content}")
