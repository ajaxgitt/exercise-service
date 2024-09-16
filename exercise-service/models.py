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
    progreso = Column(Integer, default=0)
    capitulos = relationship("Capitulo", back_populates="modulo")
    progreso_usuario = relationship("ProgresoUsuario", back_populates="modulo")
    
    def cap_completados(self, db:Session) -> bool:
        total_capitulos = db.query(func.count(Capitulo.id)).filter(Capitulo.modulo_id == self.id).scalar()
        capitulos_completados = db.query(func.count(Capitulo.id)).filter(Capitulo.modulo_id == self.id, Capitulo.completado == True).scalar()
        return total_capitulos == capitulos_completados
    
    def progreso_user(self, db:Session) -> bool:
        total_capitulos = db.query(func.count(Capitulo.id)).filter(Capitulo.modulo_id == self.id).scalar()
        capitulos_completados = db.query(func.count(Capitulo.id)).filter(Capitulo.modulo_id == self.id, Capitulo.completado == True).scalar() 
        if total_capitulos == 0:
            self.progreso = 0
        else:
            self.progreso = int((capitulos_completados / total_capitulos )*100)
        db.commit()
        return self.progreso

class Capitulo(Base):
    __tablename__ = "capitulos"

    id = Column(Integer, primary_key=True)
    modulo_id = Column(Integer, ForeignKey("modulos.id"))
    nombre_capitulo = Column(String(255), index=True)
    problema = Column(Text)
    pista = Column(String(255), index=True)
    descripcion_code = Column(Text)
    solucion = Column(String(255), index=True)
    completado = Column(Boolean, default=False)
    
    modulo = relationship("Modulo", back_populates="capitulos")


class ProgresoUsuario(Base):
    __tablename__ = "progreso_usuario"
    
    id = Column(Integer, primary_key=True, index=True)
    id_usuario_externo = Column(String(255), index=True)  
    id_modulo = Column(Integer, ForeignKey('modulos.id')) 
    completado = Column(Boolean, default=False)  
    modulo = relationship("Modulo", back_populates="progreso_usuario")

Base.metadata.create_all(bind=engine)