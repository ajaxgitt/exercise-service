from pydantic import BaseModel
from typing import List
from datetime import datetime


class Pregunta(BaseModel):
    pregunta: str
    opciones: List[str]
    respuesta_correcta: str
    
class Pregunta2(BaseModel):
    respuesta_correcta: str
    
class ModelQuiz(BaseModel):
    quiz: List[Pregunta2]
    


class DatosModel(BaseModel):
    modulo_id: int
    completado: bool
    fecha: str  

    @classmethod
    def create(cls, modulo_id: int, completado: bool):
        return cls(
            modulo_id=modulo_id,
            completado=completado,
            fecha=datetime.now().isoformat()  
        )

class ModulosCompletados(BaseModel):
    datos: List[DatosModel]  



    
    
class ModuloCreate(BaseModel):
    nombre: str
    teoria: str
    quiz: List[Pregunta]


class CapituloShema(BaseModel):
    id:int
    modulo_id: int
    nombre_capitulo: str
    problema: str
    pista: str
    solucion: str
    
class CapituloCreate(BaseModel):
    modulo_id: int
    nombre_capitulo: str
    problema: str
    pista: str
    solucion: str
    


class CapituloShema(BaseModel):
    id:int
    modulo_id: int
    nombre_capitulo: str
    problema: str
    pista: str
    solucion: str



class ModuloSchema(BaseModel):
    id: int
    nombre: str
    capitulos: List[CapituloShema]
    
    class Config:
        orm_mode = True
        

        
class ModuloResponse(ModuloCreate):
    id: int
    class Config:
        orm_mode = True
        
class CreateUser(BaseModel):
    id: int
    id_usuario_externo: int
   



class ProgresoUser(BaseModel):
    id: int
    id_usuario_externo: int
    modulos_completados : List[ModuloSchema]
    capitulos_completados : List[ModuloSchema]
    
    
    
    
    
class ModuloSchemaid(BaseModel):
    quiz: List[Pregunta]
    
    