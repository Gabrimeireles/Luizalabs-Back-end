# Sistema Bancário em Python (POO + FastAPI)

Projeto desenvolvido no **bootcamp DIO | LuizaLabs - Back-end com Python - 2ª Edição**.

Repositório de estudo e evolução de um sistema bancário em duas abordagens:

- aplicação CLI orientada a objetos
- API bancária assíncrona com FastAPI e JWT

## Tecnologias

- Python 3.x
- FastAPI
- SQLAlchemy Async
- SQLite (aiosqlite)
- JWT (`python-jose`)
- Passlib (`pbkdf2_sha256`)

## Estrutura do repositório

- `banco_poo.py`: implementação original em CLI (POO)
- `app/main.py`: entrada da API FastAPI
- `app/api/routes/`: rotas (`auth`, `accounts`, `transactions`)
- `app/services/`: regras de negócio
- `app/models/`: modelos ORM (`User`, `Account`, `Transaction`)
- `app/schemas/`: contratos de request/response
- `requirements.txt`: dependências da API

## Regras de negócio da API

- Depósitos e saques devem ter valor maior que zero.
- Saque exige saldo suficiente.
- Saque respeita limite por operação da conta.
- Saque respeita limite de quantidade por conta (`limite_saques`).
- Conta corrente é vinculada ao usuário autenticado.

## Como executar a API

### 1) Instalar dependências

```bash
pip install -r requirements.txt
```

### 2) Subir servidor

```bash
python -m uvicorn app.main:app --reload
```

### 3) Acessar documentação OpenAPI

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Fluxo de autenticação JWT

1. `POST /auth/register` para cadastrar usuário.
2. `POST /auth/login` para obter `access_token`.
3. No Swagger, clicar em **Authorize** e informar:

```text
Bearer <seu_token>
```

4. Consumir endpoints protegidos.

## Endpoints principais

- `POST /auth/register`
- `POST /auth/login`
- `POST /accounts`
- `GET /accounts`
- `GET /accounts/{account_id}`
- `POST /accounts/{account_id}/transactions`
- `GET /accounts/{account_id}/statement`
- `GET /health`

## Testes automatizados

### 1) Instalar dependências de desenvolvimento

```bash
pip install -r requirements-dev.txt
```

### 2) Executar testes

```bash
python -m pytest
```

### 3) Executar testes com cobertura

```bash
python -m pytest --cov=app --cov-report=term-missing --cov-report=xml
```

Cobertura atual da API:

- **96%** de cobertura total (`TOTAL 303 stmts / 12 miss`)
- **25 testes** automatizados passando

## Como executar o modo CLI (POO)

```bash
python banco_poo.py
```

## Autor

- Nome: `Gabriel Resende Meireles`
- LinkedIn: `https://www.linkedin.com/in/Gabrimeireles`
