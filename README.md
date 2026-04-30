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

Comando de start:

```bash
python run.py
```

Healthcheck:

```bash
/health
```

## Popular dados demo

```bash
curl -X POST http://127.0.0.1:8000/api/bootstrap/seed
```

## Login demo

- empresa: `1`
- e-mail: `engenheiro@obralog.com`
- senha: `123456`

## Banco

Por padrao usa SQLite local para desenvolvimento:

- `sqlite:///./obralog.db`

Em producao, o backend passa a usar `DATABASE_URL` automaticamente.
