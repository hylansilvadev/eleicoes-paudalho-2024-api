# Usar uma imagem base oficial do Python
FROM python:3.12-slim

# Definir o diretório de trabalho na imagem
WORKDIR /app

# Copiar os arquivos do projeto para o contêiner
COPY . /app

# Instalar dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar as dependências do projeto usando Poetry
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root

# Expor a porta 8000 para a API
EXPOSE 8000

# Comando para iniciar o FastAPI e o Celery
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 & celery -A celery_app worker --loglevel=info & celery -A celery_app beat --loglevel=info"]