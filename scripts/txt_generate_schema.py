import csv
from collections import defaultdict

# File paths
input_file = "data/input/db_schema.csv"
output_file = "data/input/db_schema.txt"

# Read and organize schema data
schema_data = defaultdict(lambda: defaultdict(list))
with open(input_file, newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        schema = row["schema_name"]
        table = row["table_name"]
        column_info = f"{row['column_name']}:{row['data_type']}"
        schema_data[schema][table].append(column_info)

# Generate simple text output
output = []
for schema, tables in sorted(schema_data.items()):
    output.append(f"Schema: {schema}")
    for table, columns in sorted(tables.items()):
        output.append(f"  Table: {table}")
        for col in columns:
            output.append(f"    {col}")
        output.append("")  # Blank line after table
    output.append("")  # Blank line after schema

# Write to text file
with open(output_file, "w") as f:
    f.write("\n".join(output))

print(f"Simplified schema written to {output_file}")
