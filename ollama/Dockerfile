FROM ollama/ollama:latest

WORKDIR /app

# Copiem scriptul de pornire
COPY start.sh .
RUN chmod +x start.sh

# Expunem portul pentru API
EXPOSE 11434

# Înlocuim entrypoint-ul implicit cu shell-ul nostru
ENTRYPOINT ["/bin/sh", "-c", "./start.sh"]
