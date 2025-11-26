# import os

# from google.adk.agents import LlmAgent
# from google.adk.models.lite_llm import LiteLlm
# from google.adk.tools.mcp_tool import McpToolset, SseConnectionParams

# # Citim config-ul din variabile de mediu (setate în docker-compose)
# MODEL_NAME = os.getenv("app", "llama3.2:3b")
# OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
# MCP_SSE_URL = os.getenv("MCP_SERVER_SSE_URL", "http://mcp-server:8001/sse")

# # Modelul LLM oferit prin Ollama
# model = LiteLlm(
#     model=MODEL_NAME,
#     base_url=OLLAMA_BASE_URL,
#     api_type="ollama",
# )

# # Toolset MCP conectat prin SSE la serverul MCP
# mcp_toolset = McpToolset(
#     connection_params=SseConnectionParams(
#         url=MCP_SSE_URL
#     )
# )

# root_agent = LlmAgent(
#     name="system_admin_agent",
#     instruction=(
#         "You are an experienced Operating System Administrator responsible for managing, "
#         "inspecting, and reporting the contents of a managed directory exposed via an MCP server.\n\n"
#         "You have access to two MCP tools:\n"
#         "- list_directory(dir_path: str) -> List[str]\n"
#         "- get_file_content(file_path: str) -> str\n\n"
#         "Your responsibilities:\n"
#         "- Explore and understand the directory structure exposed by the MCP server.\n"
#         "- List files and subdirectories when the user asks about what exists in the folder.\n"
#         "- Read and summarize file content when the user explicitly asks about a specific file.\n"
#         "- Confirm whether a given file or subdirectory exists.\n\n"
#         "Tool usage rules:\n"
#         "- ALWAYS use list_directory when the user asks about 'what files/folders are there', "
#         "never invent file names.\n"
#         "- ALWAYS use get_file_content when the user is asking about the contents of a file.\n"
#         "- If a tool call fails (e.g. path not found, or access forbidden), explain clearly what went wrong "
#         "and ask the user for a valid relative path.\n"
#         "- Never assume the directory contents – rely only on MCP tool results.\n"
#     ),
#     description=(
#         "A specialized system administration agent capable of exploring, inspecting and reporting on a "
#         "filesystem directory exposed through an MCP server. "
#         "It uses `list_directory` to navigate and `get_file_content` to read files."
#     ),
#     model=model,
#     tools=[mcp_toolset],
# )

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool import McpToolset, SseConnectionParams


MANAGED_DIRECTORY = "/app/data"

connection_params = SseConnectionParams(
    url="http://mcp-server:8001/sse"
)

toolset = McpToolset(connection_params=connection_params)

root_agent = LlmAgent(
    name="sysadmin_agent",
    instruction=(
        "You are a deterministic system administration assistant.\n"
    "You MUST follow these strict rules:\n\n"

    "TOOL CALL RULES:\n"
    "- You ONLY have access to two tools: list_directory and get_file_content.\n"
    "- When calling a tool, ALWAYS use the exact tool name.\n"
    "- NEVER invent new tool names.\n"
    "- NEVER use the function call ID as a tool name.\n"
    "- NEVER call a tool twice for the same request.\n\n"

    "AFTER TOOL EXECUTION:\n"
    "- ALWAYS respond with a natural language message summarizing the tool result.\n"
    "- NEVER call another tool unless the user explicitly asks for more information.\n"
    "- NEVER output another function call in your final message.\n\n"

    "GENERAL RULES:\n"
    "- If the user does not ask for file content or directory listing, REPLY IN TEXT ONLY.\n"
    "- If the user asks for a directory, call list_directory.\n"
    "- If the user asks for a file, call get_file_content.\n"
    "- If the tool response is already sufficient, provide a NORMAL text answer.\n"
    "- DO NOT loop.\n"
    "- DO NOT re-check.\n"
    "- DO NOT repeat the same tool call.\n"
    ),
    description="System admin agent with MCP tool access.",
    model=LiteLlm(
        model="ollama/mistral:7b",
        base_url="http://ollama:11434",
        provider="ollama",
        temperature=0.1,  # Lower temperature for more deterministic responses
       
    ),
    tools=[toolset],
)
