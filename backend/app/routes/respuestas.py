from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models import Respuesta, Pareja

router = APIRouter()

@router.post("/responder")
def responder(user_id: int, pregunta_id: int, respuesta: str):
    db = SessionLocal()

    # Buscar pareja
    pareja = db.query(Pareja).filter(
        ((Pareja.user1_id == user_id) | (Pareja.user2_id == user_id)) &
        (Pareja.estado == "conectados")
    ).first()

    if not pareja:
        raise HTTPException(status_code=404, detail="No tienes pareja")

    # Validar si respondió
    respuesta_existente = db.query(Respuesta).filter(
        Respuesta.user_id == user_id,
        Respuesta.pregunta_id == pregunta_id
    ).first()

    if respuesta_existente:
        raise HTTPException(status_code=400, detail="Ya respondiste esta pregunta")

    # Crear respuesta
    nueva_respuesta = Respuesta(
        user_id=user_id,
        pareja_id=pareja.id,
        pregunta_id=pregunta_id,
        respuesta=respuesta
    )

    db.add(nueva_respuesta)
    db.commit()

    # Revisar si ambos respondieron
    respuestas = db.query(Respuesta).filter(
        Respuesta.pareja_id == pareja.id,
        Respuesta.pregunta_id == pregunta_id
    ).all()

    if len(respuestas) == 2:
        return {
            "mensaje": "Ambos respondieron 💙",
            "detalle": "Pueden ver sus respuestas"
        }

    return {
        "mensaje": "Respuesta guardada ❤️"
    }
