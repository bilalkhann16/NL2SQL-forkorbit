import pytest
import pandas as pd
from app.core.nl2sql import NL2SQL


def create_test_cases():
    test_cases = [
        # "What is the birth date of “Vice President of Engineering” ?",
        # "What department is the “Chief Executive Officer” part of? ",
    ]
    return test_cases


def execute_test_case(query, schema_info):
    try:
        sql_query = NL2SQL().run(query)
        return sql_query.get("sql_query", "No SQL query generated")
    except Exception as e:
        return str(e)


def main():
    test_cases = create_test_cases()
    schema_info = {}  # Replace with actual schema info if needed

    for i, case in enumerate(test_cases):
        print(f"Test Case {i+1}: {case}")
        result = execute_test_case(case, schema_info)


if __name__ == "__main__":
    main()
