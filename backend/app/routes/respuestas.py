from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models import (Respuesta, Pareja, Pregunta, EstadisticaPareja, Logro)

router = APIRouter()

def crear_logro(db, pareja_id, codigo, titulo, descripcion):

    logro_existente = db.query(Logro).filter(
        Logro.pareja_id == pareja_id,
        Logro.codigo == codigo
    ).first()

    if logro_existente:
        return False

    nuevo_logro = Logro(
        pareja_id=pareja_id,
        codigo=codigo,
        titulo=titulo,
        descripcion=descripcion
    )

    db.add(nuevo_logro)

    return True

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

    # Se revisa si ambos respondieron
    respuestas = db.query(Respuesta).filter(
        Respuesta.pareja_id == pareja.id,
        Respuesta.pregunta_id == pregunta_id
    ).all()

    if len(respuestas) == 2:

        estadistica = db.query(
            EstadisticaPareja
        ).filter(
            EstadisticaPareja.pareja_id == pareja.id
        ).first()

        pregunta = db.query(
            Pregunta
        ).filter(
            Pregunta.id == pregunta_id
        ).first()

        # Estadística general
        estadistica.preguntas_respondidas += 1

        # Estadísticas por categoría
        if pregunta.categoria == "recuerdo":
            estadistica.recuerdos_guardados += 1

        elif pregunta.categoria == "gratitud":
            estadistica.agradecimientos += 1

        elif pregunta.categoria == "meta":
            estadistica.metas_compartidas += 1

        elif pregunta.categoria == "profunda":
            estadistica.conversaciones_profundas += 1

        elif pregunta.categoria == "confianza":
            estadistica.actos_confianza += 1

# LOGROS DE DESCUBRIMIENTO
        if estadistica.preguntas_respondidas >= 1:

            if crear_logro(
                db,
                pareja.id,
                "KNOW_1",
                "🌱 Comenzando la historia",
                "Toda gran conexión comienza con una pregunta."
            ):
                estadistica.logros_desbloqueados += 1

        if estadistica.preguntas_respondidas >= 5:

            if crear_logro(
                db,
                pareja.id,
                "KNOW_5",
                "🧩 Primeras piezas",
                "Han comenzado a descubrir quiénes son realmente."
            ):
                estadistica.logros_desbloqueados += 1

        if estadistica.preguntas_respondidas >= 15:

            if crear_logro(
                db,
                pareja.id,
                "KNOW_15",
                "❤️ Conociéndonos mejor",
                "Cada respuesta revela una nueva parte de su historia."
            ):
                estadistica.logros_desbloqueados += 1

        if estadistica.preguntas_respondidas >= 25:

            if crear_logro(
                db,
                pareja.id,
                "KNOW_25",
                "🌟 Exploradores del alma",
                "Han ido más allá de la superficie y siguen descubriéndose."
            ):
                estadistica.logros_desbloqueados += 1


        # ==================================
        # LOGROS EMOCIONALES
        # ==================================

        if estadistica.recuerdos_guardados >= 1:

            if crear_logro(
                db,
                pareja.id,
                "MEMORY_BOOK",
                "📸 Primer recuerdo guardado",
                "Han comenzado a construir su historia."
            ):
                estadistica.logros_desbloqueados += 1

        if estadistica.conversaciones_profundas >= 1:

            if crear_logro(
                db,
                pareja.id,
                "DEEP_TALK",
                "🌙 Primera conversación profunda",
                "Se han abierto emocionalmente."
            ):
                estadistica.logros_desbloqueados += 1

        if estadistica.agradecimientos >= 7:

            if crear_logro(
                db,
                pareja.id,
                "GRATITUDE_7",
                "🌷 Semana de gratitud",
                "La gratitud fortalece las relaciones duraderas."
            ):
                estadistica.logros_desbloqueados += 1

        if estadistica.actos_confianza >= 5:

            if crear_logro(
                db,
                pareja.id,
                "SAFE_PLACE",
                "🕊️ Refugio emocional",
                "Han construido un espacio seguro para compartir emociones."
            ):
                estadistica.logros_desbloqueados += 1
        
        if estadistica.metas_compartidas >= 3:

            if crear_logro(
                db,
                pareja.id,
                "SHARED_DREAM",
                "🚀 Sueño compartido",
                "Han comenzado a construir una visión de futuro juntos."
            ):
                estadistica.logros_desbloqueados += 1

        if estadistica.conversaciones_profundas >= 5:
            if crear_logro(
                db,
                pareja.id,
                "OPEN_HEART",
                "💎 Corazón abierto",
                "Han compartido conversaciones que fortalecen profundamente su conexión."
            ):
                estadistica.logros_desbloqueados += 1

        db.commit()

        return {
            "mensaje": "Ambos respondieron 💙",
            "detalle": "Pueden ver sus respuestas"
        }

    return {
        "mensaje": "Respuesta guardada ❤️"
    }


# Logros
@router.get("/logros/{pareja_id}")
def obtener_logros(pareja_id: int):

    db = SessionLocal()

    logros = db.query(Logro).filter(
        Logro.pareja_id == pareja_id
    ).all()

    return [
        {
            "codigo": logro.codigo,
            "titulo": logro.titulo,
            "descripcion": logro.descripcion,
            "fecha": logro.fecha
        }
        for logro in logros
    ]