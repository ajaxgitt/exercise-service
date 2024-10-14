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
    



#schema para crear un nuevo modulo    
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
    
    

#schema para crear un nuevo capitulo
class CapituloCreate(BaseModel):
    modulo_id: int
    nombre_capitulo: str
    problema: str
    pista: str
    solucion: str
    


class CapituloShema(BaseModel):
    modulo_id: int
    nombre_capitulo: str
    problema: str
    pista: str
    solucion: str





        
class ModuloResponse(ModuloCreate):
    id: int
    class Config:
        orm_mode = True
        
        

class DatosModelo(BaseModel):
    modulo_id: int
    completado: bool


class DatosCapitulo(BaseModel):
    id : int
    modulo_id: int
    nombre_capitulo: str
    


    
    
    
class ModuloSchemaid(BaseModel):
    quiz: List[Pregunta]
    
    
# schema para verificar los modulos terminados
class HistoryModel(BaseModel):
    usuario_id:int 
    modulo_id: int
    fecha_completado: datetime
    estado: bool
    calificacion:int
    
    
# schema para crear los modulos terminados
class CreateHistoryModel(BaseModel):
    modulo_id: int
    estado: bool
    calificacion : int
    
    
#historial modelos id

class Hismodel(BaseModel):
    modulo_id : int
    usuario_id : int
    fecha_completado : datetime
    estado : bool
    calificacion : int
    
    class Config:
        orm_mode = True
        
class Hismodel2(BaseModel):
    usuario_id : int
    fecha_completado : datetime
    estado : bool
    calificacion : int
    
    class Config:
        orm_mode = True
    
    
class ModuloSchema(BaseModel):
    id: int
    nombre: str
    historial:List[Hismodel2]
    capitulos: List[DatosCapitulo]
    
    class Config:
        orm_mode = True
        
class ModuloSchema2(BaseModel):
    id: int
    nombre: str
    capitulos: List[DatosCapitulo]
    
    class Config:
        orm_mode = True

