import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

URL = "http://loaclhost:8000/mcp"

async def main():
    async with streamable_http_client(URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 내가 원하는 코드는 여기서부터 시작..
            tools = (await session.list_tools()).tools
            print("도구: ", [t.name for t in tools]) 