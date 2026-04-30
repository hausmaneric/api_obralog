import os
import subprocess
import sys

import uvicorn


if __name__ == "__main__":
    if os.getenv("RUN_MIGRATIONS_ON_START", "true").lower() == "true":
        subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], check=True)
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
