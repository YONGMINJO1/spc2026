from mcp.server.fastmcp import FastMCP

# mcp = FastMCP("my-http-mcp-server", port=5555)
mcp = FastMCP("my-http-mcp-server") # 기본값은 8000임

@mcp.tool()
def hello(name:str) -> str:
    """사용자에게 인사말을 생성하는 도구
        매게변수:
            name(str) : 인사할 대상의 이름

        반환값:
            str: "Hello, {name}" 형태의 인사말
    """

    return f"Hello, {name}"

@mcp.tool()
def add(a:int, b:int)-> int:
    """ 두 정수 a 와 b를 더한다"""
    return a + b

@mcp.tool()
def now() -> str:
    """현재 시간을 한국어로 포맷하여 반환하는 도구"""
    from datatime import datatime
    return datatime.now().strftime("지금 시간은 %Y-%m-%d %H:%M:%S 입니다.")


if __name__ == "__main__":
    mcp.run(transport="streamable-http")