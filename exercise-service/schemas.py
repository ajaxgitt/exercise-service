from pydantic import BaseModel
from typing import List

class Pregunta(BaseModel):
    pregunta: str
    opciones: List[str]
    respuesta_correcta: str
    
    
class ModuloCreate(BaseModel):
    nombre: str
    teoria: str
    quiz: List[Pregunta]



class CapituloCreate(BaseModel):
    modulo_id: int
    nombre_capitulo: str
    problema: str
    pista: str
    solucion: str
    
    

class ModuloSchema(BaseModel):
    id: int
    nombre: str
    progreso: float
    capitulos: List[CapituloCreate]
    

    class Config:
        orm_mode = True
        
class ModuloResponse(ModuloCreate):
    id: int
    class Config:
        orm_mode = True
        
class ProgresoUser(BaseModel):
    pass
   
    
    
    
    
