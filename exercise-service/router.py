from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Modulo, Capitulo
from .schemas import (ModuloCreate , CapituloCreate , ProgresoUser,
                      ModuloResponse, ModuloSchema)
from typing import List
from fastapi import APIRouter
from . database import SessionLocal
import json

 
problems = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db    
    finally:
        db.close()

@problems.get("/api/modulo/{modulo_id}")
def get_modulo(modulo_id:int, db:Session = Depends(get_db)):
    
    db_modulo = db.query(Modulo).filter(Modulo.id == modulo_id).first()
    if db_modulo is None:
        return HTTPException(status_code=404, detail="Modulo no encontrado ")
    
    return db_modulo

@problems.get("/api/modulos/", response_model=List[ModuloSchema])
def get_modulos(db: Session = Depends(get_db)):
    """Obtiene todos los módulos de la base de datos"""
    modulos = db.query(Modulo).all()
    return modulos



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
    print(f"este es el modulo {buscar_modulo}")
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

# @problems.get('/api/progreso/', response_model=ProgresoUser)
# def get_progreso_user()


