import uvicorn
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from database import SessionLocal, engine
from models import Tarefa, Base, Usuario
from auth import verificar_senha, verificar_token, hash_senha, criar_token
from schemas import UsuarioCreate, UsuarioOutput, TokenOutput

Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_usuario_atual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verificar_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    
    email = payload.get("email")
    usuario = db.scalars(select(Usuario).where(Usuario.email == email)).first()
    if usuario is None:
        raise HTTPException(status_code=401, detail="Usuario nao encontrado")
    return usuario
class TarefaInput(BaseModel):
    titulo: str

class TarefaOutput(BaseModel):
    id: int
    titulo: str
    concluida: bool

    class Config:
        from_attributes = True #permite que o Pydantic leia dados de objetos SQLAlchemy, não só de dicionários.


@app.post("/tarefas", response_model=TarefaOutput)
def criar_tarefa(input: TarefaInput, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_atual)):
    nova_tarefa = Tarefa(titulo=input.titulo)
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    return nova_tarefa

@app.get("/tarefas", response_model=list[TarefaOutput])
def listar_tarefas(db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_atual)):
    if usuario is None:
        return HTTPException(status_code=401, detail="Usuário nao está logado")
    return db.query(Tarefa).all()

@app.delete("/tarefas/{id}")
def deletar_tarefa(id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_atual)):
    tarefa_excluida = db.scalars(select(Tarefa).where(Tarefa.id == id)).first()
    if tarefa_excluida:
        db.delete(tarefa_excluida)
        db.commit()
        return {"mensagem": "Tarefa excluída com sucesso!"}
    else:
        raise HTTPException(status_code=404, detail={"mensagem":"tarefa nao encontrada"})


@app.patch("/tarefas/{id}")
def concluir_tarefa(id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_atual)):
    tarefa_atualizar = db.scalars(select(Tarefa).where(Tarefa.id == id)).first()
    if tarefa_atualizar:
        tarefa_atualizar.concluida = True
        db.commit()
        return {"mensagem": "Tarefa atualizada com sucesso!"}
    else:
        raise HTTPException(status_code=404, detail={"mensagem":"tarefa nao encontrada"})

@app.post("/usuarios", response_model=UsuarioOutput)
def criar_usuario(input: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.scalars(select(Usuario).where(Usuario.email == input.email)).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado!")
    novo_usuario = Usuario(email=input.email, senha_hash = hash_senha(input.senha))
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@app.post("/login", response_model=TokenOutput)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Email ou senha inválidos!")

    if not verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos!")

    token = criar_token({"email": usuario.email})
    return {"access_token": token, "token_type": "bearer"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
