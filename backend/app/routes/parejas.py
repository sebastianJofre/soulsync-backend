from fastapi import APIRouter
from app.database import SessionLocal
from app.models import Pareja
from fastapi import HTTPException
from datetime import datetime, timedelta
import random
import string

router = APIRouter()

def actualizar_nivel_relacion(pareja):
     
    if pareja.racha >= 100:
        pareja.nivel_relacion = "Alma sincronizada 🌌"

    elif pareja.racha >= 75:
        pareja.nivel_relacion = "Amor consciente 💎"

    elif pareja.racha >= 50:
        pareja.nivel_relacion = "Vínculo profundo 🌙"

    elif pareja.racha >= 30:
        pareja.nivel_relacion = "Relación fuerte 🔥"

    elif pareja.racha >= 21:
        pareja.nivel_relacion = "Confianza creciente 🤝"

    elif pareja.racha >= 14:
        pareja.nivel_relacion = "Química emocional ✨"

    elif pareja.racha >= 7:
        pareja.nivel_relacion = "Conexión real ❤️"

    elif pareja.racha >= 3:
        pareja.nivel_relacion = "Interés mutuo 👀"

    else:
        pareja.nivel_relacion = "Conociéndose 💫"

def generar_codigo():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

#Endpoint generar código
@router.post("/parejas/generar")
def generar_pareja(user_id: int):
    db = SessionLocal()

    pendiente = db.query(Pareja).filter(
        (Pareja.user1_id == user_id) &
        (Pareja.estado == "pendiente")
    ).first()

    if pendiente:
        db.delete(pendiente)
        db.commit()

    # VALIDACIÓN
    pareja_existente = db.query(Pareja).filter(
        ((Pareja.user1_id == user_id) | (Pareja.user2_id == user_id)) &
        (Pareja.estado == "conectados")
    ).first()

    if pareja_existente:
        raise HTTPException(status_code=400, detail="Ya tienes una pareja activa")

    codigo = generar_codigo()

    nueva = Pareja(
        user1_id=user_id,
        codigo=codigo
    )

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return {"codigo": codigo}

#Endpoint para enlazar código
@router.post("/parejas/unirse")
def unirse_pareja(user_id: int, codigo: str):
    db = SessionLocal()

    # VALIDACIÓN
    pareja_existente = db.query(Pareja).filter(
        ((Pareja.user1_id == user_id) | (Pareja.user2_id == user_id)) &
        (Pareja.estado == "conectados")
    ).first()

    if pareja_existente:
        raise HTTPException(status_code=400, detail="Ya estás en una pareja")

    pareja = db.query(Pareja).filter(Pareja.codigo == codigo).first()

    if not pareja:
        raise HTTPException(status_code=404, detail="Código inválido")

    if pareja.user2_id is not None:
        raise HTTPException(status_code=400, detail="Código ya utilizado")

    if pareja.user1_id == user_id:
        raise HTTPException(status_code=400, detail="No puedes unirte a tu propio código")

    pareja.user2_id = user_id
    pareja.estado = "conectados"
    pareja.racha = 1
    pareja.ultimo_check = datetime.utcnow()

    db.commit()

    return {"mensaje": "Pareja conectada exitosamente"}


#Endpoint para la interacción de parejas
@router.post("/parejas/interactuar")
def interactuar(user_id: int):
    db = SessionLocal()

    pareja = db.query(Pareja).filter(
        ((Pareja.user1_id == user_id) | (Pareja.user2_id == user_id)) &
        (Pareja.estado == "conectados")
    ).first()

    if not pareja:
        raise HTTPException(status_code=404, detail="No tienes pareja")

    #  VALIDACIÓN PARA LA PRIMERA VEZ AL UNIRSE
    if pareja.racha == 1 and (datetime.utcnow() - pareja.ultimo_check).seconds < 10:
        return {
            "mensaje": "Primera interacción ❤️",
            "racha": pareja.racha
        }

    #Para cuando pase el primer día de racha 
    ahora = datetime.utcnow()
    diferencia = ahora - pareja.ultimo_check

    if diferencia < timedelta(days=1):
        return {
            "mensaje": "Primera interacción ❤️",
            "racha": pareja.racha,
            "nivel": pareja.nivel_relacion
        }

    elif diferencia < timedelta(days=2):
        pareja.racha += 1
        pareja.ultimo_check = ahora

        actualizar_nivel_relacion(pareja)

    else:
        pareja.racha = 1
        pareja.ultimo_check = ahora

    db.commit()

    return {
        "mensaje": "Interacción registrada ❤️",
        "racha": pareja.racha,
        "nivel": pareja.nivel_relacion
    }