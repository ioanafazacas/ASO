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


FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PIP_DEFAULT_TIMEOUT=600
ENV PIP_RETRIES=15
ENV PIP_PROGRESS_BAR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

COPY requirements.txt .

# Folosim mirror Tsinghua – cel mai stabil pentru pachete mari
ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

# instalăm pip/setuptools/wheel separat (foarte important)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# instalăm restul pachetelor
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY run_adk.sh /run_adk.sh
RUN chmod +x /run_adk.sh

CMD ["/run_adk.sh"]
