from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Modulo, Capitulo, HistorialModelos
from .schemas import *


from fastapi import  HTTPException
from typing import List
from fastapi import APIRouter
from .services import verify_token



problems = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@problems.get('/api/id/{token}')
def token_id(token:str):
    """funcion para obtener el id del usuario usando el token"""
    id_user = verify_token(token=token)
    return int(id_user['sub'])

@problems.get("/api/modulos/", response_model=List[ModuloSchema])
def get_modulos(db: Session = Depends(get_db)):
    """Obtiene todos los módulos de la base de datos"""
    modulos = db.query(Modulo).all()
    return modulos


@problems.get("/api/modulos/user/{token}", response_model=List[ModuloSchema])
def get_modulos_user(token: str, db: Session = Depends(get_db)):
    """funcion para obtener a todos los modelos y el avance usando el token del usuario"""
    
    id_user = verify_token(token=token)
    id_token = int(id_user['sub'])
    
    modulos = db.query(Modulo).all()  
    
    result = []
    for modulo in modulos:
        historial_usuario = [
            Hismodel2(
                usuario_id=histo.usuario_id,
                fecha_completado=histo.fecha_completado,
                estado=histo.estado,
                calificacion=histo.calificacion
            )
            for histo in modulo.historial if histo.usuario_id == id_token
        ]
        
        capitulos = [
            DatosCapitulo(
                id = capitulo.id,
                modulo_id= capitulo.modulo_id,
                nombre_capitulo= capitulo.nombre_capitulo
            )
            for capitulo in modulo.capitulos  
        ]


        result.append(ModuloSchema(
            id=modulo.id,
            nombre=modulo.nombre,
            historial=historial_usuario,
            capitulos=capitulos
        ))

    return result





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


# historial del usuario en modeloss


@problems.get('/api/historial-modulos/', response_model=List[HistoryModel])
def get_module_history(db:Session = Depends(get_db)):
    db_models = db.query(HistorialModelos).all()
    return db_models
    

@problems.post('/api/modulo-terminado/{token}', response_model=CreateHistoryModel)
def create_module_history(historial:CreateHistoryModel,token:str, db:Session = Depends(get_db)):
    """funcion para crear un historial de usuario"""
    id_user = verify_token(token=token)
    id_token = int(id_user['sub'])
    
    histo = db.query(HistorialModelos).filter(
    HistorialModelos.usuario_id == id_token,
    HistorialModelos.modulo_id == historial.modulo_id,
    HistorialModelos.estado == True
    ).first()

    if histo:
        raise HTTPException(status_code=400, detail="Ya resolviste este Quiz")

    nuevo_historial = HistorialModelos(
        usuario_id = id_token,
        modulo_id = historial.modulo_id,
        estado = historial.estado,
        calificacion = historial.calificacion
    )
    
    db.add(nuevo_historial)
    db.commit()
    db.refresh(nuevo_historial)
    
    return nuevo_historial

@problems.get("/api/history-models/{token}", response_model=List[Hismodel])
def get_history_user(token:str, db:Session = Depends(get_db)):
    id_user = verify_token(token=token)
    id_token = int(id_user['sub'])
    
    db_ser = db.query(HistorialModelos).filter(HistorialModelos.usuario_id == id_token).all()
    
    return db_ser
    
    
 
 
