#!/bin/bash

# =============================
#  ADK WEB – RUNNER UNIVERSAL
# =============================

APP_DIR="/app"
CONFIG="$APP_DIR/adk_config.yml"
AGENT="$APP_DIR/agent.py"

echo "=== Checking project structure ==="

if [ ! -f "$AGENT" ]; then
  echo "❌ ERROR: agent.py not found at $AGENT"
  exit 1
else
  echo "✔ agent.py found"
fi

if [ ! -f "$CONFIG" ]; then
  echo "❌ ERROR: adk_config.yml not found at $CONFIG"
  exit 1
else
  echo "✔ adk_config.yml found"
fi

echo "=== Checking root_agent existence ==="
if ! grep -q "root_agent" "$AGENT"; then
  echo "❌ ERROR: No 'root_agent' symbol exported in agent.py"
  exit 1
else
  echo "✔ root_agent exported"
fi

echo "=== Exporting environment variables for ADK ==="

export MODEL_NAME="llama3.2:3b"
export OLLAMA_BASE_URL="http://ollama:11434"
export MCP_SERVER_SSE_URL="http://mcp-server:8001/sse"

echo "MODEL_NAME=$MODEL_NAME"
echo "OLLAMA_BASE_URL=$OLLAMA_BASE_URL"
echo "MCP_SERVER_SSE_URL=$MCP_SERVER_SSE_URL"

echo "=== Running ADK Web ==="

# ADK expects to receive the **folder containing adk_config.yml**
cd $APP_DIR

# Start ADK Web on all interfaces
exec adk web --host 0.0.0.0 "$APP_DIR"
