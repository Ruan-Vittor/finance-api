# routers/transacoes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import get_usuario_atual
import models, schemas

router = APIRouter(prefix="/transacoes", tags=["Transações"])

@router.get("/", response_model=list[schemas.TransacaoResponse])
def listar(db: Session = Depends(get_db), usuario=Depends(get_usuario_atual)):
    return db.query(models.Transacao).filter(
        models.Transacao.usuario_id == usuario.id
    ).all()

@router.post("/", response_model=schemas.TransacaoResponse, status_code=201)
def criar(dados: schemas.TransacaoCreate, db: Session = Depends(get_db), usuario=Depends(get_usuario_atual)):
    transacao = models.Transacao(**dados.model_dump(), usuario_id=usuario.id)
    db.add(transacao)
    db.commit()
    db.refresh(transacao)
    return transacao

@router.put("/{id}", response_model=schemas.TransacaoResponse)
def atualizar(id: int, dados: schemas.TransacaoUpdate, db: Session = Depends(get_db), usuario=Depends(get_usuario_atual)):
    transacao = db.query(models.Transacao).filter(
        models.Transacao.id == id,
        models.Transacao.usuario_id == usuario.id  # garante que é dono
    ).first()
    if not transacao:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    for campo, valor in dados.model_dump(exclude_none=True).items():
        setattr(transacao, campo, valor)
    db.commit()
    db.refresh(transacao)
    return transacao

@router.delete("/{id}")
def deletar(id: int, db: Session = Depends(get_db), usuario=Depends(get_usuario_atual)):
    transacao = db.query(models.Transacao).filter(
        models.Transacao.id == id,
        models.Transacao.usuario_id == usuario.id
    ).first()
    if not transacao:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    db.delete(transacao)
    db.commit()
    return {"mensagem": "Transação removida"}