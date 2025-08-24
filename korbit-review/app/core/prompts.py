from app.core.path_setup import db_schema_simplified_path, db_schema_full_json_path
from app.core.utils import create_text_prompt_from_list
from loguru import logger
import json

with open(db_schema_simplified_path, "r") as f:
    db_schema_simplified = f.read()

with open(db_schema_full_json_path, "r") as f:
    db_schema_full_json = json.load(f)


SCHEMA_IDENTIFIER = """
You are an expert database. Your task is to identify, all the schema and tables that are useful to form SQL query for the given user_question. 

Guidelines:
1. Identify the schema and tables that are relevant to the user_question.
2. Ensure that the identified schema and tables are sufficient to answer the question.
3. Make sure the spelling of the schema and tables is correct.
4. Provide a reason behind why you chose these schema and tables.
5. Use the following format for your output:

{{
    "used_schema": ["schema1", "schema2"],
    "used_tables": ["table1", "table2"]
    "reason": "Explain why these schema and tables are relevant to the question."
}}

{schema}

Example 1:
Input: "List of employees and their departments"
Output:
{{
    "used_schema": ["HumanResources"],
    "used_tables": ["Employee", "EmployeeDepartmentHistory", "Department"],
    "reason": "These tables contain information about employees and their department affiliations, which is necessary to answer the question."
}}

Example 2:
Input: "Email addresses of all active employees"
Output:
{{
    "used_schema": ["HumanResources", "Person"],
    "used_tables": ["Employee", "EmailAddress"],
    "reason": "These tables contain information about employees and their email addresses, which is necessary to answer the question."
}}
""".format(
    schema=db_schema_simplified
)


SQL_QUERY_GENERATOR = """
You are an expert SQL query generator. Your task is to generate a SQL query based on the user_question and the provided schema and table information. 

Guidelines:
1. Use the provided schema and tables to construct a valid SQL query.
2. Ensure that the query is syntactically correct and follows SQL standards.
3. Include all necessary joins, conditions, and clauses to answer the user_question.
4. If the user_question is ambiguous, make reasonable assumptions to clarify the intent.
5. The output must be in the following JSON format:
```json
{{
    "sql_query": "SELECT ... FROM ... WHERE ..."
}}

schema and table information:
{system_context}

Example 1:
Input: "List of employees and their departments"

Output:
```json
{{
    "sql_query": "SELECT e.BusinessEntityID, e.JobTitle, d.Name AS DepartmentName FROM HumanResources.Employee AS e JOIN HumanResources.EmployeeDepartmentHistory AS edh ON e.BusinessEntityID = edh.BusinessEntityID JOIN HumanResources.Department AS d ON edh.DepartmentID = d.DepartmentID WHERE edh.EndDate IS NULL;"
}}
```
"""


def get_context_from_schema(used_schema: list, used_tables: list) -> str:
    final_tables = []
    for schema_name in used_schema:
        schema = db_schema_full_json.get(schema_name, {})
        tables = [table for table in schema.keys() if table in used_tables]
        if tables:
            final_tables.append(
                {
                    schema_name: {
                        table_obj: table_value
                        for table_obj, table_value in schema.items()
                        if table_obj in tables
                    }
                }
            )

    if not final_tables:
        logger.warning("No matching schema or tables found in the provided schema.")
        return ""

    final_context = create_text_prompt_from_list(final_tables)
    logger.info(
        f"Final context created from schema: {final_context[:100]}..."
    )  # Log first 100 characters for brevity
    return final_context


def get_sql_query_generator_prompt(used_schema: list, used_tables: list) -> str:
    system_context_op = get_context_from_schema(used_schema, used_tables)
    if not system_context_op:
        logger.warning(
            "No system context generated from the provided schema and tables."
        )
        return None
    return (
        SQL_QUERY_GENERATOR.replace("{system_context}", system_context_op)
        if system_context_op
        else SQL_QUERY_GENERATOR
    )
