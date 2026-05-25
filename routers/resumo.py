# routers/resumo.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_usuario_atual
import models, schemas

router = APIRouter(prefix="/resumo", tags=["Resumo"])

@router.get("/", response_model=schemas.ResumoResponse)
def resumo_geral(db: Session = Depends(get_db), usuario=Depends(get_usuario_atual)):
    transacoes = db.query(models.Transacao).filter(
        models.Transacao.usuario_id == usuario.id
    ).all()

    receitas = sum(t.valor for t in transacoes if t.tipo.value == "receita")
    despesas = sum(t.valor for t in transacoes if t.tipo.value == "despesa")

    return {"total_receitas": receitas, "total_despesas": despesas, "saldo": receitas - despesas}

@router.get("/mensal")
def resumo_mensal(db: Session = Depends(get_db), usuario=Depends(get_usuario_atual)):
    transacoes = db.query(models.Transacao).filter(
        models.Transacao.usuario_id == usuario.id
    ).all()

    mensal: dict = {}
    for t in transacoes:
        mes = t.data[:7]  # "YYYY-MM"
        if mes not in mensal:
            mensal[mes] = {"receitas": 0.0, "despesas": 0.0}
        if t.tipo.value == "receita":
            mensal[mes]["receitas"] += t.valor
        else:
            mensal[mes]["despesas"] += t.valor

    # Adiciona saldo em cada mês
    for mes in mensal:
        mensal[mes]["saldo"] = mensal[mes]["receitas"] - mensal[mes]["despesas"]

    return mensal