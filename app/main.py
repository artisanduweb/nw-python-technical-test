from routes import app
from infrastructure.db import get_context_session
from infrastructure.db_scripts import update_variant_column

@app.on_event("startup")
async def on_startup():
    async with get_context_session() as context_session:
        await update_variant_column(context_session)


if __name__ == "__main__":
  app.run()
