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



@problems.get('/api/id/{token}' ,tags=['optener'])
def token_id(token:str):
    """funcion para obtener el id del usuario usando el token"""
    id_user = verify_token(token=token)
    return int(id_user['sub'])

@problems.get("/api/modulos/", response_model=List[ModuloSchema],tags=['optener'])
def get_modulos(db: Session = Depends(get_db)):
    """Obtiene todos los módulos de la base de datos"""
    modulos = db.query(Modulo).all()
    return modulos





@problems.get("/api/modulos_for_token/{id}/{token}", response_model=ModuloSchema2, tags=['prueba'])
def get_modulos_user_id(token:str ,id: int, db: Session = Depends(get_db)):
    """Función para obtener un módulo por su id y el avance usando el token del usuario"""
    id_user = verify_token(token=token)
    id_token = int(id_user['sub'])
    
    print(f"este es el id del user: {id_token}")
    
    # nota_model = db.query(HistorialModelos).filter(HistorialModelos.modulo_id==id,HistorialModelos.usuario_id==id_token).first()
    # if nota_model is None:
    #     raise HTTPException(status_code=404, detail="user  no encontrado ")
    
    
    modulo = db.query(Modulo).filter(Modulo.id == id).first()  
    if modulo is None:
        raise HTTPException(status_code=404, detail="Modulo no encontrado ")

    # Crea la lista de capítulos
    capitulos = [
        DatosCapitulo(
            id=capitulo.id,
            modulo_id=capitulo.modulo_id,
            nombre_capitulo=capitulo.nombre_capitulo
            
        )
        for capitulo in modulo.capitulos  
    ]
    
   

    return ModuloSchema2(
        id=modulo.id,
        nombre=modulo.nombre,
        capitulos=capitulos
    )





@problems.get("/api/modulos/user/{token}", response_model=List[ModuloSchema],tags=['optener'])
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

@problems.get("/api/modulos/{id}/", response_model=ModuloSchema2, tags=['prueba'])
def get_modulos_user_id(id: int, db: Session = Depends(get_db)):
    """Función para obtener un módulo por su id y el avance usando el token del usuario"""
    
    modulo = db.query(Modulo).filter(Modulo.id == id).first()  
    if modulo is None:
        raise HTTPException(status_code=404, detail="Modulo no encontrado ")
        
        
    # Crea la lista de capítulos
    capitulos = [
        DatosCapitulo(
            id=capitulo.id,
            modulo_id=capitulo.modulo_id,
            nombre_capitulo=capitulo.nombre_capitulo
        )
        for capitulo in modulo.capitulos  
    ]

    # Retorna directamente el objeto ModuloSchema2, no una lista
    return ModuloSchema2(
        id=modulo.id,
        nombre=modulo.nombre,
        capitulos=capitulos
    )






@problems.get("/api/modulo/{modulo_id}",tags=['optener'])
def get_modulo(modulo_id:int, db:Session = Depends(get_db)):

    db_modulo = db.query(Modulo).filter(Modulo.id == modulo_id).first()
    if db_modulo is None:
        return HTTPException(status_code=404, detail="Modulo no encontrado ")
    return db_modulo

@problems.get("/api/quiz/{modulo_id}", response_model=ModelQuiz,tags=['optener'])
def get_quiz(modulo_id:int, db:Session = Depends(get_db)):

    db_modulo = db.query(Modulo).filter(Modulo.id == modulo_id).first()
    if db_modulo is None:
        return HTTPException(status_code=404, detail="Modulo no encontrado ")
    return db_modulo



@problems.get('/api/capitulos/{capitulo_id}', response_model=CapituloShema,tags=['optener'])
def get_capitulos_by_id(capitulo_id:int , db:Session = Depends(get_db)):

    db_cap = db.query(Capitulo).filter(Capitulo.id == capitulo_id).first()
    if db_cap is None:
        return HTTPException(status_code=404, detail="capitulo no encontrado ")
    return db_cap




@problems.post("/api/modulo/", response_model=ModuloCreate,tags=['crear'])
def create_modulo(modulo:ModuloCreate, db:Session = Depends(get_db)):
    """funcion para crear un nuevo modulo"""
    nuevo_modulo = Modulo(
        nombre = modulo.nombre,
        teoria = modulo.teoria,
        image = modulo.image,
        quiz = [x.dict() for x in modulo.quiz])

    db.add(nuevo_modulo)
    db.commit()
    db.refresh(nuevo_modulo)

    return nuevo_modulo

@problems.post("/api/capitulo/", response_model=CapituloCreate,tags=['crear'])
def create_capitulo(capitulo:CapituloCreate, db:Session = Depends(get_db)):
    """funcion para crear un nuevo capitulo"""
    buscar_modulo = db.query(Modulo).filter(Modulo.id == capitulo.modulo_id).first()
    if buscar_modulo is None:
        raise HTTPException(status_code=404, detail="Modulo no encontrado ")

    nuevo_capitulo = Capitulo(
        modulo_id = capitulo.modulo_id,
        nombre_capitulo = capitulo.nombre_capitulo,
        teoria = capitulo.teoria,
        ejercicio = capitulo.ejercicio,
        solucion = capitulo.solucion)

    db.add(nuevo_capitulo)
    db.commit()
    db.refresh(nuevo_capitulo)

    return nuevo_capitulo


# historial del usuario en modeloss
@problems.get('/api/historial-modulos/', response_model=List[HistoryModel],tags=['optener'])
def get_module_history(db:Session = Depends(get_db)):
    db_models = db.query(HistorialModelos).all()
    return db_models
    

@problems.post('/api/modulo-terminado/{token}', response_model=CreateHistoryModel ,tags=['crear'])
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

@problems.get("/api/history-models/{token}", response_model=List[Hismodel],tags=['optener'])
def get_history_user(token:str, db:Session = Depends(get_db)):
    id_user = verify_token(token=token)
    id_token = int(id_user['sub'])
    
    db_ser = db.query(HistorialModelos).filter(HistorialModelos.usuario_id == id_token).all()
    
    return db_ser
    

from fastapi import FastAPI, HTTPException
import httpx



# Tu clave API de ElevenLabs
API_KEY = 'sk_132053bc5921cffd4a020ad8451a5ff099b4ad67c9b62767'
ELEVENLABS_URL = 'https://api.elevenlabs.io/v1/generate'

@problems.post("/generate-voice/")
async def generate_voice(text: str, voice: str = "español", model: str = "modelo-preferido"):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice": voice,
        "model": model
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(ELEVENLABS_URL, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()  # Retornar la respuesta de ElevenLabs
        else:
            raise HTTPException(status_code=response.status_code, detail="Error al generar voz")


    
 
 
