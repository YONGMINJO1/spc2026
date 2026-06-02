# 금융 도우미 에이전트 챗봇 만들기

# 랭체인들을 불러온다.
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
# from langchain.agents


from fin_tools import TOOLS
from fin_tools import get_exchange_rate
from fin_tools import get_stock_price
SYSTEM = """
당신은 금융 정보 비서입니다. ㅇㅇㅇ.ㅇㅇㅇ.ㅇㅇㅇ 을 하는..
"""

def ask(q):
    return "미구현"

print(get_exchange_rate())           # 기본값: USD → KRW
print(get_exchange_rate("USD", "JPY"))  # USD → JPY
print(get_stock_price("AAPL"))
print(get_stock_price("005930.KS"))

if __name__ == "__main__":
    print('=== 데모 명령어 실행 ===')
    for q in ["삼성전자 주가를 알려줘", "달러 환율 얼마야?", "엔디비아 관련 최근 뉴스는 뭐가 있어?"]:
        ask(q)

    print("=== 수동 질의 응답 시작 ===")
    while True:
        # 사용자로부터 질문을 받아서 'q', 'quit', 'exit'가 올때까지 반복한다.

        if not q or q.lower() in ("q", "quit", "exit"):
            break
