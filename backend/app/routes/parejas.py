from fastapi import APIRouter
from app.database import SessionLocal
from app.models import Pareja, EstadisticaPareja
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

    estadistica = EstadisticaPareja(
        pareja_id=pareja.id
    )

    db.add(estadistica)

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


@router.get("/parejas/estadisticas/{pareja_id}")
def obtener_estadisticas(pareja_id: int):

    db = SessionLocal()

    estadistica = db.query(
        EstadisticaPareja
    ).filter(
        EstadisticaPareja.pareja_id == pareja_id
    ).first()

    if not estadistica:
        return {"mensaje": "No existen estadísticas"}

    return {
        "preguntas_respondidas": estadistica.preguntas_respondidas,
        "conversaciones_profundas": estadistica.conversaciones_profundas,
        "agradecimientos": estadistica.agradecimientos,
        "metas_compartidas": estadistica.metas_compartidas,
        "recuerdos_guardados": estadistica.recuerdos_guardados,
        "logros_desbloqueados": estadistica.logros_desbloqueados,
        "compatibilidad": estadistica.compatibilidad
    }

#Historia
@router.get("/parejas/historia/{pareja_id}")
def obtener_historia(pareja_id: int):

    db = SessionLocal()

    pareja = db.query(
        Pareja
    ).filter(
        Pareja.id == pareja_id
    ).first()

    if not pareja:
        raise HTTPException(
            status_code=404,
            detail="Pareja no encontrada"
        )

    estadistica = db.query(
        EstadisticaPareja
    ).filter(
        EstadisticaPareja.pareja_id == pareja_id
    ).first()

    if not estadistica:
        raise HTTPException(
            status_code=404,
            detail="Estadísticas no encontradas"
        )

    return {
        "nivel_relacion": pareja.nivel_relacion,
        "racha": pareja.racha,
        "preguntas_descubiertas": estadistica.preguntas_respondidas,
        "conversaciones_profundas": estadistica.conversaciones_profundas,
        "agradecimientos": estadistica.agradecimientos,
        "metas_compartidas": estadistica.metas_compartidas,
        "recuerdos_guardados": estadistica.recuerdos_guardados,
        "logros_desbloqueados": estadistica.logros_desbloqueados,
        "actos_confianza": estadistica.actos_confianza,
    }

#Resumen Semanal
@router.get("/parejas/resumen-semanal/{pareja_id}")
def resumen_semanal(pareja_id: int):

    db = SessionLocal()

    estadistica = db.query(
        EstadisticaPareja
    ).filter(
        EstadisticaPareja.pareja_id == pareja_id
    ).first()

    if not estadistica:
        return {
            "mensaje": "No existen estadísticas"
        }

    return {
        "mensaje": "Resumen semanal ❤️",

        "preguntas": estadistica.preguntas_respondidas,

        "profundas": estadistica.conversaciones_profundas,

        "agradecimientos": estadistica.agradecimientos,

        "recuerdos": estadistica.recuerdos_guardados,

        "metas": estadistica.metas_compartidas,

        "confianza": estadistica.actos_confianza,

        "logros": estadistica.logros_desbloqueados
    }