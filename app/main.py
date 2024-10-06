from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager


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