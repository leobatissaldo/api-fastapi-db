import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from database import SessionLocal, engine
from models import Tarefa, Base


Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TarefaInput(BaseModel):
    titulo: str

class TarefaOutput(BaseModel):
    id: int
    titulo: str
    concluida: bool

    class Config:
        from_attributes = True #permite que o Pydantic leia dados de objetos SQLAlchemy, não só de dicionários.


@app.post("/tarefas", response_model=TarefaOutput)
def criar_tarefa(input: TarefaInput, db: Session = Depends(get_db)):
    nova_tarefa = Tarefa(titulo=input.titulo)
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    return nova_tarefa

@app.get("/tarefas", response_model=list[TarefaOutput])
def listar_tarefas(db: Session = Depends(get_db)):
    return db.query(Tarefa).all()

@app.delete("/tarefas/{id}")
def deletar_tarefa(id: int, db: Session = Depends(get_db)):
    tarefa_excluida = db.scalars(select(Tarefa).where(Tarefa.id == id)).first()
    if tarefa_excluida:
        db.delete(tarefa_excluida)
        db.commit()
        return {"mensagem": "Tarefa excluída com sucesso!"}
    else:
        raise HTTPException(status_code=404, detail={"mensagem":"tarefa nao encontrada"})


@app.patch("/tarefas/{id}")
def concluir_tarefa(id: int, db: Session = Depends(get_db)):
    tarefa_atualizar = db.scalars(select(Tarefa).where(Tarefa.id == id)).first()
    if tarefa_atualizar:
        tarefa_atualizar.concluida = True
        db.commit()
        return {"mensagem": "Tarefa excluída com sucesso!"}
    else:
        raise HTTPException(status_code=404, detail={"mensagem":"tarefa nao encontrada"})
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)