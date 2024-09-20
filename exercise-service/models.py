from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, Text
from sqlalchemy.orm import relationship, Session
from .database import Base, engine
from sqlalchemy import func


class Modulo(Base):
    __tablename__ = "modulos"
    
    id = Column(Integer,primary_key=True, index=True)
    nombre = Column(String(255), unique=True, index=True)
    teoria = Column(Text)
    quiz = Column(JSON, default=[])    
    capitulos = relationship("Capitulo", back_populates="modulo")
    
    
        
class Capitulo(Base):
    __tablename__ = "capitulos"

    id = Column(Integer, primary_key=True)
    modulo_id = Column(Integer, ForeignKey("modulos.id"))
    nombre_capitulo = Column(String(255), index=True)
    problema = Column(Text)
    pista = Column(String(255), index=True)
    descripcion_code = Column(Text)
    solucion = Column(String(255), index=True)
    
    modulo = relationship("Modulo", back_populates="capitulos")


class ProgresoUsuario(Base):
    __tablename__ = "progreso_usuario"
    
    id = Column(Integer, primary_key=True, index=True)
    id_usuario_externo = Column(Integer)  
    modulos_completados = Column(JSON, default=[])  
    capitulos_completados = Column(JSON, default=[])  
    
    
   
    
    

Base.metadata.create_all(bind=engine)