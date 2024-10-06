from bson import ObjectId
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from app.core.database import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("API START")
    
    yield
    
    print("API DOWN")

args = {
    "title": "API ELEICOES PAUDALHO 2024",
    "lifespan":lifespan
}


app = FastAPI(**args)


@app.get(
    path="/"
)
async def root() -> str:
    return f"bem vindo a api das eleições da cidade de paudalho"


@app.get("prefeito/last")
async def get_ultimo_documento():
    try:
        document = await db["eleicoes_data_prefeito"].find_one(sort=[("_id", -1)])
        if document:
            # Converte o ObjectId para string para garantir que é serializável
            document["_id"] = str(document["_id"])
            return document
        else:
            return {"message": "Nenhum documento encontrado"}
    except Exception as e:
        return {"error": str(e)}
    
    
@app.get("vereador/last")
async def get_ultimo_documento():
    try:
        document = await db["eleicoes_data_vereadores"].find_one(sort=[("_id", -1)])
        if document:
            # Converte o ObjectId para string para garantir que é serializável
            document["_id"] = str(document["_id"])
            return document
        else:
            return {"message": "Nenhum documento encontrado"}
    except Exception as e:
        return {"error": str(e)}