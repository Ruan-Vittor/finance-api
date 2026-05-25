from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db
from auth import hash_senha, verificar_senha, criar_token
from routers import transacoes, resumo

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance API", description="API de controle financeiro pessoal")

app.include_router(transacoes.router)
app.include_router(resumo.router)

@app.get("/")
def status():
    return {"status": "online"}

@app.post("/registro", response_model=schemas.UsuarioResponse, status_code=201)
def registrar(dados: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    from models import Usuario
    existe = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    usuario = Usuario(email=dados.email, senha_hash=hash_senha(dados.senha))
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

@app.post("/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    from models import Usuario
    usuario = db.query(Usuario).filter(Usuario.email == form.username).first()
    if not usuario or not verificar_senha(form.password, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    token = criar_token({"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}