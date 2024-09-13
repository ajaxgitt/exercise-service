from pydantic import BaseModel
from typing import List

# class Pregunta(BaseModel):
#     texto: str
#     opciones: List[str]
#     respuesta_correcta: str
    
    
class ModuloCreate(BaseModel):
    id_user: int
    nombre: str
    teoria: str
    quiz: List 



class CapituloCreate(BaseModel):
    title: str
    problema: str
    solucion: str
    pista: str
    descripcion_code: str
    modulo_id: int
    
    
