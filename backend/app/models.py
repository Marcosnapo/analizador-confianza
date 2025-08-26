from sqlalchemy import Column, Integer, String
from .database import Base
# En la primera línea, añade ForeignKey y relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

    # ... (código existente de la clase User) ...
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    histories = relationship("History", back_populates="owner")    
    # Añade esta línea dentro de la clase User para vincularla al historial
    histories = relationship("History", back_populates="owner")

# AÑADE ESTA NUEVA CLASE AL FINAL DEL ARCHIVO
class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    result = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="histories")
