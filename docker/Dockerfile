FROM python:3.9-slim

WORKDIR /app

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r backend/requirements.txt && \
    pip install --no-cache-dir -r frontend/requirements.txt

RUN mkdir -p /app/data/uploads /app/data/vector_db /app/data/knowledge_base

EXPOSE 8000 8501


RUN echo '#!/bin/bash\n\
echo "Starting TalentIntervuAI..."\n\
cd /app/backend && python main.py &\n\
cd /app/frontend && streamlit run main.py --server.port 8501 --server.address 0.0.0.0 &\n\
wait' > /app/start.sh && chmod +x /app/start.sh


CMD ["/app/start.sh"]
