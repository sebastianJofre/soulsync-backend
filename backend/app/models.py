from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from datetime import datetime
from sqlalchemy import DateTime
from datetime import datetime


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Pareja(Base):
    __tablename__ = "parejas"

    id = Column(Integer, primary_key=True, index=True)

    user1_id = Column(Integer, ForeignKey("usuarios.id"))
    user2_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)

    codigo = Column(String, unique=True)
    estado = Column(String, default="pendiente")
    
    racha = Column(Integer, default=0)
    ultimo_check = Column(DateTime, default=datetime.utcnow)
    nivel_relacion = Column(String, default="Conociéndose 💫")

class Pregunta(Base):
    __tablename__ = "preguntas"

    id = Column(Integer, primary_key=True, index=True)
    texto = Column(String)
    fecha = Column(DateTime, default=datetime.utcnow)

class Respuesta(Base):
    __tablename__ = "respuestas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuarios.id"))
    pareja_id = Column(Integer, ForeignKey("parejas.id"))
    pregunta_id = Column(Integer, ForeignKey("preguntas.id"))
    respuesta = Column(String)
    fecha = Column(DateTime, default=datetime.utcnow)