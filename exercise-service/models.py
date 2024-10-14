from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy import func
from .database import Base, engine



class HistorialModelos(Base):
    __tablename__ = 'historialModelos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, nullable=False)  
    modulo_id = Column(Integer, ForeignKey("modulos.id"), nullable=False)
    fecha_completado = Column(TIMESTAMP, server_default=func.now(), nullable=True) 
    estado = Column(Boolean, default=False)
    calificacion = Column(Integer, nullable=False)
    
    
    modulo = relationship("Modulo", back_populates="historial", foreign_keys=[modulo_id])

class HistorialCapitulos(Base):
    __tablename__ = 'historialCapitulos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, nullable=False)  
    capitulo_id = Column(Integer, ForeignKey("capitulos.id"), nullable=False)
    fecha_completado = Column(TIMESTAMP, server_default=func.now(), nullable=True) 
    estado = Column(Boolean, default=False)
    # calificacion = Column(Integer, nullable=False) # es obligatorio

    capitulo = relationship("Capitulo", back_populates="historial")

class Modulo(Base):
    __tablename__ = "modulos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), unique=True, index=True)
    teoria = Column(Text)
    quiz = Column(JSON, default=[])
    
    capitulos = relationship("Capitulo", back_populates="modulo")
    historial = relationship("HistorialModelos", back_populates="modulo")


class TestCase(Base):
    __tablename__ = "test_case"

    id = Column(Integer, primary_key=True)
    entrada = Column(String(255)) 
    salida_esperada = Column(String(255))
    exercise_id = Column(Integer, ForeignKey('capitulos.id'))

    exercise = relationship("Capitulo", back_populates="casos_de_prueba")
    
    
class Capitulo(Base):
    __tablename__ = "capitulos"

    id = Column(Integer, primary_key=True)
    modulo_id = Column(Integer, ForeignKey("modulos.id"))
    nombre_capitulo = Column(String(255), index=True)
    problema = Column(Text)
    pista = Column(String(255), index=True)
    descripcion_code = Column(Text)
    solucion = Column(String(255), index=True)
    
    casos_de_prueba = relationship("TestCase", back_populates="exercise", cascade="all, delete-orphan")
    modulo = relationship("Modulo", back_populates="capitulos")
    historial = relationship("HistorialCapitulos", back_populates="capitulo")

Base.metadata.create_all(bind=engine)
