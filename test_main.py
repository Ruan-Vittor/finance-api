import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import get_db
from models import Base

# Banco em memória só para testes — não toca no finance.db real
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Substitui o banco real pelo de teste
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    """Cria as tabelas antes de cada teste e apaga depois."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


# ── TESTE 1: API está online ──────────────────────────────────────
def test_status():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "online"}


# ── TESTE 2: Registro de usuário com sucesso ─────────────────────
def test_registro_sucesso():
    response = client.post("/registro", json={
        "email": "teste@email.com",
        "senha": "senha123"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "teste@email.com"


# ── TESTE 3: Registro com email duplicado deve retornar 400 ──────
def test_registro_email_duplicado():
    client.post("/registro", json={"email": "teste@email.com", "senha": "senha123"})
    response = client.post("/registro", json={"email": "teste@email.com", "senha": "outrasenha"})
    assert response.status_code == 400
    assert "já cadastrado" in response.json()["detail"]


# ── TESTE 4: Login com credenciais corretas retorna token ─────────
def test_login_sucesso():
    client.post("/registro", json={"email": "teste@email.com", "senha": "senha123"})
    response = client.post("/login", data={
        "username": "teste@email.com",
        "password": "senha123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


# ── TESTE 5: Login com senha errada retorna 401 ───────────────────
def test_login_senha_errada():
    client.post("/registro", json={"email": "teste@email.com", "senha": "senha123"})
    response = client.post("/login", data={
        "username": "teste@email.com",
        "password": "senhaerrada"
    })
    assert response.status_code == 401


# ── TESTE 6: Rota protegida sem token retorna 401 ─────────────────
def test_transacoes_sem_token():
    response = client.get("/transacoes")
    assert response.status_code == 401