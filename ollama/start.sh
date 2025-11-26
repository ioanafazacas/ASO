#!/bin/sh
# Start Ollama service and pre-load the model

echo ">>> Starting Ollama service..."
ollama serve &

# Așteaptă puțin până serverul e pregătit
sleep 10

echo ">>> Pulling model llama3.2:3b ..."
ollama pull mistral:7b || echo "Model already exists or failed to pull."

# Menține containerul activ
tail -f /dev/null
