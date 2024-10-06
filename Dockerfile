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
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Instalar o Poetry sem ambiente virtual e atualizar o pip
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry lock --no-update && \
    poetry install --no-root

# Configurar o supervisord
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expor a porta 8000 para a API
EXPOSE 8000

# Comando para iniciar o supervisord
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
