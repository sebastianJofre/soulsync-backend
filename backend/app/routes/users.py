from fastapi import APIRouter
from app.schemas import UsuarioCrear
from app.database import SessionLocal
from app.models import Usuario
from app.utils.security import hash_password
from app.utils.security import verify_password
from fastapi import HTTPException
from app.schemas import UsuarioLogin

router = APIRouter()

@router.post("/usuarios")
def crear_usuario(usuario: UsuarioCrear):
    db = SessionLocal()

    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        password=hash_password(usuario.password)
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {
        "mensaje": "Usuario guardado en BD",
        "id": nuevo_usuario.id
    }


@router.post("/login")
def login(usuario: UsuarioLogin):
    db = SessionLocal()

    user = db.query(Usuario).filter(Usuario.email == usuario.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not verify_password(usuario.password, user.password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    return {
        "mensaje": "Login exitoso",
        "user_id": user.id
    }