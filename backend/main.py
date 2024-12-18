from fastapi import FastAPI
from controller.usuario_router import usuario_router

app = FastAPI(
    title="Easy Park: Estacionar nunca foi tão fácil!",
    description="Documentação das rotas da aplicação"
)


@app.get("/")
def home():
    return "Easy Park: Estacionar nunca foi tão fácil!"


app.include_router(router=usuario_router)
