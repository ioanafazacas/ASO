# FROM python:3.12-slim

# WORKDIR /app

# ENV PYTHONUNBUFFERED=1

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# # AGENT_NAME nu e obligatoriu, dar e ok să îl setăm
# ENV AGENT_NAME=app

# CMD ["adk", "web", "--host", "0.0.0.0", "/app"]

#--------------------------------------------------------------------

# FROM python:3.12-slim

# WORKDIR /app

# ENV PYTHONUNBUFFERED=1

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# # add startup script
# COPY run_adk.sh /run_adk.sh
# RUN chmod +x /run_adk.sh

# CMD ["/run_adk.sh"]


FROM python:3.11-slim

WORKDIR /app

# 1) Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# instalăm ADK CLI
RUN pip install --no-cache-dir google-adk

# 2) Put the agent in a subfolder called "agent"
RUN mkdir -p /app/app
COPY agent.py /app/app/agent.py
RUN touch /app/app/_init_.py

# 3) Run ADK Web UI from the parent folder (/app),
#    where each subfolder (here 'agent') is one agent.
CMD ["adk", "web", "--host", "0.0.0.0", "/app"]

