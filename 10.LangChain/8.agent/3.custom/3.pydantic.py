import json

from typing import Literal
from pydantic import BaseModel,Field

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent

load_dotenv()

class SendEmailInput(BaseModel):
    """이메일 전송 도구의 인자"""
    to: str = Field(description="수신자 이메일 주소(반즈기 유효한 이메일 형식)")
    subject: str = Field(description="이메일 제목 (50자 이내, 간결하게)")
    body: str = Field(description="이메일 본문 (반드시 한국어로 작성)")
    priority: Literal["low","normal","high"] = Field(default="normal",description="우선순위, urgent한 경우 high 사용")

# @tool(args_schema=SendEmailInput)

class SearchInput(BaseModel):
    """검색 도구의 인자"""
    query: str = Field(description="검색어")
    max_result: int = Field(default=5, ge=1, le=20, description="결과 갯수 (1~20)")

    sort_by : Literal["relevance","data"] = Field(default="relevence", description="정렬 기준, 최진 정보가 중요하면 data 사용")

# @tool(args_schema=SearchInput)

llm = ChatOpenAI(model="gpt-4o-mini")
# llm_with_tools = llm.bind_tools([send_emall, search])