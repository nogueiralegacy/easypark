from fastapi import FastAPI
from controller.usuario_router import usuario_router
from controller.placa_router import placa_router
from controller.carro_router import carro_router
from controller.registro_router import registro_router
from controller.view_router import view_router

app = FastAPI(
    title="Easy Park: Estacionar nunca foi tão fácil!",
    description="Documentação das rotas da aplicação"
)


@app.get("/")
def home():
    return "Easy Park: Estacionar nunca foi tão fácil!"


app.include_router(router=usuario_router)
app.include_router(router=placa_router)
app.include_router(router=carro_router)
app.include_router(router=registro_router)
app.include_router(router=view_router)
