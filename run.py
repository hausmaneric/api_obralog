import os
import logging

import uvicorn
from alembic import command
from alembic.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("obralog.run")


def run_migrations() -> None:
    logger.info("Running Alembic migrations...")
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    logger.info("Alembic migrations finished.")


if __name__ == "__main__":
    if os.getenv("RUN_MIGRATIONS_ON_START", "true").lower() == "true":
        run_migrations()
    port = int(os.getenv("PORT", "8000"))
    logger.info("Starting ObraLog API on port %s", port)
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
