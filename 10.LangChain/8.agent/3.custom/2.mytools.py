from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent

load_dotenv()

@tool
def get_word_length(word: str) -> int:
    """단어을 글자 수를 제어서 숫자로 반환한다."""
    return len(word)

@tool
def calculate_tip(amount:float,percent:float) -> float:
    """음식점 영수증 금액과 팁 비율(%)을 입력 받아서 팁 금액을 계산단다.
    인자값
    """

# @tool
# def search_user(user_id: str) -> dict:
#     """사용자 ID로 사용자 정보를 조회한다. 존재하지 않으면 {} 빈 dict를 반환한다
#     """
#     db = {
#         "u001": {"name":}
#     } 