from bson import ObjectId
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.concurrency import asynccontextmanager

from app.core.database import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("API START")
    
    yield
    
    print("API DOWN")

args = {
    "title": "API ELEICOES PAUDALHO 2024",
    "lifespan": lifespan
}

app = FastAPI(**args)


@app.get(
    path="/"
)
async def root() -> str:
    return f"bem vindo a api das eleições da cidade de paudalho"


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            acao = data.get("acao")
            if acao == "receber_prefeito":
                document = await db["eleicoes_data_prefeitos"].find_one(sort=[("_id", -1)])
                if document:
                    document["_id"] = str(document["_id"])
                    await websocket.send_json(document)
                else:
                    await websocket.send_json({"message": "Nenhum documento encontrado"})
            elif acao == "receber_vereador":
                document = await db["eleicoes_data_vereadores"].find_one(sort=[("_id", -1)])
                if document:
                    document["_id"] = str(document["_id"])
                    await websocket.send_json(document)
                else:
                    await websocket.send_json({"message": "Nenhum documento encontrado"})
            else:
                await websocket.send_json({"error": "Ação desconhecida"})
    except WebSocketDisconnect:
        print("WebSocket desconectado")
    except Exception as e:
        await websocket.send_json({"error": str(e)})