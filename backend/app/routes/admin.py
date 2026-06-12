from fastapi import APIRouter
from app.database import SessionLocal
from app.models import Pregunta

router = APIRouter()

@router.post("/admin/preguntas")
def crear_pregunta(
    texto: str,
    categoria: str,
    nivel_minimo: str
):
    db = SessionLocal()

    pregunta = Pregunta(
        texto=texto,
        categoria=categoria,
        nivel_minimo=nivel_minimo
    )

    db.add(pregunta)
    db.commit()

    return {"mensaje": "Pregunta creada"}