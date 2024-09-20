from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Modulo, Capitulo, ProgresoUsuario
from .schemas import *
# from .schemas import (ModuloCreate , CapituloCreate , ProgresoUser,CreateUser,CapituloShema,
#                        ModelQuiz,ModuloSchema)

from fastapi import  HTTPException
from typing import List
from fastapi import APIRouter
from . database import SessionLocal
from .services import verify_token
from datetime import datetime



problems = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@problems.get("/api/modulos/", response_model=List[ModuloSchema])
def get_modulos(db: Session = Depends(get_db)):
    """Obtiene todos los módulos de la base de datos"""
    modulos = db.query(Modulo).all()
    return modulos




@problems.get("/api/modulo/{modulo_id}")
def get_modulo(modulo_id:int, db:Session = Depends(get_db)):

    db_modulo = db.query(Modulo).filter(Modulo.id == modulo_id).first()
    if db_modulo is None:
        return HTTPException(status_code=404, detail="Modulo no encontrado ")
    return db_modulo

@problems.get("/api/quiz/{modulo_id}", response_model=ModelQuiz)
def get_quiz(modulo_id:int, db:Session = Depends(get_db)):

    db_modulo = db.query(Modulo).filter(Modulo.id == modulo_id).first()
    if db_modulo is None:
        return HTTPException(status_code=404, detail="Modulo no encontrado ")
    return db_modulo



@problems.get('/api/capitulos/{capitulo_id}', response_model=CapituloShema)
def get_capitulos_by_id(capitulo_id:int , db:Session = Depends(get_db)):

    db_cap = db.query(Capitulo).filter(Capitulo.id == capitulo_id).first()
    if db_cap is None:
        return HTTPException(status_code=404, detail="capitulo no encontrado ")
    return db_cap




@problems.post("/api/modulo/", response_model=ModuloCreate)
def create_modulo(modulo:ModuloCreate, db:Session = Depends(get_db)):
    """funcion para crear un nuevo modulo"""
    nuevo_modulo = Modulo(
        nombre = modulo.nombre,
        teoria = modulo.teoria,
        quiz = [x.dict() for x in modulo.quiz])

    db.add(nuevo_modulo)
    db.commit()
    db.refresh(nuevo_modulo)

    return nuevo_modulo

@problems.post("/api/capitulo/", response_model=CapituloCreate)
def create_capitulo(capitulo:CapituloCreate, db:Session = Depends(get_db)):
    """funcion para crear un nuevo capitulo"""
    buscar_modulo = db.query(Modulo).filter(Modulo.id == capitulo.modulo_id).first()
    if buscar_modulo is None:
        raise HTTPException(status_code=404, detail="Modulo no encontrado ")

    nuevo_capitulo = Capitulo(
        modulo_id = capitulo.modulo_id,
        nombre_capitulo = capitulo.nombre_capitulo,
        problema = capitulo.problema,
        pista = capitulo.pista,
        solucion = capitulo.solucion)

    db.add(nuevo_capitulo)
    db.commit()
    db.refresh(nuevo_capitulo)

    return nuevo_capitulo


@problems.put('/api/complete/modulo/{id_usuario_externo}/{modulo_id}')
def update_progress_model(id_usuario_externo: int, modulo_id: int, model_update: ModulosCompletados, db: Session = Depends(get_db)):
    """ Función para actualizar el progreso del usuario en módulos completados """
    buscar_user = db.query(ProgresoUsuario).filter(ProgresoUsuario.id_usuario_externo == id_usuario_externo).first()

    if buscar_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    print(model_update)

    buscar_user.modulos_completados = model_update
    # db.commit()

    return buscar_user






@problems.post("/api/capitulo/", response_model=CapituloCreate)
def create_capitulo(capitulo:CapituloCreate, db:Session = Depends(get_db)):
    """funcion para crear un nuevo capitulo"""
    buscar_modulo = db.query(Modulo).filter(Modulo.id == capitulo.modulo_id).first()
    if buscar_modulo is None:
        raise HTTPException(status_code=404, detail="Modulo no encontrado ")

    nuevo_capitulo = Capitulo(
        modulo_id = capitulo.modulo_id,
        nombre_capitulo = capitulo.nombre_capitulo,
        problema = capitulo.problema,
        pista = capitulo.pista,
        solucion = capitulo.solucion)

    db.add(nuevo_capitulo)
    db.commit()
    db.refresh(nuevo_capitulo)

    return nuevo_capitulo


@problems.get('/api/id/{token}')
def token_id(token:str):
    """funcion para obtener el id del usuario usando el token"""
    id_user = verify_token(token=token)
    return int(id_user['sub'])


@problems.get('/api/progreso/{token}', response_model=ProgresoUser)
def get_progreso_user(token:str, db:Session = Depends(get_db)):
    """funcion para poder ver el progreso de un usuario externo al servivio usando el token"""
    id_user = verify_token(token=token)
    id_token = int(id_user['sub'])

    user = db.query(ProgresoUsuario).filter(ProgresoUsuario.id_usuario_externo == id_token).first()
    if user is None:
        raise HTTPException(status_code=404, detail="user no encontrado ")
    return user




@problems.post('/api/create_user/{id_user}', response_model=CreateUser)
def create_user(id_user:int, db:Session = Depends(get_db)):

    new_user = ProgresoUsuario(id_usuario_externo = id_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user










