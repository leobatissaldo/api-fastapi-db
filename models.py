from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Tarefa(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    concluida = Column(Boolean, default=False)

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, index=True, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    senha_hash = Column(String, nullable=False)
