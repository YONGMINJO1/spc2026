# pip install yfinance

# 틀들 추가
# 1. 네이버 뉴스를 가져온다
# 2. 구글 검색으로 기업 개요/최증 정보를 조회한다.
# 3. 환율을 조회한다.
# 4. 주가를 조회한다.

import os
import re

import requests
from langchain_core.tools import tool

@tool
def get_news():
    """네이버 뉴스에서 키워드로 최신 기사 제목/링크를 검색한다."""
    # never_cid = os.getenv("NAVER_CLIENT_ID")
    # naver_secret = os.getenv("NAVER_CLIENT_SECRET")

    # resp = requests.get("https://openai.naver.com/v1/search/news.json",
    #                     params={"query": query, "display":5, "sort":"data"},
    #                     headers={"X-Naver-Client"})
    return "미구현"

@tool
def get_comany_info():
    return "미구현"

@tool
def get_exchange_rate(base: str="USD", target: str = "KRW") -> str:
    """base 통화 기준으로 target 통화 환율을 조회한다."""

    url = f"https://open.er-api.com/v6/latest/{base}"
    response = requests.get(url)
    
    data = response.json()
    rate = data["rates"][target]  
    return f"1 {base} = {rate:.2f} {target}"

@tool
def get_stock_price(ticker):
    """yfinance 로 다양한 기업의 주가를 가져온다.
    애플('APPL')과 삼성전자('005930'))"""
    
    import yfinance as yf
    stock = yf.Ticker(ticker) 
    data = yf.Ticker(ticker).history(period="1d")
    price = data["Close"].iloc[-1]
    currency = stock.info.get("currency","USD")
    
    # print(data)
    return f"{ticker} 현재가: {price:.2f} {currency}"

TOOLS = [get_news, get_comany_info, get_exchange_rate, get_stock_price]