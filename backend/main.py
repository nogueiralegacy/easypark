from fastapi import FastAPI
from routes import test_router

app = FastAPI(
    title="Easy Park",
    description="Documentação das rotas da aplicação"
)

@app.get("/")
def home():
    return "Easy Park: Estacionar nunca foi tão fácil!"

app.include_router(router=test_router)
