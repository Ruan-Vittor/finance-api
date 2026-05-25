from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

# ─── USUÁRIO ───────────────────────────────────────
class UsuarioCreate(BaseModel):
    email: str
    senha: str

class UsuarioResponse(BaseModel):
    id: int
    email: str

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str

# ─── TRANSAÇÕES ────────────────────────────────────
class TipoTransacao(str, Enum):
    receita = "receita"
    despesa = "despesa"

class TransacaoCreate(BaseModel):
    descricao: str = Field(min_length=2, max_length=100)
    valor: float = Field(gt=0)
    tipo: TipoTransacao
    categoria: str = Field(min_length=2, max_length=50)
    data: str  # "YYYY-MM-DD"

class TransacaoUpdate(BaseModel):
    descricao: Optional[str] = Field(default=None, min_length=2, max_length=100)
    valor: Optional[float] = Field(default=None, gt=0)
    tipo: Optional[TipoTransacao] = None
    categoria: Optional[str] = Field(default=None, min_length=2, max_length=50)
    data: Optional[str] = None

class TransacaoResponse(BaseModel):
    id: int
    descricao: str
    valor: float
    tipo: TipoTransacao
    categoria: str
    data: str
    usuario_id: int

    model_config = {"from_attributes": True}

# ─── RESUMO ────────────────────────────────────────
class ResumoResponse(BaseModel):
    total_receitas: float
    total_despesas: float
    saldo: float