# 💰 Finance API

API REST para controle financeiro pessoal, desenvolvida com **FastAPI**, **SQLAlchemy** e **JWT Authentication**.

## 🚀 Tecnologias

- Python 3.13
- FastAPI
- SQLAlchemy + SQLite
- JWT (python-jose)
- Bcrypt (hash de senhas)
- Pydantic v2

## ⚙️ Como rodar localmente

**1. Clone o repositório**
```bash
git clone https://github.com/Ruan-Vittor/finance-api.git
cd finance-api
```

**2. Instale as dependências**
```bash
pip install fastapi uvicorn sqlalchemy python-jose python-multipart bcrypt
```

**3. Inicie o servidor**
```bash
uvicorn main:app --reload
```

**4. Acesse a documentação**
```
http://localhost:8000/docs
```

## 🔑 Autenticação

A API usa autenticação JWT. Para acessar rotas protegidas:

1. Crie uma conta em `POST /registro`
2. Faça login em `POST /login` e copie o `access_token`
3. Clique em **Authorize** no Swagger e cole o token

## 📌 Endpoints

### Autenticação
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/registro` | Criar conta |
| POST | `/login` | Autenticar e obter token |

### Transações
| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| GET | `/transacoes` | Listar transações | ✅ |
| POST | `/transacoes` | Criar transação | ✅ |
| PUT | `/transacoes/{id}` | Atualizar transação | ✅ |
| DELETE | `/transacoes/{id}` | Remover transação | ✅ |

### Resumo
| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| GET | `/resumo` | Saldo geral | ✅ |
| GET | `/resumo/mensal` | Breakdown por mês | ✅ |

## 📂 Estrutura do projeto

```
finance_api/
├── main.py          # Rotas principais e configuração
├── database.py      # Conexão com o banco
├── auth.py          # JWT e hash de senhas
├── models.py        # Tabelas do banco (SQLAlchemy)
├── schemas.py       # Validação de dados (Pydantic)
└── routers/
    ├── transacoes.py
    └── resumo.py
```