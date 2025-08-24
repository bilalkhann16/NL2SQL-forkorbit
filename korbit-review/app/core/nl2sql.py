from app.utils.llm_client import LLMClient
from app.config import Config
from app.core.prompts import SCHEMA_IDENTIFIER, get_sql_query_generator_prompt
from loguru import logger


class NL2SQL:
    def __init__(self):
        self.llm_client = LLMClient()
        self.provider = Config.LLM_PROVIDER.lower()
        self.model = Config.LLM_MODEL
        logger.info(
            f"NL2SQL initialized with provider: {self.provider}, model: {self.model}"
        )

    def identify_schema(self, nl_query: str) -> str:
        """Identifies the relevant tables from the schema for the given natural language query."""
        response = self.llm_client.generate_json(
            system_prompt=SCHEMA_IDENTIFIER, user_prompt=nl_query
        )
        return response

    def get_sql_query(self, nl_query: str, used_schema: list, used_tables: list) -> str:
        """Generates SQL query for the given natural language query and schema."""
        system_prompt = get_sql_query_generator_prompt(
            used_schema=used_schema, used_tables=used_tables
        )
        response = self.llm_client.generate_json(
            system_prompt=system_prompt, user_prompt=nl_query
        )
        logger.debug(f"SQL query generator response: {response}")
        return response

    def run(self, nl_query: str) -> dict:
        """Runs the NL2SQL pipeline."""
        schema_output = self.identify_schema(nl_query)

        used_schema = schema_output.get("used_schema", [])
        used_tables = schema_output.get("used_tables", [])
        sql_query = self.get_sql_query(nl_query, used_schema, used_tables)

        logger.info(
            f"Generated SQL query: \n\n {sql_query.get("sql_query", "No SQL query generated")} \n\n"
        )
        return sql_query
