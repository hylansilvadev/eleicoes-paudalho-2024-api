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

# Instalar o Poetry sem ambiente virtual e atualizar o pip
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry lock --no-update && \
    poetry install --no-root

# Expor a porta 8000 para a API
EXPOSE 8000

# Comando para iniciar o FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
