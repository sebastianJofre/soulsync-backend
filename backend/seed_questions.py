from app.database import SessionLocal
from app.models import Pregunta

db = SessionLocal()

preguntas = [
    {
        "texto": "¿Cuál fue tu primera impresión de mí?",
        "categoria": "recuerdo",
        "nivel_minimo": "Conociéndose 💫"
    },
    {
        "texto": "¿Cuál es uno de tus recuerdos favoritos de nosotros?",
        "categoria": "recuerdo",
        "nivel_minimo": "Conociéndose 💫"
    }
]

for p in preguntas:

    pregunta = Pregunta(
        texto=p["texto"],
        categoria=p["categoria"],
        nivel_minimo=p["nivel_minimo"]
    )

    db.add(pregunta)

db.commit()

print("Preguntas cargadas")