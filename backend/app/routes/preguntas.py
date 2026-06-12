from fastapi import APIRouter
from app.database import SessionLocal
from app.models import Pregunta, Pareja
from datetime import datetime
import random

router = APIRouter()

@router.get("/preguntas")
def obtener_pregunta(user_id: int):

    db = SessionLocal()

    pareja = db.query(Pareja).filter(
        ((Pareja.user1_id == user_id) |
         (Pareja.user2_id == user_id)) &
        (Pareja.estado == "conectados")
    ).first()

    if not pareja:
        return {
            "mensaje": "No tienes pareja conectada"
        }

    nivel = pareja.nivel_relacion

    categorias = ["divertida", "recuerdo"]

    if nivel in [
        "Conexión real ❤️",
        "Química emocional ✨",
        "Confianza creciente 🤝",
        "Relación fuerte 🔥",
        "Vínculo profundo 🌙",
        "Amor consciente 💎",
        "Alma sincronizada 🌌"
    ]:
        categorias.append("gratitud")

    if nivel in [
        "Química emocional ✨",
        "Confianza creciente 🤝",
        "Relación fuerte 🔥",
        "Vínculo profundo 🌙",
        "Amor consciente 💎",
        "Alma sincronizada 🌌"
    ]:
        categorias.append("meta")

    if nivel in [
        "Relación fuerte 🔥",
        "Vínculo profundo 🌙",
        "Amor consciente 💎",
        "Alma sincronizada 🌌"
    ]:
        categorias.append("confianza")

    if nivel in [
        "Amor consciente 💎",
        "Alma sincronizada 🌌"
    ]:
        categorias.append("profunda")
    
    preguntas = db.query(Pregunta).filter(
        Pregunta.categoria.in_(categorias)
    ).all()

    if not preguntas:
        return {
            "mensaje": "No existen preguntas disponibles"
        }

    pregunta = random.choice(preguntas)

    return {
        "pregunta_id": pregunta.id,
        "texto": pregunta.texto,
        "categoria": pregunta.categoria,
        "nivel_actual": nivel
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