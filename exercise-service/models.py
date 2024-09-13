from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, Text
from sqlalchemy.orm import relationship
from .database import Base, engine

class Modulo(Base):
    __tablename__ = "modulos"
    
    id = Column(Integer,primary_key=True, index=True)
    nombre = Column(String(255), unique=True, index=True)
    id_user = Column(Integer, index=True) 
    teoria = Column(Text)
    quiz = Column(JSON, default=[])
    completado = Column(Boolean, default=False)
    
    
    
    
    capitulos = relationship("Capitulo", back_populates="modulo")

class Capitulo(Base):
    __tablename__ = "capitulos"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), index=True)
    problema = Column(Text)
    solucion = Column(String(255), index=True)
    pista = Column(String(255), index=True)
    descripcion_code = Column(Text)
    modulo_id = Column(Integer, ForeignKey("modulos.id"))
    completado = Column(Boolean, default=False)
    

    modulo = relationship("Modulo", back_populates="capitulos")

Base.metadata.create_all(bind=engine)
