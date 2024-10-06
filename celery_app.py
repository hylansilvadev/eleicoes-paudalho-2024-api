from celery import Celery
from celery.schedules import crontab
from motor.motor_asyncio import AsyncIOMotorClient
import requests
import asyncio
from app.core.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import nest_asyncio
from bs4 import BeautifulSoup
import time
import random

# Aplicar o patch do nest_asyncio para permitir loops aninhados
nest_asyncio.apply()

# Configurando Celery para usar SQLite como broker e backend
celery_app = Celery(
    'tasks',
    broker='sqla+sqlite:///celery_broker.sqlite',
    backend='db+sqlite:///celery_backend.sqlite'
)

celery_app.conf.update(
    broker_connection_retry_on_startup=True,
    worker_concurrency=1,  # Importante para SQLite
    task_acks_late=True,
    worker_prefetch_multiplier=1
)

# Configuração do Celery Beat
celery_app.conf.beat_schedule = {
    "fetch-and-save-prefeitos-every-two-minutes": {
        "task": "fetch_and_save_data_prefeitos",
        "schedule": crontab(minute="*/2"),
    },
    "fetch-and-save-vereadores-every-two-minutes": {
        "task": "fetch_and_save_data_vereadores",
        "schedule": crontab(minute="*/2"),
    },
}
celery_app.conf.timezone = 'UTC'

# Configuração do SQLAlchemy para o SQLite
engine = create_engine('sqlite:///celery_results.sqlite')
Session = sessionmaker(bind=engine)

# Função para criar uma nova conexão MongoDB
def get_mongodb_client():
    return AsyncIOMotorClient(
        settings.MONGODB_URL,
        tls=True,
        # Ignora verificação de certificado SSL para testes
        tlsAllowInvalidCertificates=True
    )

@celery_app.task(name="fetch_and_save_data_vereadores")
def fetch_and_save_data_vereadores():
    return fetch_and_save_data(settings.URL_VEREADORES, "eleicoes_data_vereadores")

@celery_app.task(name="fetch_and_save_data_prefeitos")
def fetch_and_save_data_prefeitos():
    return fetch_and_save_data(settings.URL_PREFEITO, "eleicoes_data_prefeitos")

def fetch_and_save_data(url, collection_name):
    try:
        response = make_request_with_retry(url)
        if response.status_code == 200:
            data = response.json()

            # Usar asyncio.run() para executar a corrotina assíncrona
            result = asyncio.run(save_data_to_mongodb(data, collection_name))

            return result
        else:
            print(f"Erro ao obter os dados: {response.status_code}")
            return None
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        import traceback
        traceback.print_exc()
        return None

def make_request_with_retry(url, max_retries=5):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    retries = 0
    while retries < max_retries:
        response = requests.get(url, headers=headers)
        if response.status_code == 429:
            print("Recebido erro 429 - Too Many Requests. Aguardando antes de tentar novamente...")
            time.sleep(random.uniform(1, 5))  # Espera de 1 a 5 segundos antes de tentar novamente
            retries += 1
        else:
            return response
    raise Exception(f"Máximo de tentativas alcançado ao tentar acessar {url}")

async def save_data_to_mongodb(data, collection_name):
    client = get_mongodb_client()
    try:
        db = client[settings.DATABASE_NAME]
        collection = db[collection_name]
        result = await collection.insert_one(data)
        print(f"Dados inseridos com sucesso. ID do documento: {result.inserted_id}")
        return str(result.inserted_id)
    except Exception as e:
        print(f"Ocorreu um erro ao inserir os dados no MongoDB: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        client.close()