from motor.motor_asyncio import AsyncIOMotorClient
import requests
from app.core.settings import settings
import asyncio

response = requests.get("https://resultados.tse.jus.br/oficial/ele2024/619/dados/pe/pe25119-z0017-c0011-e000619-u.json")
if response.status_code == 200:
        data = response.json()

# Configurando a conexão com o MongoDB
client = AsyncIOMotorClient(settings.MONGODB_URL)
db = client[settings.DATABASE_NAME]

# Função para salvar os dados na coleção
async def save_data(data):
    try:
        collection = db['eleicoes_data']
        result = await collection.insert_one(data)
        print(f"Dados inseridos com sucesso. ID do documento: {result.inserted_id}")
    except Exception as e:
        print(f"Ocorreu um erro ao inserir os dados: {e}")

# Executando a função de inserção
if __name__ == "__main__":
    asyncio.run(save_data(data))
