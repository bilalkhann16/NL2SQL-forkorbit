import csv
import json
from collections import defaultdict

# File paths
input_file = "data/input/db_schema.csv"
output_file = "schema.json"

# Read and organize schema data
schema_data = defaultdict(lambda: defaultdict(list))
with open(input_file, newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        schema = row["schema_name"]
        table = row["table_name"]
        column_info = {
            "column_name": row["column_name"],
            "data_type": row["data_type"],
            "max_length": int(row["max_length"]) if row["max_length"] != "-1" else -1,
            "precision": int(row["precision"]),
            "scale": int(row["scale"]),
            "is_nullable": bool(int(row["is_nullable"])),
            "is_identity": bool(int(row["is_identity"])),
        }
        schema_data[schema][table].append(column_info)

# Convert to JSON structure
json_data = {}
for schema, tables in schema_data.items():
    json_data[schema] = {}
    for table, columns in tables.items():
        json_data[schema][table] = columns

# Write to JSON file
with open(output_file, "w") as f:
    json.dump(json_data, f, indent=2)

print(f"Full schema written to {output_file}")
