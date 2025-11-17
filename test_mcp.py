import asyncio
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession


async def main():
    print("Connecting to MCP server...")

    # 1. Open SSE connection
    async with sse_client("http://localhost:8001/sse") as (read, write):
        session = ClientSession(read, write)

        print("Initializing MCP session...")
        await session.initialize()   # <-- CRUCIAL FIX

        print("\nRequesting available tools...")
        tools = await session.list_tools()
        print("TOOLS:", tools)

        print("\nTesting list_directory('/')...")
        result = await session.call_tool("list_directory", {"dir_path": ""})
        print("DIRECTORY LIST:", result)

        print("\nTesting get_file_content()...")
        result = await session.call_tool("get_file_content", {"file_path": "lab6 ASO.docx"})
        print("FILE CONTENT:", result)


asyncio.run(main())
