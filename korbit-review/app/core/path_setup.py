import os

work_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

data_dir = os.path.join(work_dir, "data")
db_schema_simplified_path = os.path.join(data_dir, "input", "db_schema.txt")
db_schema_full_json_path = os.path.join(data_dir, "input", "db_schema.json")
