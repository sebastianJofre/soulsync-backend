from fastapi import APIRouter
from app.database import SessionLocal
from app.models import Pregunta
from datetime import datetime
import random

router = APIRouter()

@router.get("/preguntas")
def obtener_pregunta():
    db = SessionLocal()
    preguntas = db.query(Pregunta).all()

    pregunta = random.choice(preguntas)

    return {
        "pregunta_id": pregunta.id,
        "texto": pregunta.texto
    }

@router.get("/pregunta-del-dia")
def pregunta_del_dia():
    db = SessionLocal()

    hoy = datetime.utcnow().date()

    pregunta = db.query(Pregunta).filter(
        Pregunta.fecha >= hoy
    ).first()

    if not pregunta:
        pregunta = random.choice(db.query(Pregunta).all())

    return {
        "pregunta": pregunta.texto,
        "pregunta_id": pregunta.id
    }