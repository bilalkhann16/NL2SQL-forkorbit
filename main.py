from fastapi import FastAPI
from app.api.v1.nl2sql import router as nl2sql_router
from loguru import logger

app = FastAPI(title="NL2SQL Agent")

app.include_router(nl2sql_router, prefix="/api/v1")

if __name__ == "__main__":
    logger.info("Starting NL2SQL Agent server")
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
