# models.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum
from database import Base
import enum

class TipoTransacao(enum.Enum):
    receita = "receita"
    despesa = "despesa"

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    senha_hash: Mapped[str]
    transacoes: Mapped[list["Transacao"]] = relationship(back_populates="usuario")

class Transacao(Base):
    __tablename__ = "transacoes"

    id: Mapped[int] = mapped_column(primary_key=True)
    descricao: Mapped[str]
    valor: Mapped[float]
    tipo: Mapped[TipoTransacao]
    categoria: Mapped[str]
    data: Mapped[str]  # formato "YYYY-MM-DD"
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    usuario: Mapped["Usuario"] = relationship(back_populates="transacoes")