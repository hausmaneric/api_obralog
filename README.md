# Backend ObraLog

## Executar

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Deploy no Railway

Variaveis recomendadas:

- `DATABASE_URL`: URL do PostgreSQL do Railway
- `SECRET_KEY`: chave secreta forte para tokens
- `ACCESS_TOKEN_EXPIRE_MINUTES`: validade do token bearer
- `CORS_ORIGINS`: origens permitidas separadas por virgula
- `AUTO_CREATE_TABLES=false`: recomendado em producao, usando Alembic
- `RUN_MIGRATIONS_ON_START=true`: aplica `alembic upgrade head` no boot

Comando de start:

```bash
python run.py
```

Healthcheck:

```bash
/health
```

## Migracoes

Criar/rodar migracoes:

```bash
alembic upgrade head
```

## Popular dados demo

```bash
curl -X POST http://127.0.0.1:8000/api/bootstrap/seed
```

## Login demo

- empresa: `1`
- e-mail: `engenheiro@obralog.com`
- senha: `123456`

Resposta de login:

- `access_token`
- `token_type=bearer`
- `expires_in`

Use no header:

```text
Authorization: Bearer <token>
```

## Banco

Por padrao usa SQLite local para desenvolvimento:

- `sqlite:///./obralog.db`

Em producao, o backend passa a usar `DATABASE_URL` automaticamente, com normalizacao para PostgreSQL no Railway.
