from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import BaseModel
from app.core.nl2sql import convert_nl_to_sql
from app.core.schema_parser import parse_schema_csv
from app.config import Config
from loguru import logger
import os

router = APIRouter()


class NLQuery(BaseModel):
    query: str


@router.post("/nl2sql")
async def nl_to_sql(query: NLQuery):
    logger.info(f"Received NL2SQL request with query: {query.query}")
    try:
        schema_path = Config.SCHEMA_PATH

        if not os.path.exists(schema_path):
            logger.error(f"Schema file not found: {schema_path}")
            raise HTTPException(status_code=400, detail="Schema file not found")

        schema_info = parse_schema_csv(schema_path)
        result = convert_nl_to_sql(query.query, schema_info)

        if "error" in result:
            logger.error(f"NL2SQL failed: {result['error']}")
            raise HTTPException(status_code=500, detail=result["error"])

        logger.info(f"Returning SQL query: {result['sql_query']}")
        return {"sql_query": result["sql_query"]}
    except Exception as e:
        logger.error(f"NL2SQL request failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
