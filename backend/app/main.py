from fastapi import FastAPI
from app.routes.users import router as users_router
from app.database import engine
from app.models import Base
from app.routes.parejas import router as parejas_router
from app.routes.preguntas import router as preguntas_router
from app.routes.respuestas import router as respuestas_router
from app.routes import admin

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users_router)
app.include_router(parejas_router)
app.include_router(preguntas_router)
app.include_router(respuestas_router)
app.include_router(admin.router)

@app.get("/")
def home():
    return {"mensaje": "SoulSync API funcionando correctamente"}