# 💰 Finance API

![Tests](https://github.com/Ruan-Vittor/finance-api/actions/workflows/tests.yml/badge.svg)

API REST para controle financeiro pessoal com autenticação JWT, desenvolvida com **FastAPI** e **SQLAlchemy**.

## 🚀 Tecnologias

- Python 3.11
- FastAPI
- SQLAlchemy + SQLite
- JWT (python-jose)
- Bcrypt (hash de senhas)
- Pydantic v2
- pytest + FastAPI TestClient

## ⚙️ Como rodar localmente

**1. Clone o repositório**
```bash
git clone https://github.com/Ruan-Vittor/finance-api.git
cd finance-api
```

**2. Crie e ative o ambiente virtual**
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate       # Linux/Mac
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Inicie o servidor**
```bash
uvicorn main:app --reload
```

**5. Acesse a documentação**
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

## 🧪 Testes

O projeto possui cobertura de testes automatizados com pytest e integração contínua via GitHub Actions.

```bash
pytest test_main.py -v
```

Cenários cobertos:
- Status da API
- Registro de usuário
- Validação de email duplicado
- Login com credenciais corretas
- Rejeição de senha incorreta
- Proteção de rotas com JWT

## 📂 Estrutura do projeto

```
finance_api/
├── main.py          # Rotas principais e configuração
├── database.py      # Conexão com o banco
├── auth.py          # JWT e hash de senhas
├── models.py        # Tabelas do banco (SQLAlchemy)
├── schemas.py       # Validação de dados (Pydantic)
├── test_main.py     # Testes automatizados
└── routers/
    ├── transacoes.py
    └── resumo.py
```