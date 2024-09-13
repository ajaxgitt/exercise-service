from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Modulo, Capitulo
from .schemas import ModuloCreate , CapituloCreate 
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
        

@problems.post("/api/modulo/", response_model=ModuloCreate)
def create_modulo(modulo: ModuloCreate, db: Session = Depends(get_db)):

    
    
    db_modelo = Modulo(
        id_user = modulo.id_user,
        nombre = modulo.nombre,
        teoria = modulo.teoria,
        quiz =  modulo.quiz
        )
    
    db.add(db_modelo)
    db.commit()
    
    return db_modelo



@problems.post("/api/capitulo/", response_model=CapituloCreate)
def create_capitulo(capitulo: CapituloCreate, db: Session = Depends(get_db)):
    # Verifica si la unidad asociada existe
    modulo = db.query(Modulo).filter(Modulo.id == capitulo.modulo_id).first()
    if not modulo:
        raise HTTPException(status_code=404, detail="Modulo not found")

    # Crear un nuevo nivel
    db_capitulo = Capitulo(
        title=capitulo.title,
        problema = capitulo.problema,
        solucion = capitulo.solucion,
        pista = capitulo.pista,
        descripcion_code = capitulo.descripcion_code,
        modulo_id = capitulo.modulo_id
    )
    
    # Añadir el nivel a la base de datos
    db.add(db_capitulo)
    db.commit()
    # db.refresh(db_level)
    
    return db_capitulo

