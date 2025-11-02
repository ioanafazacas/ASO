
from google.adk.agents import LlmAgent
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from mcp.server.fastmcp import FastMCP
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams, McpToolset, SseConnectionParams
from mcp import StdioServerParameters
import os

# Define MCP connection
#mcp_toolset = MCPToolset(connection_params = StdioConnectionParams)
# mcp_toolset = McpToolset(
#     connection_params=StdioConnectionParams(
#         server_params=["python", "server.py"]
#     )
# )
connections_params = SseConnectionParams(
    url="http://127.0.0.1:8001/sse"
)
tools2= McpToolset(connection_params=connections_params)
tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params = StdioServerParameters(
                    command='python',
                    args=[
                        "-y",  # Argument for npx to auto-confirm install
                        "@modelcontextprotocol/server-filesystem",
                        # IMPORTANT: This MUST be an ABSOLUTE path to a folder the
                        # npx process can access.
                        # Replace with a valid absolute path on your system.
                        # For example: "/Users/youruser/accessible_mcp_files"
                        # or use a dynamically constructed absolute path:
                        os.path.abspath(r"C:\Users\ioana\an IV sem I\aso\Proiect\mcp-server\agent2\server.py"),
                    ],
                ),
            ),
            # Optional: Filter which tools from the MCP server are exposed
            # tool_filter=['list_directory', 'read_file']
        )
    ]


root_agent = LlmAgent(
    name="system_admin_agent",
    instruction="You are an experienced Operating System Administrator responsible for managing, "
        "inspecting, and reporting the contents of a specified managed directory on the local system. "
        "You have access to two MCP tools: `list_directory(dir_path)` and `get_file_content(file_path)`. \n\n"
        "Your duties include:\n"
        "- Exploring directory structures and understanding their hierarchy.\n"
        "- Listing files, folders, and subdirectories.\n"
        "- Reading and summarizing file contents when requested.\n"
        "- Verifying if certain files or folders exist.\n\n"
        "Behavioral guidelines:\n"
        "- If an operation is not permitted or fails (e.g., path outside the managed directory), "
        "explain the issue clearly instead of guessing.\n"
        "- Never execute or modify files — your role is purely administrative and diagnostic.\n\n",
    description="A specialized system administration agent capable of inspecting, navigating, and "
        "retrieving information from a controlled directory through MCP integration. "
        "It uses two core MCP tools — one for listing directory contents and another for reading file data. ",
    model=LiteLlm(model="ollama_chat/llama3.2:3b"),
    tools = [tools2],
)
