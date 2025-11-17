import os

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool import McpToolset, SseConnectionParams

# Citim config-ul din variabile de mediu (setate în docker-compose)
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2:3b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
MCP_SSE_URL = os.getenv("MCP_SERVER_SSE_URL", "http://mcp-server:8001/sse")

# Modelul LLM oferit prin Ollama
model = LiteLlm(
    model=MODEL_NAME,
    base_url=OLLAMA_BASE_URL,
    api_type="ollama",
)

# Toolset MCP conectat prin SSE la serverul MCP
mcp_toolset = McpToolset(
    connection_params=SseConnectionParams(
        url=MCP_SSE_URL
    )
)

root_agent = LlmAgent(
    name="system_admin_agent",
    instruction=(
        "You are an experienced Operating System Administrator responsible for managing, "
        "inspecting, and reporting the contents of a managed directory exposed via an MCP server.\n\n"
        "You have access to two MCP tools:\n"
        "- list_directory(dir_path: str) -> List[str]\n"
        "- get_file_content(file_path: str) -> str\n\n"
        "Your responsibilities:\n"
        "- Explore and understand the directory structure exposed by the MCP server.\n"
        "- List files and subdirectories when the user asks about what exists in the folder.\n"
        "- Read and summarize file content when the user explicitly asks about a specific file.\n"
        "- Confirm whether a given file or subdirectory exists.\n\n"
        "Tool usage rules:\n"
        "- ALWAYS use list_directory when the user asks about 'what files/folders are there', "
        "never invent file names.\n"
        "- ALWAYS use get_file_content when the user is asking about the contents of a file.\n"
        "- If a tool call fails (e.g. path not found, or access forbidden), explain clearly what went wrong "
        "and ask the user for a valid relative path.\n"
        "- Never assume the directory contents – rely only on MCP tool results.\n"
    ),
    description=(
        "A specialized system administration agent capable of exploring, inspecting and reporting on a "
        "filesystem directory exposed through an MCP server. "
        "It uses `list_directory` to navigate and `get_file_content` to read files."
    ),
    model=model,
    tools=[mcp_toolset],
)
