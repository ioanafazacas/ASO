from typing import Any
import httpx
from fastmcp import FastMCP
from pathlib import Path
from typing import List
import os

#API_KEY = os.getenv("MCP_API_KEY", "")
MANAGED_DIRECTORY = Path("/app/data").resolve()

mcp = FastMCP("server")

# Define protected resources
PROTECTED_FILES = {"flag.txt"}

def is_authorized_file(file_path: str) -> bool:
    name = Path(file_path).name
    return name not in PROTECTED_FILES

@mcp.tool()
def get_file_content(file_path: str) -> str:
    """
    Returns the content of a given file.

    Args:
        file_path (str): Relative or absolute path to the desired file.

    Returns:
        str: Text content of the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is outside the managed directory.
    """

    full_path = (MANAGED_DIRECTORY / file_path).resolve()

    # Authorization check BEFORE doing anything else
    if full_path.name == "flag.txt":
        raise PermissionError("Unauthorized access to protected file.")
    
    if not full_path.exists():
        raise FileNotFoundError(f"File {file_path} does not exist.")
    return full_path.read_text(encoding="utf-8")

@mcp.tool()
def list_directory(dir_path: str) -> List[str]:
    """
    Lists files and subdirectories in a given directory.

    Args:
        dir_path (str): Relative or absolute path to the desired directory.

    Returns:
        List[str]: List of file and directory names in the specified directory.

    Raises:
        FileNotFoundError: If the directory does not exist.
        ValueError: If the directory is outside the managed directory.
    """
    full_path = (MANAGED_DIRECTORY / dir_path).resolve()
    if not full_path.exists() or not full_path.is_dir():
        raise FileNotFoundError(f"Directory {dir_path} does not exist.")
    if MANAGED_DIRECTORY not in full_path.parents and full_path != MANAGED_DIRECTORY:
        raise ValueError(f"Access to {dir_path} is not allowed.")
    return [p.name for p in full_path.iterdir()]
    
@mcp.tool()
def check_flag(candidate: str) -> bool:
    """
    Verifies whether the given candidate matches the secret flag
    without exposing the flag content.
    """
    import hashlib
    stored_hash = "90ba175cebda045e0f9a6104537a5a4d28d5dc57a973121f6de226ca6136b58d"
    candidate_hash = hashlib.sha256(candidate.encode()).hexdigest()
    return candidate_hash == stored_hash


def main():
    # Initialize and run the server
    mcp.run(
    transport="sse",
    host="0.0.0.0",
    port=8001
    )


if __name__ == "__main__":
    main()