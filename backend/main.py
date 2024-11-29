from fastapi import FastAPI
from routes import test_router
from contextlib import asynccontextmanager
from message import init_consumer
import threading

#O PROGRAMA NÃO DÁ SHUTDOWN KKKKKKKKKK
#PENSAR EM UMA SOLUÇÃO
@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = threading.Thread(target=init_consumer)
    thread.start()
    yield
    thread.join()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return "salve"

app.include_router(router=test_router)
