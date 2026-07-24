from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine("sqlite:///tarefas.db") #cria se o motor de conexao(define modelo e arquivo)

SessionLocal = sessionmaker(bind=engine) #"fabrica" de sessoes. permite que semrpe seja criado uma sessao

class Base(DeclarativeBase): #caracteristico do sqlalchemy, todos que herdarem dessa classe serao definidos como tabela no banco
    pass