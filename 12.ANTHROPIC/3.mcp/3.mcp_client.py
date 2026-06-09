import asyncio

from mcp import clientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(command="python", args="2.mcp_server.py")

    async with stdio_client(server_params) as (read, write):
        async with clientSession(read, write) as session:
            # 아래 코드를 통해서 서버/ 클라 간에 handsshake 가 이루어짐
            await session.initialize()

            # 여기서부터 실제로 내가 서버에 호출하고 싶은 코드를 작성
            result = await session.call_tool("hello",{"name":"john"})
            print(result.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())